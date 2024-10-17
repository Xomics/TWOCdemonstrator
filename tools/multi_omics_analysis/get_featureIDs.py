# get_featureIDs.py

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

def get_ID(in_file, ID_column, out_file):
    omics_df = pd.read_csv(in_file)
    IDs = omics_df[ID_column]
    IDs.to_csv(out_file, sep='\t', header=False)

def run_script(omics_metadata_url, ID_column, out_file):
    input_file = download_file(omics_metadata_url, 'input_file.csv')
    get_ID(input_file, ID_column, out_file)
    print(f"IDs saved to {out_file}")

if __name__ == '__main__':
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser(description='Get IDs from omics file')
        parser.add_argument('-i', '--input_file', required=True, help='URL to the input csv file containing omics metadata')
        parser.add_argument('-c', '--column_name', required=True, help='Name of the ID column in the metadata file')
        parser.add_argument('-o', '--output_file', required=True, help='Output file to save the tsv file with IDs')
        return parser.parse_args()

    args = parse_args()
    run_script(args.input_file, args.column_name, args.output_file)


  