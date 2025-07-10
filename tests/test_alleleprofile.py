import pytest

from exceptions.fhir import (
    InvalidMoleculeTypeError,
    LocationCardinalityError,
    MissingAlleleStateError,
    MissingFocusCodingError,
    RepresentationCardinalityError,
)
from profiles.allele import Allele as FhirAllele


@pytest.fixture
def example_allele_profile():
    return {
    "resourceType" : "MolecularDefinition",
    "id" : "example-allelesliced-cyp2c19-1016",
    "meta" : {
      "profile" : ["http://hl7.org/fhir/StructureDefinition/allelesliced"]
    },
    "moleculeType" : {
      "coding" : [{
        "system" : "http://hl7.org/fhir/sequence-type",
        "code" : "dna",
        "display" : "DNA Sequence"
      }]
    },
    "location" : [
        {
      "sequenceLocation" : {
        "sequenceContext" : {
          "reference" : "MolecularDefinition/example-sequence-nm0007694-url",
          "type" : "MolecularDefinition",
          "display" : "Starting Sequence Resource: (CYP2C19), mRNA, NM_000769.4"
        },
        "coordinateInterval" : {
          "coordinateSystem" : {
            "system" : {
              "coding" : [{
                "system" : "http://loinc.org",
                "code" : "LA30102-0",
                "display" : "1-based character counting"
              }],
              "text" : "1-based character counting"
            }
          },
          "startQuantity" : {
            "value" : 1016
          }
        }
      }
    }
    ],
    "representation" : [{
      "focus" : {
        "coding" : [{
          "system" : "http://hl7.org/fhir/moleculardefinition-focus",
          "code" : "allele-state",
          "display" : "Allele State"
        }]
      },
      "code" : [{
        "coding" : [{
          "system" : "https://www.pharmvar.org",
          "code" : "*1",
          "display" : "*1"
        }]
      }],
      "literal" : {
        "value" : "G"
      }
    },
    {
      "focus" : {
        "coding" : [{
          "system" : "http://hl7.org/fhir/moleculardefinition-focus",
          "code" : "context-state",
          "display" : "Context State"
        }]
      },
      "literal" : {
        "value" : "A"
      }
    }]
  }


def test_missing_moleculeType(example_allele_profile):
    example_allele_profile.pop("moleculeType")
    with pytest.raises(InvalidMoleculeTypeError, match=r"The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele."):
        FhirAllele(**example_allele_profile)

def test_missing_location(example_allele_profile):
    example_allele_profile.pop("location")
    with pytest.raises(LocationCardinalityError, match=r"The `location` field must contain exactly one item. `location` has a 1..1 cardinality for Allele."):
        FhirAllele(**example_allele_profile)

def test_missing_representation(example_allele_profile):
    example_allele_profile.pop("representation")
    with pytest.raises(RepresentationCardinalityError, match=r"The `representation` field must contain exactly one item. `representation` has a 1..* cardinality for Allele."):
        FhirAllele(**example_allele_profile)

def test_missing_allele_state_code(example_allele_profile):
    example_allele_profile["representation"][0]["focus"]["coding"][0]["code"] = "random-state"
    with pytest.raises(MissingAlleleStateError, match=r"At least one 'allele-state' must be present in 'focus.coding'."):
        FhirAllele(**example_allele_profile)

def test_missing_allele_state_system(example_allele_profile):
    example_allele_profile["representation"][0]["focus"]["coding"][0]["system"] = None
    with pytest.raises(MissingFocusCodingError, match=r"Each 'allele-state' coding entry must have a 'system' defined."):
        FhirAllele(**example_allele_profile)

def test_missing_context_state_system(example_allele_profile):
    example_allele_profile["representation"][1]["focus"]["coding"][0]["system"] = None
    with pytest.raises(MissingFocusCodingError, match=r"Each 'context-state' coding entry must have a 'system' defined."):
        FhirAllele(**example_allele_profile)
