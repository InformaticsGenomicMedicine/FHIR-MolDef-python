#source: https://github.com/cancervariants/metakb/blob/staging/server/tests/conftest.py#L548 
#made up example data but extra
example_synthetic_data={
        "id": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
        "name": "V600E", 
        "description": "BRAF V600E variant",
        "digest": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L", 
        "expressions": [
            {
            "id": "expression:1", 
            "syntax": "hgvs.p",
            "value": "NP_004324.2:p.Val600Glu",
            "syntax_version": "21.0" 
            }
        ],
        "aliases": ["VAL600GLU", "V640E", "VAL640GLU" ], 
        "extensions": [
            {
                "name": "civic_variant_url",
                "value": "civicdb.org/links/variants/12",
                "description": "CIViC Variant URL",
                "extensions": [
                        {   "id": "extension.sub_extension:1",
                            "name": "extension.sub_extension.name",
                            "value":"extension.sub_extension.value",
                            "description": "extension.sub_extension.description"
                        }
                ]
            }
        ],
        "location": {
            "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
            "name": "NP_004324.2",
            "description": "My location description",
            "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
            "type": "SequenceLocation",
            "sequenceReference": {
                "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
                "type": "SequenceReference",
                "residueAlphabet": "aa",
                "moleculeType": "protein",
                "circular": False,
                "sequence": "V", # A sequenceString that is a literal representation of the referenced sequence.
                "extensions": [
                    {   
                        "id": "sequence_reference.extension:1",
                        "name": "sequence_reference.name",
                        "value": "sequence_reference.value",
                        "description": "sequence_reference.description",
                        "extensions": [
                            {   "id": "sequence_reference.sub_extension:1",
                                "name": "sequence_reference.sub_extension.name",
                                "value":"sequence_reference.sub_extension.value",
                                "description": "sequence_reference.sub_extension.description"
                            }
                        ] 
                    }
                ]
            },
            "aliases": ["Ensembl:ENSP00000288602.6"],
            "start": 599,
            "end": 600,
            "sequence": "V", # The literal sequence encoded by the sequenceReference at these coordinates.
            "extensions": [
                {   
                    "id": "sequence_location.extension:1",
                    "name": "sequence_location.name",
                    "value": "sequence_location.value",
                    "description": "sequence_location.description",
                    "extensions": [
                        {   "id": "sequence_location.sub_extension:1",
                            "name": "sequence_location.sub_extension.name",
                            "value":"sequence_location.sub_extension.value",
                            "description": "sequence_location.sub_extension.description"
                        }
                    ] 
                }
            ]
        },
        "state": {
            "id": "state:1",
            "name": "state",
            "description": "My description for state",
            "sequence": "E", 
            "type": "LiteralSequenceExpression",
            "extensions":[
                {   
                    "id": "state.extension:1",
                    "name": "state.name",
                    "value": "state.value",
                    "description": "state.description",
                    "extensions": [
                        {   "id": "state.sub_extension:1",
                            "name": "state.sub_extension.name",
                            "value":"state.sub_extension.value",
                            "description": "state.sub_extension.description"
                        }
                    ] 
                },
            ],
            "aliases": ["my_sequence"]
        },
    }
