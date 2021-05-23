import rule_base_setup_file_V2

from flask import Flask, request
from flask import jsonify
import json_ext

from flask_cors import CORS
import pandas as pd
from flasgger import Swagger




#%%

app = Flask(__name__)
CORS(app)
Swagger(app)
app.json_encoder = json_ext.JSONEncoder
app.config['JSON_AS_ASCII'] = False

#%%

@app.route("/get_rules_json/", methods=['GET'])
def get_rules_json():
    """
    Create management rules by entering 
    Call this api passing a language name and get back its features
    ---
    tags:
      - Get rules in json form
    parameters:
        - in: query
          name: DeviceType
          schema:
          type: string
          description: assign DeviceType
        - in: query
          name: PointType
          schema:
          type: string
          description: assign PointType
        - in: query
          name: IdDescription
          schema:
          type: string
          description: IdDescription 
        - in: query
          name: Expression
          schema:
          type: string
          description: expression of conditions
        - in: query
          name: Description
          schema:
          type: string
          description: Description
        - in: query
          name: EventName
          schema:
          type: string
          description: EventName
        - in: query
          name: Level
          schema:
          type: string
          description: Level
    responses:
      500:
        description: request fail
      200:
        description: request success        
    """       
    DeviceType = request.values.get('DeviceType')
    PointType = request.values.get('PointType')
    IdDescription = request.values.get('IdDescription')
    Expression = request.values.get('Expression')
    Description = request.values.get('Description')
    EventName = request.values.get('EventName')
    Level = request.values.get('Level')
    set_rule = rule_base_setup_file_V2.Set_up_rules(DeviceType=DeviceType,
                        PointType=PointType,
                        IdDescription=IdDescription,
                        Expression=Expression,
                        Description=Description,
                        EventName=EventName,
                        Level=Level).create_text()
    set_rule = jsonify(set_rule)
    return set_rule

@app.route("/name_list/", methods=['GET'])
def name_list():
    
    """
    Use this api to get the hole data in TPKD building
    Call this api passing a language name and get back its features
    ---
    tags:
      - Get rules in json form
    parameters:
      - name: DeviceType
        in: path
        type: string
        required: query
        description: DeviceType      
    responses:
      500:
        description: request fail
      200:
        description: request success
        schema:
          id: Schema
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """   
    
    name_list = list(pd.read_excel('210310_point-mappings_v18.xlsx',sheet_name='DeviceList')["type"].dropna().unique())
    name_list = jsonify(name_list)
    return name_list

@app.route("/device_points/<DeviceType>", methods=['GET'])
def device_points(DeviceType):
    """
    Assign specific DeviceType to get which points can be set
    Call this api passing a language name and get back its features
    ---
    tags:
      - Get rules in json form
    parameters:
      - name: DeviceType
        in: path
        type: string
        required: true
        description: DeviceType

    responses:
      500:
        description: request fail
      200:
        description: request success
        schema:
          id: Schema
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """    
    point_list = pd.read_excel('210310_point-mappings_v18.xlsx',sheet_name='PointList')
    point_list = list(point_list[point_list["DeviceType"]==DeviceType]["PointType"].dropna().unique())

    point_list = jsonify(point_list)
    return point_list


if __name__ == '__main__':
    # http://127.0.0.1:5010/apidocs/
    app.run(debug=False,host="127.0.0.1",port="5001")