dta <- read.table('intervals_midpoints_gene_names_length.bed', sep='\t', header=FALSE)

# User-defined
MYbreaks = 50

pdf('distrib_window_size.pdf', width=15)

a <- hist(dta[,5], breaks = MYbreaks, freq=FALSE, plot=FALSE)
Mynames = a$mids
Mynames[which(a$counts == 0)] <- '.'
barplot(a$counts/sum(a$counts), names.arg = Mynames, ylim = c(0,1), las=2)

length(which(dta[,5] > 1000000)) # only 28 genes have windows larger than 1Mb
# a$counts[1] is 31'745bp
length(which(dta[,5] > a$counts[1])) # only 3705 genes have a window larger than 31'745bp
length(which(dta[,5] > a$counts[1]))/sum(a$counts) # and they represent only 10.89 of the genes
# So for ~ 90% of the genes, the window size is below 31kb

dta2 <- dta[which(dta[,5] < a$counts[1]), ]
b <- hist(dta2[,5], breaks = 50, freq=FALSE, plot=FALSE)
Mynames = b$mids
Mynames[which(b$counts == 0)] <- '.'
barplot(b$counts/sum(b$counts), names.arg = Mynames, ylim = c(0,0.05), las=2)

dev.off()


# sed -n -e 33765,33771p -e 23992,23999p  sorted_sorghum_v3_genes_in_builtCHRM.bed
