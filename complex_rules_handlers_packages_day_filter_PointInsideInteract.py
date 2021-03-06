#%%
import pandas as pd
import json
import re
import handler_v1

#%%
# transfer import variables to dict form
def define_rules(**info):
    return info
# create single rule set
#%%
# create single rule in each token
def single_rule_create(single_rule,token):

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

def rule_dict_create(ori_rule,x_rule,Interact):
    dict_judgement_string = {}
    if_interact = 0
    for rule in list(ori_rule.keys()):
        # create rules
        if ("hour" not in ori_rule[rule]["PointType"]) and ("weekday" not in ori_rule[rule]["PointType"]):
            dict_judgement_string.update({rule:single_rule_create(ori_rule[rule],rule)})
        # create hour rules
        elif "hour" in ori_rule[rule]["PointType"]:
            time_low_str,time_high_str = single_rule_create_time(ori_rule[rule],list(x_rule.keys())[0])
            dict_judgement_string.update({rule:F"{time_low_str} and {time_high_str}"})
        # create weekday rules
        elif "weekday" in ori_rule[rule]["PointType"]:
            time_low_str,time_high_str = single_rule_create_weekday(ori_rule[rule],list(x_rule.keys())[0])
            dict_judgement_string.update({rule:F"{time_low_str} and {time_high_str}"})

        # create interactive rules
        if "Interact" in list(ori_rule[rule].keys()):
            if_interact +=1
    if if_interact>0:
        for interact in list(Interact.keys()):
            dict_judgement_string.update({interact:Interact[interact]})

    return dict_judgement_string



def dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator,Message_Title,Message,SilentTime,message_target):
    if message_target == "dev":
        dict_handler = handler_v1.handler_creater_dev(IdDescription=IdDescription,Message_Title=Message_Title,Message=Message,SilentTime=SilentTime)
    elif message_target == "off":
        dict_handler = handler_v1.handler_creater_off(IdDescription=IdDescription,Message_Title=Message_Title,Message=Message,SilentTime=SilentTime)
    elif message_target == "dev_off":
        dict_handler = handler_v1.handler_creater_dev_and_off(IdDescription=IdDescription,Message_Title=Message_Title,Message=Message,SilentTime=SilentTime)

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

def main(EventName,Level,PointId,Description,DeviceType,DeviceId,Floor,GUID,x_rule,y_rule,Message_Title,Message,SilentTime,message_target,Interact):

    y_rule_keys = list(y_rule.keys())
    #
    y_rule_keys = list(y_rule.keys())
    arguments = {"arguments":{list(x_rule.keys())[0]:{"_t":"topic"}}}
    # time is not composed as a device, only can be regarded as a rule
    for rule in y_rule_keys:
        temp_PointId = F"{y_rule[rule]['DeviceId']}-{y_rule[rule]['PointType']}"
        if ("hour" not in temp_PointId) and ("weekday" not in temp_PointId):
            arguments["arguments"].update({F"{rule}":{"_t":"cache","key":F"shadow/points/{temp_PointId}/presentvalue"}})
    # x_rule
    judgement_string_x = rule_dict_create(ori_rule=x_rule,x_rule=x_rule,Interact=Interact)
    # y_rule
    judgement_string_y = rule_dict_create(ori_rule=y_rule,x_rule=x_rule,Interact=Interact)

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
    IdDescription += "-interact-informed-alarm"

    calculator.update(conditions)
    dict_id = dict_id_create_complex_rules(IdDescription,EventName,Level,PointId,Description,DeviceType,Floor,DeviceId,GUID,calculator,Message_Title,Message,SilentTime,message_target)
    return dict_id

if __name__ == '__main__':
    #
    EventName = "?????????????????????????????????????????????????????????"
    Level = "??????"
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
    EventName = "?????????????????????????????????????????????????????????"
    Level = "??????"
    PointId = "AHU_37_15_PRE-CV_POS"
    Description = F"{PointId}-{EventName}"
    DeviceType = "FCU"
    Floor = "15"
    DeviceId = "AHU_37_15_PRE"
    GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
    SilentTime = "5"
    Title = "AC system warning"
    Message_Title = "AHU_?????????????????????"
    Message = "?????????????????????????????????????????????????????????"
    x_rule = {"x":{"DeviceId":"AHU","PointType":"CV_POS","LowerBound":70}}
    y_rule = {"y1":{
        "DeviceId":"AHU_37_15_PRE","PointType":"SA_T","LowerBound":28},
        "y2":{
        "DeviceId":"AHU_37_15_PRE","PointType":"FAN_RUN_CMD","SetValue":"True"},
        "y3":{
        "DeviceId":"hour","PointType":"hour","UpperBound":18,"LowerBound":8}
        }
    # ????????????
    EventName = "??????????????????????????????"
    Level = "??????"
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
    Message_Title = "FCU_????????????"
    Message = F"????????????{DeviceId}????????????"
    message_target = "dev_off"

    # FCU ??????????????????????????????????????????
    EventName = "FCU????????????????????????????????????"
    Level = "??????"
    PointId = "FCU_601_14-COM_AL"
    Description = F"{PointId}-{EventName}"
    DeviceType = "FCU"
    Floor = "14"
    DeviceId = "FCU_601_14"
    GUID = "461f19ae-68fe-4cd0-8c35-0f1bd223c2f0"
    x_rule = {"x":{"DeviceId":"FCU_601_14","PointType":"COM_AL","SetValue":"False"}}
    y_rule = {"y1":{
        "DeviceId":"hour","PointType":"hour","UpperBound":20,"LowerBound":8},
        "y2":{
        "DeviceId":"weekday","PointType":"weekday","UpperBound":4,"LowerBound":-1},
        "y3":{
        "DeviceId":"FCU_601_14","PointType":"ST1","SetValue":"True"},
        "y4":{
        "DeviceId":"FCU_601_14","PointType":"RA_T","Interact":"True"},
        "y5":{
        "DeviceId":"FCU_601_14","PointType":"RA_T_SP","Interact":"True"}
        }
    Interact = {"Interact":"(y4.value - y5.value > 2)"}
    SilentTime = "3600"
    Title = "FCU_COM_AL_warning"
    Message_Title = "FCU_????????????"
    Message = F"????????????{DeviceId}????????????"
    message_target = "dev_off"

    print(main(EventName=EventName,
    Level=Level,
    PointId=PointId,
    Description=Description,
    DeviceType=DeviceType,
    Floor=Floor,
    DeviceId=DeviceId,
    GUID=GUID,
    x_rule=x_rule,
    y_rule=y_rule,
    Message_Title=Message_Title,
    Message=Message,
    SilentTime=SilentTime,
    message_target=message_target,
    Interact=Interact))
#
# %%
