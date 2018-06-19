#!/bin/bash

#################### License ##########################
license=cbsulogin2.tc.cornell.edu:8990
export SENTIEON_LICENSE=$license
RELEASE=/programs/sentieon-genomics-201711.01
#######################################################

$RELEASE/bin/sentieon driver -t 60 -r /workdir/rjl278/Sorghum/WGS/DB/Sbicolor_313_v3.0.fa --algo GVCFtyper TERRA_485.vcf\
	GVCFs_links/*.gvcf --call_conf 30 --emit_conf 30
