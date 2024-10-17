import sys
import json
import argparse
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
    Parse CLI args.

    Returns
    -------
    dict
        User CLI args
    """
    usage = "usage: python3 analyze.py \
        -i[--omics] https://raw.githubusercontent.com/user/repo/branch/path/to/transcriptomics_Su_2020_feature-data.csv \
        -s[--samples] https://raw.githubusercontent.com/user/repo/branch/path/to/samples_dict.json \
        -f[--feature] IL6 \
        -o[--out] results.png"
    required=["omics","samples","feature"]
    parser = argparse.ArgumentParser(usage)
    parser.add_argument('-i', '--omics',
                      dest="omics", 
                      help="transcriptomics-feature-data file(csv). [required]",
                      )
    parser.add_argument('-s', '--samples',
                      dest="samples", 
                      help="sample list JSON file. [required]",
                      )
    parser.add_argument('-f', '--feature',
                      dest="feature", 
                      help="Feature of Interest",
                      )
    parser.add_argument('-o', '--out',
                      dest="out", 
                      help="results [optional]",
                      default="results.png"
                      )
    parser.add_argument('-v', '--verbose',
                      dest="verbose", 
                      help="run with verbose. [optional]",
                      default=True,
                      action="store_true"
                      )
    args = parser.parse_args()
    for r in required:
        if args.__dict__[r] is None:
            parser.print_help()
            parser.error("parameter '%s' is required !" % r)
            sys.exit(1)
            
    if args.verbose:
        print( '# STARTING SERVICE\n' )
        print( '# Your input arguments are:' )
        print( '# >omics:', args.omics)
        print( '# >samples:', args.samples)
        print( '# >feature:', args.feature)
        print( '# VERBOSE:', args.verbose )
        verbose = args.verbose
    else:
        verbose = False
    return args

def calculate_iqr_limits(data):
    """
    Calculate the IQR-based limits for data to ignore outliers.
    
    Parameters:
    ----------
    data : array-like
        The data to calculate limits for.
    
    Returns:
    -------
    float
        Lower limit.
    float
        Upper limit.
    """
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    return lower_limit, upper_limit

# Main
if __name__ == '__main__':
    print('# running script:', input, '\n')
    
    args = parse_args()

    # Download the files from the provided URLs
    local_omics_file = download_file(args.omics, 'omics_data.csv')
    local_samples_file = download_file(args.samples, 'samples.json')

    # Get feature data file and read it as a dataframe
    df = read_omics_data(local_omics_file)
    # Create an empty list and append the desired feature
    features_list = [args.feature]
    
    # Load the sample list from the JSON file
    with open(local_samples_file, 'r') as f:
        samples_dict = json.load(f)
    
    # Create a list to store data for boxplots
    data_for_boxplot = []
    labels = []
    all_values = []

    for group, sample_list in samples_dict.items():
        # Check for missing sample IDs
        missing_samples = [sample for sample in sample_list if sample not in df.columns]
        if missing_samples:
            print(f"Warning: The following samples from group '{group}' are not found in the dataframe: {missing_samples}")
        
        # Filter out missing sample IDs
        valid_samples = [sample for sample in sample_list if sample in df.columns]
        
        if not valid_samples:
            print(f"No valid samples found for group '{group}', skipping this group.")
            continue
        
        # Get values for the feature of interest for the valid samples
        df_subset = subset_omics_data(df, feature_list=features_list, sample_list=valid_samples)
        print(f'{group} subset:')
        
        # Append the data to the list for boxplots
        data_for_boxplot.append(df_subset.values.flatten())
        labels.append(group)

        # Collect all values for IQR calculation
        all_values.extend(df_subset.values.flatten())

    # Calculate IQR limits for all values
    lower_limit, upper_limit = calculate_iqr_limits(all_values)

    # Plot the boxplot
    fig = plt.figure(figsize=(15, 10))
    plt.ylabel(str(args.feature))
    plt.boxplot(data_for_boxplot, labels=labels)
    
    # Automatically adjust the y-axis limit based on IQR
    plt.ylim(lower_limit, upper_limit)
    

    # Save and show plot
    print("--------")
    print(args.out)
    plt.savefig(args.out)
    plt.show()
