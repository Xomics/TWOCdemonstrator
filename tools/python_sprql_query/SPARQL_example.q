SELECT ?s
	WHERE { SERVICE <https://dbpedia.org/sparql> {
		?s a ?o .
	}
} LIMIT 3