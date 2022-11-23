from rdflib import Graph

# functions

def sparql_query(q, endpoint):
    fdp_g = Graph().parse(endpoint)
    for row in fdp_g.query(q):
        print(row)
    return None

if __name__ == '__main__':
    q = '
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ex: <http://example.com/>
        prefix obo: <http://purl.obolibrary.org/obo/>
        prefix edam: <http://edamontology.org/>
        prefix sio: <http://semanticscience.org/resource/>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix ncit: <http://purl.obolibrary.org/obo/>
        prefix mondo: <http://purl.obolibrary.org/obo/mondo.owl/>
        prefix gecko: <http://purl.obolibrary.org/obo/gecko.owl/>
        prefix exo: <http://purl.obolibrary.org/obo/exo.owl/>

        select (count(?o) as ?Number_of_Covid19_Diagnosed)
            where {
                ?s mondo:C173069 ?o .
                'FILTER (?o = true)
            }'
    e = 'https://fdp.cmbi.umcn.nl/blazegraph/#splash'
    main(q, e)