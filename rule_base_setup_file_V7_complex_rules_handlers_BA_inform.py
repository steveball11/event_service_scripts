#%%
import pandas as pd
import json
import re
import complex_rules_handlers_packages_day_filter_BA_inform
#%%
# points inside certain facility
class Set_up_rules:

    def __init__(self,DeviceType,PointType,EventName,Level,x_rule,y_rule,Message_Title,Message,SilentTime,message_target):

        self.mapping_doc = r'210310_point-mappings_v18.xlsx'
        self.df_list = pd.read_excel(self.mapping_doc,sheet_name='DeviceList')
        self.DeviceType = DeviceType
        self.PointType = PointType
        self.EventName = EventName
        self.Level = Level
        self.x_rule = x_rule
        self.y_rule = y_rule
        self.Message_Title = Message_Title
        self.Message = Message
        self.SilentTime = SilentTime
        self.message_target = message_target
        self.name_list = self.read_all_PointTypes()
        self.df_setup = self.create_setup_df()
        self.Series_post_str = self.create_post_str_Series()
        self.combine_txt = self.create_text()


    def read_all_PointTypes(self):
        name_list = pd.read_excel(self.mapping_doc,sheet_name='DeviceList')["type"].dropna().unique()
        return name_list

    def create_setup_df(self):
        print(self.message_target)
        mask_assign = self.df_list["name"].str.contains(self.DeviceType)
        pointID_series = (self.df_list.loc[mask_assign,'name_mod'] + '-' +  self.PointType)
        df_setup = pd.DataFrame([self.df_list.loc[mask_assign,'id'], pointID_series, (self.df_list.loc[mask_assign,'name_mod'])]).T
        df_setup = df_setup.reset_index(drop=True)
        df_setup.columns = ['GUID','PointId','DeviceId']
        df_setup["DeviceType"] = self.DeviceType
        df_setup["PointType"] = self.PointType
        df_setup['floor'] = df_setup['DeviceId'].str.split('_').str[-1].values
        df_setup["floor"][df_setup["floor"]=="PRE"] = df_setup['DeviceId'].str.split('_').str[-2].values
        df_setup["EventName"] = self.EventName
        df_setup["Description"] = df_setup['PointId'] + F"-{self.EventName}"
        df_setup["Level"] = self.Level
        df_setup["Message_Title"] = self.Message_Title
        df_setup["Message"] = self.Message
        df_setup["SilentTime"] = self.SilentTime
        df_setup["message_target"] = self.message_target

        # append Device ID to x_rules
        df_setup["x_rule"] = str(self.x_rule)
        for i,deviceid in enumerate(df_setup["DeviceId"]):
            for rule_key in list(eval(df_setup.loc[i,"x_rule"]).keys()):
                temp_dict = eval(df_setup.loc[i,"x_rule"])
                temp_dict[rule_key].update({"DeviceId":df_setup.loc[i,"DeviceId"]})
                df_setup.loc[i,"x_rule"] = str(temp_dict)
        # append Device ID to y_rules
        df_setup["y_rule"] = str(self.y_rule)
        for i,deviceid in enumerate(df_setup["DeviceId"]):
            for rule_key in list(eval(df_setup.loc[i,"y_rule"]).keys()):
                temp_dict = eval(df_setup.loc[i,"y_rule"])
                temp_dict[rule_key].update({"DeviceId":df_setup.loc[i,"DeviceId"]})
                if "time" in temp_dict[rule_key]["PointType"]:
                    temp_dict[rule_key]["DeviceId"] = "time"
                df_setup.loc[i,"y_rule"] = str(temp_dict)
        # Message Device ID replace
        for i,deviceid in enumerate(df_setup["DeviceId"]):
            df_setup.loc[i,"Message"] = df_setup.loc[i,"Message"].replace("DEVICEID",deviceid)
        return df_setup


    def create_post_str_Series(self):
        for i in range(len(self.df_setup)):
            self.df_setup.loc[i,"rule_base_set"] = complex_rules_handlers_packages_day_filter_BA_inform.main(EventName=self.df_setup.loc[i,"EventName"],
            Level=self.df_setup.loc[i,"Level"],
            PointId=self.df_setup.loc[i,"PointId"],
            Description=self.df_setup.loc[i,"Description"],
            DeviceType=self.df_setup.loc[i,"DeviceType"],
            DeviceId=self.df_setup.loc[i,"DeviceId"],
            GUID=self.df_setup.loc[i,"GUID"],
            Floor=self.df_setup.loc[i,"floor"],
            x_rule=eval(self.df_setup.loc[i,"x_rule"]),
            y_rule=eval(self.df_setup.loc[i,"y_rule"]),
            Message_Title=self.df_setup.loc[i,"Message_Title"],
            Message=self.df_setup.loc[i,"Message"],
            SilentTime=self.df_setup.loc[i,"SilentTime"],
            message_target=self.df_setup.loc[i,"message_target"])
        Series_setup_str = self.df_setup.loc[:,"rule_base_set"]
        return Series_setup_str


    def create_text(self):
        combine_txt = "["
        for i,txt in enumerate(self.df_setup["rule_base_set"]):
            if i!= len(self.df_setup["rule_base_set"])-1:
                combine_txt = combine_txt + txt[1:-1] + ","
            else:
                combine_txt = combine_txt + txt[1:-1]
        combine_txt = combine_txt + "]"
        return combine_txt

    def save_text(self,save_txt):
        text_file = open(save_txt, "w",encoding='UTF-8')
        text_file.write(self.combine_txt)
        text_file.close()
        return print("Save post string success")

    def every_id_list(self,id_save_txts):
        id_list = []
        for rule in self.Series_post_str:
            id_list.append(eval(rule)[0]["_id"])
        text_file = open(id_save_txts, "w",encoding='UTF-8')
        text_file.write(json.dumps(id_list))
        text_file.close()
        print("Save post string id success")
        return id_list

