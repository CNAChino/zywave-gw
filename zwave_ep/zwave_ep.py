from rx import Observable, Observer
from queue import Queue
from threading import Thread

_SHUTDOWN = False

class ZwaveEPWorker(Thread):
    def __init__(self, queue, dispatcher):
        print('Creating and starting ZwaveEPWorker')
        super(ZwaveEPWorker, self).__init__()
        self._queue = queue
        self.daemon = True
        self.running = True
        self._dispatcher = dispatcher
        self.start()

    def run(self):
        print('ZwaveEPWorker:  running')
        while True:
            if _SHUTDOWN:
                print('ZwaveEPWorker: shutting down')
                break;
            event = self._queue.get()
            if event is None:
                break
            self.processEvent(event)

    def processEvent(self, event):
        event.destination = 'awsiot_ep'
        self._dispatcher.add_event(event)


class ZwaveEP():
    def __init__(self, dispatcher, num_t = 2):
        print('Creating Zwave Event Processor, with {} threads'.format(num_t))
        self._dispatcher = dispatcher
        self.inChannel = Queue(num_t)
        self._threads = []
        for _ in range(num_t):
            self._threads.append(ZwaveEPWorker(self.inChannel, dispatcher))

    def add_event(self,event):
        self.inChannel.put(event)

    def wait_until_shutdown(self):
        print('ZwaveEP: Waiting on threads to finish')
        for t in self._threads:
            t.join()
        print('ZwaveEP: threads finished exiting...')

    def stop(self):
        print('ZwaveEP: Stopping DispatcherTP')
        _SHUTDOWN = True
        for t in self._threads:
            self.inChannel.put(None)

    @property
    def inChannel(self):
        return self._inChannel

    @inChannel.setter
    def inChannel(self, value):
        self._inChannel = value

if __name__ == '__main__':
    pass
