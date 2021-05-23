#%%
import pandas
import json
#%%
EventName = "上班時間出風溫度未隨冰水閥開度增加降低"
Level = "警報"
PointId = "AHU_37_15_PRE-CV_POS"
Description = F"{PointId}-{EventName}"
DeviceType = "FCU"
Floor = "15"
DeviceId = "AHU_37_15_PRE"
GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
SilentTime = "5"
Message_Title = "AC system warning"
Message = "上班時間出風溫度未隨冰水閥開度增加降低"
x_rule = {"x":{"DeviceId":"AHU","PointType":"CV_POS","UpperBound":70}}
y_rule = {"y1":{
    "DeviceId":"AHU_37_15_PRE","PointType":"SA_T","UpperBound":28},
    "y2":{
    "DeviceId":"AHU_37_15_PRE","PointType":"FAN_RUN_CMD","SetValue":"True"},
    "y3":{
    "DeviceId":"time","PointType":"time","UpperBound":18,"LowerBound":8}
    }


# {
#             "_t": "api",
#             "method": "POST",
#             "uri": "https://bms-dev-api.aubix.com",
#             "mediaType": "application/json",
#             "content": "{
#                 \"type\":\"notification\",
#                 \"act\":\"push\",
#                 \"id\":\"atashinchi\",
#                 \"method\":[\"email\",\"fcm\",\"line\"],
#                 \"title\":\"我們這一家\",
#                 \"message\":[
#                     \"哈囉你好嗎\",
#                     \"衷心感謝\",
#                     \"珍重再見\",
#                     \"期待再相逢♪\"],
#                 \"target\":{\"role_name\":[\"FC\",\"technician\"]},
#                 \"silent_time\":10}"
# }

#%%
dict_handler = {"_t": "api",
            "method": "POST",
            "uri": "https://bms-dev-api.aubix.com",
            "mediaType": "application/json",
}

# 待填補字串 POINTID TITLE_ID MESSAGE
dict_content_str = '{"type":"notification",\
"act":"push",\
"id":"POINTID",\
"method":["email","fcm","line"],\
"title":"TITLE",\
"message":["MESSAGE"],\
"target":{"role_name":["FC","technician"]}\
"silent_time" : "SLIENTTIME"}'
text_file = open("json_dump_test.txt", "w")
dict_content_str = dict_content_str.replace("POINTID",PointId)
dict_content_str = dict_content_str.replace("TITLE",Title)
dict_content_str = dict_content_str.replace("MESSAGE",Message)
dict_content_str = dict_content_str.replace("SLIENTTIME",SilentTime)
dict_handler.update({"content":dict_content_str})
dict_content_str = json.dumps(dict_content_str,ensure_ascii=False)
print(dict_content_str + "\n")
print(dict_content_str + "\n")
print(json.dumps(dict_handler,ensure_ascii=False))


# text_file.write(dict_content_str)
# text_file.close()


# %%
