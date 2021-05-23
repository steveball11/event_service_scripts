import pandas as pd
import numpy as np
import json
#%%
df_list = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='List')
df_point_type_FCU = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='PointType_FCU')
df_point_type_AHU = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='PointType_AHU')
df_point_type_CDS = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='PointType_CDS')
df_point_type_LDS = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='PointType_LDS')
df_point_type_FACP = pd.read_excel('point_type_and_GUID_mapping.xlsx',sheet_name='PointType_FACP')

#%%


#%%
df_rulebase_set_file = pd.DataFrame([])
mask_FCU = df_list["DeviceID"].str.contains("FCU")
mask_AHU = df_list["DeviceID"].str.contains("AHU")
mask_CDS = df_list["DeviceID"].str.contains("CDS")
mask_LDS = df_list["DeviceID"].str.contains("LDS")
mask_FACP = df_list["DeviceID"].str.contains("FACP")

for point_type in df_point_type_FCU['PointType']:
    df_temp = pd.DataFrame([df_list.loc[mask_FCU,'GUID'], df_list.loc[mask_FCU,'DeviceID_mod'] + '-' +  point_type, df_list.loc[mask_FCU,'DeviceID_mod']]).T
    df_rulebase_set_file = pd.concat([df_rulebase_set_file,df_temp])

for point_type in df_point_type_AHU['PointType']:
    df_temp = pd.DataFrame([df_list.loc[mask_AHU,'GUID'], df_list.loc[mask_AHU,'DeviceID_mod'] + '-' +  point_type, df_list.loc[mask_AHU,'DeviceID_mod']]).T
    df_rulebase_set_file = pd.concat([df_rulebase_set_file,df_temp])

for point_type in df_point_type_CDS['PointType']:
    df_temp = pd.DataFrame([df_list.loc[mask_CDS,'GUID'], df_list.loc[mask_CDS,'DeviceID_mod'] + '-' +  point_type, df_list.loc[mask_CDS,'DeviceID_mod']]).T
    df_rulebase_set_file = pd.concat([df_rulebase_set_file,df_temp])

for point_type in df_point_type_LDS['PointType']:
    df_temp = pd.DataFrame([df_list.loc[mask_LDS,'GUID'], df_list.loc[mask_LDS,'DeviceID_mod'] + '-' +  point_type, df_list.loc[mask_LDS,'DeviceID_mod']]).T
    df_rulebase_set_file = pd.concat([df_rulebase_set_file,df_temp])
    
for point_type in df_point_type_FACP['PointType']:
    df_temp = pd.DataFrame([df_list.loc[mask_FACP,'GUID'], df_list.loc[mask_FACP,'DeviceID_mod'] + '-' +  point_type, df_list.loc[mask_FACP,'DeviceID_mod']]).T
    df_rulebase_set_file = pd.concat([df_rulebase_set_file,df_temp])
    

#%%
df_rulebase_set_file = df_rulebase_set_file.reset_index(drop=True)    
df_rulebase_set_file.columns = ['GUID','PointId','DeviceId']
df_rulebase_set_file["DeviceType"] = df_rulebase_set_file["PointId"].str.split("-").str[0].str.split("_").str[0]
df_rulebase_set_file["PointType"] = df_rulebase_set_file["PointId"].str.split("-").str[1]
df_rulebase_set_file['floor'] = df_rulebase_set_file['DeviceId'].str.split('_').str[-1].values
#  PAH 樓層設定
df_rulebase_set_file.loc[df_rulebase_set_file["DeviceId"].str.contains("PRE"),"floor"] = df_rulebase_set_file.loc[df_rulebase_set_file["DeviceId"].str.contains("PRE"),"DeviceId"].str.split('_').str[-2].values

