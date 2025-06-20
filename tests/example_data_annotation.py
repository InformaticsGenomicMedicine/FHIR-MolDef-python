#source: https://github.com/cancervariants/metakb/blob/staging/server/tests/conftest.py#L548 
# This file is the annotation of what was inputed in the jupyter notebook: full_vrs_trans.ipynb


# This is the input data used in the full_vrs_trans.py script.
# Note: We are currently unable to translate the extensions in the metadata of the VRS allele,
# so that part is currently commented out below.
# This script will annotate the mappings for VRS Allele 2.0 and the FHIR Allele profile.
input_vrs_data = {
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
            "syntax_version": "21.0",
            "extensions": [
                {
                    "id": "sub-expression:1", 
                    "name": "expression.name.1", 
                    "value": "expression.value.1",
                    "description": "expression.description.1",
                    "extensions": [
                        {
                            "id": "sub-sub-expression:2",
                            "name": "expression.sub.name.2",
                            "value": "expression.sub.value,2",
                            "description": "expression.description.2"
                        }
                    ]
                }
            ]
        }
    ],
    "aliases": ["VAL600GLU", "V640E", "VAL640GLU"],
    #TODO: A translation was not created for this yet
    # "extensions": [
    #     {
    #         "name": "civic_variant_url",
    #         "value": "civicdb.org/links/variants/12",
    #         "description": "CIViC Variant URL",
    #         "extensions": [
    #             {
    #                 "id": "extension.sub_extension:1",
    #                 "name": "extension.sub_extension.name",
    #                 "value": "extension.sub_extension.value",
    #                 "description": "extension.sub_extension.description"
    #             }
    #         ]
    #     }
    # ],
    "location": {
        "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "name": "NP_004324.2",
        "description": "My location description",
        "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "type": "SequenceLocation",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "name": "sequence_reference.name",
            'aliases':["sequence_reference.aliase"],
            'description': 'sequence_reference.description',
            "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
            "type": "SequenceReference",
            "residueAlphabet": "aa",
            "moleculeType": "protein",
            "circular": False,
            "sequence": "V", # A sequenceString that is a literal representation of the referenced sequence.
            "extensions": [
                {
                    "id": "sequence_reference.extension:1",
                    "name": "sequence_reference.extension.name",
                    "value": "sequence_reference.extension.value",
                    "description": "sequence_reference.extension.description",
                    "extensions": [
                        {
                            "id": "sequence_reference.sub_extension:1",
                            "name": "sequence_reference.sub_extension.name",
                            "value": "sequence_reference.sub_extension.value",
                            "description": "sequence_reference.sub_extension.description"
                        }
                    ]
                }
            ]
        },
        "aliases": ["Ensembl:ENSP00000288602.6"],
        "start": 599,
        "end": 600,
        "sequence": "V",# The literal sequence encoded by the sequenceReference at these coordinates.
        "extensions": [
            {
                "id": "sequence_location.extension:1",
                "name": "sequence_location.name",
                "value": "sequence_location.value",
                "description": "sequence_location.description",
                "extensions": [
                    {
                        "id": "sequence_location.sub_extension:1",
                        "name": "sequence_location.sub_extension.name",
                        "value": "sequence_location.sub_extension.value",
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
        "extensions": [
            {
                "id": "state.extension:1",
                "name": "state.name",
                "value": "state.value",
                "description": "state.description",
                "extensions": [
                    {
                        "id": "state.sub_extension:1",
                        "name": "state.sub_extension.name",
                        "value": "state.sub_extension.value",
                        "description": "state.sub_extension.description"
                    }
                ]
            }
        ],
        "aliases": ["my_sequence"]
    }
}

# This output is generated by converting the original VRS value (input_vrs_data) into a FHIR allele profile.
output_fhir__data = {
  "resourceType": "MolecularDefinition",
  "contained": [
    { # This contained value is coming from vrs.location.sequence 
      "resourceType": "MolecularDefinition",
      "id": "vrs-location-sequence", # Hardcoded value
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
      "id": "vrs-location-sequenceReference", # Hardcoded value
      "extension": [
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/id",
          "valueString": "sequence_reference.id"
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/name",
          "valueString": "sequence_reference.name"
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/description",
          "valueString": "sequence_reference.description"
        },
        {
          "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/aliases",
          "valueString": "sequence_reference.aliase"
        },
        {
          "id": "sequence_reference.extension:1",
          "extension": [
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
              "valueString": "sequence_reference.extension.name"
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
              "valueString": "sequence_reference.extension.value"
            },
            {
              "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
              "valueString": "sequence_reference.extension.description"
            },
            {
              "id": "sequence_reference.sub_extension:1",
              "extension": [
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                  "valueString": "sequence_reference.sub_extension.name"
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                  "valueString": "sequence_reference.sub_extension.value"
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                  "valueString": "sequence_reference.sub_extension.description"
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
            "code": "protein"
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
                  "code": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y"
                }
              ]
            }
          ],
          "literal": {
            "encoding": {
              "coding": [
                {
                  "system": "vrs 2.0 codes for alphabet",
                  "code": "aa"
                }
              ]
            },
            "value": "V"
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
        "sequenceContext": { # TODO: double check this:sequenceLocation.sequenceContext is a 1..1 so then how would we be able to have mulitple conatined valued?
          "reference": "#vrs-location-sequence", #TODO: double check this
          "type": "Sequence", #TODO: double check this 
          "display": "VRS location.sequence as contained FHIR Sequence" #TODO: double check this
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
          "extension": [
            {
              "id": "sub-expression:1", # vrs.expressions.extensions.id 
              "extension": [
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                  "valueString": "expression.name.1" # vrs.expressions.extensions.name 
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                  "valueString": "expression.value.1" # vrs.expressions.extensions.value 
                },
                {
                  "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                  "valueString": "expression.description.1" # vrs.expressions.extensions.description  
                },
                {
                  "id": "sub-sub-expression:2", # vrs.expressions.extensions.extensions.id  
                  "extension": [
                    {
                      "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                      "valueString": "expression.sub.name.2" # vrs.expressions.extensions.extensions.name 
                    },
                    {
                      "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                      "valueString": "expression.sub.value,2" # vrs.expressions.extensions.extensions.value 
                    },
                    {
                      "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                      "valueString": "expression.description.2" # vrs.expressions.extensions.extensions.description
                    }
                  ]
                }
              ]
            }
          ],
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

#The following output shows the result of taking that FHIR allele profile (output_fhir_data) and converting it back to VRS, completing a round trip.
round_trip_back_to_vrs = {
  "id": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",  # fhir.allele.identifier.system & fhir.allele.identifier.value
  "type": "Allele",
  "name": "V600E",  # fhir.allele.identifier.system & fhir.allele.identifier.value
  "description": "BRAF V600E variant",  # fhir.allele.description
  "aliases": ["VAL600GLU", "V640E", "VAL640GLU"],  # fhir.allele.identifier.system & fhir.allele.identifier.value
  "extensions": None,  # Not translateable yet
  "digest": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",  # fhir.allele.identifier.system & fhir.allele.identifier.value
  "expressions": [
    {
      "id": "expression:1", # fhir.allele.representation.code.id
      "extensions": [
        {
          "id": "sub-expression:1", # fhir.allele.representation.code.extension.id
          "extensions": [
            {
              "id": "sub-sub-expression:2", # fhir.allele.representation.code.extension.extension.id
              "extensions": None,
              "name": "expression.sub.name.2", # fhir.allele.representation.code.extension.extension.name
              "value": "expression.sub.value,2", # fhir.allele.representation.code.extension.extension.value
              "description": "expression.description.2" # fhir.allele.representation.code.extension.extension.description
            }
          ],
          "name": "expression.name.1", # fhir.allele.representation.code.extension.name
          "value": "expression.value.1", # fhir.allele.representation.code.extension.value
          "description": "expression.description.1" # fhir.allele.representation.code.extension.description
        }
      ],
      "syntax": "hgvs.p", # fhir.allele.representation.code.coding.display
      "value": "NP_004324.2:p.Val600Glu", # fhir.allele.representation.code.coding.code
      "syntax_version": "21.0" # fhir.allele.representation.code.coding.version
    }
  ],
  "location": {
    "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",  # fhir.allele.location[0].id
    "type": "SequenceLocation",
    "name": "NP_004324.2", # fhir.allele.location[0].extension[0].url & fhir.allele.location[0].extension[0].value
    "description": "My location description", # fhir.allele.location[0].extension[0].url & fhir.allele.location[0].extension[0].value
    "aliases": ["Ensembl:ENSP00000288602.6"], # fhir.allele.location[0].extension[0].url & fhir.allele.location[0].extension[0].value
    "extensions": [
      {
        "id": "sequence_location.extension:1", # fhir.allele.location[0].extension[4].id
        "extensions": [
          {
            "id": "sequence_location.sub_extension:1", # fhir.allele.location[0].extension[4].extension[3].id
            "extensions": None,
            "name": "sequence_location.sub_extension.name", # fhir.allele.location[0].extension[4].extension[3].extension[0].url & fhir.allele.location[0].extension[4].extension[3].extension[0].value
            "value": "sequence_location.sub_extension.value", # fhir.allele.location[0].extension[4].extension[3].extension[1].url & fhir.allele.location[0].extension[4].extension[3].extension[1].value
            "description": "sequence_location.sub_extension.description" # fhir.allele.location[0].extension[4].extension[3].extension[2].url & fhir.allele.location[0].extension[4].extension[3].extension[2].value
          }
        ],
        "name": "sequence_location.name", # fhir.allele.location[0].extension[4].extension[0].url & fhir.allele.location[0].extension[4].extension[0].value
        "value": "sequence_location.value", # fhir.allele.location[0].extension[4].extension[1].url & fhir.allele.location[0].extension[4].extension[1].value
        "description": "sequence_location.description" # fhir.allele.location[0].extension[4].extension[2].url & fhir.allele.location[0].extension[4].extension[2].value
      }
    ],
    "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y", # fhir.allele.location[0].extension[3].url & fhir.allele.location[0].extension[3].value
    "sequenceReference": {
      "id": "sequence_reference.id", #TODO: double check 
      "type": "SequenceReference", #TODO: double check 
      "name": "sequence_reference.name",  #TODO: double check 
      "description": "sequence_reference.description",  #TODO: double check 
      "aliases": ["sequence_reference.aliase"], #TODO: double check 
      "extensions": [
        {
          "id": "sequence_reference.extension:1", # fhir.allele.contained[1].extension[0].extension[3].id
          "extensions": [
            {
              "id": "sequence_reference.sub_extension:1", # fhir.allele.contained[1].extension[0].extension[3].id
              "extensions": None,
              "name": "sequence_reference.sub_extension.name", # fhir.allele.contained[1].extension[0].extension[3].extension[0].url & fhir.allele.contained[1].extension[0].extension[3].extension[0].value
              "value": "sequence_reference.sub_extension.value", # fhir.allele.contained[1].extension[0].extension[3].extension[1].url & fhir.allele.contained[1].extension[0].extension[3].extension[1].value
              "description": "sequence_reference.sub_extension.description" # fhir.allele.contained[1].extension[0].extension[3].extension[2].url & fhir.allele.contained[1].extension[0].extension[3].extension[2].value
            }
          ],
          "name": "sequence_reference.extension.name", # fhir.allele.contained[1].extension[0].extension[0].url & fhir.allele.contained[1].extension[0].extension[0].value
          "value": "sequence_reference.extension.value", # fhir.allele.contained[1].extension[0].extension[1].url & fhir.allele.contained[1].extension[0].extension[1].value
          "description": "sequence_reference.extension.description" # fhir.allele.contained[1].extension[0].extension[2].url & fhir.allele.contained[1].extension[0].extension[2].value
        }
      ],
      "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y", # fhir.allele.contained[1].representation[0].code[0].coding[0].code
      "residueAlphabet": "aa", # fhir.allele.contained[1].representation[0].literal.encoding.coding[0].code
      "circular": False, # Hardcoded value
      "sequence": "V", # fhir.allele.contained[1].representation[0].literal.value
      "moleculeType": "protein" # fhir.allele.contained[1].moleculeType.coding[0].code
    },
    "start": 599, # fhir.allele.location[0].sequenceLocation.coordinateInterval.startQuantity.value
    "end": 600, # fhir.allele.location[0].sequenceLocation.coordinateInterval.endQuantity.value
    "sequence": "V" # fhir.allele.contained[0].representation[0].literal.value
  },
  "state": {
    "id": "state:1", # fhir.allele.representation[0].literal.id
    "type": "LiteralSequenceExpression",
    "name": "state", # fhir.allele.representation[0].literal.extension.url & fhir.allele.representation[0].literal.extension.system
    "description": "My description for state",# fhir.allele.representation[0].literal.extension.url & fhir.allele.representation[0].literal.extension.system
    "aliases": ["my_sequence"], # fhir.allele.representation[0].literal.extension.url & fhir.allele.representation[0].literal.extension.system
    "extensions": [
      {
        "id": "state.extension:1", # fhir.allele.representation[0].literal.extension[3].id
        "extensions": [
          {
            "id": "state.sub_extension:1", # fhir.allele.representation[0].literal.extension[3].extension[3].id
            "extensions": None,
            "name": "state.sub_extension.name", # fhir.allele.representation[0].literal.extension[3].extension[3].extension[0].url and # fhir.allele.representation[0].literal.extension[3].extension[3].extension[0].value 
            "value": "state.sub_extension.value", # fhir.allele.representation[0].literal.extension[3].extension[3].extension[1].url and # fhir.allele.representation[0].literal.extension[3].extension[3].extension[1].value 
            "description": "state.sub_extension.description" # fhir.allele.representation[0].literal.extension[3].extension[3].extension[2].url and # fhir.allele.representation[0].literal.extension[3].extension[3].extension[2].value 
          }
        ],
        "name": "state.name", # fhir.allele.representation[0].literal.extension[3].extension[0].url and # fhir.allele.representation[0].literal.extension[3].extension[0].value 
        "value": "state.value",  # fhir.allele.representation[0].literal.extension[3].extension[1].url and # fhir.allele.representation[0].literal.extension[3].extension[1].value 
        "description": "state.description" # fhir.allele.representation[0].literal.extension[3].extension[2].url and # fhir.allele.representation[0].literal.extension[3].extension[2].value 
      }
    ],
    "sequence": "E" # fhir.allele.representation[0].literal.value
  }
}