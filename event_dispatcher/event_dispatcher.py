from queue import Queue
from threading import Thread
import time

_SHUTDOWN = False

class DispatcherWorker(Thread):
    def __init__(self, queue, channels):
        print('Creaeting and Starting DispatcherWorker')
        super(DispatcherWorker, self).__init__()
        self._queue = queue
        self.daemon = True
        self.running = True
        self._channels = channels
        self.start()

    def run(self):
        print('DispatcherWorker: running')
        while True:
            if _SHUTDOWN:
                print('DispatcherWorker: shutting down')
                break;
            event = self._queue.get()
            if event is None:
                break
            self.processEvent(event)
            self._queue.task_done()
        print('Dispatcher Worker Exiting...')

    def processEvent(self, event):
        print('Routing Event: timestamp={}, src={}, dest={}, payload={}'.format(event.timestamp, event.source, event.destination, event.payload))
        channel = self._channels[event.destination]
        channel.put(event) 
        # TODO check if thread safe
        # routing loging


class Dispatcher():
    def __init__(self):
        self._channels = {}
        pass

    def start(self, num_t = 2):
        print('DispatcherWorker: starting with {} threads'.format(num_t))
        self._q = Queue(num_t)
        self._threads = []
        for _ in range(num_t):
            self._threads.append(DispatcherWorker(self._q, self._channels))

    def add_event(self,event):
        self._q.put(event)

    def wait_until_shutdown(self):
        print('DispatcherWorker: Waiting on threads to finish')
        for t in self._threads:
            t.join()
        print('DispatcherWorker: threads finished, exiting...')

    def add_channel(self,channel_id, channel):
        self._channels[channel_id] = channel

    def stop(self):
        print('Stopping DispatcherTP')
        _SHUTDOWN = True
        for t in self._threads:
            self._q.put(None)


class Event():
    def __init__(self):
        pass

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value    


if __name__ == '__main__':
    pool = Dispatcher()
    pool.start()
    pool.add_channel('zwave_ep', Queue());
    for i in range(100):
        event = Event()
        event.timestamp = time.time()
        event.source = 'zwave_net_id'
        event.destination = 'zwave_ep'
        event.payload = 'count = {}'.format(i)
        pool.add_event(event)
    pool.start()
    pool.wait_complete()
