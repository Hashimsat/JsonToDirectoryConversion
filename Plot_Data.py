import json
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.gridspec as gridspec
from al_plot_utils import latex_plt, plot_image, cm2inch, label_subplots, swarm_boxplot, CircularDistance_Array
import glob
import matplotlib.colors as mcolors

#draw figures for all blocks for each subject

#json_file_path ='.\data\Tasks\TestTask\Subjects\\4XU9xj2icaenzivtYhgovOwW6so2\\2021-11-19\9.23.11\data.json'
rootdirr = '/Users/hashim/PhD/PhD Project/Code and Data/Pilot Studies/Pilot12-Flipped Version Replication2/Data/Extracted Data/data/Subjects'
# json_pattern = rootdirr + "/**/*.json"
json_pattern = rootdirr + "/**/*data.json"


BlockNum = 0;

print(json_pattern)
file_list = glob.glob(json_pattern,recursive=True)   #find all files with .json ending in directory and subdirectory, store path in list
# ------------------------------------
# 1. Load data and compute performance
# ------------------------------------
matplotlib = latex_plt(matplotlib)
# Load data
for file in file_list:

    print(file)

    #BlockNum = BlockNum + 1  #store block num

    df1 = pd.read_json(file)
    df1.reset_index(drop=True)

    if df1.empty:
        print('empty hai bro ', file)

    else:

        # -----------------
        # 2. Prepare figure
        # -----------------

        # Size of figure
        fig_height = 20
        fig_width = 30

        # Create figure
        f = plt.figure(figsize=cm2inch(fig_width, fig_height))
        f.canvas.draw()
        # f.canvas.tostring_argb()

        # Create plot grid
        #gs_0 = gridspec.GridSpec(3, 1, wspace=0.5, hspace=0.7, top=0.95, bottom=0.085, left=0.18, right=0.95)
        gs_0 = gridspec.GridSpec(3, 1, wspace=0.5, hspace=0.8, top=0.9, bottom=0.06, left=0.2, right=0.95)
        # Plot colors
        colors = ["#92e0a9", "#69b0c1", "#6d6192", "#352d4d"]
        sns.set_palette(sns.color_palette(colors))

        # ----------------------------
        # 3. Plot Each Block Individually for Each Subject
        # ----------------------------

        # Create subplot grid and axis
        # gs_00 = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=gs_0[0])
        # Create subplot grid
        gs_01 = gridspec.GridSpecFromSubplotSpec(9, 1, subplot_spec=gs_0[0:2], hspace=1)

        ax_10 = plt.Subplot(f, gs_01[0:3, 0])
        f.add_subplot(ax_10)

        # Indicate plot range and x-axis
        #plot_range = (200, 225)
        # plot_range = (0,26)
        # x = np.linspace(0, plot_range[1]-plot_range[0]-1, plot_range[1]-plot_range[0])

        #Plot Predator Mean, Predator Actual Location and Player Torch Placement
        N = np.arange(len(df1))

       # print(df1['PredatorType'][0:20])

        cmap, norm = mcolors.from_levels_and_colors([1, 2, 3, 4], ['#FFD700', 'black', '#4CBB17'])   # Different colour predator actual mean depending on type of predator

        ax_10.plot(N,df1['PredatorMean'], '--',linewidth=3, color="#800080")
        #ax_10.scatter(N,df1['PredatorAngle'], 'go',linewidth=4)#,markerfacecolor="#173817",markersize=9)
        ax_10.scatter(N, df1['PredatorAngle'], c = df1['PredatorType'], cmap=cmap, norm=norm)  # ,markerfacecolor="#173817",markersize=9)
        ax_10.plot(N,df1['torchAngle'], linewidth=3, color="#f30a49", alpha=0.8)
        ax_10.set_ylabel('Position',fontsize=9)
        ax_10.legend(["Predator Mean", "Predator Actual Location","Player Torch Placement"], loc=4, framealpha=0.6,fontsize = 7)
        ax_10.set_ylim(-50, 415)
        ax_10.yaxis.set_tick_params(labelsize=8)
        ax_10.xaxis.set_tick_params(labelsize=8)
        ax_10.set_xticks(np.arange(0, len(N)+5, 10))

        # Prediction errors
        ax_11 = plt.Subplot(f, gs_01[3:5, 0])
        f.add_subplot(ax_11)
        ax_11.plot(df1['PredictionError'], linewidth=3, color="#090030", alpha=1)
        ax_11.set_ylabel('PE',fontsize=9)
        ax_11.legend(['Prediction Error'],loc = 1,fontsize=8)
        ax_11.yaxis.set_tick_params(labelsize=8)
        ax_11.xaxis.set_tick_params(labelsize=8)
        ax_11.set_xticks(np.arange(0, len(N)+5, 10))
        #ax_11.set_xlabel('Trial',fontsize=10)

        # Absolute Estimation Error (torch angle - predator mean)
        ax_12 = plt.Subplot(f, gs_01[5:7, 0])
        f.add_subplot(ax_12)

        Estimation_Error = CircularDistance_Array(df1['PredatorMean'], df1['torchAngle'])
        Estimation_Error = abs(Estimation_Error)

        ax_12.plot(Estimation_Error, linewidth=3, color="#04879c", alpha=1)
        ax_12.legend(['Estimation Error'], loc=1, fontsize=8)
        #ax_12.set_xlabel('Trial', fontsize=10)
        ax_12.set_ylabel('Abs EE', fontsize=9)
        ax_12.yaxis.set_tick_params(labelsize=8)
        ax_12.xaxis.set_tick_params(labelsize=8)
        ax_12.set_yticks(np.arange(0, 300, 100))
        #ax_12.set_yticks(np.arange(0, 330, 100))
        ax_12.set_xticks(np.arange(0, len(N)+5, 10))

        # Initiation Reaction Times with threshold markers for limits for different predators
        ax_13 = plt.Subplot(f, gs_01[7:9, 0])
        f.add_subplot(ax_13)

        #ax_13.plot(df1['RTInitiation'], linewidth=3, color="#04879c", alpha=1)
        ax_13.scatter(N, (df1['RTTorchON'] - df1['RTConfirmation']), c=df1['PredatorType'], cmap=cmap, norm=norm,label='RT Torch On')
        print('Max RT', (df1['RTTorchON'] - df1['RTConfirmation']).max())
        #ax_13.scatter(N, df1['RTConfirmation'], c=df1['PredatorType'], cmap=cmap, norm=norm, label='RT Conf')

        ax_13.axhline(y=1000, color='#FFD700', linestyle='--')  # Threshold line for cheetah at 3050ms (2050ms initial delay)
        ax_13.axhline(y=5000, color='#000000', linestyle='--')  # # Threshold line for panther at 7050ms (2050ms initial delay)
        ax_13.axhline(y=3000, color='#4CBB17', linestyle='--')  # # Threshold line for leopard at 5050ms (2050ms initial delay)
        ax_13.set_xticks(np.arange(0, len(N)+5, 10))
        #ax_13.legend(ax_13[:2],['RT Init'], loc=1, fontsize=8)
        #ax_13.legend()
        ax_13.set_xlabel('Trial', fontsize=10)
        ax_13.set_ylabel('RT (ms)', fontsize=9)
        ax_13.yaxis.set_tick_params(labelsize=8)
        ax_13.xaxis.set_tick_params(labelsize=8)
        ax_13.set_yticks(np.arange(0, 6000, 1000))

        # Delete unnecessary axes
        sns.despine()

        #plt.show()

        # -------------------------------------
        # 5. Add subplot labels and save figure
        # -------------------------------------

        BlockNum = df1['BlockNumber'].iloc[1]
        BlockNum = BlockNum.astype(int)
        PredatorName = df1['PredatorName'].iloc[1]

        Time = df1['time'].iloc[2]

        name = df1['subjectID'].iloc[2] +' Block'+ str(BlockNum) +' ' + PredatorName  + '.png'

        #name = 'Hash Following Predator'+'.png'

        print(name)

        FigureFolder = '/Users/hashim/PhD/PhD Project/Code and Data/Pilot Studies/Pilot12-Flipped Version Replication2/Plots/Raw Data Plots'

       # FigureFolder = 'D:\MPSCog\Orientation Year\Heekeren Lab\PhD Project\Pilot Studies\Data_1\HashimTestPlots\\AverageRTPerPredator\\RTTimeSeriesCombined'

        # Save figure
        savename = os.path.join(FigureFolder,name)
        labelx = -0.05
        ax_10.yaxis.set_label_coords(labelx, 0.5)
        ax_11.yaxis.set_label_coords(labelx, 0.5)
        ax_12.yaxis.set_label_coords(labelx, 0.5)
        ax_13.yaxis.set_label_coords(labelx, 0.5)

        plt.savefig(savename, transparent=True, dpi=600)



    #f.align_labels()
    # # Show plot
    # plt.show()
    # print(name)









# x = 100*df['HitMiss']
#
# plt.figure()
# df['PredatorAngle'].plot()
# df['PredatorMean'].plot()
# df['torchAngle'].plot()
# df['PredictionError'].plot()
# #plt.plot(x)
# plt.legend()
# plt.show()
# #plt.show()

# plt.figure()
# df['PredictionError'].plot()
# plt.show()