# %%
DeviceType = "AHU"
PointType = "CV_POS"
EventName = "上班時間出風溫度未隨冰水閥開度增加降低"
Level = "警報"
x_rule = {"x":{"PointType":"CV_POS","LowerBound":70}}
y_rule = {"y1":{"PointType":"SA_T","LowerBound":28},
    "y2":{"PointType":"FAN_RUN_CMD","SetValue":"True"},
    "y3":{"PointType":"time","UpperBound":18,"LowerBound":8}
    }





# 漏水警報
# DeviceType = "LDS"
# PointType = "COM_AL"
# EventName = "通訊異常警報"
# Level = "嚴重"
# x_rule = {"x":{"PointType":"COM_AL","SetValue":"True"}}
# y_rule = {"y1":{"PointType":"time","UpperBound":24,"LowerBound":-1}
#     }
# Message_Title = "LDS-通訊異常警報"
# SilentTime = "3600"
# Message = "DEVICEID-通訊異常警報"
# message_target = "dev_off"
# save_name = "LDS_COM_AL_informed.txt"
# save_name_ID = F"{save_name[0:-4]}_ID.txt"

# DeviceType = "FCU"
# PointType = "COM_AL"
# EventName = "上班時間設備通訊警報"
# Level = "警報"
# x_rule = {"x":{"PointType":"COM_AL","SetValue":"True"}}
# y_rule = {"y3":{"PointType":"time","UpperBound":18,"LowerBound":8}
#     }


