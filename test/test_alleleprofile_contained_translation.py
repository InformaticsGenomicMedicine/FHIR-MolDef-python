import pytest

from moldeftranslator.allele_translator import VrsFhirAlleleTranslation
from profiles.alleleprofile import AlleleProfile


@pytest.fixture
def example():
    return {
    "resourceType": "MolecularDefinition",
    # This is the ID for the whole example
    "id": "TBD-THIS-IS-A-DEMO-EXAMPLE",
    # In this example the contained list contains the sequence that we are referncing to in the Allele Profile
    "contained": [
        {
            "resourceType": "MolecularDefinition",
            # This is the id for the SequenceProfile 
            "id": "example-sequence-nc000002-acc",
            "moleculeType": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sequence-type",
                        "code": "dna",
                        "display": "DNA Sequence",
                    }
                ]
            },
            # Remember SequenceProfile dones't include a location or memeberState only.
            "representation": [
                {
                    "code": [
                        {
                            "coding": [
                                {
                                    "system": "http://www.ncbi.nlm.nih.gov/refseq",
                                    # This is were we need to capture the reference sequence
                                    "code": "NC_000002.12",
                                    "display": "TBD-THIS IS A DEMO EXAMPLE",
                                }
                            ]
                        }
                    ]
                }
            ],
        }
    ],
    "moleculeType": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sequence-type",
                # This is were we currently capture the code, but might potentially need to capture it from the sequence value. 
                "code": "dna",
                "display": "DNA Sequence",
            }
        ]
    },
    "location": [
        {
            "sequenceLocation": {
                "sequenceContext": {
                    "reference": "#example-sequence-nm0007694-acc",
                    "type": "MolecularDefinition",
                    "display": "TBD-THIS IS A DEMO EXAMPLE",
                },
                "coordinateInterval": {
                    "coordinateSystem": {
                        "system": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "LA30100-4",
                                    # This is where we will identify the type of indexing
                                    "display": "0-based interval counting",
                                }
                            ],
                            "text": "0-based interval counting",
                        }
                    },
                    # start value
                    "startQuantity": {"value": 27453448},
                    # end value 
                    "endQuantity": {"value": 27453449},
                },
            }
        }
    ],
    "representation": [
        {
            "focus": {
                "coding": [
                    {
                        "code": "allele-state",
                        "display": "Allele State",
                        # Based off of the cardinality of AlleleSplice, system is required because it has a cardinality of 1..1
                        "system": "TBD"
                    }
                ]
            },
            "literal": {
                # We capture the sequence value from allele-state and not the context-state. 
                "value": "T",
            },
        }
    ],
}

@pytest.fixture
def allele_translator():
    return VrsFhirAlleleTranslation()

@pytest.fixture
def allele_profile(example):
    return AlleleProfile(**example)

@pytest.fixture
def vrs_expected_outputs():
    return {
        True: {
    "_id": "ga4gh:VA.fXvhngewkkyVwzEeSJRr5tro8Jcol6Q-",
    "type": "Allele",
    "location": {
        "_id": "ga4gh:VSL.nLMbYalHO4OEI2axqkyTMCQxrH98UpDN",
        "type": "SequenceLocation",
        "sequence_id": "ga4gh:SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g",
        "interval": {
            "type": "SequenceInterval",
            "start": {"type": "Number", "value": 27453448},
            "end": {"type": "Number", "value": 27453449},
        },
    },
    "state": {"type": "LiteralSequenceExpression", "sequence": "T"},
},
        False: {  # Unnormalized output
            "type": "Allele",
            "location": {
                "type": "SequenceLocation",
                "sequence_id": "refseq:NC_000002.12",
                "interval": {
                    "type": "SequenceInterval",
                    "start": {"type": "Number", "value": 27453448},
                    "end": {"type": "Number", "value": 27453449}
                }
            },
            "state": {"type": "LiteralSequenceExpression", "sequence": "T"}
        }
    }

@pytest.mark.parametrize("normalize", [True, False])
def test_translate_allele_profile(allele_translator, allele_profile, vrs_expected_outputs, normalize):
    output_dict = allele_translator.translate_contained_allele_profile_to_vrs_allele(
        allele_profile, normalize=normalize
    ).as_dict()

    assert output_dict == vrs_expected_outputs[normalize]




