#%%
import pandas as pd
import json
import re
import complex_rules_package_hour
#%%
# points inside certain facility
class Set_up_rules:

    def __init__(self,DeviceType,PointType,EventName,Level,x_rule,y_rule):
        self.mapping_doc = r'210310_point-mappings_v18.xlsx'
        self.df_list = pd.read_excel(self.mapping_doc,sheet_name='DeviceList')
        self.DeviceType = DeviceType
        self.PointType = PointType
        self.EventName = EventName
        self.Level = Level
        self.x_rule = x_rule
        self.y_rule = y_rule
        self.name_list = self.read_all_PointTypes()
        self.df_setup = self.create_setup_df()
        self.Series_post_str = self.create_post_str_Series()
        self.combine_txt = self.create_text()

    def read_all_PointTypes(self):
        name_list = pd.read_excel(self.mapping_doc,sheet_name='DeviceList')["type"].dropna().unique()
        return name_list

    def create_setup_df(self):
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

        return df_setup


    def create_post_str_Series(self):
        for i in range(len(self.df_setup)):
            self.df_setup.loc[i,"rule_base_set"] = complex_rules_package_hour.main(EventName=self.df_setup.loc[i,"EventName"],
            Level=self.df_setup.loc[i,"Level"],
            PointId=self.df_setup.loc[i,"PointId"],
            Description=self.df_setup.loc[i,"Description"],
            DeviceType=self.df_setup.loc[i,"DeviceType"],
            DeviceId=self.df_setup.loc[i,"DeviceId"],
            GUID=self.df_setup.loc[i,"GUID"],
            Floor=self.df_setup.loc[i,"floor"],
            x_rule=eval(self.df_setup.loc[i,"x_rule"]),
            y_rule=eval(self.df_setup.loc[i,"y_rule"]))
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
        li = []
        for rule in self.Series_post_str:
            li.append(eval(rule)[0]["_id"])
        text_file = open(id_save_txts, "w",encoding='UTF-8')
        text_file.write(json.dumps(li))
        text_file.close()
        print("Save post string id success")
        return li

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

DeviceType = "AHU"
PointType = "ST1"
EventName = "上班時間AHU未運轉"
Level = "警報"
x_rule = {"x":{"PointType":"ST1","SetValue":"False"}}
y_rule = {"y3":{"PointType":"time","UpperBound":21,"LowerBound":7.5}
    }
# 上班時間出風溫度過高
DeviceType = "AHU"
PointType = "SA_T"
EventName = "AHU開機時出風溫度過高"
Level = "警報"
x_rule = {"x":{"PointType":"SA_T","LowerBound":28}}
y_rule = {"y1":{"PointType":"FAN_RUN_CMD","SetValue":"True"}
    }
save_name = "AHU-SA_T-FAN_RUN_CMD_informed.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"


# 上班時間FCU回風溫度過高
DeviceType = "FCU"
PointType = "RA_T"
EventName = "上班時間回風溫度過高"
Level = "警報"
x_rule = {"x":{"PointType":"RA_T","LowerBound":28}}
y_rule = {"y1":{"PointType":"hour","UpperBound":21,"LowerBound":9}
    }
save_name = "FCU-RA_T-time.txt"
save_name_ID = F"{save_name[0:-4]}_ID.txt"

# DeviceType = "FCU"
# PointType = "COM_AL"
# EventName = "上班時間設備通訊警報"
# Level = "警報"
# x_rule = {"x":{"PointType":"COM_AL","SetValue":"True"}}
# y_rule = {"y3":{"PointType":"time","UpperBound":18,"LowerBound":8}
#     }

# PointId = "AHU_37_15_PRE-CV_POS"
# Description = F"{PointId}-{EventName}"
# Floor = "15"
# DeviceId = "AHU_37_15_PRE"
# GUID = "a5a49315-3bb4-444c-83f8-3a4ed2da0189"
# x_rule = {"x":{"DeviceId":"AHU_37_15_PRE","PointType":"CV_POS","LowerBound":70}}
# y_rule = {"y1":{
#     "DeviceId":"AHU_37_15_PRE","PointType":"SA_T","UpperBound":28},
#     "y2":{
#     "DeviceId":"AHU_37_15_PRE","PointType":"FAN_RUN_CMD","SetValue":"True"},
#     "y3":{
#     "DeviceId":"time","PointType":"time","UpperBound":18,"LowerBound":8}
#     }
# Set_up_rules(DeviceType=DeviceType,PointType=PointType,EventName=EventName,Level=Level,x_rule=x_rule,y_rule=y_rule).create_text()


Set_up_rules(DeviceType=DeviceType,PointType=PointType,EventName=EventName,Level=Level,x_rule=x_rule,y_rule=y_rule).save_text(save_name)
Set_up_rules(DeviceType=DeviceType,PointType=PointType,EventName=EventName,Level=Level,x_rule=x_rule,y_rule=y_rule).every_id_list(save_name_ID)


# %%
