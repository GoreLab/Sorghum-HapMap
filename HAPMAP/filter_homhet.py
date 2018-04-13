#!/usr/bin/env python

# Extract positions with monomorphic markers and with a certain threshold of heterozygosity
# The input file is the HWE output file from vcftools
# rjl278@cornell.edu


import sys
import os

hwe_file = sys.argv[1]
threshold = sys.argv[2]

monomorphic = list()

with open(hwe_file) as h:
    next(h)
    for lines in h:
        b = lines.split("\t")
        chromosome = b[0]
        position = b[1]
        alleles = b[2].split("/")
        total = int(alleles[0]) + int(alleles[1]) + int(alleles[2])      
        percentage = (int(alleles[1])*100)/total
        if (alleles[1] == "0" and alleles[2] == "0" or percentage > int(threshold)):
            coordinate = chromosome+"_"+position
            monomorphic.append(coordinate)

print ("\n".join(monomorphic))