#!/usr/bin/env python3
import json
import re

import requests


def query_results(query: str) -> list[str]:
    return [
        res['v']['value'] for res in requests.post(
            'https://staging.gss-data.org.uk/sparql',
            headers={'Accept': 'application/sparql-results+json'},
            data={'query': query}
        ).json()['results']['bindings']
    ]


with open('external.json', 'r') as ext_file:
    ext_defs = json.load(ext_file)


LOCAL_DEF = re.compile(r'gss_data/.*#')

ext_defs['definitions'] = {
    "dim_ext_uri": {
        "$id": "#dim_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            uri for uri in query_results(
                'SELECT DISTINCT * { ?v a <http://purl.org/linked-data/cube#DimensionProperty> }')
            if uri != 'http://purl.org/linked-data/cube#measureType' and LOCAL_DEF.search(uri) is None
        ]
    },
    "attr_ext_uri": {
        "$id": "#attr_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            uri for uri in query_results(
                'SELECT DISTINCT * { ?v a <http://purl.org/linked-data/cube#AttributeProperty> }')
            if LOCAL_DEF.search(uri) is None
        ]
    },
    "unit_ext_uri": {
        "$id": "#unit_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            uri for uri in query_results(
                'SELECT DISTINCT * { [] <http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure> ?v }')
            if LOCAL_DEF.search(uri) is None
        ]
    },
    "meas_ext_uri": {
        "$id": "#meas_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            uri for uri in query_results(
                'SELECT DISTINCT * { [] <http://purl.org/linked-data/cube#measureType> ?v }')
            if LOCAL_DEF.search(uri) is None
        ]
    },
    "cs_ext_uri": {
        "$id": "#cs_ext_uri",
        "type": "string",
        "format": "uri",
        "enum": [
            uri for uri in query_results(
                'SELECT DISTINCT * { ?v a <http://www.w3.org/2004/02/skos/core#ConceptScheme> }')
            if LOCAL_DEF.search(uri) is None
        ]
    }
}

with open('external.json', 'w') as ext_file:
    json.dump(ext_defs, ext_file, indent=4)
