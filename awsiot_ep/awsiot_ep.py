from rx import Observable, Observer
from queue import Queue
from threading import Thread

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
        # TODO send to AWS IOT
        _dailyEventCount += 1


class AWSIotEP():
    def __init__(self, dispatcher, num_t = 2):
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