#%% 異常規則
# 基本規則
df_rulebase_set_file["id_description"] = "_alarm"
df_rulebase_set_file["expression"] = "x.value != None and x.value > 20"
df_rulebase_set_file["description"] = df_rulebase_set_file['PointId'] + "_異常"
df_rulebase_set_file["Event_Name"] = "異常"
df_rulebase_set_file["level"] = "警報"
#%%
# 特定點位規則
# FCU RA
mask_FCU_RA = df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("RA_T") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_SP") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_H_AL_SP") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_L_AL_SP") 
df_rulebase_set_file.loc[mask_FCU_RA,"expression"] = "x.value != None and x.value > 28"
# 異常描述
df_rulebase_set_file.loc[mask_FCU_RA,"description"] = df_rulebase_set_file.loc[mask_FCU_RA,'DeviceId'] + " 回風溫度過高" + " (" + df_rulebase_set_file.loc[mask_FCU_RA,'PointType']  + "> 28°C)"
df_rulebase_set_file.loc[mask_FCU_RA,"Event_Name"] = "回風溫度過高異常"
#%%
# CDS
mask_CDS_co2 =  df_rulebase_set_file["DeviceType"].str.contains("CDS") & df_rulebase_set_file["PointType"].str.contains("CO2") & ~df_rulebase_set_file["PointType"].str.contains("SP")
df_rulebase_set_file.loc[mask_CDS_co2,"expression"] = "x.value != None and x.value > 950"
# 異常描述
df_rulebase_set_file.loc[mask_CDS_co2,"description"] = df_rulebase_set_file.loc[mask_CDS_co2,'DeviceId'] + " CO2過高" + " (" + df_rulebase_set_file.loc[mask_CDS_co2,'PointType']  + "> 950ppm)"
df_rulebase_set_file.loc[mask_CDS_co2,"Event_Name"] = "二氧化碳濃度過高"
#%%
# FCU COM_AL
mask_FCU_COM_AL =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("COM_AL")
df_rulebase_set_file.loc[mask_FCU_COM_AL,"expression"] = "x.value != None and x.value == True"
# 異常描述
df_rulebase_set_file.loc[mask_FCU_COM_AL,"description"] = df_rulebase_set_file.loc[mask_FCU_COM_AL,'DeviceId'] + " 設備通訊異常" 
df_rulebase_set_file.loc[mask_FCU_COM_AL,"Event_Name"] = "設備通訊異常"
#%%
# FCU RA_T_SP
mask_FCU_RA_T_SP =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("RA_T_SP")
df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"expression"] = "x.value != None and x.value <18  or x.value >28 "
# 異常描述
df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"description"] = df_rulebase_set_file.loc[mask_FCU_RA_T_SP,'DeviceId'] + " 設定溫度超出界線" 
df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"Event_Name"] = "設定溫度異常"
#%%
# FCU TRIP_AL
mask_FCU_TRIP_AL =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("TRIP_AL")
df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"expression"] = "x.value != None and x.value == True "
# 異常描述
df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"description"] = df_rulebase_set_file.loc[mask_FCU_TRIP_AL,'DeviceId'] + "設備跳脫" 
df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"Event_Name"] = "設備跳脫"

#%% 數據採集異常
# 特定點位規則
# FCU RA
# mask_FCU_RA = df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("RA_T") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_SP") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_H_AL_SP") & ~df_rulebase_set_file["PointType"].str.contains("RA_T_L_AL_SP") 
# df_rulebase_set_file.loc[mask_FCU_RA,"expression"] = "x.value == None"
# # 異常描述
# df_rulebase_set_file.loc[mask_FCU_RA,"description"] = df_rulebase_set_file.loc[mask_FCU_RA,'PointId'] + " 數據採集異常"
# df_rulebase_set_file.loc[mask_FCU_RA,"Event_Name"] = "數據採集異常"

# # CDS
# mask_CDS_co2 =  df_rulebase_set_file["DeviceType"].str.contains("CDS") & df_rulebase_set_file["PointType"].str.contains("CO2") & ~df_rulebase_set_file["PointType"].str.contains("SP")
# df_rulebase_set_file.loc[mask_CDS_co2,"expression"] = "x.value == None"
# # 異常描述
# df_rulebase_set_file.loc[mask_CDS_co2,"description"] = df_rulebase_set_file.loc[mask_CDS_co2,'PointId'] + " 數據採集異常"
# df_rulebase_set_file.loc[mask_CDS_co2,"Event_Name"] = "數據採集異常"

# # FCU COM_AL
# mask_FCU_COM_AL =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("COM_AL")
# df_rulebase_set_file.loc[mask_FCU_COM_AL,"expression"] = "x.value != None and x.value == True"
# # 異常描述
# df_rulebase_set_file.loc[mask_FCU_COM_AL,"description"] = df_rulebase_set_file.loc[mask_FCU_COM_AL,'PointId'] + " 數據採集異常" 
# df_rulebase_set_file.loc[mask_FCU_COM_AL,"Event_Name"] = "數據採集異常"

