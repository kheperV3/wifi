#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import time
import datetime
#import string

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def PyString(s) :
      if s[len(s)-1] == '\0' :
            s = s[0:len(s)-1]
      return s
      
def CString(s):
      if s[len(s)-1] != '\0' :
            s = s + '\0'
      return s 

def intents_callback(hermes, intentMessage) : 
  

    if intentMessage.intent.intent_name == 'louisros:name' :
            global n 
            n = ""       
            hermes.publish_continue_session(intentMessage.session_id,"premier caractère",["louisros:signe","louisros:name"])
                                           
      
    elif intentMessage.intent.intent_name == 'louisros:signe' :
            s = ""
            m = ""
            t = ""
            s = intentMessage.slots.s.first().value 
            m = intentMessage.slots.m.first().value
            t = intentMessage.slots.t.first().value
            if s != 'fin' :
                  if m != "" :
                        s = m[0]
                  if t == 'grand' :
                  #s = string.upper(s) 
                        x = 0
                  n = n + s          
                  hermes.publish_continue_session(intentMessage.session_id,"suivant",["louisros:signe","louisros:name"])
            else:
                  resul = n
                          
                  hermes.publish_end_session(intentMessage.session_id, resul)


if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:           
        h.subscribe_intents(intents_callback).start()
        
