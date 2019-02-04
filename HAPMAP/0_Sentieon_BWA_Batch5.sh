#!/bin/bash

###################  Batch5  ########################## 

###################  License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################

mkdir -p /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files

FILENAME=$1   # that would be the first argument after the name of the script

count=0

while read LINE; do

    let count++;
    line=(${LINE[@]});

    #radical=${line[0]}; # it's the fastq file name, but it does not have the path
    sample=${line[0]};

    fastqfile1=/workdir/rjl278/Sorghum/WGS/PAT/NEW/Fastq/${sample}/$(echo *_1.fq.gz);
    fastqfile2=/workdir/rjl278/Sorghum/WGS/PAT/NEW/Fastq/${sample}/$(echo *_2.fq.gz);

    # RGID:flowcell.lane  # In Illumina data, read group IDs are composed using the flowcell + lane name and number, making them a globally unique identifier across all sequencing data in the world.
    # RGSM: samplename
    # RGPL: illumina
    # RGLB: lib1  # in this experiment, we have no way of knowing if they made different libraries for the same sample and mixed these libraries; they probably did single library prep.
    # RGPU:  # There is another read group tag called PU (referring to the platform unit, holding flowcell lane information) that is not required by GATK but takes precedence over ID for base recalibration if it is present.
    # we can extract all this information from the file name; otherwise, it's in the first line of each fastq

    rg=($(zcat  $fastqfile1 | head -n 1)); ## @K00317:10:H7W7HBBXX:1:1101:23094:1525 1:N:0:ATTCCT; both mates in the pair have the same radical name and should have the same read group
    IFS=":"; inf=(${rg[0]});  ## inf is just @K00317:10:H7W7HBBXX:1:1101:23094:1525, split by the colon (instrunment name, runID, flowcellID, lane, tile, x, y)
    unset IFS;
    rgid=${inf[2]}.${inf[3]};
    rgsm=$sample;
    rgpu=${inf[2]}_${sample}.${inf[3]};
    
    echo $rg
    echo $rgpu;
    echo $rgid;
    echo $rgsm;
    echo "@RG\tID:$rgid\tSM:$rgsm\tPL:illumina\tLB:lib1\tPU:$rgpu";

    bwa mem -aM -R "@RG\tID:$rgid\tSM:$rgsm\tPL:illumina\tLB:lib1\tPU:$rgpu" -t 60 -w 3 -K 10000000 -c 10000 /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa "<gzip -dc $fastqfile1" "<gzip -dc $fastqfile2" | $RELEASE/bin/sentieon util sort -o sorted_${sample}.bam -t 60 --sam2bam -i -;
    mv sorted* /workdir/rjl278/Sorghum/WGS/PAT/NEW/bam_files/

done < $FILENAME
