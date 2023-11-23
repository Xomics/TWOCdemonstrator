# import statements

import sys
import re

from rdflib import Graph, URIRef

from optparse import OptionParser


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

	usage = "usage: %prog -q my_query -s my_FDP -o report.txt"
	required=["query", "service"]
	parser = OptionParser(usage)
	parser.add_option('-q', '--query',
		              dest="query", 
					  help="script with your SPARQL query. [required]",
					  default=None
					  )
	parser.add_option('-s', '--service',
		              dest="service", 
					  help="link to the SPARQL end-point service. [required]",
					  default=None
					  )
	parser.add_option('-o', '--output',
		              dest="output", 
					  help="report file name with SPARQL query results. [optional]",
					  default="report.txt"
					  )
	parser.add_option('-e', '--example',
		              dest="example", 
					  help="start an example run. [example]",
		              default=False,
		              action="store_true"
		              )
	parser.add_option('-v', '--verbose',
		              dest="verbose", 
					  help="run with verbose. [optional]",
		              default=False,
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
		print( '# >Query:', options.query)
		print( '# >Outfile:', options.output)
		print( '# >Endpoint:', options.service)
		print( '# VERBOSE:', options.verbose )
		verbose = options.verbose
	else:
		verbose = False
	return options


# functions

def read_query(query, service):

	with open(query, 'r') as infile:
		data = infile.read()
		qin = data
	
	# WHERE { SERVICE <https://dbpedia.org/sparql> {
	if( service != 'none' ):
	
		if( 'SERVICE' not in qin.upper() ):
		
			print('# ERROR : No `SERVICE` keyword was found in your query, please check your script !')
			exit()
			
		elif( qin.upper().count('SERVICE') > 1):
		
			print('# ERROR : Your query countains multiple instances of the the `SERVICE` keyword !')
			exit()
		
		elif( not re.search( ('SERVICE.*\<.*\>' ), qin, flags=re.IGNORECASE ) ):
			
			print('# ERROR : Your query should countain the `SERVICE` keyword in the following format, e.g., SERVICE <https://dbpedia.org/sparql>')
			exit()
		
		else :
		
			qin = re.sub( 'SERVICE.*\<.*\>', ('SERVICE <' + service + '>'), qin, flags=re.IGNORECASE )
			
	else :
	
		if( 'SERVICE' not in qin.upper() ):
		
			print('# WARNING : No SPARQL end-point service was selected, nor did we find one in your query, please check if this is intended !')
			
		else : 
		
			print('# WARNING : No SPARQL end-point service was selected, please check if this is intended !')
		
	return qin


def sparql_query_to_file(q, output):
	"""
    function to query a sparql endpoint and save the results to a file

    params:
        q(str): sparql query
            The endpoint needs to be specified in the query 
            with SERVICE <endpoint> { ... }
        filename(str): name of the file to save the results to
    """

	fdp_g = Graph()
	# print('#EMPTY GRAPH', fdp_g)
	
#		fdp_g.parse(
#		data=
#		"""
#			<x:> a <c:> .
#			<y:> a <c:> .
#		""",
#		format="turtle"
#	)

	qres = fdp_g.query(q)
	# print('#FILLED GRAPH', qres)
	
#	qres = fdp_g.query(
#		"""
#		SELECT ?s
#		WHERE {
#		  SERVICE <https://dbpedia.org/sparql> {
#			?s a ?o .
#		  }
#		}
#		LIMIT 3
#		"""
#	)

	with open(output, 'w') as outfile:
	
		if qres:
			for row in qres:
				print(row.s) # prints to screen
				outfile.write(row.s + "\n") # prints to file
			
		else: outfile.write("# no results were returned .. ") # I'm not sure if qres can be empty, but just in case ..


# main

if __name__ == '__main__':

	print('# running script:', input, '\n')
	
	options = parse_args()

	qin = read_query(options.query, options.service)

	print('\n# QUERY:\n',qin,'\n') # SET TO VERBOSE ONLY !

	sparql_query_to_file(qin, options.output)

	