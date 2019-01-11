
_dailyEventCount = 0

class ZwaveEP():

    # TODO handle incoming/outgoing messages messages.
    # map openzwave to MQTT

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def dailyEventCount(self):
        global _dailyEventCount
        return _dailyEventCount

    def processEvent(self, event):
        global _dailyEventCount
        event.destination = 'awsiot_ep'
        self._dispatcher.add_event(event)
        _dailyEventCount += 1


