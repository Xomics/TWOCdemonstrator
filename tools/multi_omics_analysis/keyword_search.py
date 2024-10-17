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
