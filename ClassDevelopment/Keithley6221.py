"""
@author: Christopher Broyles
@date: September 18, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()


class K6221:
    def __init__(self, visa_address):
        self.visa_address = visa_address
        return
    
    _source_current_setMethods = ['set_current','set_currentRange','set_voltageLimit', 'set_autoRange']
    _source_current_setMethods = ['get_current','get_currentRange','get_voltageLimit']

    def set_current(self,current):
        handle = rm.open_resource(self.visa_address)
        handle.write("CURR "+ str(current))
        handle.close()
        return
    
    current_options = {'options': None, 'range':'-105e-3 to 105e-3'}

    def set_currentRange(self,currentRange):
        handle = rm.open_resource(self.visa_address)
        handle.write("CURR:RANG " + str(currentRange))
        handle.close()
        return
    
    currentRange_options = {'options': None, 'range':'-105e-3 to 105e-3 Amps'}

    def set_autoRange(self, status):
        handle = rm.open_resource(self.visa_address)
        handle.write("CURR:RANG:AUTO  " + status)
        handle.close()
        return
    
    autoRange_options = {'options': {'ON':'ON', 'OFF':'OFF'}, 'range': None}
        
    
    def set_voltageCompliance(self,voltageCompliance):
        handle = rm.open_resource(self.visa_address)
        handle.write("CURR:COMP " + str(voltageCompliance))
        handle.close()
        return
    
    voltageLimit_options = {'options': None, 'range': '0.1 to 10 Volts'}
    
    def set_output(self,status):
        handle = rm.open_resource(self.visa_address)
        handle.write("OUTP  " + str(status))
        handle.close()
        return
    
    utput_options = {'options': {'ON':'ON', 'OFF':'OFF'}, 'range': None}
    
    def get_current(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData =handle.query("SOUR:CURR?")
            return float(stringData)
        finally:
            handle.close()

    def get_currentRange(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData =handle.query("SOUR:CURR:RANG?")
            return float(stringData)
        finally:
            handle.close()
    
    def get_voltageLimit(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData =handle.query("SOUR:CURR:COMP?")
            return float(stringData)
        finally:
            handle.close()

    def get_autoRange(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData =handle.query("SOUR:CURR:RANG:AUTO?")
            return float(stringData)
        finally:
            handle.close()
    def get_output(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData = handle.write("OUTP?")
            return stringData
        finally:
            handle.close()
        return


        
        
