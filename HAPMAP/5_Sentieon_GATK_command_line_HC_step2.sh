#!/bin/bash

#################### License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################

mkdir -p /workdir/rjl278/Sorghum/WGS/PAT/MERGE/gvcf_files

for myfile in `ls realigned_bam/*.bam`; do
    basefile=$(basename "$myfile" .bam | cut -c 11-);

    echo $basefile

    #$RELEASE/bin/sentieon driver -t 60 -r /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa \
    #    -i $myfile -q recal_values/recal_${basefile}.table --algo Haplotyper \
    #    --emit_mode gvcf ${basefile}.gvcf --call_conf 20 --emit_conf 20 --min_base_qual 20 
    
    #mv *.gvcf* gvcf_files/
done

#sentieon driver -t 16 -r ~/sorghum/reference_genome/sorghum_313_v3.0.fa --algo GVCFtyper $list_of_files --call_conf 20 --emit_conf 20 all.vcf