#%%
import pandas as pd
import json
# %%
# to dev
def handler_creater_dev(IdDescription,Message_Title,Point_ID,Device_ID,Message,SilentTime):
    dict_handler = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-dev-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str = '{"type":"notification",\
"act":"push",\
"id":"IDDESCRIPTION",\
"method":[{"email":null},{"fcm":null},{"line":null},\
    {"request":{\
        "description":"由 BA 自動產生之請求",\
        "reporter":{"name":"事件規則機器人","email":"","unit":"事件中心","phone":""},\
        "io_point":{"id":"POINT_ID"},\
        "device":{"name":"DEVICE_ID"}\
    }}],\
"title":"MESSAGE_TITLE",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME,\
"tenant": "google"}'
    dict_content_str = dict_content_str.replace("IdDescription",IdDescription)
    dict_content_str = dict_content_str.replace("Message_Title",Message_Title)
    dict_content_str = dict_content_str.replace("POINT_ID",Point_ID)
    dict_content_str = dict_content_str.replace("DEVICE_ID",Device_ID)
    dict_content_str = dict_content_str.replace("MESSAGE",Message)
    dict_content_str = dict_content_str.replace("SLIENTTIME",SilentTime)
    dict_handler.update({"content":dict_content_str})

    return [dict_handler]

# to formal
def handler_creater_off(IdDescription,Message_Title,Point_ID,Device_ID,Message,SilentTime):
    dict_handler = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str = '{"type":"notification",\
"act":"push",\
"id":"IDDESCRIPTION",\
"method":[{"email":null},{"fcm":null},{"line":null},\
    {"request":{\
        "description":"由 BA 自動產生之請求",\
        "reporter":{"name":"事件規則機器人","email":"","unit":"事件中心","phone":""},\
        "io_point":{"id":"POINT_ID"},\
        "device":{"name":"DEVICE_ID"}\
    }}],\
"title":"MESSAGE_TITLE",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME,\
"tenant": "google"}'
    dict_content_str = dict_content_str.replace("IdDescription",IdDescription)
    dict_content_str = dict_content_str.replace("Message_Title",Message_Title)
    dict_content_str = dict_content_str.replace("POINT_ID",Point_ID)
    dict_content_str = dict_content_str.replace("DEVICE_ID",Device_ID)
    dict_content_str = dict_content_str.replace("MESSAGE",Message)
    dict_content_str = dict_content_str.replace("SLIENTTIME",SilentTime)
    dict_handler.update({"content":dict_content_str})

    return [dict_handler]

# to formal and dev
def handler_creater_dev_and_off(IdDescription,Message_Title,Point_ID,Device_ID,Message,SilentTime):
    # def
    dict_handler_dev = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-dev-api.aubix.com",
            "mediaType": "application/json",
    }
    dict_content_str_dev = '{"type":"notification",\
"act":"push",\
"id":"IDDESCRIPTION",\
"method":[{"email":null},{"fcm":null},{"line":null},\
{"request":{\
"description":"由 BA 自動產生之請求",\
"reporter":{"name":"事件規則機器人","email":"","unit":"事件中心","phone":""},\
"io_point":{"id":"POINT_ID"},\
"device":{"name":"DEVICE_ID"}\
}}],\
"title":"MESSAGE_TITLE",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME,\
"tenant": "google"}'
    dict_content_str_dev = dict_content_str_dev.replace("IDDESCRIPTION",IdDescription)
    dict_content_str_dev = dict_content_str_dev.replace("MESSAGE_TITLE",Message_Title)
    dict_content_str_dev = dict_content_str_dev.replace("POINT_ID",Point_ID)
    dict_content_str_dev = dict_content_str_dev.replace("DEVICE_ID",Device_ID)
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
"id":"IDDESCRIPTION",\
"method":[{"email":null},{"fcm":null},{"line":null},\
{"request":{\
"description":"由 BA 自動產生之請求",\
"reporter":{"name":"事件規則機器人","email":"","unit":"事件中心","phone":""},\
"io_point":{"id":"POINT_ID"},\
"device":{"name":"DEVICE_ID"}\
}}],\
"title":"MESSAGE_TITLE",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","Technician","Developer"]},\
"silent_time": SLIENTTIME,\
"tenant": "google"}'
    dict_content_str_off = dict_content_str_off.replace("IDDESCRIPTION",IdDescription)
    dict_content_str_off = dict_content_str_off.replace("MESSAGE_TITLE",Message_Title)
    dict_content_str_off = dict_content_str_off.replace("POINT_ID",Point_ID)
    dict_content_str_off = dict_content_str_off.replace("DEVICE_ID",Device_ID)
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
    Point_ID = "FCU_601_14-COM_AL"
    Device_ID = "FCU_601_14"
    ans = (handler_creater_dev_and_off(IdDescription=IdDescription,
    Message_Title=Message_Title,
    Message=Message,
    SilentTime=SilentTime,
    Point_ID=Point_ID,
    Device_ID=Device_ID))
    print(ans)
# %%
