from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from event_dispatcher.event_dispatcher import zywave_dispatcher

_dailyEventCount = 0

class AWSIotEP():
    """ Sends or receives messages from AWS IOT """

    # TODO handle incoming/outgoing messages messages.
    # Using a aws-to-zwave Serializer/De-Serializer (MQTT)
    # onNewZwaveEvent - map / send to AWS IOT
    # onNewAWSIOTEvent - map / send to ZWAVE NETWORK

    def __init__(self):
        self._awsIotClient = self.setupAwsIotClient()

    def setupAwsIotClient(self):
        myMQTTClient = AWSIoTMQTTClient("MyPythonMQTTPub")
        myMQTTClient.configureEndpoint("a352k6gnga96jt-ats.iot.us-west-2.amazonaws.com", 8883)
        myMQTTClient.configureCredentials("./certificate/AmazonRootCA1.pem", "./certificate/private.pem", "./certificate/awsiot-certificate.pem.crt")
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(10)
        myMQTTClient.configureMQTTOperationTimeout(5)
        return myMQTTClient

    def publish(self, payload):
        self._awsIotClient.connect()
        self._awsIotClient.publish("myTopic/1", payload, 0)
        self._awsIotClient.disconnect()

    def dailyEventCount(self):
        global _dailyEventCount
        return _dailyEventCount

    def processEvent(self, event):
        global _dailyEventCount
        self.publish(event.payload)
        _dailyEventCount += 1
