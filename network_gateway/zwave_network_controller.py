import time
import openzwave
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher
from models.event import Event
from event_dispatcher.event_dispatcher import zywave_dispatcher

class ZwaveNetworkController():
    """
    This class is reponsible for starting and communicating with a zwave controller.
    """

    def __init__(self, controllerDevice, config_path="./config", user_path=".", cmd_line=""):

        self.is_running = False;

        self.options = ZWaveOption(controllerDevice, config_path, user_path, cmd_line)
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level("None")
        self.options.set_logging(True)
        self.options.lock()

        dispatcher.connect(self.zwave_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self.zwave_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(self.zwave_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
        dispatcher.connect(self.zwave_node_update, ZWaveNetwork.SIGNAL_NODE)
        dispatcher.connect(self.zwave_value_update, ZWaveNetwork.SIGNAL_VALUE)

        self.network = ZWaveNetwork(self.options, autostart=False)



    def start(self):
        self.network.start()

    def stop(self):
        self.network.stop()

    def send_command(self, command):
        # SWITCH-SET|node-id|val-id||1 or 0
        print('send_command | {}'.format(command))
        if self.network.is_ready == True:
            fields = command.split("|")
            cCommand = fields[0]
            cNodeId = int(fields[1])
            cValueId = int(fields[2])
            cVal = True if fields[3] == '1' else False

            if cCommand == 'SWITCH-SET':
                print('switching to {}'.format(cVal))
                self.network.nodes[cNodeId].set_switch(cValueId,cVal)
            else:
                print("send_command : failed.  unsupported command {}".format(cCommand))
        else:
            print("send_command : failed.  network not ready.")

    def zwave_network_started(self, network):
        print("network started : homeid {:08x} - {} nodes were found.".format(network.home_id, network.nodes_count))

    def zwave_network_failed(self, network):
        print("network : loading failed.")

    def zwave_network_ready(self, network):
        print("network : ready : {} nodes were found.".format(self.network.nodes_count))
        print("network : my controller is : {}".format(self.network.controller))
        self.network.controller.node.name = "HomeSweetHome"
        self.network.controller.node.location = "Room1"

        self.is_running = True;

        print ('Switches are')
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches():
                zNode = self.network.nodes[node]
                netReadyEvent = Event()
                netReadyEvent.timestamp = time.time()
                netReadyEvent.source = 'zwave-{}|{}'.format(self.network.home_id,zNode.node_id)
                netReadyEvent.destination = 'zwave_ep'
                netReadyEvent.payload = "NET-READY|{}|{}|{}".format(zNode.node_id,val,zNode.get_switch_state(val))
                print('payload = {}'.format(netReadyEvent.payload))
                zywave_dispatcher.add_event(netReadyEvent)


    def zwave_node_update(self, network, node):
        print("Hello from node : {}.".format(node))

    def zwave_value_update(self, network, node, value):
        print("Hello from value : {}.".format( value ))

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running = value


if __name__ == '__main__':
    zc = ZwaveNetworkController("/dev/cu.usbmodem1411",
                                config_path="/Users/carlofelicianoaureus/devel/lib/open-zwave/etc/openzwave")

    zc.start()

    time.sleep(5)

    zc.send_command("SWITCH-SET|3|72057594093060096|1")

    while zc.is_running == True:
        time.sleep(5)

    zc.stop()