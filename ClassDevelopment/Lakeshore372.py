"""
@author: Christopher Broyles
@date: September 18, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()


class LS372:
    def __init__(self, visa_address):
        self.visa_address = visa_address
        return
    
    '''
        Set Methods for Lakeshore 372
    '''

    def set_temperature(self, temperature,output = 0):
        handle = rm.open_resource(self.visa_address)
        handle.write("SETP "+ str(output) + ", " + str(temperature))
        handle.close()
        return



        


        
        
