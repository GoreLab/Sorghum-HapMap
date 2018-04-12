#!/bin/bash

#################### License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################

mkdir -p /workdir/rjl278/Sorghum/WGS/PAT/MERGE/recal_values

#Use the Indexed vcf as a reference list, knownSNP.vcf.gz

for myfile in `ls realigned_bam/*.bam`; do

    basefile=$(basename "$myfile" .bam | cut -c 11-)

    $RELEASE/bin/sentieon driver -t 40 -r /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa -i $myfile \
        --algo QualCal \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Mockler.vcf.gz \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Mace.vcf.gz \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Pat240.vcf.gz \
        recal_${basefile}.table
    
    $RELEASE/bin/sentieon driver -t 40 -r /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa -i $myfile \
        -q recal_${basefile}.table --algo QualCal \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Mockler.vcf.gz \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Mace.vcf.gz \
        -k /workdir/rjl278/Sorghum/WGS/DB/VCFs_old/Pat240.vcf.gz \
        recal_${basefile}.table.post
    
    $RELEASE/bin/sentieon driver -t 40 --algo QualCal --plot --before recal_${basefile}.table \
        --after recal_${basefile}.table.post recal_${basefile}_results.txt
    
    $RELEASE/bin/sentieon plot bqsr -o BQSR_${basefile}.pdf recal_${basefile}_results.txt
    
    rm recal_${basefile}_results.txt
    mv recal_${basefile}.table recal_values/
    mv recal_${basefile}.table.post recal_values/
    mv *.pdf recal_values/

done
