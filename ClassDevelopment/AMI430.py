"""
@author: Christopher Broyles
@date: September 18, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager("@py")

class AMI430:
    def __init__(self):
        self.visa_address = "TCPIP0::169.254.124.55::7180::SOCKET"
        return
    
    '''
        Set Methods for Keithley 6221
    '''

    def set_zero(self):
        handle = rm.open_resource(self.visa_address)
        handle.read_termination = '\r\n'
        handle.write_termination = '\n'
        handle.write("ZERO")
        handle.close()
        return
    def set_field(self,field):
        handle = rm.open_resource(self.visa_address)
        handle.read_termination = '\r\n'
        handle.write_termination = '\n'
        handle.write(f"CONF:FIELD:TARG {field}")
        handle.write("RAMP")
        time.sleep(1)
        handle.close()
        return
    def get_field(self):
        handle = rm.open_resource(self.visa_address)
        handle.read_termination = '\r\n'
        handle.write_termination = '\n'
        try:
            result1 = handle.read()
            result1 = handle.read()
            handle.write("FIELD:MAGnet?")
            string_data = handle.read()
            time.sleep(1)
            return float(string_data)
        finally:
            handle.close()
        
    def get_state(self):
        states = {
            1: "RAMPING",
            2: "HOLDING",
            3: "PAUSED",
            4: "Ramping in MANUAL UP",
            5: "Ramping in MANUAL DOWN",
            6: "ZEROING CURRENT in progress",
            7: "QUENCH!!!",
            8: "AT ZERO CURRENT",
            9: "Heating Persistent Switch",
            10: "Cooling Persistent Switch"
        }
        handle = rm.open_resource(self.visa_address)
        handle.read_termination = '\r\n'
        handle.write_termination = '\n'
        try:
            string_data = handle.read()
            string_data = handle.read()
            handle.write("State?")
            string_data = handle.read()
            return states[int(string_data)]
        finally:
            handle.close
            


        
        
