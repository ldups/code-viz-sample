import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from math import floor
from matplotlib.colors import ListedColormap
from sps_vs_value_plot import create_species_resistance_dict, relate_phenosense_data

# creates a colormap between negative and positive phenotype colors
def create_cmp(num_colors):
    vals = np.ones((num_colors, 4))
    vals[:, 0] = np.linspace(47/256, 245/256, num_colors)
    vals[:, 1] = np.linspace(200/256, 94/256, num_colors)
    vals[:, 2] = np.linspace(204/256, 84/256, num_colors)
    cmp = ListedColormap(vals)
    return cmp

# filters a data frame into different thresholds
# creates list of labels describing filtered datasets
def filter_by_bounds(thresholdlist, df):
    datasets = []
    labels = []
    for i in range(len(thresholdlist) + 1):
        if i == 0:
            lowerbound = 0
        else:
            lowerbound = thresholdlist[i-1]

        if i == len(thresholdlist):
            # sets upper bound just above possible maximum
            upperbound = 100.5
        else:
            upperbound = thresholdlist[i]

        labels.append(str(lowerbound) + ' to ' + str(floor(upperbound)))
        datasets.append(df[(df.resistance >= lowerbound) & (df.resistance < upperbound)]['SPS'].values)
    
    # return list of data frames and labels corresponding to them
    return datasets,labels

def var_res_density(key_path, title, thresholdlist, plot_path=None, axes=None, df=None, csv_path=None):
    # if data frame provided, copy to avoid mutating data frame passed as argument
    if not df is None:
        df = df.copy()
    # if csv provided instead of data frame, create data frame here
    elif not csv_path is None:
         df = create_df_w_res(key_path, csv_path)

    datasets, labels = filter_by_bounds(thresholdlist, df)

    cmp = create_cmp(len(datasets))
    
    if axes is None:
        axes = plt.gca()

    for i in range(len(datasets)):
        data = datasets[i]
        # create density curve corresponding to each data frame
        sns.kdeplot(data=data, ax=axes, color=cmp.colors[i], label = labels[i])

    axes.set_xlabel("Sequence Prediction Score")
    axes.grid(color = 'white', linestyle='-', linewidth=1)
    axes.set_facecolor('#ececec')
    axes.set_title(title)
    axes.legend(title='Fold Resistance')

    # if not subplot, save figure
    if not plot_path is None:
        plt.savefig(plot_path)

def comparative_var_res_plots(num_figs, csv_path_list, title_list, key_path, plot_path_list, threshold_list):
    """Creates violin, scatter, and density plots comparing data in csv files. Saves each plot to different file.

    Keyword arguments:
    num_figs -- number of figures to be included. csv_path_list, title_list, and plot_path_list must have at least as many elements as this.
    csv_path_list -- list of paths containing csv files to make into plots. 
    title_list -- list of titls for plots.
    key_path -- path to txt file relating test sequences to known resistance.
    plot_path_list -- list of paths to save plots to.
    threshold_list -- list of thresholds to divide violin and density plots into.
    """
    # create data frames corresponding to each csv file
    df_list = []
    for csv_path in csv_path_list:
        df = create_df_w_res(key_path, csv_path)
        df_list.append(df)

    # create mpl figure and axes for violin plot
    fig, axes = plt.subplots(nrows=1, ncols=num_figs)

    # create violin plots for each data frame on different subplot
    for i in range(0, num_figs):
        title = title_list[i]
        df = df_list[i]
        var_res_violin(key_path, title, threshold_list, axes=axes[i], df=df)

    # sets size and saves figure
    fig.set_size_inches(5*num_figs, 5)
    fig.tight_layout()
    plt.savefig(plot_path_list[0]) 

    # clear plt axes
    plt.cla()

    # create mpl figure and axes for scatter plot
    fig, axes = plt.subplots(nrows=1, ncols=num_figs)

    # create scatter plots for each data frame on different subplot
    for i in range(0, num_figs):
        title = title_list[i]
        df = df_list[i]
        accuracy_v_res_scatter(key_path, title, axes=axes[i], df=df)

    # sets size and saves figure
    fig.set_size_inches(5*num_figs, 5)
    fig.tight_layout()
    plt.savefig(plot_path_list[1]) 

    # clear plt axes
    plt.cla()

    # create mpl figure and axes for density plot
    fig, axes = plt.subplots(nrows=1, ncols=num_figs)

    # create density plots for each data frame on different subplot
    for i in range(0, num_figs):
        title = title_list[i]
        df = df_list[i]
        var_res_density(key_path, title, threshold_list, axes=axes[i], df=df)

    # sets size and saves figure
    fig.set_size_inches(5*num_figs, 5)
    fig.tight_layout()
    plt.savefig(plot_path_list[2]) 
