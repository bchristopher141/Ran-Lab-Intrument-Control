"""
@author: Christopher Broyles
@date: September 18, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()


class K2182a:
    def __init__(self, visa_address):
        self.visa_address = visa_address
        return
    
    '''
        Set Methods for Keithley 2182a
    '''

    def set_voltageRange(self,voltageRange,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write(":SENSE:CHAN " + str(channel))
        handle.write("SENS:VOLT:RANG %f" %voltageRange)
        handle.close()
    

    def get_voltage(self,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write(":SENSE:CHAN " + str(channel))
        try:
            string_data = handle.query(':read?')
            return float(string_data)
        except(RuntimeError):
            print(RuntimeError)
        return
        


        
        
