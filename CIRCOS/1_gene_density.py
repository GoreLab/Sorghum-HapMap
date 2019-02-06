#!/usr/bin/env python

## ############ Calculate Gene Density per specified bin  #######################
## Input: gff file                                                           ####       
## Roberto Lozano: rjl278@cornell.edu                                        ####

import sys
import numpy as np

gff_file        = sys.argv[1] # gff file
n               = sys.argv[2] # chromosome to test

########     Loading Chromosome size information of the cassava genome  #########


chrm = { 'Chr01' : 80884392,
                'Chr02' : 77742459,
                'Chr03' : 74386277,
                'Chr04' : 68658214,
                'Chr05' : 71854669,
                'Chr06' : 61277060,
                'Chr07' : 65505356,
                'Chr08' : 62686529,
                'Chr09' : 59416394,
                'Chr10' : 61233695 }

##################################################################################

bsize = 100000 # size of bin                   
bins = int(chrm['Chr'+str(n)])/bsize + 1  # Number of bins per chromosome

##################################################################################


genden = list()         # list where number of genes will be stored in tuples of the form ("bin_id", density)
binid = 1               # initial bin
lowl = 1                # range
upl  = int(bsize)       # range

while binid <= bins:
        tmpr2 = list() #temporary list that carrys the number of genes per each bin
        
        ### Open the gff file:
        
        with open(gff_file) as f:
                
                for lines in f:
                        a = lines.split("\t")
                        z = "Chr"+n
                        if ((a[0] == z) and  upl > int(a[3]) > lowl) :
                                tmpr2.append(float(a[3]))
        
        gendenline = binid, len(tmpr2)
        genden.append(gendenline)
        
        tmpr2 = list()  
        binid += 1
        lowl += int(bsize) - 1
        upl += int(bsize) -1
        

# Save to file :

f1 = open('genedensity_chromosome%s' %(n), 'w')
for items in genden:
        a = str(items[0])+"\t"+str(items[1])
        f1.write(a)
        f1.write("\n")
f1.close()

