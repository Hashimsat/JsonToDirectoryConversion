# inspired from https://towardsdatascience.com/extraordinary-data-visualisation-circular-chart-fe2d835ef929

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import glob


# function for theta
def get_theta(pct, num_points):
  start = pct[0] * 360
  length = (pct[1] - pct[0]) * 360
  step = 360 / num_points
  return np.arange(start, start + length + step, step)

# add data
#We create all plots at once

rootdirr = 'D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\Extracted Data\Pilot1-20.01.2022\data\Subjects'
json_pattern = rootdirr + "/**/*.json"

file_list = glob.glob(json_pattern,recursive=True)   #find all files with .json ending in directory and subdirectory, store path in list
# ------------------------------------
# 1. Load data
# ------------------------------------

for file in file_list:
    df = pd.read_json(file)
    r_gap = 1 #gap between successive trials
    num_points = 360

    # Get radial scale
    max_r = 1 + (len(df)) * r_gap

    print(len(df))

    # -------
    # Creating Figure
    fig = go.Figure()

    # Adding base circle

    # Create the base circle
    fig.add_trace(go.Scatterpolar(
        r=[1] * num_points,
        theta=get_theta([0, 1], num_points),
        mode='markers',
        line_color='black',
        line_width=3,
        showlegend=False
    ))

    colourVar = ''
    # Loop the dataframe to add all the gene cirles
    for index, seg in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r = [1 + (index + 1) * r_gap] * num_points,
            theta = np.arange(df['PredatorMean'][index],df['PredatorMean'][index]+0.2),
            mode='markers',
            # marker_color = 'green',
            marker=dict(size=[12],
                        color='green'),

            line_width=6,
            name='Trial ' + str(index + 1) + ' Predator Mean'
        ))
        #colourVar = fig.

        fig.add_trace(go.Scatterpolar(
            r=[1 + (index + 1) * r_gap] * num_points,
            theta=np.arange(df['PredatorAngle'][index], df['PredatorAngle'][index] + 0.2),
            mode='markers',
            # marker_color='blue',
            marker=dict(size=[12],
                        color='blue'),
            line_width=6,
            name='Trial ' + str(index + 1) + ' Predator Angle'
        ))

        if (np.isnan(df['torchAngle'][index]) != True):
            fig.add_trace(go.Scatterpolar(
                r=[1 + (index + 1) * r_gap] * num_points,
                theta=np.arange(df['torchAngle'][index], df['torchAngle'][index] + 0.2),
                mode='markers',
                #marker_color='red',
                marker=dict(size=[12],
                            color='red'),
                line_width=6,
                name='Trial ' + str(index + 1) + ' Torch Angle'
            ))


    # Configure the layout based on the requirements.
    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                rotation=0,
                direction="counterclockwise",
                showticklabels=True,
                showgrid=True
            ),
            radialaxis=dict(
                range=[0, 1 + (len(df) + 1) * r_gap],
                showticklabels=False,
                visible=True
            )
        )
    )

    BlockNum = df['BlockNumber'][1]

    name = df['subjectID'][2] + ' Block' + str(BlockNum) + '.html'

    print(name)

    FigureFolder = 'D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\Plots\Circular Plots_Data'

    # Save figure
    savename = os.path.join(FigureFolder,name)

    fig.write_html(savename)











