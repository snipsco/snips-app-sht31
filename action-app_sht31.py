#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

from Adafruit_SHT31 import *

CONFIG_INI = "config.ini"

class Temperature_Humidity_SHT31(object):
    def __init__(self):

        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None
            print "[Error] No config.ini file found! Please check.."
            sys.exit(1)

        self.mqtt_host = self.config.get('secret',{"mqtt_host":"localhost"}).get('mqtt_host','localhost')
        self.mqtt_port = self.config.get('secret',{"mqtt_port":"1883"}).get('mqtt_port','1883')
        self.mqtt_addr = "{}:{}".format(self.mqtt_host, self.mqtt_port)

        self.site_id = self.config.get('secret',{"site_id":"default"}).get('site_id','default')
        self.if_fahrenheit = self.config.get('secret',{"if_fahrenheit":"false"}).get('if_fahrenheit', "false")
        self.sensor = SHT31(address = 0x44)
        self.start_blocking()

    def c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def askTemperature(self, hermes, intent_message):
        temp = round(self.sensor.read_temperature(), 1)
        temp_f = round(self.c_to_f(temp), 1)
        
        print "Celsius: {}*C / Fahrenheit {}*F".format(temp, temp_f)
        msg = "The current temperature is {}{}"

        if self.if_fahrenheit.lower() == "false":
            msg = msg.format(temp, ' degree')
        elif self.if_fahrenheit.lower() == "true":
            msg = msg.format(temp_f, ' fahrenheit degree')
        else:
            msg = "No unit specified, please check config.ini file"

        hermes.publish_end_session(intent_message.session_id, msg)

    def askHumidity(self, hermes, intent_message):
        humidity = round(self.sensor.read_humidity(), 2)
        
        print "Humidity: {}%".format(humidity)
        msg = "The current humidity is {}%".format(humidity)
        
        hermes.publish_end_session(intent_message.session_id, msg)

    def master_intent_callback(self,hermes, intent_message):
        if intent_message.site_id != self.site_id:
            return
        if intent_message.intent.intent_name == 'checkTemperature':
            self.askTemperature(hermes, intent_message)
        if intent_message.intent.intent_name == 'checkHumidity':
            self.askHumidity(hermes, intent_message)

    def start_blocking(self):
        with Hermes(self.mqtt_addr) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Temperature_Humidity_SHT31()
