from zwave_ep.zwave_proxy import ZwaveProxy
from awsiot_ep.awsiot_client import AWSIOTClient
from app_config import *
import time

class Application():
    def main(self, argc, argv):
        print ('Starting Application...')
        zWaveProxy.start(ZWAVE_PROXY_THREADS)
        self.waitUntilShutdown()
        return 0

    def waitUntilShutdown(self):
        zWaveProxy.add_task('123') 
        zWaveProxy.add_task('123')
        zWaveProxy.wait_complete()
        print('waitUntilShutdown exiting')

    def shutdown(self):
        zWaveProxy.stop()

app = Application()
awsIotClient = AWSIOTClient()
zWaveProxy = ZwaveProxy()
