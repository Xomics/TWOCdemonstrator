


# import statements
from os import path
import json

from rdflib import Graph, Namespace

from isatools import isatab
from isatools.model import set_context


# functions
def load_isa(isa_file):
    '''Reading and loading an ISA Investigation
    in memory from an ISA-JSON instance

        param isa_json_file: ISA-JSON file
        return: ISA Investigation object
    '''
    with open(isa_file, 'r') as f:
        investigation = isatab.load(f)
    return investigation

def create_rdf_graph(investigation):
    '''Creating an RDF graph from an ISA Investigation
    '''
    set_context(vocab='wdt', all_in_one=False, local=False)
    set_context(vocab='obo', all_in_one=False, local=False)
#    set_context(vocab='sdo', all_in_one=False, local=False)

    ld = investigation.to_dict(ld=True)
    # Creating the namespace
    WDT = Namespace("http://www.wikidata.org/wiki/")
    WDTP = Namespace('https://www.wikidata.org/wiki/Property:')
    ISA = Namespace('https://isa.org/')
    OBO = Namespace('http://purl.obolibrary.org/obo/')


    ld_string = json.dumps(ld) # Get a string representation of the ld variable
    graph = Graph() # Create an empty graph
    graph.parse(data=ld_string, format='json-ld') # Load the data into the graph

    # Finally, bind the namespaces to the graph
    graph.bind('wdt', WDT)
    graph.bind('isa', ISA)
    graph.bind('wdtp', WDTP)
    graph.bind('obo', OBO)
    return graph


def main(file):
    investigation = load_isa(file)
    graph = create_rdf_graph(investigation)
    graph.serialize(destination='../../data/Su_2020_FAIR/isa.ttl', format='turtle')
    return

# main
if __name__ == '__main__':
    isajson_file = '../../data/Su_2020_FAIR/isa.json'
    isa_tab_file = '../../data/Su_2020_FAIR/i_investigation.txt'
    main(isa_tab_file)
