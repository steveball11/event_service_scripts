#%%
import pandas as pd
import json
import re

def dict_id_create(IdDescription,Event_Name,Level,PointId,Description,DeviceType,Floor,DeviceID,GUID,Expression):
    try:
        if_B1_R1 = (re.search("[A-Za-z]",Floor).span()[1])
        reverse_Floor = Floor[::-1]
        dict_id = [{'_id':F'{PointId}_{IdDescription}',
        'name':F"{Event_Name}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"floor":F"TPKD-{reverse_Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':{"_t":"default","arguments":{"x":{"_t":"topic"}},"conditions":{"activate":{"_t":"simple","expression":F"{Expression}"}}},
        'handlers':[]
        }]
    except:
        dict_id = [{'_id':F'{PointId}_{IdDescription}',
        'name':F"{Event_Name}",
        'level':F"{Level}",
        'description':F"{Description}",
        'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{Floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
        'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
        'calculator':{"_t":"default","arguments":{"x":{"_t":"topic"}},"conditions":{"activate":{"_t":"simple","expression":F"{Expression}"}}},
        'handlers':[]
        }]
    return dict_id



class Set_up_rules:

    def __init__(self,DeviceType,PointType,IdDescription,Expression,Description,EventName,Level):
        self.mapping_doc = r'C:\Users\Steve\Desktop\KASE\TPKD\TPKD_事件中心\API_demo\210602_point-mappings_new_v3-1.xlsx'
        self.df_list = pd.read_excel(self.mapping_doc,sheet_name='DeviceList')
        self.DeviceType = DeviceType
        self.PointType = PointType
        self.IdDescription = IdDescription
        self.Expression = Expression
        self.Description = Description
        self.EventName = EventName
        self.Level = Level
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
        print(df_setup['DeviceId'])
        df_setup['floor'] = df_setup['DeviceId'].str.split('_').str[-1].values
        df_setup["floor"][df_setup["floor"]=="PRE"] = df_setup['DeviceId'].str.split('_').str[-2].values

        df_setup["id_description"] = self.IdDescription
        df_setup["expression"] = self.Expression
        df_setup["description"] = df_setup['PointId'] + F"_{self.Description}"
        df_setup["Event_Name"] = self.EventName
        df_setup["level"] = self.Level
        return df_setup



    def create_post_str_Series(self):
        for i in range(len(self.df_setup)):
            self.df_setup.loc[i,"rule_base_set"] = json.dumps(dict_id_create(self.df_setup.loc[i,"id_description"],self.df_setup.loc[i,"Event_Name"],self.df_setup.loc[i,"level"],self.df_setup.loc[i,"PointId"],self.df_setup.loc[i,"description"],self.df_setup.loc[i,"DeviceType"],self.df_setup.loc[i,"floor"],self.df_setup.loc[i,"DeviceId"],self.df_setup.loc[i,"GUID"],self.df_setup.loc[i,"expression"]),ensure_ascii=False)
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
        return print("Success")

    def every_id_list(self,id_save_txts):
        id_list = []
        for rule in self.Series_post_str:
            id_list.append(eval(rule)[0]["_id"])
        text_file = open(id_save_txts, "w",encoding='UTF-8')
        text_file.write(json.dumps(id_list))
        text_file.close()
        print("Save post string id success")
        return id_list
#%%
if __name__ == "__main__":

    # print(Set_up_rules(DeviceType="FCU",
    #                     PointType="RA_T_SP",
    #                     IdDescription="_alarm",
    #                     Expression="x.value != None and (x.value <15 or x.value >28)",
    #                     Description="回風溫度設定異常",
    #                     EventName="回風溫度設定異常",
    #                     Level="警報").read_PointType())

    # a = (Set_up_rules(DeviceType="CDS",
    #                     PointType="CO2",
    #                     IdDescription="alarm",
    #                     Expression="x.value != None and x.value >500 ",
    #                     Description="二氧化碳濃度過高",
    #                     EventName="二氧化碳濃度過高",
    #                     Level="警報").save_text("CO2測試.txt"))

    DeviceType = "LDS"
    PointType="SHORT_AL"
    IdDescription="short_circuit_alarm"
    Expression="x.value != None and x.value ==True "
    Description="短路警報"
    EventName="短路警報"
    Level="嚴重"

    DeviceType = "CDS"
    PointType="CO2"
    IdDescription="alarm"
    Expression="x.value != None and x.value >1000 "
    Description="二氧化碳濃度過高"
    EventName="二氧化碳濃度過高"
    Level="警報"

    DeviceType = "HHWP"
    PointType="TRIP_AL"
    IdDescription="alarm"
    Expression="x.value != None and x.value == True "
    Description="熱泵跳脫警報"
    EventName="熱泵跳脫警報"
    Level="警報"

    # DeviceType = "SHWP"
    # PointType="DPS_AL"
    # IdDescription="alarm"
    # Expression="x.value != None and x.value == True "
    # Description="泵浦壓差警報"
    # EventName="泵浦壓差警報"
    # Level="警報"

    DeviceType = "PCWP"
    PointType="DPS_AL"
    IdDescription="alarm"
    Expression="x.value != None and x.value == True "
    Description="泵浦壓差警報"
    EventName="泵浦壓差警報"
    Level="警報"

    # DeviceType = "CH"
    # PointType="CH_WFS_AL"
    # IdDescription="alarm"
    # Expression="x.value != None and x.value == True "
    # Description="冰水流量低量警報"
    # EventName="冰水流量低量警報"
    # Level="警報"

    DeviceType = "CH"
    PointType="CW_WFS_AL"
    IdDescription="alarm"
    Expression="x.value != None and x.value == True "
    Description="冷卻水流量低量警報"
    EventName="冷卻水流量低量警報"
    Level="警報"

    # DeviceType = "SHWP"
    # PointType="TRIP_AL"
    # IdDescription="alarm"
    # Expression="x.value != None and x.value == True "
    # Description="二次泵跳脫警報"
    # EventName="二次泵跳脫警報"
    # Level="警報"


    DeviceType = "SHWP"
    PointType="DPS_AL"
    IdDescription="alarm"
    Expression="x.value != None and x.value == True "
    Description="泵浦壓差異常警報"
    EventName="泵浦壓差異常警報"
    Level="警報"

    # DeviceType = "CH"
    # PointType="TRIP_AL"
    # IdDescription="alarm"
    # Expression="x.value != None and x.value == True "
    # Description="冰機跳脫警報"
    # EventName="冰機跳脫警報"
    # Level="警報"



    a = (Set_up_rules(DeviceType=DeviceType,
                        PointType=PointType,
                        IdDescription=IdDescription,
                        Expression=Expression,
                        Description=Description,
                        EventName=EventName,
                        Level=Level).save_text("SHWP_DPS_AL.txt"))
    a = (Set_up_rules(DeviceType=DeviceType,
                        PointType=PointType,
                        IdDescription=IdDescription,
                        Expression=Expression,
                        Description=Description,
                        EventName=EventName,
                        Level=Level).every_id_list("SHWP_DPS_AL_id.txt"))

# %%
