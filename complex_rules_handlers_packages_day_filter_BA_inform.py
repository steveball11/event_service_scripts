#%%
import pandas as pd
import json
import re
import handler_v4_alertID

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


# create single time rule set


def single_rule_create_time(single_rule,token):
    judgement_string_low = F"Timestamp({token}.time).hour>={single_rule['LowerBound']}"
    judgement_string_high = F"Timestamp({token}.time).hour<={single_rule['UpperBound']}"
    return judgement_string_low,judgement_string_high

def single_rule_create_weekday(single_rule,token):
    judgement_string_low = F"Timestamp({token}.time).day_of_week>={single_rule['LowerBound']}"
    judgement_string_high = F"Timestamp({token}.time).day_of_week<={single_rule['UpperBound']}"
    return judgement_string_low,judgement_string_high

def rule_dict_create(ori_rule,x_rule):
    dict_judgement_string = {}
    for rule in list(ori_rule.keys()):
        if ("hour" not in ori_rule[rule]["PointType"]) and ("weekday" not in ori_rule[rule]["PointType"]):
            dict_judgement_string.update({rule:single_rule_create(ori_rule[rule],rule)})
        elif "hour" in ori_rule[rule]["PointType"]:
            time_low_str,time_high_str = single_rule_create_time(ori_rule[rule],list(x_rule.keys())[0])
            dict_judgement_string.update({rule:F"{time_low_str} and {time_high_str}"})
        elif "weekday" in ori_rule[rule]["PointType"]:
            time_low_str,time_high_str = single_rule_create_weekday(ori_rule[rule],list(x_rule.keys())[0])
            dict_judgement_string.update({rule:F"{time_low_str} and {time_high_str}"})


    return dict_judgement_string



def dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator,Message_Title,Message,SilentTime,message_target):
    if message_target == "dev":
        dict_handler = handler_v4_alertID.handler_creater_dev(IdDescription=IdDescription,Description=Description,Message_Title=Message_Title,Message=Message,Point_ID=PointId,Device_ID=DeviceId,SilentTime=SilentTime)
    elif message_target == "off":
        dict_handler = handler_v4_alertID.handler_creater_off(IdDescription=IdDescription,Description=Description,Message_Title=Message_Title,Message=Message,Point_ID=PointId,Device_ID=DeviceId,SilentTime=SilentTime)
    elif message_target == "dev_off":
        dict_handler = handler_v4_alertID.handler_creater_dev_and_off(IdDescription=IdDescription,Description=Description,Message_Title=Message_Title,Message=Message,Point_ID=PointId,Device_ID=DeviceId,SilentTime=SilentTime)
    else:
        dict_handler = []
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
        'handlers':dict_handler
        }]
    except:
        dict_id = [{'_id':F'{IdDescription}',
        'name':F"{EventName}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':calculator,
        'handlers':dict_handler
        }]
    return json.dumps(dict_id,ensure_ascii=False)

def main(EventName,Level,PointId,Description,DeviceType,DeviceId,Floor,GUID,x_rule,y_rule,Message_Title,Message,SilentTime,message_target):

    y_rule_keys = list(y_rule.keys())
    # create ID decription
    every_pointId = [F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointType']}" for rule in y_rule_keys]
    IdDescription = F"{PointId}"
    for set_id in every_pointId:
        if set_id.split("-")[0]==DeviceId:
            IdDescription += F"-{set_id.split('-')[1]}"
        elif set_id.split("-")[0]=='hour':
            IdDescription += F"-hour"
        elif set_id.split("-")[0]=='weekday':
            IdDescription += F"-weekday"
        else:
            IdDescription += F"-{set_id}"
    IdDescription += "-informed-alarm"
    #
    y_rule_keys = list(y_rule.keys())
    arguments = {"arguments":{list(x_rule.keys())[0]:{"_t":"topic"}}}
    # time is not composed as a device, only can be regarded as a rule
    for rule in y_rule_keys:
        temp_PointId = F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointType']}"
        if ("hour" not in temp_PointId) and ("weekday" not in temp_PointId):
            arguments["arguments"].update({F"{rule}":{"_t":"cache","key":F"shadow/points/{temp_PointId}/presentvalue"}})
    # x_rule
    judgement_string_x = rule_dict_create(ori_rule=x_rule,x_rule=x_rule)
    # y_rule
    judgement_string_y = rule_dict_create(ori_rule=y_rule,x_rule=x_rule)

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
    print(Description)
    dict_id = dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator,Message_Title,Message,SilentTime,message_target)
    return dict_id

