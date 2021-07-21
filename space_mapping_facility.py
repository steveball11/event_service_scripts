#%%
import pandas as pd
#%%
# 找出指定空間的設備
# 指定空間跟設備
def space_mapping(target_space,target_facility):
    df_space_list = pd.read_excel("TW-NTC-TPKD Space List_20201023.xlsx")
    df_object = pd.read_excel("物件資料20210512.xlsx")
    df_object = df_object.applymap(str)

    target_space_code = pd.DataFrame(df_space_list.loc[df_space_list.loc[:,"SpaceClass"].str.contains(target_space),"SpaceCode"])
    df_filt = pd.DataFrame()
    if len(target_space_code.index)>1:
        for space in target_space_code["SpaceCode"]:
            df_object_temp = df_object.loc[df_object.loc[:,"parent_name"]==space,:]
            df_filt = pd.concat([df_filt,df_object_temp])

    df_filt = df_filt.loc[df_object.loc[:,"name"].str.contains(target_facility),:].reset_index()
    df_filt["樓層"] = df_filt["樓層"].apply(int)
    df_filt = df_filt.loc[:,["樓層","asset_type","name","id"]].sort_values(by="樓層",ascending=True)
    df_filt["name"] = df_filt["name"].str.replace("-","_")
    return df_filt

if __name__ == "__main__":
    df = space_mapping(target_space="Lab",target_facility="FCU")
    print(df)
# %%



