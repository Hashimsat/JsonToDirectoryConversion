

# import jsonparser
# Structures("/home/ProjectsCheck/", template_file="Beautified_Data.json").create("Project002")

import json
import os
import Functions as fy

# File where json is stored
json_file_path = "/Users/hashim/PhD/PhD Project/Code and Data/Pilot Studies/Pilot13_Flipped_CombinedTimeAnxiety_MixedPredators/Data/Extracted Data/beautified_Pilot13.txt"

with open(json_file_path, 'r') as j:
    contents = json.loads(j.read())



#cwd = os.getcwd()
# Set up path where data will be saved
cwd = "/Users/hashim/PhD/PhD Project/Code and Data/Pilot Studies/Pilot13_Flipped_CombinedTimeAnxiety_MixedPredators/Data/Extracted Data"

# print(contents)

#print(cwd)

fy.jsonToDirectory(contents,cwd,'')  # Run this first#
rootdir = cwd + '/data'
#
# Create a big pandas dataframe for all subjects combined
# fy.create_combined_megapandas(rootdir) # run this after the first line has been run








