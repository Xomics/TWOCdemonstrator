# import statements

import sys
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

from functions import *


# argument values

input = sys.argv

def parse_args():
	"""
    Parse CLI options.

    Returns
    -------
    dict
        User CLI options

    """

	usage = "usage: python3 analyze.py \
        -i[--omics] mypath/transcriptomics_Su_2020_feature-data.csv \
        -m[--meta] mypath/transcriptomics_Su_2020_feature-metadata.csv \
        -s[--samples] sample_list.txt \
        -f[--feature] IL6 \
        -o[--out] results.md"
	required=["omics", "meta","samples","feature"]
	parser = OptionParser(usage)
	parser.add_option('-i', '--omics',
		              dest="omics", 
					  help="feature-data file(csv). [required]",
					  default="..\\..\\data\\Su_2020_FAIR\\transcriptomics\\transcriptomics_Su_2020_feature-data.csv"
					  )
	parser.add_option('-m', '--meta',
		              dest="meta", 
					  help="feature-metadata file(csv). [required]",
					  default="..\\..\\data\\Su_2020_FAIR\\transcriptomics\\transcriptomics_Su_2020_feature-metadata.csv"
					  )
	parser.add_option('-s', '--samples',
		              dest="samples", 
					  help="sample list. [required]",
					  default="sample_list_hosp.txt"
					  )
	parser.add_option('-f', '--feature',
		              dest="feature", 
					  help="IL6 [IL6]",
		              default="IL6"
		              #action="store_true"
		              )
	parser.add_option('-o', '--out',
		              dest="out", 
					  help="results [optional]",
		              default="results.md"
		              #action="store_true"
		              )
	parser.add_option('-v', '--verbose',
		              dest="verbose", 
					  help="run with verbose. [optional]",
		              default=True,
		              action="store_true"
		              )
	options, args = parser.parse_args()
	for r in required:
		if options.__dict__[r] is None:
			parser.print_help()
			parser.error("parameter '%s' is required !"%r)
			sys.exit(1)
			
	if options.verbose:
		print( '# STARTING SERVICE\n' )
		print( '# Your input arguments are:' )
		print( '# >omics:', options.omics)
		print( '# >meta:', options.meta)
		print( '# >samples:', options.samples)
		print( '# >feature:', options.feature)
		print( '# VERBOSE:', options.verbose )
		verbose = options.verbose
	else:
		verbose = False
	return options


# functions




# main

if __name__ == '__main__':

	print('# running script:', input, '\n')
	
	options = parse_args()
	transcriptomics_feature_data = options.omics
	df = read_omics_data(transcriptomics_feature_data)
	features_list = list()
	features_list.append(options.feature)
	sample_list = []
	with open(options.samples) as f:
		next(f)
		for line in f:
			sample_list.append(line.strip())
		#sample_list = f.read().splitlines().strip()
	df_subset = subset_omics_data(df, feature_list=features_list, sample_list=sample_list)
	fig = plt.figure(figsize =(15, 10))
    # Creating plot
	plt.ylabel("IL6")
	plt.yscale('log')
	plt.boxplot(df_subset.T,labels=["Covid Not in ICU"])
    # show plot
	plt.show()