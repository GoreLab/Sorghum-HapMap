#!/usr/bin/env python

# Extract positions with monomorphic markers and with a certain threshold of heterozygosity
# The input file is the HWE output file from vcftools
# rjl278@cornell.edu


import sys
import os

hwe_file = sys.argv[1]


exclude= list()

with open(hwe_file) as h:
    next(h)
    for lines in h:
        b = lines.split("\t")
        chromosome = b[0]
        position = b[1]
        alleles = b[2].split("/")
        expected = b[3].split("/")[1] 
        
        total = 2*(int(alleles[0])) + 2*(int(alleles[1])) + 2*(int(alleles[2]))      
        
        if (int(alleles[0]) >= int(alleles[2])):
            F = 1- (int(alleles[1])/float(expected))
            MAF = float(2*(int(alleles[2])) + int(alleles[1])) / int(total)
            Minor = alleles[2]
	    Hetz = alleles[1]
            coordinate = chromosome+"\t"+position+"\t"+str(F)+"\t"+str(MAF)+"\t"+Minor+"\t"+Hetz
  	    		
            print(coordinate)
        
        else:
            F = 1- (int(alleles[1])/float(expected))
            MAF = float(2*(int(alleles[0])) + int(alleles[1]) )/int(total)
            Minor = alleles[0]
            Hetz = alleles[1]
            coordinate = chromosome+"\t"+position+"\t"+str(F)+"\t"+str(MAF)+"\t"+Minor+"\t"+Hetz
            print(coordinate)

