import json
import numpy as np
import matplotlib.pyplot as plt
import requests
from functions import *

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def calculate_iqr_limits(data):
    quatile1 = np.percentile(data, 25)
    quatile3 = np.percentile(data, 75)
    iqr = quatile3 - quatile1
    lower_limit = quatile1 - 1.5 * iqr
    upper_limit = quatile3 + 1.5 * iqr
    return lower_limit, upper_limit

def run_script(omics_file_url, samples_file_url, feature, output_file):
    # Download the files from the provided URLs
    omics_file = download_file(omics_file_url, 'omics_data.csv')
    samples_file = download_file(samples_file_url, 'samples.json')

    # Get feature data file and read it as a dataframe
    df = read_omics_data(omics_file)
    # Create an empty list and append the desired feature
    features_list = [feature]

    # Load the sample list from the JSON file
    with open(samples_file, 'r') as f:
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

        # Append the data to the list for boxplots
        data_for_boxplot.append(df_subset.values.flatten())
        labels.append(group)

        # Collect all values for IQR calculation
        all_values.extend(df_subset.values.flatten())

    # Calculate IQR limits for all values
    lower_limit, upper_limit = calculate_iqr_limits(all_values)

    # Plot the boxplot
    fig = plt.figure(figsize=(15, 10))
    plt.ylabel(str(feature))
    plt.boxplot(data_for_boxplot, labels=labels)

    # Adjust the y-axis limit based on IQR
    plt.ylim(lower_limit, upper_limit)

    # Save and show plot
    plt.savefig(output_file)
    plt.show()

    print(f"Results saved to {output_file}")

if __name__ == '__main__':
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser(description='Analyze omics data')
        parser.add_argument('-i', '--omics', required=True, help='URL to omics-feature-data file (csv)')
        parser.add_argument('-s', '--samples', required=True, help='URL to sample list JSON file')
        parser.add_argument('-f', '--feature', required=True, help='Feature of Interest')
        parser.add_argument('-o', '--out', required=True, help='Output file to save the results')
        return parser.parse_args()

    args = parse_args()
    run_script(args.omics, args.samples, args.feature, args.out)
