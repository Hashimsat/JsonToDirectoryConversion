import pandas as pd
import json


df = pd.read_json('.\data\Tasks\TestTask\Subjects\\x8ezhFCjwYh5Idf1pxpG8CcEPEQ2\\2021-11-24\\15.35.44\data.json')

df.to_pickle("./Datadummy.pkl")

# TestDf = pd.read_pickle("./Datadummy.pkl")
# print(TestDf)