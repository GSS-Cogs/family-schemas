#!/usr/bin/env python3
import json

import requests


def query_results(query: str) -> list[dict]:
    return [
        res['v']['value'] for res in requests.post(
            'https://staging.gss-data.org.uk/sparql',
            headers={'Accept': 'application/sparql-results+json'},
            data={'query': query}
        ).json()['results']['bindings']
    ]


with open('external.json', 'r') as ext_file:
    ext_defs = json.load(ext_file)

ext_defs['definitions'] = {
    "dim_ext_uri": {
        "$id": "#dim_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            d for d in query_results(
                'SELECT DISTINCT * { ?v a <http://purl.org/linked-data/cube#DimensionProperty> }')
            if d != 'http://purl.org/linked-data/cube#measureType'
        ]
    },
    "attr_ext_uri": {
        "$id": "#attr_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": query_results(
            'SELECT DISTINCT * { ?v a <http://purl.org/linked-data/cube#AttributeProperty> }')
    },
    "unit_ext_uri": {
        "$id": "#unit_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": query_results(
            'SELECT DISTINCT * { [] <http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure> ?v }')
    },
    "meas_ext_uri": {
        "$id": "#meas_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": query_results(
            'SELECT DISTINCT * { [] <http://purl.org/linked-data/cube#measureType> ?v }')
    },
    "cs_ext_uri": {
        "$id": "#cs_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": query_results(
            'SELECT DISTINCT * { ?v a <http://www.w3.org/2004/02/skos/core#ConceptScheme> }')
    }
}

with open('external.json', 'w') as ext_file:
    json.dump(ext_defs, ext_file, indent=4)
