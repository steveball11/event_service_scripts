#%%
import pandas as pd
#%%

df_space_list = pd.read_excel("TW-NTC-TPKD Space List_20201023.xlsx")
df_object = pd.read_excel("物件資料20210512.xlsx")
df_object = df_object.applymap(str)

target_space = "Lab"
target_space_code = pd.DataFrame(df_space_list.loc[df_space_list["SpaceClass"].str.contains(target_space),"SpaceCode"])

df_object = df_object[df_object["parent_name"].str.contains('|'.join(target_space_code.loc[:,"SpaceCode"].to_list()))]
df_object = df_object[""]



# %%



