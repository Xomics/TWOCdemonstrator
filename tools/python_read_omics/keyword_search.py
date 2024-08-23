''' usage: python keyword_search.py "https://sparql.wikipathways.org/sparql" SARS-CoV-2
'''
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def run_keyword_search(endpoint_url, keyword):
    query = f"""
    PREFIX wp: <http://vocabularies.wikipathways.org/wp#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?pathway ?label WHERE {{
        ?pathway a wp:Pathway .
        ?pathway rdfs:label ?label .
        FILTER(CONTAINS(LCASE(?label), LCASE("{keyword}")))
    }}
    """

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        pathway = result["pathway"]["value"]
        label = result["label"]["value"]
        print(f"Pathway: {pathway}, Label: {label}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <SPARQL_ENDPOINT_URL> <PATHWAY_ID>")
        sys.exit(1)
    endpoint_url = sys.argv[1]
    keyword = sys.argv[2]
        # endpoint_url = "https://sparql.wikipathways.org/sparql"
        # keyword = "SARS-CoV-2"  

    run_keyword_search(endpoint_url, keyword)
