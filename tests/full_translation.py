#source: https://github.com/cancervariants/metakb/blob/staging/server/tests/conftest.py#L548 
#made up example data but extra
example_synthetic_input={
        "id": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
        "type": "Allele",
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
                "sequence": "V", 
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
            "sequence": "V", 
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


output = {
  "resourceType": "MolecularDefinition",
  "contained": [
    { # This contained value is coming from vrs.location.sequence 
      "resourceType": "MolecularDefinition",
      "id": "vrs-location-sequence",
      "moleculeType": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/sequence-type",
            "code": "protein" # vrs.location.sequenceReference.refgetAccession
          }
        ]
      },
      "representation": [
        {
          "literal": {
            "value": "V" # vrs.location.sequence
          }
        }
      ]
    },
    { # This contained value is coming from vrs.location.sequenceReference 
      "resourceType": "MolecularDefinition",
      "extension": [
        {
          "id": "sequence_reference.extension:1", # vrs.location.sequenceReference.extensions.id
          "extension": [
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
              "valueString": "sequence_reference.name" # vrs.location.sequenceReference.extensions.name
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
              "valueString": "sequence_reference.value" # vrs.location.sequenceReference.extensions.value
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
              "valueString": "sequence_reference.description" # vrs.location.sequenceReference.extensions.description
            },
            {
              "id": "sequence_reference.sub_extension:1", # vrs.location.sequenceReference.extensions.extensions
              "extension": [
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                  "valueString": "sequence_reference.sub_extension.name" # vrs.location.sequenceReference.extensions.extensions.name
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                  "valueString": "sequence_reference.sub_extension.value" # vrs.location.sequenceReference.extensions.extensions.value
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                  "valueString": "sequence_reference.sub_extension.description" # vrs.location.sequenceReference.extensions.extensions.description
                }
              ]
            }
          ]
        }
      ],
      "moleculeType": {
        "coding": [
          {
            "system": "vrs 2.0 codes for moleculeType",
            "code": "protein" # vrs.location.sequenceReference.moleculeType
          }
        ]
      },
      "representation": [
        {
          "code": [
            {
              "coding": [
                {
                  "system": "GA4GH RefGet identifier for the referenced sequence",
                  "code": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y" # vrs.location.sequenceReference.refgetAccession
                }
              ]
            }
          ],
          "literal": {
            "encoding": {
              "coding": [
                {
                  "system": "vrs 2.0 codes for alphabet",
                  "code": "aa" # vrs.location.sequenceReference.residueAlphabet
                }
              ]
            },
            "value": "V" # vrs.location.sequenceReference.sequence
          }
        }
      ]
    }
  ],
  "identifier": [
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/id",
      "value": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L" # vrs.id
    },
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/name",
      "value": "V600E" # vrs.name
    },
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
      "value": "VAL600GLU" # vrs.aliases
    },
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
      "value": "V640E" # vrs.aliases
    },
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
      "value": "VAL640GLU" # vrs.aliases
    },
    {
      "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/digest",
      "value": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L" # vrs.digest
    }
  ],
  "description": "BRAF V600E variant", # vrs.description
  "moleculeType": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sequence-type",
        "code": "protein", # vrs.location.sequenceReference.refgetAccession
        "display": "protein Sequence"
      }
    ]
  },
  "location": [
    {
      "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y", # vrs.location.id
      "extension": [
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/name",
          "valueString": "NP_004324.2" # vrs.location.name
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/description",
          "valueString": "My location description" # vrs.location.description
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/aliases",
          "valueString": "Ensembl:ENSP00000288602.6" # vrs.location.aliases
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/digest",
          "valueString": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y" # vrs.location.digest
        },
        {
          "id": "sequence_location.extension:1", # vrs.location.extensions.id
          "extension": [
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
              "valueString": "sequence_location.name" # vrs.location.extensions.name
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
              "valueString": "sequence_location.value" # vrs.location.extensions.value
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
              "valueString": "sequence_location.description" # vrs.location.extensions.description
            },
            {
              "id": "sequence_location.sub_extension:1", # vrs.location.extensions.extensions.id
              "extension": [
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                  "valueString": "sequence_location.sub_extension.name" # vrs.location.extensions.extensions.name
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                  "valueString": "sequence_location.sub_extension.value" # vrs.location.extensions.extensions.value
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                  "valueString": "sequence_location.sub_extension.description" # vrs.location.extensions.extensions.description
                }
              ]
            }
          ]
        }
      ],
      "sequenceLocation": {
        "sequenceContext": { # sequenceLocation.sequenceContext is a 1..1 so then how would we be able to have mulitple conatined valued?
          "reference": "#vrs-location-sequence",
          "type": "Sequence",
          "display": "VRS location.sequence as contained FHIR Sequence"
        },
        "coordinateInterval": {
          "coordinateSystem": {
            "system": {
              "coding": [
                {
                  "system": "http://loinc.org", # Hardcoded value
                  "code": "LA30100-4", # Hardcoded value
                  "display": "0-based interval counting" # Hardcoded value
                }
              ]
            }
          },
          "startQuantity": {
            "value": 599.0 # vrs.location.start
          },
          "endQuantity": {
            "value": 600.0 # vrs.location.end
          }
        }
      }
    }
  ],
  "representation": [
    {
      "focus": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/moleculardefinition-focus", # Hardcoded value
            "code": "allele-state" # Hardcoded value
          }
        ]
      },
      "code": [
        {
          "id": "expression:1", #vrs.expressions.id
          "coding": [
            {
              "version": "21.0", # vrs.expressions.syntax_version
              "code": "NP_004324.2:p.Val600Glu", # vrs.expressions.value
              "display": "hgvs.p" # vrs.expressions.syntax
            }
          ]
        }
      ],
      "literal": {
        "id": "state:1", # vrs.state.id
        "extension": [
          {
            "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/name",
            "valueString": "state" # vrs.state.name
          },
          {
            "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/description",
            "valueString": "My description for state" # vrs.state.description
          },
          {
            "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/aliases",
            "valueString": "my_sequence" # vrs.state.aliases
          },
          {
            "id": "state.extension:1", # vrs.state.extensions.id
            "extension": [
              {
                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                "valueString": "state.name" # vrs.state.extensions.name
              },
              {
                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                "valueString": "state.value" # vrs.state.extensions.value
              },
              {
                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                "valueString": "state.description" # vrs.state.extensions.description
              },
              {
                "id": "state.sub_extension:1", # vrs.state.extensions.extensions.id
                "extension": [
                  {
                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                    "valueString": "state.sub_extension.name" # vrs.state.extensions.extensions.name
                  },
                  {
                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                    "valueString": "state.sub_extension.value" # vrs.state.extensions.extensions.value
                  },
                  {
                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                    "valueString": "state.sub_extension.description" # vrs.state.extensions.extensions.description
                  }
                ]
              }
            ]
          }
        ],
        "value": "E" # vrs.state.sequence
      }
    }
  ]
}
