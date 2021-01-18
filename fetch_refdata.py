#!/usr/bin/env python3
import json

import requests

dims = [d['d']['value'] for d in
        requests.post('https://staging.gss-data.org.uk/sparql',
                     headers={'Accept': 'application/sparql-results+json'},
                     data={'query': 'SELECT DISTINCT * { ?d a <http://purl.org/linked-data/cube#DimensionProperty> }'}
                     ).json()['results']['bindings']
        if d['d']['value'] != 'http://purl.org/linked-data/cube#measureType'
        ]

with open('external.json', 'r') as ext_file:
    ext_defs = json.load(ext_file)

ext_defs['definitions']['dim_ext_uri'] = {
    "$id": "#dim_ext_uri",
    "type": "string",
    "format": "uri",
    "enum": dims
}

with open('external.json', 'w') as ext_file:
    json.dump(ext_defs, ext_file, indent=4)
