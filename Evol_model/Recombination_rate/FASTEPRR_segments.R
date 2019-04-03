#!/programs/bin/R/R

######### R parallelized wrapper for FastEPRR #######################
#
# You need: vcf files imputed and phased per chromosome
# This wrapper takes 4 arguments:
# 1) vcf_prefix             --> if vcf files looks like this chr1.vcf.gz, chr2.vcf.gz...   then vcf_prefix = chr
# 2) windows size           --> rho will be calculated in windows with this size
# 3) number of chromosomes  
#
# Usage example: Rscript FASTEPRR.R chr 100 10
#
# Script optimized to work with 40 cores to change this modify line 23, 45 and 46
# Three folder will be created: Step1_output, Step2_output, Step3_output
#
#####################################################################

args = commandArgs(trailingOnly=TRUE)

library(magrittr)
library(dplyr)
library(tidyr)
library(FastEPRR)
library(foreach)
library(doMC)
registerDoMC(40)

## LOAD the window files per chromosome:
window_file <- read.delim("/workdir/rjl278/Sorghum/Evol_model/Recombination/FINAL/MISSING/windows", header=F) %>%
        `colnames<-`(c("chr", "from", "to", "distance"))

### STEP 1
phased_prefix = "TERRA_SNPs_chr"

#Create the output folder for Step 1
system("mkdir -p Steptemp_output")

foreach(i=1:10) %dopar% {
    
    path = system2("pwd", stdout=TRUE)
    input = sprintf("%s/%s%d.vcf.gz",path, phased_prefix, i)
    
    window_chr <- window_file %>%
        filter(chr == i)

    for (g in 1:dim(window_chr)[1]) {
    
        from    <- window_chr[g,2]
        to      <- window_chr[g,3]
        winl    <- window_chr[g,4]
        step1_output = sprintf("Steptemp_output/chr%s_%s.coor", i,g)

        FastEPRR_VCF_step1(vcfFilePath=input, erStart=as.character(from), erEnd=as.character(to), winLength=as.character(winl), winDXThreshold=1, srcOutputFilePath=step1_output)
    }
     
}

### STEP 1 1/2 
# Combine the files
system("echo 'chr nsam wdou wxton wH wHetero wavsk2 wavr2 misInfo startPos endPos' > header.txt")
system("mkdir Step1_output")
system("for chr in {1..10}; do cat Steptemp_output/chr${chr}_* | grep -v endPos | sort -nk 10 > Step1_output/chr${chr}.tmp ; done")
system("for chr in {1..10}; do cat header.txt Step1_output/chr${chr}.tmp > Step1_output/chr${chr}.coor ; done")
system("rm Step1_output/*.tmp")

### STEP 2
system("mkdir -p Step2_output")

foreach(i=1:40) %dopar% {
    FastEPRR_VCF_step2(srcFolderPath="Step1_output", jobNumber=40, currJob= i, DXOutputFolderPath="Step2_output")
}

### STEP 3
system("mkdir -p Step3_output")
FastEPRR_VCF_step3(srcFolderPath="Step1_output", DXFolderPath="Step2_output", finalOutputFolderPath="Step3_output")
