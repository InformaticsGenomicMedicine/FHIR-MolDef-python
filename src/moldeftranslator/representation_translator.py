from moldefresource.moleculardefinition import (
    MolecularDefinitionRepresentationLiteral,
    MolecularDefinitionRepresentation,
)
from api.seqrepo_api import SeqRepoAPI


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

        start_pos = extracted.start
        end_pos = extracted.end

        sequence_id = extracted.startingMolecule.display
        if sequence_id is None:
            # this is an assumption, could be extracted.startingMolecule.display or  extracted.startingMolecule.reference
            raise ValueError(
                "The 'startingMolecule' must contain a 'display' for the sequence ID."
            )

        # capture the sequence using seqrepo
        literal_seq = self.dp.get_sequence(sequence_id, start_pos, end_pos)
        if literal_seq is None:
            raise ValueError(
                f"Failed to retrieve sequence from seqrepo for ID {sequence_id} from position {start_pos} to {end_pos}."
            )

        literal = MolecularDefinitionRepresentation(
            literal=MolecularDefinitionRepresentationLiteral(value=literal_seq)
        )

        expression.representation.append(literal)

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
