#%%
import requests
import pandas as pd
import json
#%%
req = requests.get("https://event.aubix.com/api/Alerts?status=all&opened_lt=2021-08-01T00%3A00%3A00%2B08%3A00&descending=true")
# %%
df = pd.DataFrame(req.json())
df["description"] = df.iloc[:,1].apply(lambda x: x["description"])
df["id"] = df.iloc[:,1].apply(lambda x: x["id"])
df["confirmor"] = "蔡明達"
# %%
index1 = df.index[0:2000]
index2 = df.index[2000:4000]
index3 = df.index[4000:]
comfirm_result = df.loc[index3,["id","confirmor"]].to_json(orient="records",force_ascii=False)



text_file = open("comfirm_3.txt", "w",encoding='UTF-8')
text_file.write(comfirm_result)
text_file.close()
# %%
