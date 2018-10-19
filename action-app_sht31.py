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
        self.sensor = SHT31(address = 0x44)
        self.start_blocking()
    
    def c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def askTemperature(self, hermes, intent_message):
        unit = None
        if intent_message.slots.unit:
            unit = intent_message.slots.unit.first().value
        
        if intent_message.site_id != self.site_id:
            return

        temp = round(self.sensor.read_temperature(), 1)
        temp_f = round(self.c_to_f(temp), 1)
        print "Celsius: {}*C / Fahrenheit {}*F".format(temp, temp_f)
        msg = "The current temperature is {}{}"

        if unit == "celsius":
            hermes.publish_end_session(intent_message.session_id, msg.format(temp, ' degree'))
        elif unit == "fahrenheit":
            hermes.publish_end_session(intent_message.session_id, msg.format(temp_f, ' fahrenheit degree'))
        elif unit is None:
            hermes.publish_end_session(intent_message.session_id, msg.format(temp, ' degree'))

    def askHumidity(self, hermes, intent_message):
        if intent_message.site_id != self.site_id:
            return
        humidity = round(self.sensor.read_humidity(), 2)
        print "Humidity: {}%".format(humidity)
        msg = "The current humidity is {}%".format(humidity)
        hermes.publish_end_session(intent_message.session_id, msg)

    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'coorfang:askTemperature':
            self.askTemperature(hermes, intent_message)
        if coming_intent == 'coorfang:askHumidity':
            self.askHumidity(hermes, intent_message)

    def start_blocking(self):
        with Hermes(self.mqtt_addr) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Temperature_Humidity_SHT31()
