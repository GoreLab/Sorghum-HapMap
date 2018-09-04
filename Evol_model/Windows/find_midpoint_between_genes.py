#!/usr/bin/python


# This script calculates the midpoint distance between two genes
# and outputs a series of intervals that covers each chromosome from position 1 to the end
# and breaks up the chromosome in intervals defined by these breakpoints

### INPUT: Assumes a bed format sorted by chr and then start position

import os, sys, subprocess
from collections import defaultdict

infile = sys.argv[1]

chr_len = defaultdict(int)
for line in open('chrom_length_v3.0'):
    if len(line) <= 1:
        continue
    a = line.strip().split('\t')
    chr_len[a[0]] = int(a[1])

interval = defaultdict(list)

curr_chrm = 'Chr01' ## assume a sorted file that start at Chr01...
n = 1 # for the first line
overlap = 0 # to count overlapping
midpoint = 0 # this needs to be defined for the case of overlapping genes in the first line of the file (n == 1)
for line in open(infile):
    if len(line) <= 1:
        continue
    a = line.strip().split('\t')
    chrm = a[0]
    st = int(a[1])
    end = int(a[2])
    if curr_chrm == chrm:
        if n == 1:
            listmidpoints = [1]
            prev_end = end
            n = 2
            continue
        else:
            dist = st - prev_end
            if dist < 0:
                overlap += 1
                # in case of overlapping genes, we keep reading the file
                # but we update prev_end
                prev_end = max(end, prev_end)
                to_add = midpoint+1 ## This is not updated yet, so it takes the value of the previous interval
                continue
            elif dist%2 == 0:
                midpoint = prev_end + dist/2.
            else:
                midpoint = prev_end + (dist-1)/2.
        # if write_twice, write it again to conserve the same nuymber of rows in the file. Some
        # genes are overlapping but we create a unique interval that we need to write twice
        if overlap > 0:
            for j in range(overlap):
                listmidpoints.append(midpoint)
                listmidpoints.append(to_add)
        listmidpoints.append(midpoint)
        listmidpoints.append(midpoint+1)
        prev_end = end
        overlap = 0
    else:
        listmidpoints.append(chr_len[curr_chrm]) # write the end of chr
        if overlap > 0:
            for j in range(overlap):
                listmidpoints.append(to_add)
                listmidpoints.append(chr_len[curr_chrm])
        for i in range(0, (len(listmidpoints)-1) ,2): # write up all the previous chr data
            interval[curr_chrm].append( [listmidpoints[i], listmidpoints[i+1]] )
        ## Start recording the data for the new chromosome
        listmidpoints = [1] # reset the array of midpoints
        curr_chrm = chrm
        prev_end = end
        overlap = 0
        midpoint = 0

# write the values for the last chromosome
listmidpoints.append(chr_len[curr_chrm]) # write the end of chromosome
if overlap > 0:
    for j in range(overlap):
        listmidpoints.append(to_add)
        listmidpoints.append(chr_len[curr_chrm])
for i in range(0, (len(listmidpoints)-1) ,2):
    interval[curr_chrm].append( [listmidpoints[i], listmidpoints[i+1]] )

output = open('intervals_gene_midpoints','w')
#output = open('TESTintervals_gene_midpoints','w')
for i in interval:
    for j in interval[i]:
        #output.write(str(i)+'\t'+"{0:9.0f}\t{1:9.0f}".format(j[0], j[1])+'\n')
        output.write(str(i)+'\t'+str(int(j[0]))+'\t'+str(int( j[1]))+'\n')
output.close()

os.system('rm intervals_midpoints_gene_names.bed') #remove if it exists
os.system('sort -k1,1 -k2,2n intervals_gene_midpoints > sorted_intervals_gene_midpoints')
os.system('cut -f 4 sorted_sorghum_v3_genes_in_builtCHRM.bed | paste sorted_intervals_gene_midpoints - > intervals_midpoints_gene_names.bed')
os.system('rm intervals_gene_midpoints sorted_intervals_gene_midpoints')
subprocess.call("./length_windows.sh")

