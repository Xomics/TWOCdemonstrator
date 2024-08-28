''' usage:  python fetch_mappings.py -i https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/proteomics/proteomics_IDS.tsv 
-p https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/pathway_IDs.csv
-m https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/proteomics/proteomics_Su_2020_feature-metadata.csv -s S -o output_mapped.csv
'''

import requests
import argparse
import pandas as pd

from bridgedb_script import get_mappings

url = "https://webservice.bridgedb.org/"
batch_request = url+"{org}/xrefsBatch/{source}{}"
org = 'Homo sapiens'

def parse_args():
    """
    Parse CLI options.
    
    Returns:
    -------
    Namespace
        User CLI options
    """
    parser = argparse.ArgumentParser(description='Fetch mappings from BridgeDb.')
    parser.add_argument('-p', '--pathwayids_file', required=True, help='URL to the Pathway Identifier file')
    parser.add_argument('-i', '--id_file', required=True, help='URL to the input tsv file containing omics IDs')
    parser.add_argument('-m', '--meta_file', required=True, help='URL to the feature metadata file')
    parser.add_argument('-s', '--source', required=True, help='Source database code')
    parser.add_argument('-o', '--output_file', required=True, help='Output file to save the mapped DataFrame')
    return parser.parse_args()

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

def check_mapping_supported(org, source, target, url):
    mapping_available = f"{org}/isMappingSupported/{source}/{target}"
    query = url + mapping_available.format(org=org, source=source, target=target)
    response = requests.get(query)
    return response.text

def main():
    args = parse_args()
    
    pathwayids_file_url= args.pathwayids_file
    id_file_url = args.id_file
    meta_file_url = args.meta_file
    source = args.source
    output_file = args.output_file

    # Download input files
    pathway_file = download_file(pathwayids_file_url, 'pathwayids_file.csv')
    input_file = download_file(id_file_url, 'input_file.tsv')
    meta_file = download_file(meta_file_url, 'meta_file.csv')
    

    # read in the pathway file
    path_members = pd.read_csv(pathway_file)
    path_identifiers = path_members.Identifier.to_list()
    
    # Get mappings for IDs from BridgeDb
    mappings_df = get_mappings(input_file, "Homo sapiens", source = source, case=1)

    # Get features in the pathway
    omics_in_path = mappings_df[mappings_df['mapping'].isin(path_identifiers )]

    # Read Metadata file
    meta_df = pd.read_csv(meta_file)

    # merge the mappings to the metadata dataframe
    mapped_omics = meta_df.merge(omics_in_path, left_on='database.ID', right_on='original', how='left')
    mapped_omics.dropna(inplace = True)
    mapped_omics = mapped_omics.drop_duplicates(subset='feature.name')

    # Save the filtered mappings to a CSV file 
    mapped_omics.to_csv(args.output_file, index=False)
    
    print(f"Mapped data saved to {output_file}")

if __name__ == '__main__':
    main()
