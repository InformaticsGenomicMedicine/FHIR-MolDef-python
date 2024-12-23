import pytest
from deepdiff import DeepDiff
from src.resource.moleculardefinition import MolecularDefinition
from pydantic import ValidationError

@pytest.fixture
def example_molecular_definition():
    return {
        "resourceType": "MolecularDefinition",
        "id": "example-allele1",
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/allele"]
        },
        "moleculeType": {
            "coding": [
                {"system": "http://hl7.org/fhir/sequence-type", "code": "dna", "display": "DNA Sequence"}
            ]
        },
        "location": [
            {
                "sequenceLocation": {
                    "sequenceContext": {
                        "reference": "MolecularDefinition/example-sequence-lrg584",
                        "type": "MolecularDefinition",
                        "display": "Starting Sequence Resource: LRG_584"
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
                                ],
                                "text": "0-based interval counting"
                            }
                        },
                        "startQuantity": {"value": 5001},
                        "endQuantity": {"value": 97867}
                    }
                }
            }
        ],
        "representation": [
            {
                "relative": {
                    "startingMolecule": {
                        "reference": "MolecularDefinition/example-sequence-lrg584",
                        "type": "MolecularDefinition",
                        "display": "Starting Sequence Resource: LRG_584"
                    },
                    "edit": [
                        {
                            "coordinateSystem": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "LA30100-4",
                                        "display": "0-based interval counting"
                                    }
                                ],
                                "text": "0-based interval counting"
                            },
                            "start": 5123,
                            "end": 5124,
                            "replacementMolecule": {
                                "reference": "MolecularDefinition/example-sequence-t",
                                "type": "MolecularDefinition",
                                "display": "Replacement Sequence Resource: T"
                            },
                            "replacedMolecule": {
                                "reference": "MolecularDefinition/example-sequence-c",
                                "type": "MolecularDefinition",
                                "display": "Replaced Sequence Resource: C"
                            }
                        }
                    ]
                }
            }
        ]
    }

def test_molecular_definition(example_molecular_definition):
    moldef = MolecularDefinition(**example_molecular_definition)
    model_dumped = moldef.model_dump()
    differences = DeepDiff(example_molecular_definition, model_dumped, ignore_order=True)

    assert differences == {}, f"Differences found: {differences}"
