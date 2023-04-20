
from max30102 import MAX30102
import hrcalc
import threading
import time
import numpy as np

       
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata,flags,rc):
    if rc == 0:
        print("connected Ok return code=", rc)
    else:
        print("bad connection returned code=", rc)

THINGSBOARD_HOST = 'thingsboard.cloud'
ACCESS_TOKEN = 'ZIHj40emzYy4QmWAfVn5'

client = mqtt.Client()

client.on_connect= on_connect

#set access token
client.username_pw_set(ACCESS_TOKEN)
#connect the things board using defult MQTT port and 60 seconds keepalvie interval of 60 sec
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
# time.sleep(4)



class HeartRateMonitor(object):
    """
    A class that encapsulates the max30102 device into a thread
    """
        
    #JT Feb 15, changing this so poll time may be read
    LOOP_TIME = 1
    
    
    
   
    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print('IR, Red')
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []
        bpms2 = []
        oxygen_data = []
        xs = []
        
    

        # run until told to stop
        while not self._thread.stopped:
            
            # check if any data is available
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    client.publish('v1/devices/me/telemetry', json.dumps({'irdata': ir}),1)
                    red_data.append(red)
                    if self.print_raw:
                        print("{0}, {1}".format(ir, red))
                    #client.publish('v1/devices/me/telemetry', json.dumps({'irdata': ir_data}),1)
                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                 
                    #ES - added check for valid spo2
                    
                    if valid_bpm & valid_spo2:
                        bpms.append(bpm)
                        #bpms2 = bpms
                        while len(bpms) > 4:
                            bpms.pop(0)
                        self.bpm = np.mean(bpms)
                        if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                            self.bpm = 0
                            spo2 = 0
                            if self.print_result:
                                print("Finger not detected")
                    if self.print_result:
                                bpms2.append(self.bpm)
                                oxygen_data.append(spo2)
                                client.publish('v1/devices/me/telemetry', json.dumps({'spO2': spo2}),1)
                                print("BPM: {0}, SpO2: {1}".format(self.bpm, spo2))
            client.publish('v1/devices/me/telemetry', json.dumps({'bpm': self.bpm}),1)
#             client.publish('v1/devices/me/telemetry', json.dumps({'bpm': self.bpm}),1)
#             client.publish('v1/devices/me/telemetry', json.dumps({'spO2': spo2}),1)

            time.sleep(self.LOOP_TIME)
        
       
        
        sensor.shutdown()
        client.loop_stop()
        client.disconnect()
        print(len(bpms2))
#         self.plotIr = ir_data
#         self.plotRed = red_data
        self.plotbpms = bpms2
        self.plotoxygen = oxygen_data

   
        
        
    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()
        
    
   
    def stop_sensor(self, timeout=2.0):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join(timeout)
#     """ JT- make a method that returns the IR_data, RED_data, and bpm array"""
        
#     def returnIrArray(self):
#         return self.plotIr
#     def returnRedArray(self):
#         return self.plotRed
#     def returnBPMArray(self):
#         return self.plotbpms
#     def returnOxygenArray(self):
#         return self.plotoxygen
    
    
    
