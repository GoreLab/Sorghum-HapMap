#!/usr/bin/env python

import pysam

#read the input file
myvcf=pysam.VariantFile("toy.vcf","r")

# Add the HP field to header. Say its a string and can take any no. of values. It depends what format you want to give.
myvcf.header.formats.add("AB","1","Integer","Allele Balance")

# An example showing how to add 'HP' information. Please explore further.    

head = myvcf.header

with open("out.vcf", "w") as out:
    out.write(str(head))
    
    for variant in myvcf:
        ab_value = ''
        
        for sample in variant.samples:
            
            if variant.samples[sample]['GT'][0] == variant.samples[sample]['GT'][1]:
                ab_value = 100
                variant.samples[sample]['AB']= ab_value

            if variant.samples[sample]['GT'][0] != variant.samples[sample]['GT'][1]:
                AB = float(min(variant.samples[sample]['AD'])) / float(variant.samples[sample]['DP'])
                ab_value = int(round(AB, 2)*100)
                variant.samples[sample]['AB']= ab_value  

            #if min(variant.samples[sample]['AD']) > 0 and  variant.samples[sample]['PL'][1] == 0:
            #    AB = float(min(variant.samples[sample]['AD'])) / float(variant.samples[sample]['DP'])
            #    variant.samples[sample]['AB']= int(round(AB, 2)*100)
            #if min(variant.samples[sample]['AD']) == 0 :
            #    variant.samples[sample]['AB']= 100


            


        out.write(str(variant))
