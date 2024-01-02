"""
@author: Christopher Broyles
@date: September 11, 2023
"""

import numpy as np
import time
import pyvisa

rm = pyvisa.ResourceManager()
environmentOptions = {'sourceMode':{'Voltage':"VOLT", 'Current':"CURR"},
                      'senseMode':{'Current':"CURR",'Voltage':"VOLT", "Resistance":"RES"},
                      'terminal':{'Front':"FRON", "Rear":'REAR'},
                      'output':{'ON':"ON","OFF":"OFF"}}
sourceOptions = {'CURR':{
'source':{'min':-1.05,'max':1.05,'unit':'Amp'},
'sourceRange':{'10 nA':1e-8,'100 nA':1e-7,'1 uA':1e-6,'10 uA':1e-5,'100 uA':1e-4,'1 mA':1e-3,'10 mA':1e-2,'100 mA':1e-1,'1 A':1},
'sourceLimit':{'min':0.02,'max':210,'unit':'Volt'},
'autoRange':{'ON':"ON","OFF":"OFF"}
},'VOLT':{
'source':{'min':-210,'max':210,'unit':'Volt'},
'sourceRange':{'20 mV':2e-2,'200 mV':2e-1,'2 V':2,'20 V':2e1,'200 V':2e2},
'sourceLimit':{'min':1e-9,'max':1.05,'unit':'Amp'},
'autoRange':{'ON':"ON","OFF":"OFF"}
}}
senseOptions = {'CURR':{'senseRange':{'min':10e-9,'max':1,'unit':'Amp'},
                 'autoRange':{'ON':"ON","OFF":"OFF"},
                 'fourWire': {'ON':"ON","OFF":"OFF"},
                 'nplc':{'min':0.01,'max':10,'unit':None}
},'VOLT':{
    'senseRange':{'min':0.02,'max':200,'unit':'Volt'},
    'autoRange':{'ON':"ON","OFF":"OFF"},
    'fourWire': {'ON':"ON","OFF":"OFF"},
    'nplc':{'min':0.01,'max':10,'unit':None}
},'RES':{
    'senseRange':{'min':20,'max':200e-6,'unit':'Ohm'},
    'autoRange':{'ON':"ON","OFF":"OFF"},
    'fourWire': {'ON':"ON","OFF":"OFF"},
    'nplc':{'min':0.01,'max':10,'unit':None}
}}
class K2450:
    def __init__(self, visa_address):
        self.visa_address = visa_address
        self._sourceMode_ = 'VOLT'
        self._senseMode_ = 'CURR'
        self._sourceOptions_ = sourceOptions['VOLT']
        self._senseOptions_ = senseOptions['CURR']
        self._terminal_ = 'FRON'
        self._output_ = "OFF"
        return
    
    '''
        Environment Methods for Keithley 2450
    '''
    def sourceMode(self,func):
        handle = rm.open_resource(self.visa_address)
        if func == 'GET':
            try:
                stringData = handle.query("SOUR:FUNC?")
                return stringData, environmentOptions['sourceMode']
            finally:
                handle.close()
        elif func in environmentOptions['sourceMode'].values():
            handle.write(f":SOUR:FUNC {str(func)}") 
            self._sourceMode_ = func
            self._sourceOptions_ = sourceOptions[func]
            return
    def senseMode(self,func):
        handle = rm.open_resource(self.visa_address)
        if func == "GET":
            try:
                stringData = handle.query(":SENS:FUNC?")
                return stringData, environmentOptions['senseMode']
            finally:
                handle.close()
        elif func in environmentOptions['senseMode'].values():
            handle.write(f":SENS:FUNC {str(func)}")
            self._senseMode_ = func
            self._senseOptions_ = senseOptions[func]
            return
    def terminal(self, terminal):
        handle = rm.open_resource(self.visa_address)
        if terminal == 'GET':
            try:
                stringData = handle.query(":ROUT:TERM?")
                return stringData, environmentOptions['terminal']
            finally:
                handle.close()
        elif terminal in environmentOptions['senseMode'].values():
            handle.write(f":ROUT:TERM {terminal}")
            handle.close()
            self._terminal_ = terminal
            return    
    def output(self,status = "OFF"):
        handle = rm.open_resource(self.visa_address)
        if status == 'GET':
            try:
                stringData = handle.query(":OUTP?")
                return stringData, environmentOptions['output']
            finally:
                handle.close()
        elif status in environmentOptions['output'].values():
            handle.write(f":OUTP {status}")
            handle.close()
            self._output_ = status
        return
    
    '''
        Source Methods for Keithley 2450
    '''
    def source(self, sourceValue):
        options = self._sourceOptions_['source'] 
        handle = rm.open_resource(self.visa_address)
        if sourceValue == 'GET':
            try:
                stringData = handle.query(f":SOUR:{self.sourceMode}?")
                return float(stringData), options
            finally:
                handle.close()
        elif float(sourceValue)>options['min'] & float(sourceValue)<options['max']:
            handle.write(f":SOUR:{self.sourceMode} " + str(sourceValue))
            handle.close()
            return


    def sourceRange(self, sourceRange):
        options = self._sourceOptions_['sourceRange']
        handle = rm.open_resource(self.visa_address)
        if sourceRange == 'GET':
            try:
                stringData = handle.query(f":SOUR:{self.sourceMode}:RANG?")
                return float(stringData)
            finally:
                handle.close()
        elif sourceRange in options.values():
            handle.write(f":SOUR:{self.sourceMode}:RANG " + str(sourceRange))
            handle.close()
        return
    
    def sourceAutoRange(self,status):
        options = self._sourceOptions_['autoRange']
        handle = rm.open_resource(self.visa_address)
        if status == 'GET':
            try:
                stringData = handle.query(f":SOUR:{self.sourceMode}:RANGE:AUTO?")
                return stringData
            finally:
                handle.close()
        elif status in options.values():
            handle.write(f":SOUR:{self.sourceMode}:RANGE:AUTO {status}")
            handle.close()
        return
    
    
    def sourceLimit(self, sourceLimit):
        options = self._sourceOptions_['sourceLimit']
        command = f":SOUR:{self.sourceMode}:ILIM"
        if self.func == "CURR":
            command = f":SOUR:{self.sourceMode}:VLIM"
        handle = rm.open_resource(self.visa_address)
        if sourceLimit == 'GET':
            stringData = handle.query(command + "?")
            return stringData, options
        elif sourceLimit in options.values():
            handle.write(command+str(sourceLimit))
            handle.close()
            return

    
    '''
        Sense Methods for Keithley 2450
    '''
    def fourWire(self,status = "ON"):
        options = self._senseOptions_['fourWire']
        handle = rm.open_resource(self.visa_address)
        if status == 'GET':
            stringData = handle.query(f":SENS:{self.senseMode}")
            return stringData, options
        elif status in options.values():
            handle.write(f":SENS:{self.senseMode}:RSEN {status}")
            handle.close()
            return
    def senseRange(self, senseRange):
        options = self._senseOptions_['senseRange']
        handle = rm.open_resource(self.visa_address)
        if senseRange == "GET":
            try:
                stringData = handle.query(f":SENS:{self.senseMode}:RANGE?")
                return stringData, options
            finally:
                handle.close()
        elif senseRange in options.values():
            handle.write(f":SENS:{self.senseMode}:RANGE {senseRange}")

        return
    def senseNPLC(self, nplc):
        options = self._senseOptions_["nplc"]
        handle = rm.open_resource(self.visa_address)
        if nplc == "GET":
            try:
                stringData = handle.query(f":SENS:{self.senseMode}:NPLC?")
                floatData = float(stringData)
                return stringData, 
    
    def measureCurrent(self):
        handle = rm.open_resource(self.visa_address)
        try:
            stringData = handle.query(f":MEAS:{self.senseMode}")
            return float(stringData)
        finally:
            handle.close()
    

    
    def get_current(self,points,delay=0.01,nplc=1):
        handle = rm.open_resource(self.visa_address)
        handle.write(":SENS:FUNC 'CURR'")
        handle.write(":SENS:CURR:RANGE:AUTO ON")
        handle.write(":SENS:CURR:NPLC " + str(nplc))
        handle.write(":TRIG:LOAD 'SimpleLoop',"+str(points)+"," + str(delay))
        handle.write(":INIT")
        handle.write("*WAI")
        try:
            result = handle.query(":TRAC:DATA? 1, "+str(points)+", 'defbuffer1', READ, SOUR")
            handle.write("*WAI")
            list_data = result.split(',')
            sense_data = []
            source_data = []
            for index in range(len(list_data)):
                if index%2 == 0:
                    sense_data.append(float(list_data[index]))
                else:
                    source_data.append(float(list_data[index]))
            return sense_data, source_data
        finally:
            handle.close()
        

    def get_voltage(self,points,delay=0.01,nplc=1):
        handle = rm.open_resource(self.visa_address)
        handle.write(":SENS:FUNC 'VOLT'")
        handle.write(":SENS:VOLT:NPLC " + str(nplc))
        handle.write(":TRIG:LOAD 'SimpleLoop',"+str(points)+"," + str(delay))
        handle.write(":INIT")
        handle.write("*WAI")
        try:
            result = handle.query(":TRAC:DATA? 1, "+str(points)+", 'defbuffer1', READ, SOUR")
            handle.write("*WAI")
            list_data = result.split(',')
            sense_data = []
            source_data = []
            for index in range(len(list_data)):
                if index%2 == 0:
                    sense_data.append(float(list_data[index]))
                else:
                    source_data.append(float(list_data[index]))
            return sense_data, source_data
        finally:
            handle.close()

    


