from zwave_ep.zwave_ep import ZwaveEP
from event_dispatcher.event_dispatcher import Dispatcher
#from awsiot_ep.awsiot_client import AWSIOTClient
from app_config import *
import time

class Application():
    def main(self, argc, argv):
        print ('Starting Application...')
        return start()

    def waitUntilShutdown(self):
        zWaveProxy.add_task('123') 
        zWaveProxy.add_task('123')
        zWaveProxy.wait_complete()
        print('waitUntilShutdown exiting')

    def shutdown(self):
        zWaveProxy.stop()

app = Application()

def start():

    dispatcher = Dispatcher()

    zwaveEP  = ZwaveEP(dispatcher)
    #awsIotEP = AWSIotEP(dispatcher)

    dispatcher.add_channel('zwave_ep', zwaveEP.inChannel)
    #eventDispatcher.add_channel('awsiot_ep', awsIotEP.inChannel)

    dispatcher.start()

    dispatcher.wait_until_shutdown()
    zwaveEP.wait_until_shutdown()
    #awsIotEP.wait_until_shutdown()

    return 0
