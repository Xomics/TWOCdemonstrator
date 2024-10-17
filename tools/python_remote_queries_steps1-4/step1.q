PREFIX ns1: <http://> 

# https://github.com/Xomics/FAIRDataCube/wiki/3.2-Trusted-World-of-Corona-(TWOC)#example-query 

# 1. Retrieve Study Identifier where COVID is mentioned, for example in title/description 

select ?s ?studyID ?occurrence where { 
    
service <http://145.38.185.93:7200/repositories/fdp> { 

?s ns1:schema.orgsameAs ?studyID . 

?s ?p ?occurrence . 
        
# filter (regex(?occurrence, "(?=.*COVID-19)(?=.*Multi-Omics)")) # identify the occurrence of "COVID-19" and "Multi-Omics" 

filter ( regex(?occurrence, "COVID-19") && regex(?occurrence, "Multi-Omics") ) # identify the occurrence of "COVID-19" and "Multi-Omics" 

# filter (regex(?occurrence, "COVID-19")) # identify the occurrence of "COVID-19" 

}

} limit 1000