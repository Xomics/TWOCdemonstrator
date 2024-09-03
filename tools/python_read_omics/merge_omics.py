import pandas as pd
import requests

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def run_script(proteomics_file_url, transcriptomics_file_url, output_file):
    # Download input files
    proteomics_file = download_file(proteomics_file_url, 'proteomics_file.csv')
    transcriptomics_file = download_file(transcriptomics_file_url, 'transcriptomics_file.csv')

    # Read the files
    prot_features = pd.read_csv(proteomics_file)
    trans_features = pd.read_csv(transcriptomics_file)

    # Merge the dataframes on the 'mapping' column
    common_features = pd.merge(prot_features, trans_features, on='mapping', suffixes=('_prot', '_trans'))
    common_features = common_features[['feature.name_prot', 'feature.name_trans', 'mapping']]

    # Save the merged dataframe to a CSV file
    common_features.to_csv(output_file, index=False)

    print(f"Merged data saved to {output_file}")

if __name__ == '__main__':
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser(description='Get IDs from omics file')
        parser.add_argument('-p', '--proteomics_file', required=True, help='URL to the mapped proteomics file')
        parser.add_argument('-t', '--transcriptomics_file', required=True, help='URL to the mapped transcriptomics file')
        parser.add_argument('-o', '--output_file', required=True, help='Output file to save common features')
        return parser.parse_args()

    args = parse_args()
    run_script(args.proteomics_file, args.transcriptomics_file, args.output_file)

    