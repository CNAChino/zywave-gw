from event_processors.zwave_ep import ZwaveEP
from event_processors.awsiot_ep import AWSIotEP
from event_dispatcher.event_dispatcher import zywave_dispatcher
from app_config import *
import time
from network_gateway.zwave_network_controller import ZwaveNetworkController

class Application():
    """
    Class to bootstrap , shutdown the appliation
    """
    def main(self, argc, argv):
        #dispatcher = Dispatcher()

        zwaveEP  = ZwaveEP()
        awsIotEP = AWSIotEP()

        zywave_dispatcher.add_event_processor('zwave_ep', zwaveEP)
        zywave_dispatcher.add_event_processor('awsiot_ep', awsIotEP)

        #zywave_dispatcher.start()



        zc = ZwaveNetworkController("/dev/cu.usbmodem1411",
                                    config_path="/Users/carlofelicianoaureus/devel/lib/open-zwave/etc/openzwave")

        zc.start()

        zywave_dispatcher.wait_until_shutdown()
        zwaveEP.wait_until_shutdown()
        awsIotEP.wait_until_shutdown()

        zc.stop()

        return 0

app = Application()
