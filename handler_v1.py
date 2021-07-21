#%%
import pandas as pd
import json
# %%
def handler_creater_dev(IdDescription,Message_Title,Message,SilentTime):
    dict_handler = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-dev-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str = '{"type":"notification",\
"act":"push",\
"id":"IdDescription",\
"method":["email","fcm","line"],\
"title":"Message_Title",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME}'
    dict_content_str = dict_content_str.replace("IdDescription",IdDescription)
    dict_content_str = dict_content_str.replace("Message_Title",Message_Title)
    dict_content_str = dict_content_str.replace("MESSAGE",Message)
    dict_content_str = dict_content_str.replace("SLIENTTIME",SilentTime)
    dict_handler.update({"content":dict_content_str})

    return [dict_handler]

def handler_creater_off(IdDescription,Message_Title,Message,SilentTime):
    dict_handler = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str = '{"type":"notification",\
"act":"push",\
"id":"IdDescription",\
"method":["email","fcm","line"],\
"title":"Message_Title",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME}'
    dict_content_str = dict_content_str.replace("IdDescription",IdDescription)
    dict_content_str = dict_content_str.replace("Message_Title",Message_Title)
    dict_content_str = dict_content_str.replace("MESSAGE",Message)
    dict_content_str = dict_content_str.replace("SLIENTTIME",SilentTime)
    dict_handler.update({"content":dict_content_str})

    return [dict_handler]

def handler_creater_dev_and_off(IdDescription,Message_Title,Message,SilentTime):
    # def
    dict_handler_dev = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-dev-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str_dev = '{"type":"notification",\
"act":"push",\
"id":"IdDescription",\
"method":["email","fcm","line"],\
"title":"Message_Title",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME}'
    dict_content_str_dev = dict_content_str_dev.replace("IdDescription",IdDescription)
    dict_content_str_dev = dict_content_str_dev.replace("Message_Title",Message_Title)
    dict_content_str_dev = dict_content_str_dev.replace("MESSAGE",Message)
    dict_content_str_dev = dict_content_str_dev.replace("SLIENTTIME",SilentTime)
    dict_handler_dev.update({"content":dict_content_str_dev})

    # off
    dict_handler_off = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str_off = '{"type":"notification",\
"act":"push",\
"id":"IdDescription",\
"method":["email","fcm","line"],\
"title":"Message_Title",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","technician","developer"]},\
"silent_time": SLIENTTIME}'
    dict_content_str_off = dict_content_str_off.replace("IdDescription",IdDescription)
    dict_content_str_off = dict_content_str_off.replace("Message_Title",Message_Title)
    dict_content_str_off = dict_content_str_off.replace("MESSAGE",Message)
    dict_content_str_off = dict_content_str_off.replace("SLIENTTIME",SilentTime)
    dict_handler_off.update({"content":dict_content_str_off})

    dict_handler = [dict_handler_dev,dict_handler_off]

    return dict_handler
if __name__ == '__main__':
    SilentTime = "5"
    Title = "FCU_COM_AL_warning"
    Message_Title = "FCU_通訊異常"
    Message = "上班時間FCU通訊異常"
    IdDescription = "FCU_601_14-COM_AL_time"
    print(type(handler_creater_dev_and_off(IdDescription,Message_Title,Message,SilentTime)))
# %%
