select ?individual ?covid ?icu where { 

service <http://145.38.185.93:7200/repositories/fdp> { 

?individual <http://edamontology.org/data_1188>  "https://doi.org/10.1016/j.cell.2020.10.037" . 

?individual <http://purl.obolibrary.org/obo/MONDO_0100096> ?covid .  # COVID-19 status (YES/NO) 

?individual <http://purl.obolibrary.org/obo/NCIT_C53511> ?icu .  # ICU status (YES/NO) 

filter(?covid = "YES"^^xsd:boolean)

} 

} limit 1000 