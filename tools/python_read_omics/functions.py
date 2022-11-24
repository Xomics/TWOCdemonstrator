# functions to read omics data and omics feature metadata from tabular files

import pandas as pd

def read_omics_data(file_path):
    """Read omics file into pandas data frame.

    :param file_path: Path to .csv file containing omics data (features in rows,
      samples in columns)
    :return: Omics data
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(file_path, index_col = "feature.name")
    return df

# function to read omics feature metadata file into pandas data frame

# function to create PID from available omics feature metadata
def create_feature_PID(df):
    """Concatenate database ID and database name to generate feature PID.
    
    :param df: Pandas dataframe containing feature metadata
    :rtype: pandas.DataFrame
    """
    for index, row in df.iterrows():
        if df.at[index, 'database'] == "https://www.ebi.ac.uk/chebi/":
            pid = str("http://purl.bioontology.org/ontology/CHEBI/CHEBI:" + str(df.at[index, 'database.ID']))
            df.at[index, 'PID'] = pid
        else :
            pid =  str(df.at[index, 'database']) + str(df.at[index, 'database.ID'])
            df.at[index, 'PID'] = pid    
        
    return df


# subset based on  feature and/or sample IDs
def subset_omics_data(df, **kwargs):
    """Subset omics dataframe on a list of features and/or sample IDs 
    
    :param df: Pandas dataframe containing omics data
    :param feature_list: List object with feature names (strings)
    :param sample_list: List object with sample names (strings)
    :rtype: pandas.DataFrame
    """
    if 'feature_list' in kwargs:
        df = df[df.index.isin(kwargs['feature_list'])]
    if 'sample_list' in kwargs:
        df = df.loc[:,kwargs['sample_list']]
    
    return df  

# calculate mean
def calculate_means(df):
    """Subset omics dataframe on a list of features and/or sample IDs 
    
    :param df: Pandas dataframe containing omics data
    :rtype: Dictionary
    """
    means = df.transpose().mean()
    dictionary = means.to_dict()
    
    return dictionary  


