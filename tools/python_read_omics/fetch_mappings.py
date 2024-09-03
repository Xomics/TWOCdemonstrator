# fetch_mappings.py

import requests
import pandas as pd
from bridgedb_script import get_mappings

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def run_script(pathwayids_file_url, id_file_url, meta_file_url, source, output_file):
    # Download input files
    pathway_file = download_file(pathwayids_file_url, 'pathwayids_file.csv')
    input_file = download_file(id_file_url, 'input_file.tsv')
    meta_file = download_file(meta_file_url, 'meta_file.csv')

    # Read in the pathway file
    path_members = pd.read_csv(pathway_file)
    path_identifiers = path_members.Identifier.to_list()

    # Get mappings for IDs from BridgeDb
    mappings_df = get_mappings(input_file, "Homo sapiens", source=source, case=1)

    # Get features in the pathway
    omics_in_path = mappings_df[mappings_df['mapping'].isin(path_identifiers)]

    # Read Metadata file
    meta_df = pd.read_csv(meta_file)

    # Merge the mappings to the metadata dataframe
    mapped_omics = meta_df.merge(omics_in_path, left_on='database.ID', right_on='original', how='left')
    mapped_omics.dropna(inplace=True)
    mapped_omics = mapped_omics.drop_duplicates(subset='feature.name')

    # Save the filtered mappings to a CSV file 
    mapped_omics.to_csv(output_file, index=False)

    print(f"Mapped data saved to {output_file}")

if __name__ == '__main__':
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser(description='Fetch mappings from BridgeDb.')
        parser.add_argument('-p', '--pathwayids_file', required=True, help='URL to the Pathway Identifier file')
        parser.add_argument('-i', '--id_file', required=True, help='URL to the input tsv file containing omics IDs')
        parser.add_argument('-m', '--meta_file', required=True, help='URL to the feature metadata file')
        parser.add_argument('-s', '--source', required=True, help='Source database code')
        parser.add_argument('-o', '--output_file', required=True, help='Output file to save the mapped DataFrame')
        return parser.parse_args()

    args = parse_args()
    run_script(args.pathwayids_file, args.id_file, args.meta_file, args.source, args.output_file)
