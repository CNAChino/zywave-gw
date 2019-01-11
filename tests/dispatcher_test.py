import unittest, time
from event_processors.zwave_ep import ZwaveEP 
from event_processors.awsiot_ep import AWSIotEP
from event_dispatcher.event_dispatcher import Dispatcher
from models.event import Event

class TestDispatcher(unittest.TestCase):

    def test_zwaveep(self):
        dispatcher = Dispatcher()

        zwaveEP  = ZwaveEP(dispatcher)
        awsIotEP = AWSIotEP(dispatcher)

        dispatcher.add_event_processor('zwave_ep', zwaveEP)
        dispatcher.add_event_processor('awsiot_ep', awsIotEP)

        event = Event()
        event.timestamp = time.time()
        event.source = 'zwave_net_id'
        event.destination = 'zwave_ep'
        event.payload = 'LIGHT-ON'

        dispatcher.add_event(event)

        time.sleep(1)

        dispatcher.stop()

        self.assertEqual(zwaveEP.dailyEventCount(), 1)
        self.assertEqual(awsIotEP.dailyEventCount(), 1)

        dispatcher.wait_until_shutdown()

if __name__ == '__main__':
    unittest.main()
