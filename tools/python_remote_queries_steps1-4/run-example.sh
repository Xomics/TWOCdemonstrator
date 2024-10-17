# run step 1 : Find study on COVID-19 with multi-omics data.

python3 remote_query_standalone.py -q step1.q -s http://145.38.185.93:7200/repositories/fdp -o step1.report.txt


# run step 2 : Fetch information from individuals included in the study, and check their COVID-19 disease status and ICU admission status.

python3 remote_query_standalone.py -q step2.q -s http://145.38.185.93:7200/repositories/fdp -o step2.report.txt


# run step 3.1 : Get subject identifiers from step 2.

grep "subject" step2.report.txt | cut -f2 | while read line ; 

do echo "s|\"http\:\/\/example\.com\/.*\"|\"$line\"|" >> step3.samples.sed ; done


# run step 3.2 : Use subject identifiers to use in the query of step 3, resulting in a list of all different samples taken from these individuals.

while read line ; do sed -r -e $line step3.q > step3.q.tmp ; 

python3 remote_query_standalone.py -q step3.q.tmp -s http://145.38.185.93:7200/repositories/fdp -o step3.report.txt.tmp >> step3.report.collect.txt ; done < step3.samples.sed
	

# run step 4 : Use sample identifiers from step 3 to search for availability of transcriptomics data thereof, 
# resulting in a list of raw individual transcriptomics files available, 
# including their combined (meta)data feature tables with corresponding names and links.

mysamples=$( while read line ; do grep "subject" | sed 's|http://example.com/||' | cut -f2 ; done < step3.report.collect.txt )

for element in $mysamples ;

	do echo '# SAMPLE QUERY: ' $element >> step4.report.collect.txt ;

	sedstring=" s|\"http\:\/\/example\.com\/.*\"|\"$element\"| " ;

	sed -r $sedstring $line step4.q > step4.q.tmp ; python3 remote_query_standalone.py -q step4.q.tmp -s http://145.38.185.93:7200/repositories/fdp -o step4.report.txt.tmp >> step4.report.collect.txt ; done

grep -E -i '# subject|# predicate|# object|# sample|# no result' step4.report.collect.txt > step4.report.final.txt


# run step 5 : Use (meta)data feature tables from step 4 to run the python_read_omics functions.py script : Extract IL6 transcript values for the available samples from step 4.

# run step 6 : Use the results from step 5, together with patient metadata from step 2, to build a graph and perform statistics on IL6 for COVID-19 patients admitted to ICU or hospital only.

# see IL6.ipynb by XiaoFeng for steps 5 and 6.
