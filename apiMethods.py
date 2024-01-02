import os
import importlib.util

def findInstrumentFile(instrument, directory='./ClassDevelopment'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if instrument['model'].lower() in file.lower() and file.endswith('.py'):
                return os.path.join(root, file)
    return None
    
def getInstrument(instrumentData):
    module_path = findInstrumentFile(instrumentData)
    
    if module_path:
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        # Import module as class object
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        #Get Instrument class by className
        instrumentClass  = getattr(module, instrumentData['name'][0] + instrumentData['model'])
        instrument = instrumentClass(instrumentData['address'])
        return instrument
    else:
        return None
    
def getMethods(instrumentData):
        instrument = getInstrument(instrumentData)
        if instrument:            
            methods = dir(instrument)
            return methods
        else:
             return None

def getMethodInfo(instrumentData,methodName):
        instrument = getInstrument(instrumentData)
        if instrument:
            method = getattr(instrument,methodName)
            num_params = method.__code__.co_argcount
            param_names = method.__code__.co_varnames[1:num_params]
            return param_names
        else:
            return None
        
def executeMethod(instrumentData,methodName,param_list):
    instrument = getInstrument(instrumentData)
    if instrument:
         method = getattr(instrument,methodName)
         if callable(method):
              method(*param_list)
         else:
              return
         return 
    else:
         return None
    


# Example instrument data
instrument = {
    'id': 1,
    'name': "Keithley",
    'model': "2450",
    'address': "GPIB::17",
    'setMethods': [],
    'getMethods': []
}

# Usage
print(findInstrumentFile(instrument))
methods = getMethods(instrument)
methodInfo = getMethodInfo(instrument,'set_voltage')
if methods:
    print(methods)
    print('set_voltage', methodInfo)
else:
    print("Module not found or class not defined.")

