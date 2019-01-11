from event_processors.zwave_ep import ZwaveEP
from event_processors.awsiot_ep import AWSIOTClient
from event_dispatcher.event_dispatcher import Dispatcher
from app_config import *
import time

class Application():
    """
    Class to bootstrap , shutdown the appliation
    """
    def main(self, argc, argv):
        dispatcher = Dispatcher()

        zwaveEP  = ZwaveEP(dispatcher)
        awsIotEP = AWSIotEP(dispatcher)

        dispatcher.add_channel('zwave_ep', zwaveEP.inChannel)
        dispatcher.add_channel('awsiot_ep', awsIotEP.inChannel)

        dispatcher.start()

        dispatcher.wait_until_shutdown()
        zwaveEP.wait_until_shutdown()
        awsIotEP.wait_until_shutdown()

        return 0

app = Application()
