This repository includes code use in the article:

Working Title:
#  Comparative Sorghum-Maize HapMap

## SNP calling:
1_Sentieon_merge_and_remove_duplicates.sh

2_bam_stat.sh

3_Sentieon_GATK_command_line_Indel_realigner.sh

4_Sentieon_GATK_command_line_Recal_providing_list.sh

5_Sentieon_GATK_command_line_HC_step2.sh

6_joint_variant_calling.sh

## Describing the Population:

PrincipalComponentAnalysis.Rmd: (/HAPMAP/)
Calculates principal component analysis on the marker matrix using SNPrelate. Plots included

## Evolutionary model:

## Plots: 
(CIRCOS and ... folders)

1_gene_density.py Calculates gene density per chromosome from a gff3 file
