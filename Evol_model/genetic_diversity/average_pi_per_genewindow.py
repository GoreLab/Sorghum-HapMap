#!/usr/bin/python


# This script calculates the average nucleotide diversity for each window
# defined around a gene
# INPUT: Assumes a bed format sorted by chr and then start position
# The bed file is the output of badtools and
# and contains one line per SNP, with its pi value, and the gene window in which it is
# The present script will just average the values per window, counting every nucleotide in the genome
# and giving them a 0 value for non-polymorphic positions

import os, sys, subprocess
from collections import defaultdict

infile = sys.argv[1] # pi_per_window.bed

p = subprocess.Popen(['head','-n', '1', infile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
myheader = p.communicate()[0]
## If running version 2.7, use:
#myheader = myheader.strip().split('\t')
## If running version 3.x, use:
myheader = str(myheader,'UTF-8').strip().split('\t')

output = open('average_'+infile,'w')
output.write('chrm\tst\tend\tgene\tlengthWin\tnbSNPs\tSNPdensity\tpi\n')
#output = open('TESTaverage_pi_per_genewindow.bed','w')
curr_val = []
prev_gene = myheader[3]
count_snp = 0
for line in open(infile):
    if len(line) <= 1:
        continue
    a = line.strip().split('\t')
    chrm = a[0]
    st = a[1]
    end = a[2]
    gene = a[3]
    length = int(a[4])
    if a[8] != '.':
        pi = float(a[8])
    else:
        pi = a[8]
    if prev_gene == gene: # that will never happens if pi = '.'
        curr_val.append(pi)
        count_snp += 1
        window = chrm+'\t'+st+'\t'+end+'\t'+gene+'\t'+str(length)+'\t'+str(count_snp)
    else:
        if curr_val[0] != '.':
            if count_snp > 1:
                output.write(window + '\t' +"{0:4.4f}\t{1:8.8f}".format( count_snp/float(prev_length), sum(curr_val)/float(prev_length) ) + '\n' )
            else:
                output.write(prev_chrm+'\t'+prev_st+'\t'+str(prev_end)+'\t'+prev_gene+'\t'+str(prev_length)+'\t'+str(count_snp)+'\t' +"{0:4.4f}\t{1:8.8f}".format( count_snp/float(prev_length), sum(curr_val)/float(prev_length) ) + '\n' )
        else:
            output.write(prev_chrm+'\t'+prev_st+'\t'+str(prev_end)+'\t'+prev_gene+'\t'+str(prev_length)+'\t0\tNA\tNA\n')
        curr_val = [pi] # re-initiate the list with new values
        count_snp = 1
    prev_chrm = chrm
    prev_st = st
    prev_end = end
    prev_length = length
    prev_gene = gene

# for the last line
if curr_val[0] != '.':
    output.write(window + '\t' +"{0:4.4f}\t{1:8.8f}".format( count_snp/float(prev_length), sum(curr_val)/float(prev_length) ) + '\n' )
else:
    output.write(prev_chrm+'\t'+prev_st+'\t'+str(prev_end)+'\t'+prev_gene+'\t'+str(prev_length)+'\t0\tNA\tNA\n')
output.close()
