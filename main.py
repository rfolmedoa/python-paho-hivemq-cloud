# loading environment variables from a .env file
from dotenv import load_dotenv 
import os
load_dotenv()
hivemq_username = os.getenv("USERNAME")
hivemq_password = os.getenv("PASSWORD")
hivemq_cluster_url = os.getenv("CLUSTER_URL")

# This library allows Python applications to connect to an MQTT broker
import paho.mqtt.client as paho
from paho import mqtt

# This library allows you to control which warnings are displayed
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("----------PUBLISHER/SUSCRIBER----------")

# setting callbacks for different events to see if it works, print the message etc.
# callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code {}.".format(rc)) # rt: reason code

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid)) # mid: message ID

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(hivemq_username, hivemq_password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(hivemq_cluster_url, 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("#", qos=1) # qos: quality of service 

# ask for a message in the terminal
payload_to_publish = input("Type the message you wish to publish: ")

# a single publish, this can also be done in loops, etc.
client.publish("topic1", payload=payload_to_publish, qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever() # continuously monitors network traffic for incoming and outgoing messages.