# # FCU RA_T_SP
# mask_FCU_RA_T_SP =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("RA_T_SP")
# df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"expression"] = "x.value != None and x.value <18  or x.value >28 "
# # 異常描述
# df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"description"] = df_rulebase_set_file.loc[mask_FCU_RA_T_SP,'PointId'] + " 數據採集異常" 
# df_rulebase_set_file.loc[mask_FCU_RA_T_SP,"Event_Name"] = "數據採集異常"
# #%%
# # FCU TRIP_AL
# mask_FCU_TRIP_AL =  df_rulebase_set_file["DeviceType"].str.contains("FCU") & df_rulebase_set_file["PointType"].str.contains("TRIP_AL")
# df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"expression"] = "x.value != None and x.value == True "
# # 異常描述
# df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"description"] = df_rulebase_set_file.loc[mask_FCU_TRIP_AL,'PointId'] + " 數據採集異常" 
# df_rulebase_set_file.loc[mask_FCU_TRIP_AL,"Event_Name"] = "數據採集異常"

#%%
# # LDS COMAL
# mask_LDS_COMAL = df_rulebase_set_file["DeviceType"].str.contains("LDS") & df_rulebase_set_file["PointType"].str.contains("COM_AL")
# df_rulebase_set_file.loc[mask_LDS_COMAL,"expression"] = "x.value != None and x.value == True "
# # 異常描述
# df_rulebase_set_file.loc[mask_LDS_COMAL,"description"] = df_rulebase_set_file.loc[mask_LDS_COMAL,'PointId'] + " 通訊警報"
# df_rulebase_set_file.loc[mask_LDS_COMAL,"Event_Name"] = "設備通訊異常"
# df_rulebase_set_file.loc[mask_LDS_COMAL,"id_description"] = "communication_error"

# # LDS SHORTAL
# mask_LDS_SHORTAL = df_rulebase_set_file["DeviceType"].str.contains("LDS") & df_rulebase_set_file["PointType"].str.contains("SHORT_AL")
# df_rulebase_set_file.loc[mask_LDS_SHORTAL,"expression"] = "x.value != None and x.value == True "
# # 異常描述
# df_rulebase_set_file.loc[mask_LDS_SHORTAL,"description"] = df_rulebase_set_file.loc[mask_LDS_SHORTAL,'PointId'] + " 短路警報"
# df_rulebase_set_file.loc[mask_LDS_SHORTAL,"Event_Name"] = "設備短路異常"
# df_rulebase_set_file.loc[mask_LDS_SHORTAL,"id_description"] = "short_circuit_alarm"

# # LDS LEAK
# mask_LDS_LeakAL = df_rulebase_set_file["DeviceType"].str.contains("LDS") & df_rulebase_set_file["PointType"].str.contains("LEAK_AL")
# df_rulebase_set_file.loc[mask_LDS_LeakAL,"expression"] = "x.value != None and x.value == True "
# # 異常描述
# df_rulebase_set_file.loc[mask_LDS_LeakAL,"description"] = df_rulebase_set_file.loc[mask_LDS_LeakAL,'PointId'] + " 漏液警報"
# df_rulebase_set_file.loc[mask_LDS_LeakAL,"Event_Name"] = "漏液異常"
# df_rulebase_set_file.loc[mask_LDS_LeakAL,"id_description"] = "Leak_alarm"

# # LDS BREAKAL
# mask_LDS_BreakAL = df_rulebase_set_file["DeviceType"].str.contains("LDS") & df_rulebase_set_file["PointType"].str.contains("BREAK_AL")
# df_rulebase_set_file.loc[mask_LDS_BreakAL,"expression"] = "x.value != None and x.value == True "
# # 異常描述
# df_rulebase_set_file.loc[mask_LDS_BreakAL,"description"] = df_rulebase_set_file.loc[mask_LDS_BreakAL,'PointId'] + " 斷路警報"
# df_rulebase_set_file.loc[mask_LDS_BreakAL,"Event_Name"] = "斷路異常"
# df_rulebase_set_file.loc[mask_LDS_BreakAL,"id_description"] = "open_circuit_alarm"

#%%
mask_FACP_FIRE1AL = df_rulebase_set_file["DeviceType"].str.contains("FACP") & df_rulebase_set_file["PointType"].str.contains("FIRE1_AL")
df_rulebase_set_file.loc[mask_FACP_FIRE1AL,"expression"] = "x.value != None and x.value == True "
# 異常描述
df_rulebase_set_file.loc[mask_FACP_FIRE1AL,"description"] = df_rulebase_set_file.loc[mask_FACP_FIRE1AL,'PointId'] + " 火警警報"
df_rulebase_set_file.loc[mask_FACP_FIRE1AL,"Event_Name"] = "火警"
df_rulebase_set_file.loc[mask_FACP_FIRE1AL,"id_description"] = "fire_alarm"
df_rulebase_set_file.loc[mask_FACP_FIRE1AL,"level"] = "嚴重報警"

