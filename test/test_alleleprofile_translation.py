import pytest

from translators.allele_translator import VrsFhirAlleleTranslation
from profiles.allele import Allele as FhirAllele


@pytest.fixture
def example():
    return {
    "resourceType": "MolecularDefinition",
    "contained": [
        {
            "resourceType": "MolecularDefinition",
            "moleculeType": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sequence-type",
                        "code": "dna",
                        "display": "DNA Sequence"
                    }
                ]
            },
            "representation": [
                {
                    "code": [
                        {
                            "coding": [
                                {
                                    "system": "http://www.ncbi.nlm.nih.gov/refseq",
                                    "code": "NC_000002.12"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "moleculeType": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sequence-type",
                "code": "dna",
                "display": "DNA Sequence"
            }
        ]
    },
    "location": [
        {
            "sequenceLocation": {
                "sequenceContext": {
                    "reference": "MolecularDefinition/example-sequence-nc000002-url",
                    "type": "MolecularDefinition",
                },
                "coordinateInterval": {
                    "coordinateSystem": {
                        "system": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "LA30100-4",
                                    "display": "0-based interval counting"
                                }
                            ]
                        }
                    },
                    "startQuantity": {
                        "value": 27453448
                    },
                    "endQuantity": {
                        "value": 27453449
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
                        "system": "http://hl7.org/fhir/moleculardefinition-focus",
                        "code": "allele-state",
                        "display": "Allele State"
                    }
                ]
            },
            "literal": {
                "value": "T"
            }
        }
    ]
}

@pytest.fixture
def allele_translator():
    return VrsFhirAlleleTranslation()

@pytest.fixture
def allele_profile(example):
    return FhirAllele(**example)

@pytest.fixture
def vrs_expected_outputs():
    return {
        True: {  # Normalized output
            "_id": "ga4gh:VA.fXvhngewkkyVwzEeSJRr5tro8Jcol6Q-",
            "type": "Allele",
            "location": {
                "_id": "ga4gh:VSL.nLMbYalHO4OEI2axqkyTMCQxrH98UpDN",
                "type": "SequenceLocation",
                "sequence_id": "ga4gh:SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g",
                "interval": {
                    "type": "SequenceInterval",
                    "start": {"type": "Number", "value": 27453448},
                    "end": {"type": "Number", "value": 27453449}
                }
            },
            "state": {"type": "LiteralSequenceExpression", "sequence": "T"}
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
    output_dict = allele_translator.translate_allele_profile_to_vrs_allele(
        allele_profile, normalize=normalize
    ).as_dict()

    assert output_dict == vrs_expected_outputs[normalize]
