from queue import Queue
from threading import Thread
from zywave_queue import main_queue
from event_broker import event_broker
_shutdownApp = False
_eventProcessors = {}

class Dispatcher():

    """
    Send events to a Event-Processor. First an event is put to queue.  Then a worker (thread) picks up
    an event from th queue and dispatches to a proper event processor.

    Example Usage:
        dispatcher = Dispatcher()
        ...
        ep1  = EventProcessor1(dispatcher)
        ep2 = EventProcessor2(dispatcher)
        ...
        dispatcher.add_event_processor('zwave_ep', zwaveEP)
    """

    def __init__(self):
        self.start()

    def start(self, num_t = 2):
        print('DispatcherWorker: starting with {} threads'.format(num_t))
        self._threads = []
        for _ in range(num_t):
            self._threads.append(DispatcherWorker())

    def wait_until_shutdown(self):
        print('DispatcherWorker: Waiting on threads to finish')
        for t in self._threads:
            t.join()
        print('DispatcherWorker: threads finished, exiting...')

    def stop(self):
        print('Stopping DispatcherTP')
        _SHUTDOWN = True
        for t in self._threads:
            self._q.put(None)



class DispatcherWorker(Thread):

    def __init__(self):
        print('Creating and Starting DispatcherWorker')
        super(DispatcherWorker, self).__init__()
        self.daemon = True
        self.running = True
        self.start()

    def run(self):
        print('DispatcherWorker: running')
        while True:
            if _shutdownApp:
                print('DispatcherWorker: shutting down')
                break;
            event = main_queue.get()
            if event is None:
                break
            self.processEvent(event)
            main_queue.task_done()
        print('Dispatcher Worker Exiting...')

    def processEvent(self, event):
        global _eventProcessors
        print('Processing Event: timestamp={}, src={}, dest={}, payload={}'.format(event.timestamp, event.source, event.destination, event.payload))
        #ep = _eventProcessors[event.destination]
        #ep.processEvent(event)

        event_broker.processEvent(event)


