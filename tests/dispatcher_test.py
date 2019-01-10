import unittest, time
from queue import Queue
from zwave_ep.zwave_ep import ZwaveEP 
from event_dispatcher.event_dispatcher import Dispatcher
from event_dispatcher.event_dispatcher import Event

class TestDispatcher(unittest.TestCase):

    def test_zwaveep(self):
        awsQueue = Queue()
        dispatcher = Dispatcher()
        zwaveEP  = ZwaveEP(dispatcher)

        dispatcher.add_channel('awsiot_ep', awsQueue)
        dispatcher.add_channel('zwave_ep', zwaveEP.inChannel)
        dispatcher.start()

        event = Event()
        event.timestamp = time.time()
        event.source = 'zwave_net_id'
        event.destination = 'zwave_ep'
        event.payload = 'count = {}'.format(1)

        dispatcher.add_event(event)

        e = awsQueue.get()
        self.assertEqual(e.destination, 'awsiot_ep') 
        self.assertEqual(e.payload, 'count = 1')

        dispatcher.stop()
        zwaveEP.stop()

        dispatcher.wait_until_shutdown()
        zwaveEP.wait_until_shutdown()

if __name__ == '__main__':
    unittest.main()
