''' usage:  python get_path_members.py -p https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/pathway.tsv -m https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/proteomics/mapped_proteomics.csv
'''

import argparse
import pandas as pd
import requests

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

def find_common_features(pathway_file, metadata_file):
    # Read the input files
    pathway_df = pd.read_csv(pathway_file, sep='\t')
    metadata_df = pd.read_csv(metadata_file)


    # Drop rows without Ensembl ID in pathway_df and format the Ensembl ID column
    pathway_df = pathway_df.dropna(subset=['Ensembl']).copy()
    pathway_df['Ensembl'] = pathway_df['Ensembl'].str.replace('ensembl:', '', regex=False)
    

    # Find common IDs between pathway_df and metadata_df
    meta_ids = metadata_df['mapping']
    pathway_ids = pathway_df['Ensembl']
    common_ids = pd.Series(list(set(meta_ids) & set(pathway_ids)))

    # Extract the common IDs from metadata_df
    ids_in_pathway = metadata_df[metadata_df['mapping'].isin(common_ids)]

    # Create a list of unique features for further analysis
    feature_list = list(set(ids_in_pathway['feature.name']))
    return feature_list

def main():
    parser = argparse.ArgumentParser(description='Find common features between pathway and metadata files.')
    parser.add_argument('-p', '--pathway_file', required=True, help='URL to the pathway file (TSV)')
    parser.add_argument('-m', '--metadata_file', required=True, help='URL to the metadata file (CSV)')
    
    args = parser.parse_args()

    # Download the files
    pathway_file = download_file(args.pathway_file, 'pathway_file.tsv')
    metadata_file = download_file(args.metadata_file, 'metadata_file.csv')
    
    feature_list = find_common_features(pathway_file, metadata_file)
    feature_list = [element.replace('_HUMAN', '') for element in feature_list]
    print(feature_list)

if __name__ == '__main__':
    main()