#!/usr/bin/env python

"""
    This script calculates the derived allele frequencies of markers in the Sorghum HapMap v2
    It uses Maize and fox millet as outgroups
    Questions, comments, rants -> Roberto Lozano rjl278@cornell.edu
"""

# Load libraries

import subprocess
import os
import sys
import re
import gzip

## Read the file containing Deleterious position in Sorghum
## Include ref and alt alleles and the count of each allele (calculated in vcftools --counts)

#Some cleaning first
os.system('rm tmp*')
os.system('rm maize*')
os.system('rm alpos')
os.system('rm coordinates')
os.system('rm letter')
os.system('rm nuncaloveras')
os.system('rm align.tmp')
os.system('rm exon*')
os.system('rm *.fa')
os.system('rm pos*')

Master = sys.argv[1]
Numero = sys.argv[2]

os.system('echo DAF > DAF_%s.results' %(Numero))


with open( Master ) as f :
    #header = f.readline() #skip the header line

    for lines in f: # read the file lines by line

        cortado = lines.rstrip().split("\t")
        if cortado[18] == "NA" and cortado[19] =="NA" and cortado[14] =="NA":
            parejas = dict() #define the dictionary variable ( A:,C:,G:,T:)
            cuarteto = list()

            cortado = lines.split("\t")     # Split each line in elements separated by tabs
            parejas[cortado[3]]=cortado[9]  # Major Allele
            parejas[cortado[4]]=cortado[10] # Minor Allele

            # Append the list with the number of allele counts, if the allele is not present in the dictionary then it will print a 0
            try:
                cuarteto.append(parejas["A"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["C"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["G"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["T"])
            except:
                cuarteto.append("0")

            sorghum_cuarteto = ",".join(cuarteto)


            imprime = (sorghum_cuarteto+"\t"+"0,0,0,0"+"\t"+"0,0,0,0"+"\t"+"0,0,0,0")

        else:

            ######### STEP 1 -> Get the allele counts for the Sorghum Genome ############

            parejas = dict() #define the dictionary variable ( A:,C:,G:,T:)
            cuarteto = list()

            cortado = lines.split("\t")     # Split each line in elements separated by tabs
            parejas[cortado[3]]=cortado[9]  # Major Allele
            parejas[cortado[4]]=cortado[10] # Minor Allele

            # Append the list with the number of allele counts, if the allele is not present in the dictionary then it will print a 0
            try:
                cuarteto.append(parejas["A"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["C"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["G"])
            except:
                cuarteto.append("0")

            try:
                cuarteto.append(parejas["T"])
            except:
                cuarteto.append("0")

            sorghum_cuarteto = ",".join(cuarteto)

            ######### STEP 2 -> Get the position of each SNP in the CDS of the gene they are modifying  ############

            gene_sorghum =  cortado[5]
            chromosome =    cortado[1]
            position    =   cortado[2]


            print(gene_sorghum)

            # Get the exons
            os.system("more /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor_313_primary_transcript.gff3 | grep %s | grep CDS > tmp_gff" %(gene_sorghum))

            # Identify the exon where the SNP comes
            with open("tmp_gff") as f:
                for lines in f:
                    partio = lines.split("\t")
                    if partio[0] == chromosome and partio[3] <= position and partio[4] >= position:
                        strand  = partio[6]
                        desde   = int(partio[3])
                        hasta   = int(partio[4])


            if strand == "+" :

                # Extract the exon sequence:
                os.system("samtools faidx /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor_313_v3.0.fa  %s:%d-%d > exon.fa" %(chromosome, desde, hasta))
                # Extract the gene CDS:
                os.system("seqkit faidx /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor313.cds.fa -r %s > gene.fa" %(gene_sorghum))

                # Run the Blast2seq
                os.system("blastn -subject gene.fa -query exon.fa -outfmt 6 -task \"blastn-short\" | head -n 1 > align.tmp")
                #os.system("blastn -subject gene.fa -query exon.fa -outfmt 6 | head -n 1 > align.tmp")

                # desde - hasta (Genomic)  ///  desdeS - hastaS  (CDS) /// position (SNP)
                adicionar = int(position) - int(desde)

                if os.path.getsize("align.tmp") > 0:
                    blast = open("align.tmp","r")
                    for line in blast:
                        corto = line.split()
                        desdeS = corto[8]
                        hastaS = corto[9]

                    Posicion = int(desdeS) + int(adicionar)

                    blast.close()

                else:
                    Posicion = 1


            else :

                # Extract the exon sequence:
                os.system("samtools faidx /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor_313_v3.0.fa %s:%d-%d > exon.fa" %(chromosome, desde, hasta))

                # Extract the gene CDS:
                os.system("seqkit faidx /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor313.cds.fa -r %s > gene.fa" %(gene_sorghum))

                # Run the Blast2seq
                os.system("blastn -subject gene.fa -query exon.fa -outfmt 6 -task \"blastn-short\" | head -n 1 > align.tmp")
                #os.system("blastn -subject gene.fa -query exon.fa -outfmt 6 -tas | head -n 1 > align.tmp")

                # desde - hasta (Genomic)  ///  desdeS - hastaS  (CDS) /// position (SNP)
                adicionar = int(hasta) - int(position)

                if os.path.getsize("align.tmp") > 0:
                    blast = open("align.tmp","r")
                    for line in blast:
                        corto = line.split()
                        desdeS = corto[8]
                        hastaS = corto[9]

                    Posicion = int(hastaS) + int(adicionar)

                    blast.close()
                else:
                    Posicion = 1


            ######### STEP 3 -> Align the subgenome A to its homolog in Sorghum ############

            if cortado[18] == "NA":
                presenceMaizeA = "NO"
            else:
                presenceMaizeA = "YES"

            if cortado[19].rstrip() == "NA":
                presenceMaizeB = "NO"
            else:
                presenceMaizeB = "YES"

            if cortado[14] == "NA":
                presenceSetaria = "NO"
            else:
                presenceSetaria ="YES"

            if cortado[18][0:3] == "GRM":
                gene_maizeA =   cortado[18]+"_T01"
                pep_maizeA = cortado[18]+"_P01"
            elif cortado[18][0] == "A" :
                gene_maizeAp =   cortado[18]
                numero      = int(gene_maizeAp.split("_")[1])
                gene_maizeA =   gene_maizeAp.replace("FG", "FGT")
                pep_maizeA =     gene_maizeAp.replace("FG", "FGP")
            elif presenceMaizeA == "NO":
                gene_maizeA = "dummy"
                pep_maizeA = "dummy"

            if cortado[19][0:3] == "GRM":
                gene_maizeB =   cortado[19].rstrip()+"_T01"
                pep_maizeB = cortado[19]+"_P01"
            elif cortado[19][0] == "A" :
                gene_maizeBp =   cortado[19]
                numero      = int(gene_maizeBp.split("_")[1])
                gene_maizeB =   gene_maizeBp.replace("FG", "FGT")
                pep_maizeB =     gene_maizeBp.replace("FG", "FGP")
            elif presenceMaizeB == "NO":
                gene_maizeB = "dummy"
                pep_maizeB = "dummy"

            gene_setaria =  cortado[14]



            #### Sorghum_sequences
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor313.cds.fa %s > sorghum.fa ' %(gene_sorghum))
            os.system('sed -i \'s/>.*/>sorghum/g\' sorghum.fa')
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sbicolor_313_v3.1.protein_primaryTranscriptOnly.fa %s > sorghum_pep.fa ' %(gene_sorghum))
            os.system('sed -i \'s/>.*/>sorghum/g\' sorghum_pep.fa')
            os.system('sed -i \'s/\*//g\' sorghum_pep.fa')

            #### Maize_sequences
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Zea_mays.AGPv3.22.cdna.all.fa %s > maizeA.fa ' %(gene_maizeA))
            os.system('sed -i \'s/>.*/>maizeA/g\' maizeA.fa')
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Zea_mays.AGPv3.22.pep.all.fa %s > maizeA_pep.fa ' %(pep_maizeA))
            os.system('sed -i \'s/>.*/>maizeA/g\' maizeA_pep.fa')
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Zea_mays.AGPv3.22.cdna.all.fa %s > maizeB.fa ' %(gene_maizeB.rstrip()))
            os.system('sed -i \'s/>.*/>maizeB/g\' maizeB.fa')
            print(pep_maizeB)
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Zea_mays.AGPv3.22.pep.all.fa %s > maizeB_pep.fa ' %(pep_maizeB.rstrip()))
            os.system('sed -i \'s/>.*/>maizeB/g\' maizeB_pep.fa')

            #Setaria_sequences
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sitalica_312_v2.2.cds_primaryTranscriptOnly.fa %s > setaria.fa ' %(gene_setaria))
            os.system('sed -i \'s/>.*/>setaria/g\' setaria.fa')
            os.system('seqkit faidx -r /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/DB/Sitalica_312_v2.2.protein_primaryTranscriptOnly.fa %s > setaria_pep.fa ' %(gene_setaria))
            os.system('sed -i \'s/>.*/>setaria/g\' setaria_pep.fa')
            os.system('sed -i \'s/\*//g\' setaria_pep.fa')


            ## Concatenate the sequences and align
            os.system('cat sorghum_pep.fa maizeA_pep.fa maizeB_pep.fa setaria_pep.fa > toalign.fa')
            n=0
            with open('toalign.fa') as f:
                for lines in f:
                    #print lines[1]
                    if lines[0] ==">":
                        n += 1

            if n > 1:

                #Use clustal omega to do a protein alignment:
                os.system('/programs/clustalo -i toalign.fa --auto > tmp_pep.fa')

                #Use tranalign to make the alignment
                os.system('cat sorghum.fa maizeA.fa maizeB.fa setaria.fa > tmp.fa')
                os.system('/programs/emboss/bin/tranalign -asequence tmp.fa -bsequence tmp_pep.fa -outseq tmp')



                #Flat the resulting aligned fasta file:
                os.system('sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat.sh')

                #Get the exact position of the SNP in the alignment
                Z= open("letter","w+")
                W= open("pos", "w+")
                with open("tmp2") as f:
                    next(f)
                    for line in f:
                        number = 1
                        for elements in line.rstrip():
                            Z.write(elements+"\n")
                            if elements == "-" :
                                W.write("-"+"\n")
                            else:
                                W.write(str(number)+"\n")
                                number += 1

                Y= open("alpos", "w+")
                with open("tmp2") as f:
                    next(f)
                    for line in f:
                        number = 1
                        for elements in line.rstrip():
                                Y.write(str(number)+"\n")
                                number += 1

                Y.close()
                W.close()
                Z.close()

                os.system('paste letter pos alpos > coordinates')
                os.system("awk '{if ($2 == %d) print $3}' coordinates > posizao" %(Posicion))

                with open("posizao") as x:
                    for line in x:
                        Posicionalineada = int(line.rstrip())-1
                        print(Posicionalineada)


                #################### MAIZE A ##########################

                print(strand)
                if strand == "+" :
                    if presenceMaizeA == "YES":

                        os.system("seqkit faidx -r tmp1 maizeA > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:
                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        maizeA_cuarteto = "1,0,0,0"
                                    elif nucleotide == "C":
                                        maizeA_cuarteto = "0,1,0,0"
                                    elif nucleotide == "G":
                                        maizeA_cuarteto = "0,0,1,0"
                                    elif nucleotide == "T":
                                        maizeA_cuarteto = "0,0,0,1"
                                    else :
                                        maizeA_cuarteto = "0,0,0,0"
                        else:
                            maizeA_cuarteto = "0,0,0,0"
                    else:
                        maizeA_cuarteto = "0,0,0,0"


                    ##################### MAIZE B ########################

                    if presenceMaizeB == "YES":
                        os.system("seqkit faidx -r tmp1 maizeB > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:
                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        maizeB_cuarteto = "1,0,0,0"
                                    elif nucleotide == "C":
                                        maizeB_cuarteto = "0,1,0,0"
                                    elif nucleotide == "G":
                                        maizeB_cuarteto = "0,0,1,0"
                                    elif nucleotide == "T":
                                        maizeB_cuarteto = "0,0,0,1"
                                    else:
                                        maizeB_cuarteto = "0,0,0,0"
                        else:
                            maizeB_cuarteto = "0,0,0,0"
                    else:
                        maizeB_cuarteto = "0,0,0,0"


                    ##################### SETARIA ########################

                    if presenceSetaria == "YES":
                        os.system("seqkit faidx -r tmp1 setaria > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:

                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        setaria_cuarteto = "1,0,0,0"
                                    elif nucleotide == "C":
                                        setaria_cuarteto = "0,1,0,0"
                                    elif nucleotide == "G":
                                        setaria_cuarteto = "0,0,1,0"
                                    elif nucleotide == "T":
                                        setaria_cuarteto = "0,0,0,1"
                                    else:
                                        setaria_cuarteto = "0,0,0,0"
                        else:
                            setaria_cuarteto = "0,0,0,0"

                    else:
                        setaria_cuarteto = "0,0,0,0"


                    imprime = (sorghum_cuarteto+"\t"+maizeA_cuarteto+"\t"+maizeB_cuarteto+"\t"+setaria_cuarteto)

                else:

                    if presenceMaizeA == "YES":
                        os.system("seqkit faidx -r tmp1 maizeA > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:
                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        maizeA_cuarteto = "0,0,0,1"
                                    elif nucleotide == "C":
                                        maizeA_cuarteto = "0,0,1,0"
                                    elif nucleotide == "G":
                                        maizeA_cuarteto = "0,1,0,0"
                                    elif nucleotide == "T":
                                        maizeA_cuarteto = "1,0,0,0"
                                    else :
                                        maizeA_cuarteto = "0,0,0,0"
                        else:
                            maizeA_cuarteto = "0,0,0,0"

                    else:
                        maizeA_cuarteto = "0,0,0,0"


                    ##################### MAIZE B ########################

                    if presenceMaizeB == "NO":
                        maizeB_cuarteto = "0,0,0,0"

                    else:
                        os.system("seqkit faidx -r tmp1 maizeB > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:

                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        maizeB_cuarteto = "0,0,0,1"
                                    elif nucleotide == "C":
                                        maizeB_cuarteto = "0,0,1,0"
                                    elif nucleotide == "G":
                                        maizeB_cuarteto = "0,1,0,0"
                                    elif nucleotide == "T":
                                        maizeB_cuarteto = "1,0,0,0"
                                    else:
                                        maizeB_cuarteto = "0,0,0,0"
                        else:
                            maizeB_cuarteto = "0,0,0,0"

                    ##################### SETARIA ########################

                    if presenceSetaria == "YES":
                        os.system("seqkit faidx -r tmp1 setaria > tmp3")
                        os.system("sh /workdir/rjl278/Sorghum/Evol_model/Derived_alleles/flat2.sh")

                        if os.path.getsize("tmp4") > 0:

                            with open("tmp4") as f:
                                next(f)
                                for line in f:
                                    nucleotide = (line[int(Posicionalineada)])
                                    #print(nucleotide)
                                    if nucleotide == "A":
                                        setaria_cuarteto = "0,0,0,1"
                                    elif nucleotide == "C":
                                        setaria_cuarteto = "0,0,1,0"
                                    elif nucleotide == "G":
                                        setaria_cuarteto = "0,1,0,0"
                                    elif nucleotide == "T":
                                        setaria_cuarteto = "1,0,0,0"
                                    else:
                                        setaria_cuarteto = "0,0,0,0"

                        else:
                            setaria_cuarteto = "0,0,0,0"

                    else:
                        setaria_cuarteto = "0,0,0,0"



                    imprime = (sorghum_cuarteto+"\t"+maizeA_cuarteto+"\t"+maizeB_cuarteto+"\t"+setaria_cuarteto)
            else:
                imprime = (sorghum_cuarteto+"\t"+"0,0,0,0"+"\t"+"0,0,0,0"+"\t"+"0,0,0,0")


            os.system('rm tmp*')
            os.system('rm maize*')
            os.system('rm alpos')
            os.system('rm coordinates')
            os.system('rm letter')
            os.system('rm nuncaloveras')
            os.system('rm align.tmp')
            os.system('rm exon*')
            os.system('rm *.fa')
            os.system('rm pos*')

        salida = "DAF_"+ Numero + ".results"
        Resultados= open(salida, "a")
        Resultados.write(imprime)
        Resultados.write("\n")
