

# import statements
import pandas as pd
import numpy as np


# functions

def csv_parse(csv_file):

    # read in csv file
    df = pd.read_csv(csv_file)
    return df

def csv_convert(df):
    '''
    convert csv file to numpy array
    params: pandas dataframe of the input csv file
    return: dictionaries of numpy arrays
    '''

    # get the column names, skip first row as they are ontoloy terms
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    col_names = df.columns
    
    
    # get number of columns
    num_cols = len(col_names)
    
    # get number of rows
    num_rows = len(df.index)
    
    # create numpy array
    np_array = np.zeros((num_rows, num_cols))
    
    # fill numpy array
    for i in range(num_cols):
        np_array[:, i] = df[col_names[i]]
    return np_array

def csv_save(np_array, csv_file):
    # save numpy array to csv file
    
    np.savetxt(csv_file, np_array, delimiter = ',')
    return

# main
if __name__ == "__main__":

    file = 'C:\Users\z370170\Projects\TWOC\TWOCdemonstrator\tool\test_data\TWOC-phenotypes.csv'
    # read in csv file
    df = csv_parse(file)
    
    # convert csv file to numpy array
    np_array = csv_convert(df)
    
    # save numpy array to csv file
    csv_save(np_array, '')