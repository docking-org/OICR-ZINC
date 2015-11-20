# make drugs
#
./fetchdrugs.py L01 > drugs-L01.ldjson
./fetchdrugs.py 'L02' > drugs-L02.ldjson
cat drugs-L0?.ldjson | sort -u > drugs.ldjson
