''' usage:  python get_path_members.py -p /path/to/pathwayfile.tsv -m /path/to/mapped_metadata.csv
'''

import argparse
import pandas as pd

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
    feature_list = list(set(ids_in_pathway['database.ID']))
    return feature_list

def main():
    parser = argparse.ArgumentParser(description='Find common features between pathway and metadata files.')
    parser.add_argument('-p', '--pathway_file', required=True, help='Pathway file (TSV)')
    parser.add_argument('-m', '--metadata_file', required=True, help='Metadata file (CSV)')
    
    args = parser.parse_args()
    
    feature_list = find_common_features(args.pathway_file, args.metadata_file)
    feature_list = [element.replace('_HUMAN', '') for element in feature_list]
    print(feature_list)

if __name__ == '__main__':
    main()