# AHU 警報 送風溫度
DeviceType = "AHU"
PointType = "SA_T"
EventName = "AHU上班時間出風溫度過高"
Level = "警報"
x_rule = {"x":{"PointType":"SA_T","LowerBound":"28"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":20,"LowerBound":8},
          "y2":{"PointType":"weekday","UpperBound":4,"LowerBound":0}}
Message_Title = "機房室內溫度過高"
SilentTime = "0"
Message = "DEVICEID-送風溫度過高"
message_target = "None"
save_name = "AHU_SA_T_time_informed.txt"
save_name_ID = Fr"{save_name[0:-4]}_ID.txt"

# LAB FCU
# DeviceType = "FCU"
# PointType = "RA_T"
# EventName = "實驗室內溫度過高"
# Level = "警報"
# x_rule = {"x":{"PointType":"RA_T","LowerBound":"25"}}
# y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1},
#     }
# Message_Title = "實驗室室內溫度過高"
# SilentTime = "0"
# Message = "DEVICEID-實驗室內溫度過高"
# message_target = "dev_off"
# save_name = "FCU_LAB_RA_T_time_informed.txt"
# save_name_ID = F"{save_name[0:-4]}_ID.txt"

DeviceType = "LDS"
PointType = "LEAK_AL"
EventName = "漏液偵測警報"
Level = "嚴重"
x_rule = {"x":{"PointType":"LEAK_AL","SetValue":"True"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
Message_Title = "LDS-漏液偵測警報"
SilentTime = "0"
Message = "DEVICEID-漏液偵測警報"
message_target = "dev_off"
save_name = "LDS_LEAK_AL_informed_BA_inform.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"
# CDA
DeviceType = "TPS"
PointType = "RM_T"
EventName = "機房室內溫度過高"
Level = "嚴重"
x_rule = {"x":{"PointType":"RM_T","LowerBound":"28"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
Message_Title = "機房室內溫度過高"
SilentTime = "0"
Message = "DEVICEID-機房室內溫度過高"
message_target = "dev_off"
save_name = "TPS_RM_T_informed_BA_inform.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"

# # HHWP
DeviceType = "HHWP"
PointType = "TRIP_AL"
EventName = "熱水泵跳脫警報"
Level = "嚴重"
x_rule = {"x":{"PointType":"TRIP_AL","SetValue":"True"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
Message_Title = "熱水泵跳脫警報"
SilentTime = "0"
Message = "DEVICEID-熱水泵跳脫警報"
message_target = "dev_off"
save_name = "HHWP_TRIP_AL_informed_BA_inform.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"


# PCWP
DeviceType = "PCWP"
PointType = "DPS_AL"
EventName = "泵浦壓差異常警報"
Level = "嚴重"
x_rule = {"x":{"PointType":"DPS_AL","SetValue":"True"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
Message_Title = "泵浦壓差異常警報"
SilentTime = "0"
Message = "DEVICEID-泵浦壓差異常警報"
message_target = "dev_off"
save_name = "PCWP_DPS_AL_informed_BA_inform.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"

# SHWP
DeviceType = "SHWP"
PointType = "DPS_AL"
EventName = "泵浦壓差異常警報"
Level = "嚴重"
x_rule = {"x":{"PointType":"DPS_AL","SetValue":"True"}}
y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1}
    }
Message_Title = "泵浦壓差異常警報"
SilentTime = "300"
Message = "DEVICEID-泵浦壓差異常警報"
message_target = "dev_off"
save_name = "SHWP_DPS_AL_informed_BA_inform.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"

# # LAB FCU
# DeviceType = "FCU"
# PointType = "RA_T"
# EventName = "實驗室內溫度過高"
# Level = "警報"
# x_rule = {"x":{"PointType":"RA_T","LowerBound":"25"}}
# y_rule = {"y1":{"PointType":"hour","UpperBound":24,"LowerBound":-1},
#     }
# Message_Title = "實驗室室內溫度過高"
# SilentTime = "0"
# Message = "DEVICEID-實驗室內溫度過高"
# message_target = "dev_off"
# save_name = "FCU_LAB_RA_T_time_informed.txt"
# save_name_ID = F"{save_name[0:-4]}_ID.txt"


Set_up_rules(DeviceType=DeviceType, PointType=PointType, EventName=EventName, Level=Level, x_rule=x_rule, y_rule=y_rule, Message_Title=Message_Title, Message=Message, SilentTime=SilentTime, message_target=message_target).save_text(save_name)
Set_up_rules(DeviceType=DeviceType, PointType=PointType, EventName=EventName, Level=Level, x_rule=x_rule, y_rule=y_rule, Message_Title=Message_Title, Message=Message, SilentTime=SilentTime, message_target=message_target).every_id_list(save_name_ID)


# %%