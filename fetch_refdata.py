#!/usr/bin/env python3
import json

import requests


def query_results(query: str) -> list[dict]:
    return requests.post('https://staging.gss-data.org.uk/sparql',
                         headers={'Accept': 'application/sparql-results+json'},
                         data={'query': query}
                         ).json()['results']['bindings']


dims = [
    d['d']['value'] for d in query_results(
        'SELECT DISTINCT * { ?d a <http://purl.org/linked-data/cube#DimensionProperty> }')
    if d['d']['value'] != 'http://purl.org/linked-data/cube#measureType'
]

attrs = [
    a['a']['value'] for a in query_results(
        'SELECT DISTINCT * { ?a a <http://purl.org/linked-data/cube#AttributeProperty> }')
]

units = [
    u['u']['value'] for u in query_results(
        'SELECT DISTINCT * { [] <http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure> ?u }')
]

with open('external.json', 'r') as ext_file:
    ext_defs = json.load(ext_file)

ext_defs['definitions']['dim_ext_uri'] = {
    "$id": "#dim_ext_uri",
    "type": "string",
    "format": "uri",
    "enum": dims
}

ext_defs['definitions']['attr_ext_uri'] = {
    "$id": "#attr_ext_uri",
    "type": "string",
    "format": "uri",
    "enum": attrs
}

ext_defs['definitions']['unit_ext_uri'] = {
    "$id": "#attr_ext_uri",
    "type": "string",
    "format": "uri",
    "enum": units
}

with open('external.json', 'w') as ext_file:
    json.dump(ext_defs, ext_file, indent=4)
