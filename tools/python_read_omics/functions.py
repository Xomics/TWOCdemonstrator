# functions to read omics data and omics feature metadata from tabular files

import pandas as pd

# function to read omics file into pandas data frame
# input:
def read_omics_data(file_path):
    df = pd.read_csv(file_path)
    return df

# function to read omics feature metadata file into pandas data frame

# function to create PID from available omics feature metadata

# subset based on sample IDs / feature IDs

# calculate mean


df = read_omics_data("../../data/Su_2020_FAIR/metabolomics/metabolomics_Su_2020_feature-data.csv")
print(df.shape)