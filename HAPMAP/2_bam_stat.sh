#!/bin/bash

for myfile in `ls bam_files/*.bam`; do

    basefile=$(basename "$myfile" .bam)

    # echo $basefile
    # echo $myfile
    samtools idxstats $myfile > stat_files/stat2_${basefile}.txt;
    samtools flagstat $myfile > stat_files/stat_${basefile}.txt;

done
