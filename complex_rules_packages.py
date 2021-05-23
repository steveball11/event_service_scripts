#%%
import pandas as pd
import json
import re

#%%
# transfer import variables to dict form
def define_rules(**info):
    return info
# create single rule set
#%%
# create single rule in each token
def single_rule_create(single_rule,token):

    temp_id = F"{single_rule['DeviceId']}-{single_rule['PointType']}"
    judgement_string = F"{token}.value!=None and "
    try:
        judgement_string += F"{token}.value<{single_rule['UpperBound']} and "
    except:
        pass
    try:
        judgement_string += F"{token}.value>{single_rule['LowerBound']} and "
    except:
        pass
    try:
        judgement_string += F"{token}.value=={single_rule['SetValue']} and "
    except:
        pass
    return judgement_string[0:-5]


# if time contains in rules
def single_rule_create_time(single_rule):
    judgement_string_low = F"Timestamp(x.time).hour>{single_rule['LowerBound']}"
    judgement_string_high = F"Timestamp(x.time).hour<{single_rule['UpperBound']}"
    return judgement_string_low,judgement_string_high

# deal with each rule
def rule_dict_create(ori_rule):
    dict_judgement_string = {}
    for rule in list(ori_rule.keys()):
        if "time" not in ori_rule[rule]["DeviceId"]:
            dict_judgement_string.update({rule:single_rule_create(ori_rule[rule],rule)})
        else:
            time_low_str,time_high_str = single_rule_create_time(ori_rule[rule])
            dict_judgement_string.update({rule:F"{time_low_str} and {time_high_str}"})

    return dict_judgement_string





def dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator):
    try:
        if_B1_R1 = (re.search("[A-Za-z]",Floor).span()[1])
        reverse_Floor = Floor[::-1]
        dict_id = [{'_id':F'{IdDescription}',
        'name':F"{EventName}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"floor":F"TPKD-{reverse_Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':[]
        }]
    except:
        dict_id = [{'_id':F'{IdDescription}',
        'name':F"{EventName}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':[]
        }]
    return json.dumps(dict_id,ensure_ascii=False)

def main(EventName,Level,PointId,Description,DeviceType,DeviceId,Floor,GUID,x_rule,y_rule):

    y_rule_keys = list(y_rule.keys())
    # create ID decription
    every_pointId = [F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointType']}" for rule in y_rule_keys]
    IdDescription = F"{PointId}"
    for set_id in every_pointId:
        if set_id.split("-")[0]==DeviceId:
            IdDescription += F"-{set_id.split('-')[1]}"
        elif set_id.split("-")[0]=='time':
            IdDescription += F"-time"
        else:
            IdDescription += F"-{set_id}"
    IdDescription += "-alarm"
    #
    y_rule_keys = list(y_rule.keys())
    arguments = {"arguments":{list(x_rule.keys())[0]:{"_t":"topic"}}}
    # time is not composed as a device, only can be regarded as a rule
    for rule in y_rule_keys:
        temp_PointId = F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointType']}"
        if "time" not in y_rule[rule]['DeviceId']:
            arguments["arguments"].update({F"{rule}":{"_t":"cache","key":F"shadow/points/{temp_PointId}/presentvalue"}})
    # x_rule
    judgement_string_x = rule_dict_create(x_rule)
    # y_rule
    judgement_string_y = rule_dict_create(y_rule)

    # calcultor_string
    calculator = {"_t":"default"}
    # add arguments
    calculator.update(arguments)
    # expression combine
    expression_str = F"({judgement_string_x['x']})"
    for rule in list(judgement_string_y.keys()):
        expression_str += F" and ({judgement_string_y[rule]})"

    conditions = {"conditions":
            {"activate":
            {"_t":"simple"
            ,"expression":expression_str}
        }
    }
    calculator.update(conditions)
    dict_id = dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator)
    return dict_id

if __name__ == '__main__':
    EventName = "上班時間設備通訊異常"
    Level = "警報"
    PointId = "FCU_333_8-COM_AL"
    Description = F"{PointId}-{EventName}"
    DeviceType = "FCU"
    Floor = "8"
    DeviceId = "FCU_333_8"
    GUID = "9599b326-0bd3-449d-9bc6-5293c249a13f"
    x_rule = {"x":{"DeviceId":"FCU_333_8","Point":"COM_AL","SetValue":"True"}}
    y_rule = {"y1":{
        "DeviceId":"time","Point":"time","UpperBound":18,"LowerBound":8},
        }
    EventName = "上班時間出風溫度未隨冰水閥開度增加降低"
    Level = "警報"
    PointId = "AHU_37_15_PRE-CV_POS"
    Description = F"{PointId}-{EventName}"
    DeviceType = "AHU"
    Floor = "15"
    DeviceId = "AHU_37_15_PRE"
    GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
    x_rule = {"x":{"DeviceId":"AHU_37_15_PRE","PointType":"CV_POS","UpperBound":70}}
    y_rule = {"y1":{
        "DeviceId":"AHU_37_15_PRE","PointType":"SA_T","UpperBound":28},
        "y2":{
        "DeviceId":"AHU_37_15_PRE","PointType":"FAN_RUN_CMD","SetValue":"True"},
        "y3":{
        "DeviceId":"time","PointType":"time","UpperBound":18,"LowerBound":8}
        }
    print(main(EventName=EventName,Level=Level,PointId=PointId,Description=Description,DeviceType=DeviceType,Floor=Floor,DeviceId=DeviceId,GUID=GUID,x_rule=x_rule,y_rule=y_rule))

# %%
