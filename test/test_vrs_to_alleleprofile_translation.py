import pytest
from moldeftranslator.allele_translator import VrsFhirAlleleTranslation
from ga4gh.vrs import models
from decimal import Decimal

@pytest.fixture
def example():
    return {  # Normalized output
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
        }

@pytest.fixture
def allele_translator():
    return VrsFhirAlleleTranslation()

@pytest.fixture
def vrs_allele(example):
    return models.Allele(**example)

@pytest.fixture
def alleleprofile_expected_outputs():
    return {'resourceType': 'MolecularDefinition',
 'identifier': [{'value': 'ga4gh:VA.fXvhngewkkyVwzEeSJRr5tro8Jcol6Q-',
   'assigner': {'display': 'Global Alliance for Genomics and Health'}}],
 'moleculeType': {'coding': [{'system': 'http://hl7.org/fhir/sequence-type',
    'code': 'dna',
    'display': 'DNA Sequence'}]},
 'location': [{'sequenceLocation': {'sequenceContext': {'display': 'NC_000002.12'},
    'coordinateInterval': {'coordinateSystem': {'system': {'coding': [{'system': 'http://loinc.org',
         'code': 'LA30100-4',
         'display': '0-based interval counting'}]}},
     'startQuantity': {'value': Decimal('27453448')},
     'endQuantity': {'value': Decimal('27453449')}}}}],
 'representation': [{'focus': {'coding': [{'system': 'http://hl7.org/fhir/moleculardefinition-focus',
      'code': 'allele-state'}]},
   'literal': {'value': 'T'}}]}

def test_translate_vrs_to_alleleprofile(allele_translator, vrs_allele, alleleprofile_expected_outputs):
    output_dict = allele_translator.vrs_allele_to_allele_profile(vrs_allele).model_dump()
    assert output_dict == alleleprofile_expected_outputs
