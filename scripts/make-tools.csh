# script to export tool compounds
#
wget -o logs/log12 -O toolcompounds.txt "http://zinc15.docking.org/substances/having/tools.ldjson?count=all&sort=no&output_fields=inchikey+preferred_name+synonyms+atc_classifications+genes+trials+zinc_id+references+tools"


