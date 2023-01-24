# import statements
import pandas as pd
import numpy as np
import datetime


# functions

def csv_parse(csv_file):

    # read in csv file
    df = pd.read_csv(csv_file)
    return df

def header_reconstruct(header, ontology_terms, units, value_type):
    '''
    reconstruct the header of the csv file
    params: header, ontology_terms, units, value_type
    return: reconstructed header
    '''
    new_header = []
    for i in range(len(header)):
        if units[i] == 'None':
            new_header.append(header[i],ontology_terms[i])
        else:
            new_header.append(header[i], ontology_terms[i])
            new_header.append(units[i])
            new_header.append()
    return new_header

def csv_convert(df):
    '''
    convert csv file to numpy array
    params: pandas dataframe of the input csv file
    return: dictionaries of numpy arrays
    '''

    # check if units exist, if so save all units into a list
    
    units = df.iloc[0].tolist()

    # get ontology terms as list in column headers
    ontology_terms = df.iloc[1].tolist()

    # save header as a list
    header = df.iloc[2].tolist()

    df = df.iloc[1:].reset_index(drop=True)
    col_names = df.columns

    # get the row names
    row_names = df.iloc[:,0].values
    individual_ids = row_names

    # generate uniqid as the exact time stamp
    uniqids = []
    for id in individual_ids:
        uniqid = id + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        uniqids.append(uniqid)

    # recontruct the dataframe
    recon_df = pd.DataFrame()
    new header 


    
def csv_save(np_array, csv_file):
    # save numpy array to csv file
    
    np.savetxt(csv_file, np_array, delimiter = ',')
    return

# main
if __name__ == "__main__":

    file = 'C:\\Users\\z370170\\Projects\\TWOC\\TWOCdemonstrator\\tool\\test_data\\TWOC-phenotypes.csv'
    # read in csv file
    df = csv_parse(file)
    
    # convert csv file to numpy array
    np_array = csv_convert(df)
    
    # save numpy array to csv file
    csv_save(np_array, '')