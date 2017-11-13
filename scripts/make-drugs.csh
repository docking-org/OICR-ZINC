# make drugs
#
setenv ZINC_CONFIG_OVERRIDE ~/.zinc15/oicr-override.cfg
./fetchdrugs.py > drugs.txt 
grep _HUMAN drugs.txt > drugs.ldjson
