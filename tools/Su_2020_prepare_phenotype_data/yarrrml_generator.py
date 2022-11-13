# import statements
import pandas as pd
import numpy as np


# functions

def read_csv(csv_file):
    # read in csv file
    df = pd.read_csv(csv_file)
    return df

def write_yarrrml(yarrrml, df):
    with open(yarrrml, 'w') as file:
        file.write('prefixes:')
        file.write('  - rml: http://semweb.mmlab.be/ns/rml#')
        file.write('  - ql: http://semweb.mmlab.be/ns/ql#')
        file.write('  - rr: http://www.w3.org/ns/r2rml#')
        file.write('  - xsd: http://www.w3.org/2001/XMLSchema#')
        file.write('  - rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        file.write('  - rdfs: http://www.w3.org/2000/01/rdf-schema#')
        file.write('  - foaf: http://xmlns.com/foaf/0.1/')
        file.write('  - schema: http://schema.org/')
        file.write('  - dcterms: http://purl.org/dc/terms/')
        file.write('  - dct: http://purl.org/dc/terms/')
        file.write('  - skos: http://www.w3.org/2004/02/skos/core#')
        file.write('  - owl: http://www.w3.org/2002/07/owl#')
        file.write('  - dc: http://purl.org/dc/elements/1.1/')
        file.write('  - dcat: http://www.w3.org/ns/dcat#')
        file.write('  - void: http://rdfs.org/ns/void#')
        file.write('  - prov: http://www.w3.org/ns/prov#')
        file.write('  - qb: http://purl.org/linked-data/cube#')
    return

# main
if __name__ == "__main__":
    file = 'phenotype_data.csv'
    yarrrml = 'yarrrml.yml'
    write_yarrrml(yarrrml, read_csv(file))

