#!/usr/local/bin/bash

# this script is called in the python script
awk '{ print $3-$2+1; }' intervals_midpoints_gene_names.bed | paste intervals_midpoints_gene_names.bed - > intervals_midpoints_gene_names_length.bed
