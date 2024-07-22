import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from optparse import OptionParser
from functions import *

# Argument values
input = sys.argv

def parse_args():
    """
    Parse CLI options.

    Returns
    -------
    dict
        User CLI options
    """
    usage = "usage: python3 analyze.py \
        -i[--omics] mypath/transcriptomics_Su_2020_feature-data.csv \
        -m[--meta] mypath/transcriptomics_Su_2020_feature-metadata.csv \
        -s[--samples] samples_dict.json \
        -f[--features] LAG3,TRAF2,IL10 \
        -o[--out] results.png"
    required=["omics", "meta","samples","features"]
    parser = OptionParser(usage)
    parser.add_option('-i', '--omics',
                      dest="omics", 
                      help="transcriptomics-feature-data file(csv). [required]",
                      default="..\\..\\data\\Su_2020_FAIR\\transcriptomics\\transcriptomics_Su_2020_feature-data.csv"
                      )
    parser.add_option('-m', '--meta',
                      dest="meta", 
                      help="feature-metadata file(csv). [required]",
                      default="..\\..\\data\\Su_2020_FAIR\\transcriptomics\\transcriptomics_Su_2020_feature-metadata.csv"
                      )
    parser.add_option('-s', '--samples',
                      dest="samples", 
                      help="sample list JSON file. [required]",
                      default="samples_dict.json"
                      )
    parser.add_option('-f', '--features',
                      dest="features", 
                      help="Comma-separated list of features of interest",
                      )
    parser.add_option('-o', '--out',
                      dest="out", 
                      help="results [optional]",
                      default="results.png"
                      )
    parser.add_option('-v', '--verbose',
                      dest="verbose", 
                      help="run with verbose. [optional]",
                      default=True,
                      action="store_true"
                      )
    options, args = parser.parse_args()
    for r in required:
        if options.__dict__[r] is None:
            parser.print_help()
            parser.error("parameter '%s' is required !" % r)
            sys.exit(1)
            
    if options.verbose:
        print( '# STARTING SERVICE\n' )
        print( '# Your input arguments are:' )
        print( '# >omics:', options.omics)
        print( '# >meta:', options.meta)
        print( '# >samples:', options.samples)
        print( '# >features:', options.features)
        print( '# VERBOSE:', options.verbose )
        verbose = options.verbose
    else:
        verbose = False
    return options

# Main
if __name__ == '__main__':
    print('# running script:', input, '\n')
    
    options = parse_args()
    # Get feature data file and read it as a dataframe
    transcriptomics_feature_data = options.omics
    # Read the omics data using the function 'read_omics_data'
    df = read_omics_data(transcriptomics_feature_data)
    # Create a list of features from the comma-separated string
    features_list = options.features.split(',')
    print(features_list)
    
    # Load the sample list from the JSON file
    with open(options.samples, 'r') as f:
        samples_dict = json.load(f)
    
    # Plot the boxplots for each feature
    fig, axes = plt.subplots(len(features_list), 1, figsize=(15, 10 * len(features_list)))
    if len(features_list) == 1:
        axes = [axes]
    
    for ax, feature in zip(axes, features_list):
        # Create a list to store data for boxplots
        data_for_boxplot = []
        labels = []
        
        for group, sample_list in samples_dict.items():
            # Get all the feature of interest values for each sample in the sample list
            df_subset = subset_omics_data(df, feature_list=[feature], sample_list=sample_list)
            print(f'{group} subset for {feature}:')
            print(df_subset)
            
            # Append the data to the list for boxplots
            data_for_boxplot.append(df_subset.values.flatten())
            labels.append(group)
        
        # Plot the boxplot for the current feature
        ax.boxplot(data_for_boxplot, labels=labels)
        ax.set_title(f'Boxplot for {feature}')
        ax.set_ylabel(feature)
        #ax.set_yscale('log')
        ax.set_ylim(0, 250)
    
    # Save and show plot
    print("--------")
    print(options.out)
    plt.tight_layout()
    plt.savefig(options.out)
    plt.show()
