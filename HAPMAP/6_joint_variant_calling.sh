### Extract only the SNPs on the 10 main chromosomes
vcftools --vcf all.vcf --remove-indels --chr Chr01 --chr Chr02 --chr Chr03 --chr Chr04 --chr Chr05 --chr Chr06 --chr Chr07 --chr Chr08 --chr Chr09 --chr Chr10 --recode --out SNP
mv SNP.recode.vcf SNP.vcf

vcftools --vcf SNP.vcf --max-alleles 2 --recode --out SNP_bial;
mv SNP_bial.recode.vcf SNP_bial.vcf;

rm SNP.vcf all.vcf all.vcf.idx SNP.log
