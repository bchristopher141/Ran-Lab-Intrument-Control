# -*- coding: utf-8 -*-
"""
@author: Christopher Broyles
@date: September 11, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()


class SR830:
    def __init__(self,visa_address):
        self.visa_address = visa_address

    def set_amplitude(self,amplitude):
        handle = rm.open_resource(self.visa_address)
        handle.write(f"SLVL {float(amplitude)}")
        handle.close()
        return 'set_amplitude method'
    
    def set_frequency(self, frequency):
        handle = rm.open_resource(self.visa_address)
        handle.write(f"FREQ {float(frequency)}")
        handle.close()
        return 'set_frequency method'
    
    def get_amplitude(self):
        handle = rm.open_resource(self.visa_address)
        handle.write(f"OUTX 1")
        read = float(handle.query('SLVL?'))
        handle.close()
        return 'get_amplitude method'
    
    def get_frequency(self):
        handle = rm.open_resource(self.visa_address)
        handle.write(f"OUTX 1")
        read = float(handle.query('FREQ?'))
        handle.close()
        return 'get_frequency method'

    def get_x(self):
        handle = rm.open_resource(self.visa_address)
        try:
            string_data = handle.query(f"OUTP? 1")
            numerical_data = float(string_data)
            return numerical_data
        finally:
            handle.close()
        return 1
    def get_y(self):
        handle = rm.open_resource(self.visa_address)
        try:
            string_data = handle.query(f"OUTP? 2")
            numerical_data = float(string_data)
            return numerical_data
        finally:
            handle.close()
        return 2
    def get_R(self):
        handle = rm.open_resource(self.visa_address)
        try:
            string_data = handle.query(f"OUTP? 3")
            numerical_data = float(string_data)
            return numerical_data
        finally:
            handle.close()
        return 3
    def get_Theta(self):
        handle = rm.open_resource(self.visa_address)
        try:
            string_data = handle.query(f"OUTP? 4")
            numerical_data = float(string_data)
            return numerical_data
        finally:
            handle.close()  
        return 4


    