mask_FACP_FIRE2AL = df_rulebase_set_file["DeviceType"].str.contains("FACP") & df_rulebase_set_file["PointType"].str.contains("FIRE2_AL")
df_rulebase_set_file.loc[mask_FACP_FIRE2AL,"expression"] = "x.value != None and x.value == True "
# 異常描述
df_rulebase_set_file.loc[mask_FACP_FIRE2AL,"description"] = df_rulebase_set_file.loc[mask_FACP_FIRE2AL,'PointId'] + " 火警警報"
df_rulebase_set_file.loc[mask_FACP_FIRE2AL,"Event_Name"] = "火警"
df_rulebase_set_file.loc[mask_FACP_FIRE2AL,"id_description"] = "fire_alarm"
df_rulebase_set_file.loc[mask_FACP_FIRE2AL,"level"] = "嚴重報警"

mask_FACP_FIRE_TRB_AL = df_rulebase_set_file["DeviceType"].str.contains("FACP") & df_rulebase_set_file["PointType"].str.contains("TRB_AL")
df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,"expression"] = "x.value != None and x.value == True "
# 異常描述
df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,"description"] = df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,'PointId'] + " 火警跳脫警報"
df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,"Event_Name"] = "火警點跳脫"
df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,"id_description"] = "fire_trip_alarm"

#%%
df_rulebase_set_file["rule_base_set"] = np.nan
#%%


def dict_id_create(id_description,Event_Name,level,PointId,description,DeviceType,floor,DeviceID,GUID,expression):
    dict_id = [{'_id':F'{PointId}_{id_description}',
           'name':F"{Event_Name}",
           'level':F"{level}",
           'description':F"{description}",
           'labels':[{'device':F"{GUID}"},{"floor":F"TPKD-{floor}"},{"point":F"{PointId}"},{"deviceType":F"{DeviceType}"}],
           'trigger':{"_t": "subscriber","topic": F"points/{PointId}/presentvalue"},
           'calculator':{"_t":"default","arguments":{"x":{"_t":"topic"}},"conditions":{"activate":{"_t":"simple","expression":F"{expression}"}}},
           'handlers':[]
           }]
    return dict_id




def save_text(df_rulebase_set_file_assign,save_txt):
    combine_txt = "["
    for i,txt in enumerate(df_rulebase_set_file_assign["rule_base_set"]):
        if i!= len(df_rulebase_set_file_assign["rule_base_set"])-1:
            combine_txt = combine_txt + txt[1:-1] + ","
        else:
            combine_txt = combine_txt + txt[1:-1]
    combine_txt = combine_txt + "]"
    text_file = open(save_txt, "w")
    
    text_file.write(combine_txt)
    
    text_file.close()

#%%
for i in range(len(df_rulebase_set_file)):
    df_rulebase_set_file.loc[i,"rule_base_set"] = json.dumps(dict_id_create(df_rulebase_set_file.loc[i,"id_description"],df_rulebase_set_file.loc[i,"Event_Name"],df_rulebase_set_file.loc[i,"level"],df_rulebase_set_file.loc[i,"PointId"],df_rulebase_set_file.loc[i,"description"],df_rulebase_set_file.loc[i,"DeviceType"],df_rulebase_set_file.loc[i,"floor"],df_rulebase_set_file.loc[i,"DeviceId"],df_rulebase_set_file.loc[i,"GUID"],df_rulebase_set_file.loc[i,"expression"]),ensure_ascii=False)
df_rulebase_set_file.to_excel("RuleBase_test_set.xlsx")
#%%
# FCU RA
df_rulebase_set_file_assign = df_rulebase_set_file.loc[mask_FCU_RA,:]
save_txt = "FCU_RA_post_str.txt"
save_text(df_rulebase_set_file_assign,save_txt)



df_rulebase_set_file_assign = df_rulebase_set_file.loc[mask_FACP_FIRE1AL,:]
save_txt = "FACP_FIRE1AL_post_str.txt"
save_text(df_rulebase_set_file_assign,save_txt)

df_rulebase_set_file_assign = df_rulebase_set_file.loc[mask_FACP_FIRE2AL,:]
save_txt = "FACP_FIRE2AL_post_str.txt"
save_text(df_rulebase_set_file_assign,save_txt)

df_rulebase_set_file_assign = df_rulebase_set_file.loc[mask_FACP_FIRE_TRB_AL,:]
save_txt = "FACP_FIRE_TRB_AL_post_str.txt"
save_text(df_rulebase_set_file_assign,save_txt)
#%%
