#!/usr/bin/python
import datetime
import paho.mqtt.publish as publish
import my_secrets


def publish_data(topic, payload): 
    publish.single(topic, payload, hostname=my_secrets.hostname, port=my_secrets.port, client_id=my_secrets.client_id, auth=my_secrets.auth)

# read and print the actual time / date information to the command line
now = datetime.datetime.now()
print("*******************************************************************")
print("*** RKI SCRAPER ***************************************************")
print("Actual Time/Date of call: %s"%(now.strftime("%Y-%m-%d %H:%M:%S")))
print("*******************************************************************")

# read RKI history buffer

# read RKI data from RKI page

# process RKI data to get 7 day incident value

# update RKI history buffer with new value

# publish RKI data to MQTT
publish_data('std/devTest/s/test/', 'HELLO')
