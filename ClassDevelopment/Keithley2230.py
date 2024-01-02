"""
@author: Christopher Broyles
@date: September 18, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()


class K2230:
    def __init__(self, visa_address):
        self.visa_address = visa_address
        return
    
    '''
        Set Methods for Keithley 2450
    '''

    def set_voltage(self,voltage, channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        handle.write("INST "+str(channel))
        handle.write("VOLT %f"%voltage)    
        handle.close()
        return

    def set_curret(self,current,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        handle.write("INST "+str(channel))
        handle.write("CURR %f"%current)
        handle.close()
        return
    
    def set_voltageLimit(self,voltageLimit, channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        handle.write("INST "+str(channel))
        handle.write("VOLT:LIM " + str(voltageLimit))
        handle.close()
        return
    
    def set_currentLimit(self,currentLimit,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        handle.write("INST "+str(channel))
        handle.write("CURR:LIM " + str(currentLimit))
        handle.close()
        return
    
    '''
        Get Methods for Keithley 2450
    '''

    def get_current(self,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        try:
            string_data = handle.query('MEAS:CURR? ' + channel)
            return float(string_data)
        finally:
            handle.close()
    def get_voltage(self,channel):
        handle = rm.open_resource(self.visa_address)
        handle.write("SYS:REM")
        try:
            string_data = handle.query('MEAS:VOLT? ' + channel)
            return float(string_data)
        finally:
            handle.close()
