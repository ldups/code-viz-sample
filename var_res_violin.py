import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from math import floor
from matplotlib.colors import ListedColormap
from sps_vs_value_plot import create_species_resistance_dict, relate_phenosense_data

def var_res_violin(key_path, title, thresholdlist, plot_path=None, axes=None, df=None, csv_path=None):
    # if data frame provided, copy to avoid mutating data frame passed as argument
    if not df is None:
        df = df.copy()
    # if csv provided instead of data frame, create data frame here
    elif not csv_path is None:
         df = create_df_w_res(csv_path, key_path)

    datasets, labels = filter_by_bounds(thresholdlist, df)

    # if no axes corresponding to subplot provided, get current axes to use
    if axes is None:
        axes = plt.gca()
    violin_parts = axes.violinplot(dataset=datasets, showextrema=False)

    num_violins = len(violin_parts['bodies'])

    cmp = create_cmp(num_violins)

    for [violin, cmap] in zip(violin_parts['bodies'], cmp.colors):
        violin.set_facecolor(cmap)
        violin.set_edgecolor('black')

    axes.legend(labels=labels, title='True phenotype (fold resistance)', loc='upper center', ncol=3)
    axes.set_title(title)
    axes.set_ylabel('SPS')
    axes.set_xticklabels([])
    
    # if plot path provided, save fig
    if not plot_path is None:
        plt.savefig(plot_path)
