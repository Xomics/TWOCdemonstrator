PREFIX wdt: <http://www.wikidata.org/entity/>

	select ?sampleID ?fileTopic ?fileLink where { # select ?assay ?sampleID ?datafileID ?target_datafileID ?fileTopic ?fileLink where { 

	service <http://145.38.185.93:7200/repositories/fdp> {
	
		?datafileID ?p ?sampleID .
		FILTER (regex(str(?sampleID), "http://example.com/MYSAMPLE"))
		
		?assay wdt:P527 ?datafileID . # wdt:P527 = has part(s)
		
		?assay wdt:P527 ?target_datafileID . # wdt:P527 = has part(s)
		
		?target_datafileID wdt:P527 ?fileTopic. # wdt:P527 = has part(s)
		FILTER ((datatype(?fileTopic) = wdt:Q5227290) &&  regex(str(?fileTopic), "Feature Annotation File|Pseudobulk File") ) # wdt:Q5227290 = data file
		
		?target_datafileID wdt:P527 ?fileLink. # wdt:P527 = has part(s)
		FILTER ( datatype(?fileLink) = wdt:Q82799 ) # && regex(str(?fileLink), "transcriptomics" ) ) # wdt:Q82799 = name
	}

} limit 1000