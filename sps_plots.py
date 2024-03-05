from check_accuracy import calc_balanced_accuracy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_sps_plot(csv_file_path=None, df=None, RMSE_rank = 0.05, bw_method = 0.07, fig_path = 'plot.png', title = 'Model Predictions', neg_pheno_name = -1, pos_pheno_name = 1, neg_pheno_color = '#2fc8cc', pos_pheno_color = '#F55E54', percent_accuracy = True, axes=None):
    '''creates density plot of sequence prediction score for each species in each ESL run 
    plot has two lines: 1 corresponds to negative phenotype (-1), 1 to positive phenotype (1)
    can either pass csv file or dataframe but not both
    required columns in data: SPS values, true phenotype, input RMSE
    
    Args:
        param1: csv file path to create chart from
        param2: dataframe to create chart from
        param3: RMSE percentage rank to be included in chart (0.05 = lowest 5 percent)
        param4: bw_method (smoothing) used to make plot, higher numbers smooth plot more
        param5: path to save plot to, default is 'plot.png'
        param6: title of plot
        param7: name given to negative phenotype in legend
        param8: name given to positive phenotype in legend
        param9: color of negative phenotype line
        param10: color of positive phenotype line
        param11: display percent accuracy, default is true

    Saves plot to file path provided
    '''
    # reads cvs into pandas dataframe object if no dataframe provided
    if df is None:
        df = pd.read_csv(csv_file_path)

    # copies dataframe if provided to avoid mutating dataframe passed as argument
    else:
        df = df.copy()

    # if no axes provided, gets current axes from matplotlib
    # when axes are provided, skips this step so that plot can be drawn directly on larger plot as a subplot
    if axes is None:
        fig, axes = plt.subplots(figsize=(8, 5))
    
    # converts input_RMSE to percentage rank
    df['RMSE_Rank'] = df.input_RMSE.rank(pct = True)

    # selects true_phenotype and SPS columns based on RMSE percentage rank
    df =  df[df['RMSE_Rank'] < RMSE_rank]
    #data_wide = df.pivot(columns='true_phenotype', values='SPS')

    # creates density plot
    sns.kdeplot((df.loc[df['true_phenotype'] == 1])['SPS'], color=pos_pheno_color, bw_method=bw_method, ax=axes, label=pos_pheno_name)
    sns.kdeplot((df.loc[df['true_phenotype'] == -1])['SPS'], color=neg_pheno_color, bw_method=bw_method, ax=axes, label=neg_pheno_name)
    
    # labels axes and adds title
    title = title + '\nlowest ' + "{0:.0%}".format(RMSE_rank) + ' of RMSE models combined'
    
    #adds caption with percent accuracy
    if percent_accuracy:
        xlabel = 'Sequence Prediction Score\n' + "{0:.0%} percent accuracy".format(calc_percent_accuracy_from_df(df)) + ', ' + "{0:.0%} percent balanced accuracy".format(calc_balanced_accuracy(df))
    else:
        xlabel = 'Sequence Prediction Score'
    axes.set_xlabel(xlabel)
    
    axes.set_title(title)
    axes.set_ylabel('Normalized Counts')
    
    # style
    axes.grid(color = 'white', linestyle='-', linewidth=1)
    axes.set_facecolor('#ececec')

    # legend labels and title
    axes.legend(labels=[pos_pheno_name, neg_pheno_name], title='True Phenotype')
    
    plt.tight_layout()

    # saves plot
    plt.savefig(fig_path)

# calculates percent accuracy directly from csv file- no longer use
def calc_percent_accuracy_from_csv(csv_file_path):
    csv_file = open(csv_file_path, 'r')
    num_correct = 0
    total_num = 0
    for row in csv_file.readlines()[1:]:
        row = row.strip().split(',')
        total_num += 1
        true_pheno = float(row[-1])
        sps = float(row[-2])
        if true_pheno * sps > 0:
            num_correct += 1
    csv_file.close()
    return num_correct / total_num

# calculates percent accuracy from data frame
def calc_percent_accuracy_from_df(df):
    num_correct = 0
    total_num = len(df.index)
    # list comprehension to get tuples of SPS and true phenottype values
    # call is_row_correct for each tuples then sum values
    num_correct = sum([is_row_correct(x, int(y)) for x, y in zip(df['SPS'], df['true_phenotype'])]) 
    return num_correct/total_num

def is_row_correct(SPS, true_phenotype):
    # returns 1 if correct, 0 if incorrect
    # correct sequence prediction when SPS*true_phenotype > 0
    # seq with +1 phenotype should have positive SPS, seq with -1 phenotype should have negative SPS
    if SPS*true_phenotype > 0:
        return 1
    return 0
