#!/bin/bash


#################### License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################

mkdir -p /workdir/rjl278/Sorghum/WGS/PAT/MERGE/dedup_bam
mkdir -p /workdir/rjl278/Sorghum/WGS/PAT/MERGE/stat_files


for myfile in `ls NEW/bam_files/*.bam`; do

    basefile=$(basename "$myfile" .bam)
    #oldcount=$(ls /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all | grep -P "${basefile}_[^dup]*.bam$" )
    oldcount=$(ls /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all | grep -v bai| grep -P "${basefile}_[^dup]*.bam$" | wc -l )
    temporal=$(ls /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all | grep -v bai| grep -P "${basefile}_[^dup]*.bam$")
    name1=$(echo $temporal | cut -d" " -f1) 
    name2=$(echo $temporal | cut -d" " -f2)

    if (($oldcount == 2))
    then
        echo $name1
        echo $name2
        echo $basefile

        $RELEASE/bin/sentieon driver -t 40 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name1 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name2 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files/$basefile.bam \
            --algo LocusCollector --fun score_info ${basefile}_scores.txt

        $RELEASE/bin/sentieon driver -t 40 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name1 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name2 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files/$basefile.bam --algo Dedup --rmdup --score_info ${basefile}_scores.txt --metrics ${basefile}_metrics.txt --optical_dup_pix_dist 2500 dedup_${basefile}.bam

    else
        echo $name1
        echo $basefile 

        $RELEASE/bin/sentieon driver -t 40 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name1 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files/$basefile.bam \
            --algo LocusCollector --fun score_info ${basefile}_scores.txt
        
        $RELEASE/bin/sentieon driver -t 40 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/OLD/bam_all/$name1 -i \
            /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files/$basefile.bam --algo Dedup --rmdup --score_info ${basefile}_scores.txt --metrics ${basefile}_metrics.txt --optical_dup_pix_dist 2500 dedup_${basefile}.bam

    fi
        
    mv dedup_${basefile}.bam* /workdir/rjl278/Sorghum/WGS/PAT/MERGE/dedup_bam/
    rm *_scores.txt*
    mv *_metrics.txt /workdir/rjl278/Sorghum/WGS/PAT/MERGE/stat_files/

done
