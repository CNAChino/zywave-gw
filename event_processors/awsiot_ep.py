from rx import Observable, Observer
from queue import Queue
from threading import Thread
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

_SHUTDOWN = False
_dailyEventCount = 0

class AWSIotEPWorker(Thread):
    def __init__(self, queue, dispatcher):
        print('Creating and starting AWSIotEPWorker')
        super(AWSIotEPWorker, self).__init__()
        self._queue = queue
        self.daemon = True
        self.running = True
        self._dispatcher = dispatcher
        self.start()
        self._awsIotClient = self.setupAwsIotClient()

    def setupAwsIotClient(self):
        myMQTTClient = AWSIoTMQTTClient("MyPythonMQTTPub")
        myMQTTClient.configureEndpoint("a352k6gnga96jt-ats.iot.us-west-2.amazonaws.com", 8883)
        myMQTTClient.configureCredentials("./AmazonRootCA1.pem.txt", "./f282b8b2a8-private.pem.key", "./f282b8b2a8-certificate.pem.crt")
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(10)
        myMQTTClient.configureMQTTOperationTimeout(5)
        return myMQTTClient

    def publish(self, payload):
        self._awsIotClient.connect()
        self._awsIotClient.publish("myTopic/1", payload, 0)
        self._awsIotClient.disconnect()

    def run(self):
        global _SHUTDOWN
        print('AWSIotEPWorker:  running')
        while True:
            if _SHUTDOWN:
                print('AWSIotEPWorker: shutting down')
                break;
            event = self._queue.get()
            if event is None:
                break
            self.processEvent(event)

    def processEvent(self, event):
        global _dailyEventCount
        print('TODO send to AWS IOT')
        self.publish(event.payload)
        _dailyEventCount += 1


class AWSIotEP():
    def __init__(self, dispatcher):
        num_t = 1
        print('Creating AWS IOT Event Processior, with {} threads'.format(num_t))
        self._dispatcher = dispatcher
        self.inChannel = Queue(num_t)
        self._threads = []
        for _ in range(num_t):
            self._threads.append(AWSIotEPWorker(self.inChannel, dispatcher))

    def add_event(self,event):
        self.inChannel.put(event)

    def wait_until_shutdown(self):
        print('AWSIotEP: Waiting on threads to finish')
        for t in self._threads:
            t.join()
        print('AWSIotEP: threads finished exiting...')

    def stop(self):
        global _SHUTDOWN
        print('AWSIotEP: Stopping DispatcherTP')
        _SHUTDOWN = True
        for t in self._threads:
            self.inChannel.put(None)

    def dailyEventCount(self):
        global _dailyEventCount
        return _dailyEventCount

    @property
    def inChannel(self):
        return self._inChannel

    @inChannel.setter
    def inChannel(self, value):
        self._inChannel = value

if __name__ == '__main__':
    pass
