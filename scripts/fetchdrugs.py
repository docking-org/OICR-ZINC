#!/usr/bin/env python
# fetchdrugs.py

from collections import namedtuple
import itertools
import logging
import os
import sys
from zinc.data.models.core import joinedload
from zinc.management import build_context
from zinc.data.representations import object_formatter

#code =sys.argv[1]

build_context(context=globals(),environ=os.environ)
logging.basicConfig(level=logging.DEBUG)
fields = [
   "inchikey","name","synonyms","atc_classifications", "purchasable",
   "genes", "activities", "trials", "zinc_id", 
   "drug_class", "external_references", "image_url", 
]

formatter = object_formatter('ldjson', fields)

Record = namedtuple('Record',fields)

q = db.session.query(Substance)
#q = Substance.query.filter(Substance.atc_code_names.in_([code]))
#q = q.with_subsets(['investigational'])  # This seems to be buggy (hidden subset)
q = q.filter(Substance.features.overlap(['fda', 'world', 'investigational']))
q = q.yield_per(100)

logging.info(str(q))

def create_record(query):
    for result in query:
        human_observations = result.observations\
                .filter(Observation.ortholog_name.endswith('_HUMAN'))\
                .options(joinedload(Observation.ortholog))
        human_activities = sorted(
            ((observation.ortholog.name, int(observation.affinity)) 
                for observation in human_observations),
            key=lambda item: (item[0], -item[1])
        )
        human_activities = itertools.groupby(human_activities, key=lambda item: item[0])
        human_activities = [list(group)[0] for key, group in human_activities]
        human_activities = {ortholog: affinity for ortholog, affinity in human_activities}

        data = {}
        data['inchikey'] = result.inchikey
        data['name'] = result.preferred_name
        data['synonyms'] = result.synonym_names
        data['purchasable'] = result.purchasable >= 10
        data['atc_classifications'] = [atc.__json__() for atc in result.atc_classifications]
        data['genes'] = result.gene_names
        data['trials'] = [trial.code for trial in result.trials.with_subsets(['cancer'])]
        data['zinc_id'] = result.zinc_id
        data['activities'] = human_activities
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
        data['image_url'] = 'https://zinc15.docking.org/substances/{0.zinc_id}.png'.format(result)
        record=Record(**data) 
	yield record
 
records = create_record(q)
for line in formatter(records):
    print line,


