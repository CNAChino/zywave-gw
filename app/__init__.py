from event_dispatcher import zywave_dispatcher
from network_gateway import znc
from network_gateway import awsiot_gateway

class Application():
    """
    Class to bootstrap , shutdown the appliation
    """
    def main(self, argc, argv):
        znc.start("/dev/cu.usbmodem1411",
                                    config_path="/Users/carlofelicianoaureus/devel/lib/open-zwave/etc/openzwave")

        awsiot_gateway.start()

        zywave_dispatcher.wait_until_shutdown()

        znc.stop()

        return 0

app = Application()
