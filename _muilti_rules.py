#%%
import pandas as pd
import json
import re
#%%
# transfer import variables to dict form
def define_rules(**info):
    return info


def rule_str_create(ori_rule):
    target_id = F"{ori_rule['DeviceId']}-{ori_rule['PointId']}"
    judgement_string = F"{target_id}.value != None and "
    try:
        judgement_string += F"{target_id}.value<{ori_rule['UpperBound']} and "
    except:
        pass
    try:
        judgement_string += F"{target_id}.value>{ori_rule['LowerBound']} and "
    except:
        pass
    try:
        judgement_string += F"{target_id}.value=={ori_rule['SetValue']} and "
    except:
        pass
    return judgement_string[0:-5]

def rule_str_create_time(ori_rule,PointId):
    judgement_string = ""
    judgement_string_low = F"Timestamp({PointId}.time).hour>{ori_rule['LowerBound']}"
    judgement_string_high = F"Timestamp({PointId}.time).hour<{ori_rule['UpperBound']}"
    return judgement_string_low,judgement_string_high

def dict_id_create_complex_rules(IdDescription,Event_Name,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator):
    try:
        if_B1_R1 = (re.search("[A-Za-z]",Floor).span()[1])
        reverse_Floor = Floor[::-1]
        dict_id = [{'_id':F'{IdDescription}',
        'name':F"{Event_Name}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"floor":F"TPKD-{reverse_Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':[]
        }]
    except:
        dict_id = [{'_id':F'{IdDescription}',
        'name':F"{Event_Name}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':[]
        }]
    return json.dumps(dict_id,ensure_ascii=False)
def main(Event_Name,Level,PointId,Description,DeviceId,GUID,x_rule,y_rule):
    y_rule_keys = list(y_rule.keys())
    # create ID decription
    every_pointId = [F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointId']}" for rule in y_rule_keys]
    IdDescription = F"{PointId}"
    for set_id in every_pointId:
        if set_id.split("-")[0]==DeviceId:
            IdDescription += F"-{set_id.split('-')[1]}"
        elif set_id.split("-")[0]=='time':
            IdDescription += F"-WH"
        else:
            IdDescription += F"-{set_id}"
    IdDescription += "-alarm"

    #
    y_rule_keys = list(y_rule.keys())
    arguments = {"arguments":{F"{PointId}":{"_t":"topic"}}}
    # time is not composed as a device, only can be regarded as a rule
    for rule in y_rule_keys:
        temp_PointId = F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointId']}"
        if "time" not in temp_PointId:
            arguments["arguments"].update({F"{temp_PointId}":{"_t":"cache","key":F"shadow/points/{temp_PointId}/presentvalue"}})
    # x_rule
    judgement_string_x = {PointId:rule_str_create(x_rule)}
    # y_rule
    judgement_string_y = {}
    if len(y_rule_keys)==1:
        if "time" not in y_rule[y_rule_keys[0]]["DeviceId"]:
            judgement_string_y.update({y_rule_keys[0]:rule_str_create(y_rule[y_rule_keys[0]])})
        else:
            time_low_str,time_high_str = rule_str_create_time(y_rule[y_rule_keys[0]],PointId)
            judgement_string_y.update({y_rule_keys[0]:F"{time_low_str} and {time_high_str}"})

    elif len(y_rule_keys)>1:
        for rule in y_rule_keys:
            if "time" not in y_rule[rule]["DeviceId"]:
                judgement_string_y.update({rule:rule_str_create(y_rule[rule])})
            else:
                time_low_str,time_high_str = rule_str_create_time(y_rule[rule],PointId)
                judgement_string_y.update({rule:F"{time_low_str} and {time_high_str}"})
    # calcultor_string
    calculator = {"_t":"default"}
    # add arguments
    calculator.update(arguments)
    # expression combine
    expression_str = F"({judgement_string_x[PointId]})"
    for rule in list(judgement_string_y.keys()):
        expression_str += F" and ({judgement_string_y[rule]})"

    conditions = {"conditions":
            {"activate":
            {"_t":"simple"
            ,"expression":expression_str}
        }
    }
    calculator.update(conditions)
    dict_id = dict_id_create_complex_rules(IdDescription,Event_Name,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator)
    return dict_id
Event_Name = "上班時間出風溫度未隨冰水閥開度增加降低"
Level = "警報"
PointId = "AHU_37_15_PRE-CV_POS"
Description = F"{PointId}-{Event_Name}"
DeviceType = "AHU"
Floor = "15"
DeviceId = "AHU_37_15_PRE"
GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
x_rule = {"DeviceId":"AHU_37_15_PRE","PointId":"CV_POS","UpperBound":70}
y_rule = {"y1":{
    "DeviceId":"AHU_37_15_PRE","PointId":"SA_T","UpperBound":28},
    "y2":{
    "DeviceId":"AHU_37_15_PRE","PointId":"FAN_RUN_CMD","SetValue":"True"},
    "y3":{
    "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8}
    }
# Event_Name = "上班時間設備通訊異常"
# Level = "警報"
# PointId = "FCU_326_8-COM_AL"
# Description = F"{PointId}-{Event_Name}"
# DeviceType = "FCU"
# Floor = "8"
# DeviceId = "FCU_326_8"
# GUID = "95258477-0b2c-45e3-9c67-55dd17370cdd"
# x_rule = {"DeviceId":"FCU_326_8","PointId":"COM_AL","SetValue":"True"}
# y_rule = {"y1":{
#     "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8},
#     }

# Event_Name = "上班時間設備通訊異常"
# Level = "警報"
# PointId = "FCU_333_8-COM_AL"
# Description = F"{PointId}-{Event_Name}"
# DeviceType = "FCU"
# Floor = "8"
# DeviceId = "FCU_333_8"
# GUID = "9599b326-0bd3-449d-9bc6-5293c249a13f"
# x_rule = {"DeviceId":"FCU_333_8","PointId":"COM_AL","SetValue":"True"}
# y_rule = {"y1":{
#     "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8},
#     }

print(main(Event_Name=Event_Name,Level=Level,PointId=PointId,Description=Description,DeviceId=DeviceId,GUID=GUID,x_rule=x_rule,y_rule=y_rule))

#%%


if __name__ == "__main__":
    # input rule's information
#%%
    Event_Name = "上班時間出風溫度未隨冰水閥開度增加降低"
    Level = "警報"
    PointId = "AHU_37_15_PRE-CV_POS"
    Description = F"{PointId}-{Event_Name}"
    DeviceType = "AHU"
    Floor = "15"
    DeviceId = "AHU_37_15_PRE"
    GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
    x_rule = {"DeviceId":"AHU_37_15_PRE","PointId":"CV_POS","UpperBound":70}
    y_rule = {"y1":{
        "DeviceId":"AHU_37_15_PRE","PointId":"SA_T","UpperBound":28},
        "y2":{
        "DeviceId":"AHU_37_15_PRE","PointId":"FAN_RUN_CMD","SetValue":"True"},
        "y3":{
        "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8}
        }
    # AHU_COM_AL 測試
    Event_Name = "上班時間通訊異常"
    Level = "警報"
    PointId = "AHU_37_15_PRE-COM_AL"
    Description = F"{PointId}-{Event_Name}"
    DeviceType = "AHU"
    Floor = "15"
    DeviceId = "AHU_37_15_PRE"
    GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
    x_rule = {"DeviceId":"AHU_37_15_PRE","PointId":"COM_AL","SetValue":"True"}
    y_rule = {"y1":{
        "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8},
        }
    # FCU測試

    # Event_Name = "上班時間設備通訊異常"
    # Level = "警報"
    # PointId = "FCU_326_8-COM_AL"
    # Description = F"{PointId}-{Event_Name}"
    # DeviceType = "FCU"
    # Floor = "8"
    # DeviceId = "FCU_326_8"
    # GUID = "95258477-0b2c-45e3-9c67-55dd17370cdd"
    # x_rule = {"DeviceId":"FCU_326_8","PointId":"COM_AL","SetValue":"True"}
    # y_rule = {"y1":{
    #     "DeviceId":"time","PointId":"time","UpperBound":18,"LowerBound":8},
    #     }


    ### start computing
    y_rule_keys = list(y_rule.keys())

    # create ID decription
    every_pointId = [F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointId']}" for rule in y_rule_keys]
    IdDescription = F"{PointId}"
    for set_id in every_pointId:
        if set_id.split("-")[0]==DeviceId:
            IdDescription += F"-{set_id.split('-')[1]}"
        elif set_id.split("-")[0]=='time':
            IdDescription += F"-WH"
        else:
            IdDescription += F"-{set_id}"
    IdDescription += "-alarm"

    #
    y_rule_keys = list(y_rule.keys())
    arguments = {"arguments":{F"{PointId}":{"_t":"topic"}}}
    # time is not composed as a device, only can be regarded as a rule
    for rule in y_rule_keys:
        temp_PointId = F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointId']}"
        if "time" not in temp_PointId:
            arguments["arguments"].update({F"{temp_PointId}":{"_t":"cache","key":F"shadow/points/{temp_PointId}/presentvalue"}})
    # x_rule
    judgement_string_x = {PointId:rule_str_create(x_rule)}
    # y_rule
    judgement_string_y = {}
    if len(y_rule_keys)==1:
        if "time" not in y_rule[y_rule_keys[0]]["DeviceId"]:
            judgement_string_y.update({y_rule_keys[0]:rule_str_create(y_rule[y_rule_keys[0]])})
        else:
            time_low_str,time_high_str = rule_str_create_time(y_rule[y_rule_keys[0]],PointId)
            judgement_string_y.update({y_rule_keys[0]:F"{time_low_str} and {time_high_str}"})

    elif len(y_rule_keys)>1:
        for rule in y_rule_keys:
            if "time" not in y_rule[rule]["DeviceId"]:
                judgement_string_y.update({rule:rule_str_create(y_rule[rule])})
            else:
                time_low_str,time_high_str = rule_str_create_time(y_rule[rule],PointId)
                judgement_string_y.update({rule:F"{time_low_str} and {time_high_str}"})
    # calcultor_string
    calculator = {"_t":"default"}
    # add arguments
    calculator.update(arguments)
    # expression combine
    expression_str = F"({judgement_string_x[PointId]})"
    for rule in list(judgement_string_y.keys()):
        expression_str += F" and ({judgement_string_y[rule]})"

    conditions = {"conditions":
            {"activate":
            {"_t":"simple"
            ,"expression":expression_str}
        }
    }
    calculator.update(conditions)




    dict_id = [{'_id':F'{IdDescription}',
        'name':F"{Event_Name}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':[]
        }]
    print(json.dumps(dict_id,ensure_ascii=False))




# %%
