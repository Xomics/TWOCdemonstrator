''' usage:  python fetch_mappings.py -i /path/to/proteo_IDS.tsv -m /path/to/proteomics_feature_metadata.csv -c 'Uniprot_ID' -s S -t En -o /path/to/output_mapped.csv
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
    parser.add_argument('-i', '--input_file', required=True, help='Path to the input tsv file containing IDs')
    parser.add_argument('-m', '--meta_file', required=True, help='Proteomics feature metadata file')
    parser.add_argument('-c', '--column_name', required=True, help='Name of the ID column in the metadata file')
    parser.add_argument('-s', '--source', required=True, help='Source database code')
    parser.add_argument('-t', '--target', required=True, help='Target database code')
    parser.add_argument('-o', '--output_file', required=True, help='Output file to save the mapped DataFrame')
    return parser.parse_args()

def check_mapping_supported(org, source, target, url):
    mapping_available = f"{org}/isMappingSupported/{source}/{target}"
    query = url + mapping_available.format(org=org, source=source, target=target)
    response = requests.get(query)
    return response.text

def main():
    args = parse_args()
    
    input_file = args.input_file
    meta_file = args.meta_file
    source = args.source
    target = args.target
    output_file = args.output_file
    ID_column = args.column_name
    
    # Check if the mapping type required is available
    print("Checking if mapping is supported...")
    if check_mapping_supported(org, source, target, url) == 'true':
        print("Mapping is supported, proceeding with mapping...")
    else:
        print("Mapping is not supported between source and target databases.")
    
    # Get mappings for IDs from BridgeDb
    mappings_df = get_mappings(input_file, "Homo sapiens", source = source, case=1, target=target)
    print(mappings_df)

    # Filter the mappings for the desired target DB
    mappings_df = mappings_df[mappings_df['target'] == target]
    

    # Read Metadata file
    meta_df = pd.read_csv(meta_file)
    print(meta_df)

    # merge the mappings to the metadata dataframe
    final_proteo_mapped = meta_df.merge(mappings_df, left_on=ID_column, right_on='original', how='left')

    # Save the filtered mappings to a CSV file 
    final_proteo_mapped.to_csv(args.output_file, index=False)
    
    print(f"Mapped data saved to {output_file}")

if __name__ == '__main__':
    main()
