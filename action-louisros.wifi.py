#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import time
import datetime
import string
import os

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def intents_callback(hermes, intentMessage) : 
 
    if intentMessage.intent.intent_name == 'louisros:changeSSID' :
            
 
            global phase
            global n
            phase = 0
            n = ""
            hermes.publish_continue_session(intentMessage.session_id,"nouvel S S I D premier caractère",["louisros:signe","louisros:keyOK"])
                                           
      
    elif intentMessage.intent.intent_name == 'louisros:signe' :
            s = ""
            m = ""
            t = ""
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
                  
                  hermes.publish_continue_session(intentMessage.session_id,"suivant",["louisros:signe","louisros:keyOK"])
            else:
                  global ssid
                  global key
                  if phase == 0 :
                        ssid = n
                        n = ""
                        phase = 1                                                             
                        hermes.publish_continue_session(intentMessage.session_id,"Ce nom de S S I D est-il correct?",["louisros:ssidOK","louisros:changeSSID"])

                  else:
                        key = n
                        hermes.publish_continue_session(intentMessage.session_id,"Validez vous cette clé?",["louisros:keyOK","louisros:changeSSID"])
                        
    elif intentMessage.intent.intent_name == 'louisros:ssidOK' :
            ok = intentMessage.slots.ok.first().value 
            if ok != "oui":
                  hermes.publish_end_session(intentMessage.session_id, "mise à jour abandonnée")
            else:
                  hermes.publish_continue_session(intentMessage.session_id,"nouvelle clé premier caractère",["louisros:signe"])
      
    elif intentMessage.intent.intent_name == 'louisros:keyOK' :   
            ok = intentMessage.slots.ok.first().value 
            if ok != "oui":
                  hermes.publish_end_session(intentMessage.session_id, "mise à jour abandonnée")
            else:
                  ssid = '\\"' + ssid + '\\"'
                  key = '\\"' + key + '\\"'
                  r = 'sudo echo \"\n\nnetwork = {\nssid=' + ssid + '\npsk=' + key + '\n}" >>/etc/wpa_supplicant/wpa_supplicant.conf'
                  os.system (r)

                  hermes.publish_end_session(intentMessage.session_id, "mise à jour effectuée")
      
    elif intentMessage.intent.intent_name == 'louisros:changeKEY' :
            hermes.publish_continue_session(intentMessage.session_id,"premier caractère",["louisros:signe","louisros:changeSSID"])
      

if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:           
            h.subscribe_intents(intents_callback).start()
        
