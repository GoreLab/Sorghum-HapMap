This repository includes code use in the article:

#  **A Comparative Sorghum-Maize HapMap**
![language: R](https://img.shields.io/badge/language-R-blue.svg)
![language: Python](https://img.shields.io/badge/language-Python-green.svg)
![status: WIP](https://img.shields.io/badge/status-WorkInProgress-red.svg)

![alt text](https://github.com/GoreLab/Sorghum-HapMap/blob/master/CIRCOS/GitHub_figure.svg)

## **Building the Sorghum HapMap** (/HAPMAP/)

  ### SNP calling: 
*0_Sentieon_BWA_Batch5.sh* - Sample of alignment file using BWA  
*1_Sentieon_merge_and_remove_duplicates.sh* - Merging Bam files according to Figure S2A  
*2_bam_stat.sh* - Calculate alignment stats  
*3_Sentieon_GATK_command_line_Indel_realigner.sh* - Realign reads around InDels  
*4_Sentieon_GATK_command_line_Recal_providing_list.sh* - Recalibration using high quality positions 
*5_Sentieon_GATK_command_line_HC_step2.sh* - Haplotypes (produces gVCFs)  
*6_joint_variant_calling.sh* - Call the variants and produce a VCF file.
    
  ### Describing the Population:

  *Population_structure_pub.Rmd:* - Calculates principal component analysis on the marker matrix using SNPrelate. Plots included  
  *MAF_FST.Rmd* - Calculates Allele frequency spectrum and FSTs between races  
  *Duplicates* - Checking the duplicates IBS matrix  
  *Linkage_disequilibrium.Rmd* - Code use to plot local LD plot and classic LD decay plots.  
  
  ### Misc:
*Filter_MAF_OE.py* - Extract monomorphic sites and sites with a threshold of heterozygosity   
*count_fastq.sh* - Count the number of reads in a fastq  
*vcfaddanot.py* - Add allele balancing field AB in a vcf file  

  
  


## **Deleterious alleles:**





## **Evolutionary model:**

  Recombination rates.-

  *FASTEPRR.R:* Wrappper to calculate rho across the genome in fixed windows

  *FASTEPRR_segments.R:* Wrapper to calculate rho across windows specified in a bed file

  *Recombination_Rates.Rmd:* R Notebook for plotting recombination rates across the chromosomes together with gene density 

  Genetic diversity (Pi).-


  ### Circos Plots: 
  *1_gene_density.py:* Calculates gene density per chromosome from a gff3 file
