#!/nfs/soft/www/apps/zinc15/envs/production/bin/python
# fetchdrugs.py

import os,sys
import logging
from collections import namedtuple
from zinc.data.models.core import undefer
from zinc.management import build_context
from zinc.data.representations import object_formatter

code =sys.argv[1]

build_context(context=globals(),environ=os.environ)
logging.basicConfig(level=logging.INFO)
fields = [
   "inchikey","name","synonyms","atc_classifications", "genes", "trials", "zinc_id", "drug_class", "external_references", "image_url", 
]

formatter = object_formatter('ldjson', fields)

Record = namedtuple('Record',fields)

q = Substance.query.filter(Substance.atc_code_names.in_([code]))
q = q.options(undefer(Substance.inchikey))
q = q.yield_per(100)

logging.info(str(q))

def create_record(query):
    for result in query:
        data = {}
        data['inchikey'] = result.inchikey
        data['name'] = result.preferred_name
        data['synonyms'] = result.synonym_names
        data['atc_classifications'] = [atc.__json__() for atc in result.atc_classifications]
        data['genes'] = result.gene_names
        data['trials'] = [trial.code for trial in result.trials.with_subsets(['cancer'])]
        data['zinc_id'] = result.zinc_id
        data['drug_class'] = ''
        features=result.features or ()
        if 'fda' in features:
            data['drug_class'] = 'fda'
        elif 'world' in features:
            data['drug_class'] = 'world'
        elif 'investigational' in features:
            data['drug_class'] = 'investigational'
        elif 'in-man' in features:
            data['drug_class'] = 'in-man'
        data['external_references'] = {}
        data['external_references']['drugbank'] = [item.supplier_code for item in result.catitems.filter_by(catalog_short_name='dball')]
        data['external_references']['chembl'] = [item.supplier_code for item in result.catitems.filter_by(catalog_short_name='chembl20')]
        data['image_url'] = 'http://zinc15.docking.org/substances/{0.zinc_id}.png'.format(result)
        record=Record(**data) 
	yield record
 
records = create_record(q)
for line in formatter(records):
    print line,


