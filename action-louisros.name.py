#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import time
import datetime

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
    

    if intentMessage.intent.intent_name == 'louisros:selectStation' :

        station = intentMessage.slots.radioName.first().value  
        fv = open("/var/lib/snips/skills/live","r")
        live = int(PyString(fv.read()))
        fv.close()              
        if live == 0 :
            live = 1
        if live == 4 :
            live = 2        
        fv =open("/var/lib/snips/skills/live","w") 
        fv.write(CString(str(live)))
        fv.close()

        fv=open("/var/lib/snips/skills/link","w")
        fv.write(CString(links[station]))
        fv.close()
        resul = ""
      
    elif intentMessage.intent.intent_name == 'louisros:changeVolume' :
        vol = intentMessage.slots.var.first().value 
        fv =open("/var/lib/snips/skills/volume","r")
        volume = PyString(fv.read())
        fv.close()
        if vol == "plus fort":
            v = int(volume)
            v = v + 1
            if v > 10 :
                v = 10
            volume = str(v) 
        elif vol == "moins fort":
            v = int(volume)
            v = v - 1
            if v < 0 :
                v = 0
            volume =str(v)
        else:
            volume = str(int(vol)) 
          
 
        fv =open("/var/lib/snips/skills/volume","w")
        fv.write(CString(volume))
        fv.close()
        live = 3
        fv = open("/var/lib/snips/skills/live","w") 
        fv.write(CString(str(live)))
        fv.close()
        resul = ""
            
            
            
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, resul)


if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:           
        h.subscribe_intents(intents_callback).start()
        
