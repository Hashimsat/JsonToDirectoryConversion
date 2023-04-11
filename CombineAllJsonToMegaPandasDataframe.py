import pandas as pd
import glob, os, json


rootdirr = 'D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\Extracted Data\HashimTestFollowPredator\data\Subjects'

# for root, dirs, files in os.walk(rootdir):
#     for name in files:
#         if name.endswith((".json")):
#             print(name)
#             full_path = os.path.join(root, name)
#             print(full_path)


json_pattern = rootdirr + "/**/*.json"

print(json_pattern)
file_list = glob.glob(json_pattern,recursive=True)   #find all files with .json ending in directory and subdirectory, store path in list


dfs = []
for file in file_list:
    #print(file)
    df1 = pd.read_json(file)
    dfs.append(df1)

df = pd.concat(dfs)

print(df)

df.to_pickle("D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\Extracted Data\HashimTestFollowPredator\data\Subjects/CombinedData.pkl")
df.to_csv("D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\Extracted Data\HashimTestFollowPredator\data\Subjects/CombinedData.csv")