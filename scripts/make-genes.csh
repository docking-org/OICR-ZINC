# genes:

wget -o logs/log5 -O genes.txt "http://zinc15.docking.org/orthologs/having/substances.ldjson?related.trials-memberof=cancer&organism_name=Eukaryotes&count=all"

wget -o logs/log11 -O genes2.txt "http://zinc15.docking.org/orthologs.ldjson?substances-any-atc_code_names-in=L02+L01&count=all&sort=no"

#grep _HUMAN genes.txt > genes.ldjson

cat  genes.txt genes2.txt | sort -u > genes.ldjson
