#TODO: Follow up with: https://github.com/ga4gh/vrs/issues/652
allele_identifiers= {
    'id': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/id',
    'name': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/name',
    'aliases': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases',
    'digest': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/digest',
    'location':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/location',
    'state': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/state',
    }

literal_sequence_expression_identifiers = {
    'id': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/id',
    'name':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/name',
    'description':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/description',
    'aliases':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/aliases',
    'extensions':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/extensions',
    'sequence': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/sequence',
}

expression_identifiers = {
    'id': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Expression#properties/id',
    'extensions':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Expression#properties/extensions',
    'syntax':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Expression#properties/syntax',
    'value':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Expression#properties/value',
    'syntax_version':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Expression#properties/syntax_version',
}

sequence_location_identifiers = {
    'id': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/id',
    'name':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/name',
    'description':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/description',
    'aliases':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/aliases',
    'extensions':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/extensions',
    'digest':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/digest',
    'sequenceReference':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/sequenceReference',
    'start':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/start',
    'end':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/end',
    'sequence':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/sequence',

}

sequence_reference_identifiers = {
    'id': 'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/id',
    'name':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/name',
    'description':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/description',
    'aliases':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/aliases',
    'extensions':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/extensions',
    'refgetAccession':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/refgetAccession',
    'residueAlphabet':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/residueAlphabet',
    'sequence':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/sequence',
    'moleculeType':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/moleculeType',
    'circular':'https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/circular',

}

sequence_string_identifier = {
    'id': "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/sequenceString"
}