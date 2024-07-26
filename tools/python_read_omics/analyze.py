''' usage: python analyze.py i- https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/transcriptomics/transcriptomics_Su_2020_feature-data.csv
 -m https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/transcriptomics/transcriptomics_Su_2020_feature-metadata.csv
-s https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/samples_dict.json -f IL10 -o IL10_result.png
'''

import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import requests

from functions import *

# Argument values
input = sys.argv

def download_file(url, local_filename):
    """
    Download a file from a URL and save it locally.
    
    Parameters:
    ----------
    url : str
        URL of the file to download
    local_filename : str
        Local filename to save the downloaded file
    
    Returns:
    -------
    str
        Path to the downloaded file
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def parse_args():
    """
    Parse CLI options.

    Returns
    -------
    dict
        User CLI options
    """
    usage = "usage: python3 analyze.py \
        -i[--omics] https://raw.githubusercontent.com/user/repo/branch/path/to/proteomics_Su_2020_feature-data.csv \
        -m[--meta] https://raw.githubusercontent.com/user/repo/branch/path/to/proteomics_Su_2020_feature-metadata.csv \
        -s[--samples] https://raw.githubusercontent.com/user/repo/branch/path/to/samples_dict.json \
        -f[--feature] IL10 \
        -o[--out] IL10_results.png"
    required=["omics","meta","samples","feature"]
    parser = OptionParser(usage)
    parser.add_option('-i', '--omics',
                      dest="omics", 
                      help="URL to transcriptomics-feature-data file(csv). [required]"
                      )
    parser.add_option('-m', '--meta',
                      dest="meta", 
                      help="URL to feature-metadata file(csv). [required]"
                      )
    parser.add_option('-s', '--samples',
                      dest="samples", 
                      help="URL to sample list JSON file. [required]"
                      )
    parser.add_option('-f', '--feature',
                      dest="feature", 
                      help="Feature of Interest",
                      )
    parser.add_option('-o', '--out',
                      dest="out", 
                      help="results [optional]"
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
        print( '# >feature:', options.feature)
        print( '# VERBOSE:', options.verbose )
        verbose = options.verbose
    else:
        verbose = False
    return options

# Main
if __name__ == '__main__':
    print('# running script:', input, '\n')
    
    options = parse_args()

    # Download the files from the provided URLs
    omics_file = download_file(options.omics, 'omics_data.csv')
    meta_file = download_file(options.meta, 'metadata.csv')
    samples_file = download_file(options.samples, 'samples.json')

    

    # Get feature data file and read it as a dataframe
    #  transcriptomics_feature_data = options.omics
    # Read the omics data using the function 'read_omics_data'
    df = read_omics_data(omics_file)
    print(df.head())

    # Create an empty list and append the desired feature
    features_list = [options.feature]
    #print(features_list)
    
    # Load the sample list from the JSON file
    with open(samples_file, 'r') as f:
        samples_dict = json.load(f)
    print(samples_dict)
    
    # Create a list to store data for boxplots
    data_for_boxplot = []
    labels = []
    
    for group, sample_list in samples_dict.items():
        # Get values for the feature of interest for the samples
        df_subset = subset_omics_data(df, feature_list=features_list, sample_list=sample_list)
        print(f'{group} subset:')
        print(df_subset)
        
        # Append the data to the list for boxplots
        data_for_boxplot.append(df_subset.values.flatten())
        labels.append(group)
    
    # Print data for debugging
    print("Data for boxplot:")
    print(data_for_boxplot)
    print("Labels:")
    print(labels)

    # Plot the boxplot
    fig = plt.figure(figsize=(15, 10))
    plt.ylabel(str(options.feature))
    #plt.yscale('log')
    plt.boxplot(data_for_boxplot, labels=labels)
    plt.ylim(0, 250)
    
    # Save and show plot
    print("--------")
    print(options.out)
    plt.savefig(options.out)
    plt.show()
