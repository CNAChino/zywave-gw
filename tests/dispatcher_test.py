import unittest, time
from queue import Queue
from zwave_ep.zwave_ep import ZwaveEP 
from awsiot_ep.awsiot_ep import AWSIotEP
from event_dispatcher.event_dispatcher import Dispatcher
from event_dispatcher.event_dispatcher import Event

class TestDispatcher(unittest.TestCase):

    def test_zwaveep(self):
        dispatcher = Dispatcher()
        zwaveEP  = ZwaveEP(dispatcher)
        awsIotEP = AWSIotEP(dispatcher)

        dispatcher.add_channel('awsiot_ep', awsIotEP.inChannel)
        dispatcher.add_channel('zwave_ep', zwaveEP.inChannel)
        dispatcher.start()

        event = Event()
        event.timestamp = time.time()
        event.source = 'zwave_net_id'
        event.destination = 'zwave_ep'
        event.payload = 'LIGHT-ON'

        dispatcher.add_event(event)

        time.sleep(1)

        dispatcher.stop()
        zwaveEP.stop()

        self.assertEqual(zwaveEP.dailyEventCount(), 1)
        self.assertEqual(awsIotEP.dailyEventCount(), 1)

        dispatcher.wait_until_shutdown()
        zwaveEP.wait_until_shutdown()

if __name__ == '__main__':
    unittest.main()
