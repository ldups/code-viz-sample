import argparse
from scipy.stats import fisher_exact
import statsmodels.stats.multitest as smm
import pandas as pd
import numpy as np
from get_enrichment_groups import get_category_gene_lists_hallmarks, get_gene_list
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D

rcParams.update({'figure.autolayout': True})
def enrichment_test(background, categories, selected_genes, num_genes):
    results = pd.DataFrame(columns=['Category', 'OddsRatio', 'P-value', 'FDR'])
    background = set(background)

    selected_genes = selected_genes[:num_genes]
    selected_genes = set(selected_genes)

    for name, group in categories.items():
        cat_genes = set(group) & background

        a = len(set(cat_genes) & set(selected_genes))
        b = len(set(cat_genes) -  set(selected_genes))
        c = len(set(selected_genes) - set(cat_genes))
        d = len(set(background) - set(cat_genes) - set(selected_genes))

        oddsratio, p = fisher_exact([[a, b], [c, d]])
        results.loc[-1] = name, oddsratio, p, np.nan
        results.index = results.index + 1

    results['FDR'] = smm.multipletests(results['P-value'], method='fdr_bh')[1] 

    results['Plot'] = 1/results['FDR']
    results['Category'] = results['Category'].str.replace('_', ' ')
    results.sort_values(by='Plot', inplace=True)
    cmap = plt.cm.RdPu
    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    results.plot.barh(x='Category', y='Plot', legend=None, color=cmap(rescale(results['Plot'])))

    plt.ylabel('Category')
    plt.xlabel('1/FDR')
    line = plt.axvline(20, color='red', label='Significance threshold')
    plt.legend([line], ['Significance threshold'])
    plt.title('Gene Enrichment by Category')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Complete enrichment test using Fisher exact testing')
    parser.add_argument('selected_gene_list', help='genes selected by ESL')
    parser.add_argument('background_gene_list', help='all genes that can be selected by esl')
    parser.add_argument('category_csv', help='csv file containing genes and categories they are associated with')
    parser.add_argument('num_genes', type=int, help='max number of genes selected by ESL to compare')
    args = parser.parse_args()

    categories = get_category_gene_lists_hallmarks(args.category_csv)
    background = get_gene_list(args.background_gene_list)
    selected_genes = get_gene_list(args.selected_gene_list)

    enrichment_test(background, categories, selected_genes, args.num_genes)
