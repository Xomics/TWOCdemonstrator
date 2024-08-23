''' usage: python get_pathway.py "https://sparql.wikipathways.org/sparql" WP5039
'''


import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def run_sparql_query(endpoint_url, pathway_id):
    query = f"""
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX wp: <http://vocabularies.wikipathways.org/wp#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT DISTINCT ?pathway (STR(?label) AS ?geneProduct) WHERE {{
        ?geneProduct a wp:GeneProduct . 
        ?geneProduct rdfs:label ?label .
        ?geneProduct dcterms:isPartOf ?pathwayRev .
        ?pathwayRev a wp:Pathway .
        ?pathwayRev dc:identifier ?pathway .
        ?pathwayRev dcterms:identifier "{pathway_id}"
    }}
    """

    # Set up the SPARQL endpoint
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and fetch the results
    results = sparql.query().convert()

    # Print the results
    for result in results["results"]["bindings"]:
        pathway = result["pathway"]["value"]
        geneProduct = result["geneProduct"]["value"]
        print(f"Pathway: {pathway}, Gene Product: {geneProduct}")

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <SPARQL_ENDPOINT_URL> <PATHWAY_ID>")
        sys.exit(1)

    endpoint_url = sys.argv[1]
    pathway_id = sys.argv[2]

    run_sparql_query(endpoint_url, pathway_id)
