from api.seqrepo_api import SeqRepoAPI
from moldefresource.moleculardefinition import (
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)


class RepresentationTranslator:

    def __init__(self):
        seqrepo_api = SeqRepoAPI()
        self.dp = seqrepo_api.seqrepo_dataproxy

    def _validate_representation(self, expression):
        if not hasattr(expression, "representation"):
            raise ValueError(
                "MolecularDefinition Object does not contain representation attribute"
            )
        return expression.representation
    #TODO: this method is coming from allele_translator.py
    #TODO: might need to put this in a commen place
    def _validate_indexing(self, coord_system, start):
        """Adjust the indexing based on the coordinate system.

        Args:
            CoordSystem (str): The coordinate system, which can be one of the following:
                                '0-based interval counting', '0-based character counting', '1-based character counting'.
            start (int): The start position to be adjusted.

        Raises:
            ValueError: If an invalid coordinate system is specified.

        Returns:
            int: The adjusted start position.

        """
        # TODO: need to double check
        adjustments = {
            "0-based interval counting": 0,
            "0-based character counting": 1,
            "1-based character counting": -1,
        }

        if coord_system not in adjustments:
            raise ValueError(
                "Invalid coordinate system specified. Valid options are: '0-based interval counting', '0-based character counting', '1-based character counting'."
            )

        return start + adjustments[coord_system]

    def translate_extracted_to_literal(self, expression):
        """Translates an extracted sequence representation to a literal sequence representation.

        Args:
            expression (object): The expression containing the representations to be translated.

        Raises:
            ValueError: If there is not exactly one extracted sequence in the representation.
            ValueError: If the 'startingMolecule' does not contain a 'display' for the sequence ID.
            ValueError: If the sequence cannot be retrieved from SeqRepo.

        Returns:
            object: Expression: The updated expression with the literal sequence representation appended.

        """
        representations = self._validate_representation(expression)
        extracted_list = []
        for rep in representations:
            if hasattr(rep, "extracted") and rep.extracted is not None:
                extracted_list.append(rep.extracted)

        if len(extracted_list) != 1:
            raise ValueError(
                "Must have exactly one sequence represented as a extracted sequence in order to translate to a literal sequence."
            )

        extracted = extracted_list[0]

        start_pos = extracted.coordinateInterval.start
        coordsystem = extracted.coordinateInterval.coordinateSystem.system.coding[0].display

        start = self._validate_indexing(coord_system=coordsystem,start= start_pos)
        end = extracted.coordinateInterval.end

        sequence_id = extracted.startingMolecule.display
        if sequence_id is None:
            # this is an assumption, could be extracted.startingMolecule.display or  extracted.startingMolecule.reference
            raise ValueError(
                "The 'startingMolecule' must contain a 'display' for the sequence ID."
            )

        # capture the sequence using seqrepo
        literal_seq = self.dp.get_sequence(sequence_id, start, end)
        if literal_seq is None:
            raise ValueError(
                f"Failed to retrieve sequence from seqrepo for ID {sequence_id} from position {start} to {end}."
            )

        literal = MolecularDefinitionRepresentation(
            literal=MolecularDefinitionRepresentationLiteral(value=literal_seq)
        )

        expression.representation.append(literal)
        #expression.representation.insert(0, literal)
        return expression

    def translate_repeated_to_literal(self, expression):
        """Translates a repeated sequence motif representation into a literal sequence.

        Args:
            expression (object): The expression containing the representations to be translated.

        Raises:
            ValueError: If there is not exactly one repeated sequence motif in the representations.

        Returns:
            object: The updated expression with the literal sequence representation appended.

        """
        representations = self._validate_representation(expression)

        repeated_listed = []
        for rep in representations:
            if hasattr(rep, "repeated") and rep.repeated is not None:
                repeated_listed.append(rep.repeated)

        if len(repeated_listed) != 1:
            raise ValueError(
                "Must have exactly one sequence represented as a repeated sequence motif in order to translate to a literal sequence."
            )

        literal_seq = (
            repeated_listed[0].sequenceMotif.display * repeated_listed[0].copyCount
        )

        literal = MolecularDefinitionRepresentation(
            literal=MolecularDefinitionRepresentationLiteral(value=literal_seq)
        )

        expression.representation.append(literal)

        return expression
