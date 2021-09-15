import json
import pandas as pd
import numpy as np

def read_van_data(filename):
    with open(filename,'r',encoding = "utf-8") as f:
        a = f.readlines()
    df = pd.DataFrame(a)
    data_list = list(df[0])
    oh = []
    web = []
    for i in data_list:
        tag_dict = json.loads(i)["tags"]
        try:
            oh.append(tag_dict["opening_hours"])
        except:
            oh.append(None)
    for i in data_list:
        tag_dict = json.loads(i)["tags"]
        try:
            web.append(tag_dict["website"])
        except:
            web.append(None)
    df2 = pd.DataFrame({"opening_hours":oh,"website":web})
    
    data = pd.read_json(filename, lines=True)
    data=pd.concat([data, df2], axis=1, join='inner')
    data = data.dropna(subset=['name']).reset_index()
    return data