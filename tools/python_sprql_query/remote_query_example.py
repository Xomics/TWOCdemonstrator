from rdflib import Graph, URIRef

# functions

def sparql_query_to_file(q, filename):
    fdp_g = Graph()
    with open(filename, 'w') as f:
        for s, p, o in fdp_g.query(q):
            f.write(s.n3() + ' ' + p.n3() + ' ' + o.n3() + ' .\n')
    return None

if __name__ == '__main__':
    q1 = """
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
            where { SERVICE <https://fdp.cmbi.umcn.nl/blazegraph/sparql>{
                ?s mondo:C173069 ?o .}
                FILTER (?o = true)
            }"""

    q2 = """
        select *
            where { SERVICE <https://fdp.cmbi.umcn.nl/blazegraph/sparql>{
                ?s ?p ?o .}
            } LIMIT 1000 """  
    fname = 'test_result.txt'
    sparql_query_to_file(q2, fname)