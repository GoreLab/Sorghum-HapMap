#!/usr/bin/env python

# Extract positions with monomorphic markers and with a certain threshold of heterozygosity
# The input file is the HWE output file from vcftools
# rjl278@cornell.edu


import sys
import os

hwe_file = sys.argv[1]
threshold = sys.argv[2]

exclude= list()

with open(hwe_file) as h:
    next(h)
    for lines in h:
        b = lines.split("\t")
        chromosome = b[0]
        position = b[1]
        alleles = b[2].split("/")
        expected = b[3].split("/")[1] 
        
        total = int(alleles[0]) + int(alleles[1]) + int(alleles[2])      
        percentage = (int(alleles[1])*100)/total
        
        if (int(alleles[0]) >= int(alleles[2]) and  percentage > int(threshold) or int(alleles[2]) > int(alleles[1]) ):
            F = 1- (int(alleles[1])/float(expected))
            coordinate = chromosome+"\t"+position+"\t"+str(F)
            print (coordinate)
        
        elif(percentage > int(threshold) and int(alleles[1]) > int(alleles[1])):
            F = 1- (int(alleles[1])/float(expected))
            coordinate = chromosome+"\t"+float(position)+"\t"+str(F)
            print (coordinate)