select ?sampleID ?p ?o where { 

service <http://145.38.185.93:7200/repositories/fdp> { 

?sampleID <http://semanticscience.org/resource/SIO_001403> "http://example.com/MYSAMPLE" .

} 

} limit 1000