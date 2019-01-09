from rx import Observable, Observer
from queue import Queue
from threading import Thread

_SHUTDOWN = False

class ZwaveProxyWorker(Thread):
    def __init__(self, queue):
        super(ZwaveProxyWorker, self).__init__()
        self._queue = queue
        self.daemon = True
        self.running = True
        self.start()

    def run(self):
        print('Thread running')
        while True:
            if _SHUTDOWN:
                print('Thread shutting down')
                break;
            zwEvent = self._queue.get()
            self.onIncomingZwaveEvent(zwEvent)

    def onIncomingZwaveEvent(self, zwEvent):
        src = Observable.just(zwEvent)
        src.subscribe(IncomingZwaveEventObserver())

    def onSubmitZwaveCommand(self, zwaveCommand):
        pass

class IncomingZwaveEventObserver(Observer):
    def on_next(self, value):
        print("Received {0}".format(value))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))

class ZwaveProxy():
    def __init__(self):
        pass

    def start(self, num_t):
        self._q = Queue(num_t)
        for _ in range(num_t):
            ZwaveProxyWorker(self._q)

    def add_task(self,zwEvent):
        self._q.put(zwEvent)

    def wait_complete(self):
        print('Waiting on threads to finish')
        self._q.join()

    def stop(self):
        print('Shutting down ZwaveProxy')
        _SHUTDOWN = True

if __name__ == '__main__':
    pool = ZwaveProxy()
    atexit.register(exit_handler)
    for i in range(3):
       pool.add_task('hello {}'.format(i))
    pool.wait_complete()

