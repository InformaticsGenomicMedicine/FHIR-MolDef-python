import re
from decimal import Decimal

from moldefresource.moleculardefinition import (
    # MolecularDefinition,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem
)
from src.profiles.alleleprofile import AlleleProfile
from fhir.resources.identifier import Identifier
from fhir.resources.organization import Organization
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.quantity import Quantity
from decimal import Decimal

from src.api.seqrepo_api import SeqRepoAPI
from ga4gh.vrs import models

# from src.resource.exception import InvalidVRSAlleleError
from src.normalize.allele_normalizer import AlleleNormalizer


class VrsFhirAlleleTranslation:
    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy
        self.norm = AlleleNormalizer()

    # ------------------ VRS ALLELE TO MOLDEF Allele PROFILE------------------#

    def _is_valid_vrs_allele(self, expression):
        """
        Validation step to ensure that the expression is a valid VRS Allele object.

        Args:
            expression (object): An object representing a VRS Allele.

        Raises:
            InvalidVRSAlleleError: If the expression is not a valid VRS Allele object.
        """
        conditions = [
            (expression.type == "Allele", "The expression type must be 'Allele'."),
            (
                expression.location.type == "SequenceLocation",
                "The location type must be 'SequenceLocation'.",
            ),
            (
                expression.state.type == "LiteralSequenceExpression",
                "The state type must be 'LiteralSequenceExpression'.",
            ),
        ]
        for condition, error_message in conditions:
            if not condition:
                raise ValueError(error_message)# InvalidVRSAlleleError

    def _detect_sequence_type(self, sequence_id: str) -> str:
        """Translate the prefix of the RefSeq identifier to the type of sequence.

        Args:
            sequence_id (str): The RefSeq identifier.

        Raises:
            ValueError: If the prefix doesn't match any known sequence type.

        Returns:
            str: The type of sequence
        """
        prefix_to_type = {
            "NC_": "DNA",
            "NM_": "DNA",
            "NG_": "DNA",
            "NR_": "RNA",
            "NP_": "protein",
        }

        for prefix, seq_type in prefix_to_type.items():
            if sequence_id.startswith(prefix):
                return seq_type

        raise ValueError(f"Unknown sequence type for input: {sequence_id}")

    def _translate_sequenceId(self, expression):
        """Translate the VRS Allele location.sequence_id to a RefSeq identifier using SeqRepo.

        Args:
            expression (object): An object representing a VRS Allele.

        Raises:
            ValueError: If translation fails or the ID format is unexpected.

        Returns:
            str: A RefSeq identifier.
        """
        # extract the sequence_id
        sequence_id = str(expression.location.sequence_id)
        # Use SeqRepo to translate to a RefSeq ID
        translated_ids = self.dp.translate_sequence_identifier(
            sequence_id, namespace="refseq"
        )

        if not translated_ids:
            raise ValueError(
                f"Translation failed: No RefSeq ID found for sequence ID '{sequence_id}'."
            )

        # Extract the RefSeq ID from the first translated result.
        translated_id = translated_ids[0]

        if not translated_id.startswith("refseq:"):
            raise ValueError(f"Unexpected ID format in '{translated_id}'")

        _, refseq_id = translated_id.split(":")

        return refseq_id

    def _extract_vrs_values(self, expression):
        """Extract values form a VRS Allele object.

        Args:
            expression (object): An object representing a VRS Allele.

        Returns:
            tuple: A tuple containing the GA4GH ID, RefSeq ID, start position, end position, and alternate allele sequence.
        """
        self._is_valid_vrs_allele(expression)

        ga4gh_id = str(expression._id)
        refseq_id = self._translate_sequenceId(expression)
        start_pos = expression.location.interval.start.value
        end_pos = expression.location.interval.end.value
        alt_allele = expression.state.sequence

        return ga4gh_id, refseq_id, start_pos, end_pos, alt_allele

    def vrs_allele_to_allele_profile(self, expression):
        """Converts a VRS alelel expression to an AlleleProfile

        Args:
            expression (object): Contains VRS alelel information

        Returns:
            AlleleProfile: A FHIR AlleleProfile object constructed from the given VRS Allele expression.
        """
        ga4gh_id, refseq_id, start_pos, end_pos, altAllele = self._extract_vrs_values(
            expression
        )
        #vrs only allows integer, where FHIR requires a Decimal for precision.
        start_quant = Quantity(value=int(start_pos)) 
        end_quant = Quantity(value=int(end_pos)) 

        # handling VRS deletions it returns '' in fhir string type It gets an error. So need to convert this into a string. 
        if altAllele == '':
            altAllele = ' '

        # Auto setting the Organization name
        organization = Organization(
            name="Global Alliance for Genomics and Health",
        )

        organization_reference = Reference(display=f"{organization.name}")
        
        identifier = Identifier(value=ga4gh_id, assigner=organization_reference)
        # Capturing the sequence type from the refseq ID
        sequence_type = self._detect_sequence_type(sequence_id=refseq_id)

        molType = CodeableConcept(
            coding=[
                {
                    "system":"http://hl7.org/fhir/sequence-type",
                    "code": sequence_type.lower(),
                    "display": "{} Sequence".format(sequence_type),
                }
            ]
        )
        coordSystem = CodeableConcept(
            coding=[
                {
                    #TODO: double check that this is correct 
                    "system": "http://loinc.org",
                    "code": "LA30100-4",
                    "display": "0-based interbase",
                }
            ]
        )
        seq_context_display = Reference(display=refseq_id)

        MolDefReprLiteral = MolecularDefinitionRepresentationLiteral(
            value=str(altAllele)
        )
        MolDefRepresentation = MolecularDefinitionRepresentation(
            literal=MolDefReprLiteral
        )
        MolDefLocationSequenceLocationCoordinatSystem = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system= coordSystem
            )
        MolDefLocationSequenceLocationCoordinateInterval = (
            MolecularDefinitionLocationSequenceLocationCoordinateInterval(
                coordinateSystem = MolDefLocationSequenceLocationCoordinatSystem,
                startQuantity=start_quant,
                endQuantity=end_quant
            )
        )
        MolDefLocationSequenceLocation = MolecularDefinitionLocationSequenceLocation(
            sequenceContext=seq_context_display, 
            coordinateInterval=MolDefLocationSequenceLocationCoordinateInterval,
        )

        MolDefLocation = MolecularDefinitionLocation(
            sequenceLocation=MolDefLocationSequenceLocation
        )

        FHIRAllele = AlleleProfile(
            identifier=[identifier],
            moleculeType = molType,
            #NOTE: molecularType got added and now need to represent it in a codeableconcept. Remember type is still also present but dont need for translation.
            # type=self._detect_sequence_type(sequence_id=refseq_id),
            location=[MolDefLocation],
            representation=[MolDefRepresentation],
        )
        return FHIRAllele

    # ------------------ MOLDEF ALLELE PROFILE TO VRS ALLELE------------------#

    def _validate_indexing(self, coord_system, start):
        """Adjust the indexing based on the coordinate system.

        Args:
            CoordSystem (str): The coordinate system, which can be one of the following:
                                "0-based interbase", "0-based counting", "1-based counting".
            start (int): The start position to be adjusted.

        Raises:
            ValueError: If an invalid coordinate system is specified.

        Returns:
            int: The adjusted start position.
        """
        # TODO: need to double check
        adjustments = {
            "0-based interbase": 0,
            "0-based counting": 1,
            "1-based counting": -1,
        }

        if coord_system not in adjustments:
            raise ValueError(
                "Invalid coordinate system specified. Valid options are: '0-based interbase', '0-based counting', '1-based counting'."
            )

        return start + adjustments[coord_system]

    def _validate_sequence(self, sequence: str) -> None:
        """Validate the sequence to ensure it contains valid characters as per VRS rules.

        Args:
            sequence (str): The sequence to be validated.

        Raises:
            ValueError: If the sequence contains invalid characters.

        Returns:
            str: The validated sequence.
        """
        pattern = r"^[A-Z*\-]*$"
        if not re.match(pattern, sequence):
            raise ValueError("Invalid sequence value")
        return sequence

    def _convert_decimal_to_int(self, value):
        """Validate and convert a Decimal value to an integer if possible.

        Args:
            value (Decimal): The value to be validated and converted.

        Raises:
            TypeError: If the value is not a Decimal.
            ValueError: If the Decimal value cannot be converted to an integer.

        Returns:
            int: The validated and converted integer value.
        """
        # check if the value is a decimal
        if not isinstance(value, Decimal):
            raise TypeError("Value is not a valid Decimal value.")

        if value == value.to_integral_value():
            value = int(value)
        else:
            raise TypeError(
                "Decimal Value must be able to be converted into an Integer"
            )
        return value

    def _is_valid_allele_profile(self, expression: object):
        """Validates if the given expression is a valid AlleleProfile.

        Args:
            expression (object): The expression to validate.

        Raises:
            TypeError: If the expression is not an instance of AlleleProfile.
            TypeError: If any location in the expression is not an instance of MolecularDefinitionLocation.
            TypeError: If any representation in the expression is not an instance of MolecularDefinitionRepresentation.
        """
        if not isinstance(expression, AlleleProfile):
            raise TypeError(
                "Invalid expression type: expected an instance of AlleleProfile."
            )

        if not all(
            isinstance(loc, MolecularDefinitionLocation) for loc in expression.location
        ):
            raise TypeError(
                "Each location should be an instance of MolecularDefinitionLocation."
            )

        if not all(
            isinstance(rep, MolecularDefinitionRepresentation)
            for rep in expression.representation
        ):
            raise TypeError(
                "Each representation should be an instance of MolecularDefinitionRepresentation."
            )

    def _is_valid_sequence_location(self, sequence_location):
        """Validates a sequence location object to ensure it meets specific conditions.

        Args:
            sequence_location (object): The sequence location object to validate.

        Returns:
            bool: True if the sequence location is valid, False otherwise.
        """
        if not (hasattr(sequence_location, "sequenceContext") and
                getattr(sequence_location.sequenceContext, "display", None)):
            return False

        if not hasattr(sequence_location, "coordinateInterval"):
            return False

        coordinate_interval = sequence_location.coordinateInterval

        if not (hasattr(coordinate_interval, "coordinateSystem") and
                hasattr(coordinate_interval.coordinateSystem, "system") and
                hasattr(coordinate_interval.coordinateSystem.system, "coding")):
            return False

        coding_list = coordinate_interval.coordinateSystem.system.coding
        if not any(hasattr(coding, "display") and coding.display for coding in coding_list):
            return False

        if not all(
            hasattr(coordinate_interval, attr) and
            getattr(coordinate_interval, attr) and
            getattr(coordinate_interval, attr).value is not None
            for attr in ["startQuantity", "endQuantity"]
        ):
            return False

        return True

    def _validate_location(self,expression):
        """
        Validate and extract valid sequence locations from the given expression.

        Args:
            expression (object): The expression containing sequence location information.

        Returns:
            list: A list of valid sequence location objects.
        """
        valid_sequence_locations = [] 

        for value in expression.location:
            if hasattr(value, "sequenceLocation"): 
                sequence_location = value.sequenceLocation
                if self._is_valid_sequence_location(sequence_location): 
                    valid_sequence_locations.append(sequence_location)  

        return valid_sequence_locations
    
    def _get_single_location(self, expression):
        """Validates and retrieves a single sequence location from the given expression.

        Args:
            expression (object):  The expression containing the sequence location information.

        Raises:
            ValueError: The validated sequence location.

        Returns:
            dict: The validated sequence location.
        """
        sequence_location_list = self._validate_location(expression)
        if len(sequence_location_list) != 1:
            raise ValueError(
                f"Currently only supporting 1 location. You provided {len(sequence_location_list)} locations. "
                "Each location must contain: sequenceLocation, sequenceContext, coordinateInterval, startQuantity, and endQuantity."
            )
        return sequence_location_list[0]

    def _validate_literal_representation(self, expression: object):
        """ Validates the literal representation of an expression.

        Args:
            expression (object): The expression object containing representations.

        Returns:
            list: A list of literal values extracted from the expression's representations.
        """
        literals = []

        for rep in expression.representation:
            if (
                hasattr(rep, "literal")
                and hasattr(rep.literal, "value")
                and rep.literal.value is not None
            ):
                literals.append(rep.literal.value)

        return literals

    def _get_single_literal(self, expression):
        """ Validates and retrieves a single literal representation from the given expression.

        Args:
            expression (object): The expression to be validated and parsed.

        Raises:
            ValueError: If the expression does not contain exactly one literal representation.

        Returns:
            str: The single literal representation extracted from the expression.
        """
        literals = self._validate_literal_representation(expression)
        if len(literals) != 1:
            raise ValueError(
                f"Currently only supporting 1 literal representation. You provided {len(literals)} literal representation."
            )
        return literals[0]

    def translate_allele_profile_to_vrs_allele(
        self, expression: object, normalize: bool = True
    ):
        """
        Translate an AlleleProfile to a VRS Allele.

        Args:
            expression (object): An AlleleProfile object containing allele information.
            normalize (bool, optional): Whether to normalize the VRS Allele. Defaults to True.

        Raises:
            ValueError: If the expression contains invalid data or multiple locations/literals.

        Returns:
            models.Allele: A VRS Allele object constructed from the given AlleleProfile.
        """
        self._is_valid_allele_profile(expression)

        location_data = self._get_single_location(expression)

        values_needed = {
            "refseq": location_data.sequenceContext.display,
            "start": location_data.coordinateInterval.startQuantity.value,
            "end": location_data.coordinateInterval.endQuantity.value,
        }

        # Ensure only one coding is present
        coding_list = location_data.coordinateInterval.coordinateSystem.system.coding
        if len(coding_list) != 1:
            raise ValueError("Currently only supporting 1 coding in numberingSystem")

        # Retrieve coordinate system display if available
        values_needed["coordinate_system_display"] = coding_list[0].display

        seq = self._get_single_literal(expression)

        # Process start and end positions
        refseq = values_needed["refseq"]
        # Making sure that the coordinateSystem is valid, and if so adjust the indexing of the start position
        start = self._validate_indexing(
            coord_system=values_needed["coordinate_system_display"],
            start=values_needed["start"],
        )
        # Making sure that the value is an integer and not a float.
        start_pos = self._convert_decimal_to_int(start)
        end_pos = self._convert_decimal_to_int(values_needed["end"])

        alternative_seq = self._validate_sequence(sequence=seq)

        # Create VRS interval and allele objects
        interval = models.SequenceInterval(
            start=models.Number(value=start_pos),
            end=models.Number(value=end_pos),
        )
        location = models.SequenceLocation(
            sequence_id=f"refseq:{refseq}", interval=interval
        )
        state = models.LiteralSequenceExpression(sequence=alternative_seq)

        # Return the constructed VRS allele
        allele = models.Allele(location=location, state=state)
        # normalizing VRS object
        if normalize:
            allele = self.norm.post_normalize_allele(allele)

        return allele
