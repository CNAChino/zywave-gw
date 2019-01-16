from event_dispatcher.event_dispatcher import zywave_dispatcher
_dailyEventCount = 0

class ZwaveEP():

    # TODO handle incoming/outgoing messages messages.
    # map openzwave to MQTT

    def __init__(self):
        pass

    def dailyEventCount(self):
        global _dailyEventCount
        return _dailyEventCount

    def processEvent(self, event):
        global _dailyEventCount
        event.destination = 'awsiot_ep'
        zywave_dispatcher.add_event(event)
        _dailyEventCount += 1


