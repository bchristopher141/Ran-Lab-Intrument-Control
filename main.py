from typing import List,Union
from flask import Flask, jsonify
from flask_cors import CORS
import time
import apiMethods 
app = Flask(__name__)
import apiMethods

# Your existing routes go here...


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://example.com"}})

# Create some sample data
data = [
  {
    'id': 1,
    'name': "Keithley",
    'model': "2450",
    'address': "GPIB::17",
    'setMethods': [],
    'getMethods': []
  },
  {
    'id': 2,
    'name': "Keithley",
    'model': "2182a",
    'address': "GPIB::12",
    'setMethods': [],
    'getMethods': []
  },
  {
      'id': 3,
    'name': "Lakeshore",
    'model': "372ac",
    'address': "GPIB::2",
    'setMethods': [],
    'getMethods': []
  },
  {
    'id': 4,
    'name': "Stanford Research",
    'model': "SR830",
    'address': "GPIB::5",
    'setMethods': [],
    'getMethods': []
  },
{
    'id': 5,
    'name': "Stanford Research",
    'model': "SR830",
    'address': "GPIB::6",
    'setMethods': [],
    'getMethods': []
  }
];

# Define a route to get all items
'''
This will return json object (ie. key value pair) of instruments
name, model,gpibaddress, in addition to the class method names. 

'''
import pyvisa
rm = pyvisa.ResourceManager()
import sys
import os

@app.route('/api/instruments', methods=['GET'])
def get_instruments():
    
    # resource_list = rm.list_resources()
    # intruments_array = []
    # index = 0
    # for resource in resource_list:
    #     temp_dict = {}
    #     temp_handler = rm.open_resource(resource)
    #     temp_result = temp_handler.query("*IDN?")
    #     temp_info = temp_result.strip('\n').split(',')
    #     temp_handler.close()
    #     temp_dict["id"]=index
    #     temp_dict["name"]=temp_info[0]
    #     temp_dict["model"] = temp_info[1]
    #     temp_dict['address'] = resource
    #     intruments_array.append(temp_dict)
    #     index += 1

    return jsonify({'instruments': data})

# Define a route to get a specific item
@app.route('/api/instruments/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify({'instruments': item})

@app.route('/api/instruments/<id>/<name>/<model>/<address>/<method>', methods=['GET'])
def get_method_info(id,name,model,address,method):
    instrumentData = {'id':id,'name':name,'model':model,'address':address,'method':method}
    try:
        methodParams = apiMethods.getMethodInfo(instrumentData)
        instrumentData["methodParams"]=methodParams
        return jsonify(instrumentData)
    except AttributeError:
        return jsonify({'error': 'Method not found'}), 404
    
@app.route('/api/instruments/<id>/<name>/<model>/<address>', methods=['GET'])
def get_instrument_methods(id,name,model,address):
    instrumentData = {'id':id,'name':name,'model':model,'address':address}
    try:
        methods = apiMethods.getMethods(instrumentData)
        instrumentData["methods"]=methods
        return jsonify(instrumentData)
    except AttributeError:
        return jsonify({'error': 'Instrument not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)

