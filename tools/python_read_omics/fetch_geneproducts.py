''' usage: python fetch_geneproducts.py WP5039 pathway.csv 
'''
import sys
import csv
from SPARQLWrapper import SPARQLWrapper, JSON

def fetch_gene_products(endpoint_url, pathway_id):
    query = f"""
    PREFIX wp: <http://vocabularies.wikipathways.org/wp#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    
    SELECT DISTINCT ?identifier WHERE {{
        ?geneProduct dcterms:isPartOf ?pathway .
        ?pathway dcterms:identifier "{pathway_id}" . 
        ?geneProduct dc:identifier ?identifier .
    }}
    """
    
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    identifiers = []
    for result in results["results"]["bindings"]:
        identifier = result["identifier"]["value"]
        formatted_identifier = identifier.split('/')[-1]  # Extract the value after the last '/'
        identifiers.append(formatted_identifier)

    return identifiers

def save_to_csv(identifiers, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Identifier'])  # Header
        for identifier in identifiers:
            writer.writerow([identifier])

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <PATHWAY_ID> <OUTPUT_CSV_FILE>")
        sys.exit(1)
    
    pathway_id = sys.argv[1]
    output_file = sys.argv[2]
    endpoint_url = "https://sparql.wikipathways.org/sparql"

    identifiers = fetch_gene_products(endpoint_url, pathway_id)
    save_to_csv(identifiers, output_file)
