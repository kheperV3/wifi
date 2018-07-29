#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import time
import datetime
import string

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
  

    if intentMessage.intent.intent_name == 'louisros:changeSSID' :
            global ssid 
            global key
            global phase
            ssid = "" 
            key = ""
            phase = 0
            hermes.publish_end_session(intentMessage.session_id,"sur la bonne voie")
            hermes.publish_continue_session(intentMessage.session_id,"nouvel SSID premier caractère",["louisros:signe","louisros:keyOK"])
                                           
      
    elif intentMessage.intent.intent_name == 'louisros:signe' :
            s = ""
            m = ""
            t = ""
            n = ""
      
            if len(intentMessage.slots.s):
                  s = intentMessage.slots.s.first().value 
            if len(intentMessage.slots.m):     
                  m = intentMessage.slots.m.first().value
            if len(intentMessage.slots.t):
                  t = intentMessage.slots.t.first().value
            if t != 'fin' :
                  if m != "" :
                        s = m[0]
                  if t == 'grand' :
                        s = string.upper(s) 
                        
                  n = n + s  
                  
                  hermes.publish_continue_session(intentMessage.session_id,"suivant",["louisros:signe","louisros:keyOK")
            else:
                  if phase == 0 :
                        ssid = n
                        hermes.publish_continue_session(intentMessage.session_id,"Ce nom de SSID est-il correct? ",["louisros:ssidOK"])
                        phase = 1
                  else:
                        key = n
                        hermes.publish_continue_session(intentMessage.session_id,"Validez vous cette clé? ",["louisros:keyOK"])
                        
    elif intentMessage.intent.intent_name == 'louisros:ssidOK' :
            ok = intentMessage.slots.ok.first().value 
            if ok != "oui":
                  hermes.publish_end_session(intentMessage.session_id, "mise à jour abandonnée")
            else:
                  hermes.publish_continue_session(intentMessage.session_id,"nouvelle clé",["louisros:changeKEY"])
      
    elif intentMessage.intent.intent_name == 'louisros:keyOK' :   
            ok = intentMessage.slots.ok.first().value 
            if ok != "oui":
                  hermes.publish_end_session(intentMessage.session_id, "mise à jour abandonnée")
            else:
                  r = ssid + "  " + key
                  hermes.publish_end_session(intentMessage.session_id,r)
      
    elif intentMessage.intent.intent_name == 'louisros:changeKEY' :
            hermes.publish_continue_session(intentMessage.session_id,"nouvelle clé premier caractère",["louisros:signe"])
if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:           
        h.subscribe_intents(intents_callback).start()
        