if __name__ == '__main__':
    #
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
        "DeviceId":"hour","PointType":"hour","UpperBound":20,"LowerBound":8}
        }
    EventName = "上班時間出風溫度未隨冰水閥開度增加降低"
    Level = "警報"
    PointId = "AHU_37_15_PRE-CV_POS"
    Description = F"{PointId}-{EventName}"
    DeviceType = "FCU"
    Floor = "15"
    DeviceId = "AHU_37_15_PRE"
    GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
    SilentTime = "5"
    Title = "AC system warning"
    Message_Title = "AHU_冰水閥開度異常"
    Message = "上班時間出風溫度未隨冰水閥開度增加降低"
    x_rule = {"x":{"DeviceId":"AHU","PointType":"CV_POS","LowerBound":70}}
    y_rule = {"y1":{
        "DeviceId":"AHU_37_15_PRE","PointType":"SA_T","LowerBound":28},
        "y2":{
        "DeviceId":"AHU_37_15_PRE","PointType":"FAN_RUN_CMD","SetValue":"True"},
        "y3":{
        "DeviceId":"hour","PointType":"hour","UpperBound":18,"LowerBound":8}
        }
    # 通知測試
    EventName = "上班時間設備通訊異常"
    Level = "警報"
    PointId = "FCU_601_14-COM_AL"
    Description = F"{PointId}-{EventName}"
    DeviceType = "FCU"
    Floor = "8"
    DeviceId = "FCU_601_14"
    GUID = "461f19ae-68fe-4cd0-8c35-0f1bd223c2f0"
    x_rule = {"x":{"DeviceId":"FCU_601_14","PointType":"COM_AL","SetValue":"True"}}
    y_rule = {"y1":{
        "DeviceId":"hour","PointType":"hour","UpperBound":20,"LowerBound":8},
        "y2":{
        "DeviceId":"weekday","PointType":"weekday","UpperBound":4,"LowerBound":-1}
        }
    SilentTime = "5"
    Title = "FCU_COM_AL_warning"
    Message_Title = "FCU_通訊異常"
    Message = F"上班時間{DeviceId}通訊異常"
    message_target = "dev_off"
# 漏水通知
    EventName = "LDS-漏液偵測警報"
    Level = "嚴重"
    PointId = "LDS_28_9-COM_AL"
    Description = F"{PointId}-{EventName}"
    DeviceType = "LDS"
    Floor = "9"
    DeviceId = "LDS_28_9"
    GUID = "461f19ae-68fe-4cd0-8c35-0f1bd223c2f0"
    x_rule = {"x":{"DeviceId":"LDS_28_9","PointType":"LEAK_AL","SetValue":"True"}}
    y_rule = {"y1":{
        "DeviceId":"hour","PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
    SilentTime = "0"
    Title = "LDS_LEAK_AL_warning"
    Message_Title = "LDS_漏液偵測警報"
    Message = F"{DeviceId}漏液偵測通知"
    message_target = "dev_off"


    main(EventName=EventName,Level=Level,PointId=PointId,Description=Description,DeviceType=DeviceType,Floor=Floor,DeviceId=DeviceId,GUID=GUID,x_rule=x_rule,y_rule=y_rule,Message_Title=Message_Title,Message=Message,SilentTime=SilentTime,message_target=message_target)
# %%

# %%
