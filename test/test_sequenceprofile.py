import pytest
from profiles.sequenceprofile import SequenceProfile
from pydantic import ValidationError
from fhir.resources.reference import Reference

@pytest.fixture
def example_sequence_profile():
    return {
  "resourceType" : "MolecularDefinition",
  "id" : "example-sequence-c",
  "meta" : {
    "profile" : ["http://hl7.org/fhir/StructureDefinition/sequence"]
  },
  "moleculeType" : {
    "coding" : [{
      "system" : "http://hl7.org/fhir/sequence-type",
      "code" : "dna",
      "display" : "DNA Sequence"
    }]
  },
  "representation" : [{
    "literal" : {
      "value" : "C"
    }
  }]
}

def test_missing_moleculeType(example_sequence_profile):
    example_sequence_profile.pop("moleculeType")
    with pytest.raises(ValidationError, match=r"The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for SequenceProfile."):
        SequenceProfile(**example_sequence_profile)

def test_memberState_not_allowed(example_sequence_profile):
    example_sequence_profile["memberState"] = Reference(reference="test/SequenceProfile",type="test/SequenceProfile",display="NC_000002.12").model_dump()
    with pytest.raises(ValueError, match=r"`memberState` is not allowed in SequenceProfile."):
        SequenceProfile(**example_sequence_profile)

def test_location_not_allowed(example_sequence_profile):
    example_sequence_profile["location"] = {}
    with pytest.raises(ValueError, match=r"`location` is not allowed in SequenceProfile."):
        SequenceProfile(**example_sequence_profile)