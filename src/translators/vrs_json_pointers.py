#TODO: Follow up with: https://github.com/ga4gh/vrs/issues/652
BASE_URL = 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/'
GKS_CORE_URL = 'https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/'

def build_identifier(url,entity, fields):
    return {field: f"{url}{entity}#properties/{field}" for field in fields}

allele_identifiers = build_identifier(
    url = BASE_URL,
    entity='Allele',
    fields=['id', 'name', 'aliases', 'digest', 'location', 'state']
)
literal_sequence_expression_identifiers = build_identifier(
    url = BASE_URL,
    entity='LiteralSequenceExpression',
    fields=['id', 'name', 'description', 'aliases', 'extensions', 'sequence']
)
expression_identifiers = build_identifier(
    url = BASE_URL,
    entity='Expression',
    fields=['id', 'extensions', 'syntax', 'value', 'syntax_version']
)
sequence_location_identifiers = build_identifier(
    url = BASE_URL,
    entity='SequenceLocation',
    fields=['id', 'name', 'description', 'aliases', 'extensions', 'digest', 'sequenceReference', 'start', 'end', 'sequence']
)
sequence_reference_identifiers = build_identifier(
    url = BASE_URL,
    entity='SequenceReference',
    fields=['id', 'name', 'description', 'aliases', 'extensions', 'refgetAccession', 'residueAlphabet', 'sequence', 'moleculeType', 'circular']
)
sequence_string_identifier = {
    'id': f"{BASE_URL}sequenceString"
}

extension_identifiers = build_identifier(
    url = GKS_CORE_URL,
    entity='Extension',
    fields=['id', 'extensions', 'name', 'aliases', 'value', 'description']
)