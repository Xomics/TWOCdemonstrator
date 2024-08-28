''' python merge_omics.py -p https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/proteomics/mapped_proteomics.csv
 -t https://raw.githubusercontent.com/Xomics/TWOCdemonstrator/main/data/Su_2020_FAIR/transcriptomics/mapped_transcriptomics.csv -o merged_omics.csv
'''

import pandas as pd
import argparse
import requests

def parse_args():
    """
    Parse CLI options.
    
    Returns:
    -------
    Namespace
        User CLI options
    """
    parser = argparse.ArgumentParser(description='Get IDs from omics file')
    parser.add_argument('-p', '--proteomics_file', required=True, help='URL to the mapped protoemics file')
    parser.add_argument('-t', '--transcriptomics_file', required=True, help='URL to the mapped transcriptomics file')
    parser.add_argument('-o', '--output_file', required=True, help='Output file to save common features')
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

def main():
    args = parse_args()
    
    proteomics_file_url= args.proteomics_file
    trancriptomics_file_url= args.transcriptomics_file

    # Download input files
    proteomics_file = download_file(proteomics_file_url, 'proteomics_file.tsv')
    transcriptomics_file = download_file(trancriptomics_file_url, 'transcriptomics_file.csv')

    prot_features = pd.read_csv(proteomics_file)
    trans_features = pd.read_csv(transcriptomics_file)

    common_features = pd.merge(prot_features, trans_features, on='mapping', suffixes=('_prot', '_trans'))
    common_features = common_features[['feature.name_prot', 'feature.name_trans', 'mapping' ]]
    common_features.to_csv(args.output_file, index=False)

if __name__ == '__main__':
    main()
    