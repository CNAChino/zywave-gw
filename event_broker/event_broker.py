from network_gateway import znc
from network_gateway import awsiot_gateway

class EventBroker():

    def __init__(self):
        pass

    def processEvent(self, event):
        if event.destination == 'aws_iot':
            awsiot_gateway.publish(event.payload)
        elif event.destination == 'zw_net':
            znc.send_command(event.payload)
        else:
            raise LookupError('unknown destination {}'.format(event.destination))