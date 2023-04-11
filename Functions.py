import os
import json
import random
from pathlib import Path as Path_ch
import glob
import pandas as pd


def jsonToDirectory(v, path, last_key, prefix=''):

    if isinstance(v, dict):
        path1 = join_path(path, prefix)   # join_path is function

        if not os.path.isdir(path1):  # create a new directory if one doesn't already exist
            os.makedirs(path1)
            print(path1)

        for k, v2 in v.items():
            p2 = "{}/{}".format(prefix, k)   # change prefix value to current directory
            jsonToDirectory(v2, path, k, p2)   # recursion through each key value

    # create a new json file with data
    # elif isinstance(v, list):

    elif isinstance(v, (float, int, str, list, tuple)):

        # Previous loops would have created folders for keys which store data too i.e. PredictionError,torch_angle etc.
        # we need to delete these last folders, and instead save their values into json/text files
        Path_remove = join_path(path, prefix)


        # If dict is TorchMovement, we store these in separate json files

        if 'TrackMouse' in Path_remove:
            mousetracking_data(Path_remove, last_key, v)


        else:

            # remove folder for the last key-value pair

            if os.path.isdir(Path_remove):
                os.remove(Path_remove)

            # write data to a new json
            if "HeadPhone" not in last_key:

                New_Path = Path_remove.replace(last_key, '')  # create new json folder here


                data = {last_key: v}
                New_File = New_Path+'data.json'
                write_json_data(data, New_File)

    else:
        print('{} = {}'.format(prefix, repr(v)))



def write_json_data(data,fname):

    a = []
    if not os.path.isfile(fname):
        # a.append(data)
        print(fname)
        a = data
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=4))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)
        # feeds.append(data)
        # feeds |= data   # merge dictionaries together
        d4 = data.copy()  # merge dictionaries
        d4.update(feeds)

        with open(fname, mode='w') as f:
            f.write(json.dumps(d4, indent=4))


def join_path(path,prefix):
    path1 = path + prefix  # join previous path location with new directory path
    path1 = path1.replace('__collections__', '')  # remove __collections__ folder from path
    path1 = path1.replace(':', '.')  # to convert time from 1:23:15 format to 1.23.15 format, but this also changes C:\ to C.\
    # path1 = path1.replace('.\\', ':\\')  # to convert C.\ in path to C:\

    return path1


def mousetracking_data(Path,last_key, v):

    if os.path.isdir(Path):
        os.remove(Path)

    # write data to a new json
    p = Path_ch(Path)
    New_Path = str(p.parent)

    # Get name of
    # New_Path = Path.replace(last_key, '')  # create new json folder here
    data = {last_key: v}
    New_File = New_Path + '/MouseTracking.json'
    write_json_data(data, New_File)


def create_combined_megapandas(rootdirr):

    # Function that creates a mega dataframe with all participant data combined
    # Mouse tracking data not added yet

    json_pattern = rootdirr + "/**/*data.json"

    print(json_pattern)
    file_list = glob.glob(json_pattern,
                          recursive=True)  # find all files with data.json ending in directory and subdirectory, store path in list




    dfs = []
    # print(file_list[4])
    #df1 = pd.read_json(file_list[4])

    for file in file_list:
        print(file)
        df1 = pd.read_json(file)
        dfs.append(df1)

    df = pd.concat(dfs)

    saveFile_csv = rootdirr + '/CombinedData.csv'
    saveFile_pickle = rootdirr + '/CombinedData.pkl'

    print(df)

    df.to_pickle(saveFile_pickle)
    df.to_csv(saveFile_csv)






