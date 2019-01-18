from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from zywave_queue import main_queue
from models.event import Event
import time

class AWSIotGateway():

    def __init__(self):
        self._awsIotClient = None

    def start(self):
        self._awsIotClient = AWSIoTMQTTClient("MyPythonMQTTPub")
        self._awsIotClient.configureEndpoint("a352k6gnga96jt-ats.iot.us-west-2.amazonaws.com", 8883)
        self._awsIotClient.configureCredentials("./certificate/AmazonRootCA1.pem", "./certificate/private.pem", "./certificate/awsiot-certificate.pem.crt")
        self._awsIotClient.configureOfflinePublishQueueing(-1)
        self._awsIotClient.configureDrainingFrequency(2)
        self._awsIotClient.configureConnectDisconnectTimeout(10)
        self._awsIotClient.configureMQTTOperationTimeout(5)
        self._awsIotClient.connect()

        self.subscribe()

    def subscribe(self):
        s = self._awsIotClient.subscribe("myTopic/1", 0, self.subsCallback)
        print('s = {}'.format(s))


    def publish(self, payload):
        print('AWSIotGateway : sending = {}'.format(payload))
        self._awsIotClient.publish("myTopic/1", payload, 0)

    def subsCallback(self,client, userdata, message):
        data = message.payload.decode('utf-8')
        print("message from AWSIOT is: {}".format(data))

        commandEvent = Event()
        commandEvent.timestamp = time.time()
        commandEvent.source = 'aws_iot'
        commandEvent.destination = 'zw_net'
        commandEvent.payload = data
        main_queue.put(commandEvent)

    def disconnect(self):
        self._awsIotClient.unsubscribe("myTopic/1")
        self._awsIotClient.disconnect()
