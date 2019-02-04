This repository includes code use in the article:

#  **A Comparative Sorghum-Maize HapMap**
![language: R](https://img.shields.io/badge/language-R-blue.svg)
![language: Python](https://img.shields.io/badge/language-Python-green.svg)
![status: WIP](https://img.shields.io/badge/status-WorkInProgress-red.svg)

![alt text](https://github.com/GoreLab/Sorghum-HapMap/blob/master/CIRCOS/GitHub_figure.svg)

## **Building the Sorghum HapMap**

  ### SNP calling:
  *1_Sentieon_merge_and_remove_duplicates.sh*

  *2_bam_stat.sh*

  *3_Sentieon_GATK_command_line_Indel_realigner.sh*

  *4_Sentieon_GATK_command_line_Recal_providing_list.sh*

  *5_Sentieon_GATK_command_line_HC_step2.sh*

  *6_joint_variant_calling.sh*

  ### Describing the Population:

  *PrincipalComponentAnalysis.Rmd:* (/HAPMAP/)

  Calculates principal component analysis on the marker matrix using SNPrelate. Plots included


## **Deleterious alleles:**





## **Evolutionary model:**

  Recombination rates.-

  *FASTEPRR.R:* Wrappper to calculate rho across the genome in fixed windows

  *FASTEPRR_segments.R:* Wrapper to calculate rho across windows specified in a bed file

  *Recombination_Rates.Rmd:* R Notebook for plotting recombination rates across the chromosomes together with gene density 

  Genetic diversity (Pi).-


  ### Circos Plots: 
  *1_gene_density.py:* Calculates gene density per chromosome from a gff3 file
