import rule_base_setup_file_V2

from flask import Flask, request
from flask import jsonify
import json_ext

from flask_cors import CORS
import pandas as pd





#%%

app = Flask(__name__)
CORS(app)

app.json_encoder = json_ext.JSONEncoder
app.config['JSON_AS_ASCII'] = False

#%%

@app.route("/get_rules_json/", methods=['GET'])
def get_rules_json():
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

    return set_rule

@app.route("/name_list/", methods=['GET'])
def name_list():
    name_list = list(pd.read_excel('210310_point-mappings_v18.xlsx',sheet_name='DeviceList')["type"].dropna().unique())
    name_list = jsonify(name_list)
    return name_list

@app.route("/device_points/<DeviceType>", methods=['GET'])
def device_points(DeviceType):
    name_list = pd.read_excel('210310_point-mappings_v18.xlsx',sheet_name='PointList')
    name_list = list(name_list[name_list["DeviceType"]==DeviceType]["PointType"].dropna().unique())

    name_list = jsonify(name_list)
    return name_list


if __name__ == '__main__':
    app.run(debug=False)