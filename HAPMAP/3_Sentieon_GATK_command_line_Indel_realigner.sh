#!/bin/bash

#################### License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################


### Order of the arguments matter, should be:
# driver -t -r -i algo option output

mkdir -p realigned_bam

for myfile in `ls dedup_bam/*.bam`; do

    basefile=$(basename "$myfile" | cut -c14-)
    $RELEASE/bin/sentieon driver -t 40 -r /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa \
        -i $myfile --algo Realigner \
        realigned_bam/realigned_$basefile

done
