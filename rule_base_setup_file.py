import pandas as pd
import json


def dict_id_create(IdDescription,Event_Name,Level,PointId,Description,DeviceType,Floor,DeviceID,GUID,Expression):
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
        self.df_list = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='List')
        self.DeviceType = DeviceType
        self.PointType = PointType
        self.IdDescription = IdDescription
        self.Expression = Expression
        self.Description = Description
        self.EventName = EventName
        self.Level = Level
        self.df_assign_type = self.read_PointType()
        self.df_setup = self.create_setup_df()
        self.Series_post_str = self.create_post_str_Series()
        self.combine_txt = self.create_text()
    
    def read_PointType(self):
        return pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name=F'{self.DeviceType}')
    
    def create_setup_df(self):
        mask_assign = self.df_list["DeviceID"].str.contains(self.DeviceType)
        pointID_series = (self.df_list.loc[mask_assign,'DeviceID_mod'] + '-' +  self.PointType)
        df_setup = pd.DataFrame([self.df_list.loc[mask_assign,'GUID'], pointID_series, (self.df_list.loc[mask_assign,'DeviceID_mod'])]).T
        df_setup = df_setup.reset_index(drop=True)    
        df_setup.columns = ['GUID','PointId','DeviceId']
        df_setup["DeviceType"] = self.DeviceType
        df_setup["PointType"] = self.PointType
        print(df_setup)
        df_setup['floor'] = df_setup['DeviceId'].str.split('_').str[-1].values
        
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
        text_file = open(save_txt, "w")
        text_file.write(self.combine_txt)
        text_file.close()
        return print("Success")
#%%
if __name__ == "__main__":

    print(Set_up_rules(DeviceType="CT",
                        PointType="TRIP_AL",
                        IdDescription="alarm",
                        Expression="x.value != None and x.value == True ",
                        Description="冷去水塔跳脫警報",
                        EventName="冷去水塔跳脫警報",
                        Level="嚴重").save_text("CT_TRIP_AL.txt"))