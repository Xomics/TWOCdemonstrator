


# import statements
from os import path
import json

from rdflib import Graph, Namespace, URIRef
import pprint

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
    set_context(vocab='wd', local=False, prepend_url='https://fdp.cmbi.umcn.nl/', all_in_one=False)
    #set_context(vocab='obo', all_in_one=False, local=False)
    #set_context(vocab='sdo', all_in_one=False, local=False)

    ld = investigation.to_dict(ld=True)
    
    print()
    print("---------------------------------")
    print("ld")
    print(ld)
    print("---------------------------------")
    print()
    # Creating the namespace
    WD = Namespace("http://www.wikidata.org/entity/")
    ISA = Namespace('https://isa.org/')
    OBO = Namespace('http://purl.obolibrary.org/obo/')


    ld_string = json.dumps(ld) # Get a string representation of the ld variable
    print()
    print("---------------------------------")
    print("ld_string")
    print(ld_string)
    print("---------------------------------")
    print()
    
    graph = Graph() # Create an empty graph
    
    graph.parse(data=ld_string, format='json-ld',publicID="http://xomics") # Load the data into the graph
    for stmt in graph:
        pprint.pprint(stmt)
    # Finally, bind the namespaces to the graph
    graph.bind('wdt', WD)
    graph.bind('isa', ISA)
    graph.bind('obo', OBO)
    #for stmt in graph:
    #    pprint.pprint(stmt)
    return graph

def re_base_uri():
    g = Graph()
    g.load(r'../../data/Su_2020_FAIR/isa.ttl', format='turtle')

    # Define the old and new base URIs
    old_base_uri = 'file:///D:/CMBI_work/Projects/TWOCdemonstrator/tools/Su_2020_prepare_ISA_metadata'
    new_base_uri = 'https://github.com/Xomics/TWOCdemonstrator/blob/main/data/Su_2020_FAIR/isa.ttl'

    # Iterate through the triples and update the base URI
    for s, p, o in g:
        if str(s).startswith(old_base_uri):
            g.remove((s, p, o))
            g.add((URIRef(str(s).replace(old_base_uri, new_base_uri)), p, o))
        if str(o).startswith(old_base_uri):
            g.remove((s, p, o))
            g.add((s, p, URIRef(str(o).replace(old_base_uri, new_base_uri))))

    # Save the updated RDF file
    g.serialize(destination='../../data/Su_2020_FAIR/isa_new.ttl', format='turtle')
    return

def main(file):
    investigation = load_isa(file)
    '''
    print()
    print("---------------------------------")
    print("investigation")
    print(investigation)
    print("---------------------------------")
    print()
    
    print()
    print("---------------------------------")
    print("Study")
    print(investigation.studies[0])
    print("---------------------------------")
    print()
    
    print()
    print("---------------------------------")
    print("Contacts")
    print(investigation.studies[0].contacts[0])
    print(investigation.studies[0].contacts[1])
    print("---------------------------------")
    print()
    print()
    print("---------------------------------")
    print("protocols")
    print(investigation.studies[0].protocols[0])
    print("parameters")
    print(investigation.studies[0].protocols[0].parameters[0])
    print(investigation.studies[0].protocols[1])
    print("parameters")
    print(investigation.studies[0].protocols[1].parameters[0])
    print(investigation.studies[0].protocols[1].parameters[1])
    print(investigation.studies[0].protocols[2])
    print(investigation.studies[0].protocols[3])
    print(investigation.studies[0].protocols[4])
    print(investigation.studies[0].protocols[5])
    print(investigation.studies[0].protocols[6])
    print(investigation.studies[0].protocols[7])
    print(investigation.studies[0].protocols[8])
    print(investigation.studies[0].protocols[9])
    print(investigation.studies[0].protocols[10])
    print(investigation.studies[0].protocols[11])
    print(investigation.studies[0].protocols[12])
    print(investigation.studies[0].protocols[13])
    print("---------------------------------")
    print()
    print()
    print("---------------------------------")
    print("assays")
    print(investigation.studies[0].assays[0])
    print("assays-data files")
    print(investigation.studies[0].assays[0].data_files[0])
    print(investigation.studies[0].assays[0].data_files[1])    
    print(investigation.studies[0].assays[1])
    print(investigation.studies[0].assays[2])
    print("---------------------------------")
    print()

    
    
    print(investigation.studies[0].assays[1])
    print(investigation.studies[0].assays[2])
    print("---------------------------------")
    print()
    '''
    
    graph = create_rdf_graph(investigation)
    #for stmt in graph:
    #    pprint.pprint(stmt)
    graph.serialize(destination='../../data/Su_2020_FAIR/isa-14.ttl', format='turtle')
    #re_base_uri()
    return

# main
if __name__ == '__main__':
    isajson_file = '../../data/Su_2020_FAIR/isa.json'
    #isa_tab_file = '../../data/Su_2020_FAIR/i_investigation.txt'
    #for UMD
    isa_tab_file = '/Users/junda-radboudumc/Radboudumc_projects/UMD-ISA-Collaboration/ISA_files/i_Investigation.txt'
    main(isa_tab_file)
