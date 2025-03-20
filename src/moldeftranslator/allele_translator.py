import re
from decimal import Decimal

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.identifier import Identifier
from fhir.resources.organization import Organization
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs import models

from api.seqrepo_api import SeqRepoAPI
from moldefresource.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    # MolecularDefinition,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)

# from src.resource.exception import InvalidVRSAlleleError
from normalize.allele_normalizer import AlleleNormalizer
from profiles.alleleprofile import AlleleProfile
from profiles.sequenceprofile import SequenceProfile


class VrsFhirAlleleTranslation:
    """A class to handle the translation between VRS Allele objects and FHIR AlleleProfile objects."""
    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy
        self.norm = AlleleNormalizer()

    # ------------------ VRS ALLELE TO MOLDEF Allele PROFILE------------------#

    def _is_valid_vrs_allele(self, expression):
        """Validation step to ensure that the expression is a valid VRS Allele object.

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
            "NG_": "DNA",
            "NM_": "RNA",
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
        """Converts a VRS allele expression to an AlleleProfile

        Args:
            expression (object): Contains VRS allele information

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
                    "display": f"{sequence_type} Sequence",
                }
            ]
        )
        coordSystem = CodeableConcept(
            coding=[
                {
                    #TODO: double check that this is correct
                    "system": "http://loinc.org",
                    "code": "LA30100-4",
                    "display": "0-based interval counting",
                }
            ]
        )
        seq_context_display = Reference(display=refseq_id)

        focus_value = CodeableConcept(
            coding=[Coding(
                system="http://hl7.org/fhir/moleculardefinition-focus",
                code = "allele-state")]
        )
        MolDefReprLiteral = MolecularDefinitionRepresentationLiteral(
            value=str(altAllele)
        )

        MolDefRepresentation = MolecularDefinitionRepresentation(
            focus=focus_value,
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
                                '0-based interval counting', '0-based character counting', '1-based character counting'.
            start (int): The start position to be adjusted.

        Raises:
            ValueError: If an invalid coordinate system is specified.

        Returns:
            int: The adjusted start position.

        """
        # TODO: need to double check with bob
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

        """
        if not isinstance(expression, AlleleProfile):
            raise TypeError(
                "Invalid expression type: expected an instance of AlleleProfile."
            )

    def _is_valid_sequence_location(self, locations):
        """Validates the `sequenceLocation` structure within the provided locations to ensure all necessary attributes are present for accurate translations.

        Args:
            locations (list): A list of location objects containing `sequenceLocation` attributes.

        Raises:
            ValueError: If 'sequenceLocation' is missing in any location.
            ValueError: If 'sequenceContext.display' is missing in any sequence location.
            ValueError: If 'coordinateInterval' is missing in any sequence location.
            ValueError: If 'coordinateSystem.system.coding' is missing in any coordinate interval.
            ValueError: If 'coding.display' is missing in 'coordinateSystem.system.coding'.
            ValueError: If 'startQuantity.value' is missing in any coordinate interval.
            ValueError: If 'endQuantity.value' is missing in any coordinate interval.

        Returns:
            sequence_location: The validated sequence location object.

        """
        for loc in locations:
            # Access sequenceLocation first
            sequence_location = loc.sequenceLocation
            if not sequence_location:
                raise ValueError("Missing 'sequenceLocation' in location.")

            # Check sequenceContext.display
            if not sequence_location.sequenceContext.display:
                raise ValueError("Missing 'sequenceContext.display' in sequence location.")

            # Check coordinateInterval existence
            if not sequence_location.coordinateInterval:
                raise ValueError("Missing 'coordinateInterval' in sequence location.")

            coordinate_interval = sequence_location.coordinateInterval

            # Check coordinateSystem.system.coding
            if not coordinate_interval.coordinateSystem.system.coding:
                raise ValueError("Missing 'coordinateSystem.system.coding' in coordinate interval.")

            if not any(coding.display for coding in coordinate_interval.coordinateSystem.system.coding):
                raise ValueError("Missing 'coding.display' in 'coordinateSystem.system.coding'.")

            # Check startQuantity and endQuantity
            if not getattr(coordinate_interval.startQuantity, "value", None):
                raise ValueError("Missing 'startQuantity.value' in coordinate interval.")
            if not getattr(coordinate_interval.endQuantity, "value", None):
                raise ValueError("Missing 'endQuantity.value' in coordinate interval.")

        return sequence_location

    def _get_literal_value_for_allele_state(self,representations):
        """Retrieves the literal value associated with an `allele-state` representation, if present, from the provided list of representations.

        Args:
            representations (list): A list of representation objects that may include `allele-state` details.

        Raises:
             ValueError: If the `allele-state` representation is present but lacks a `literal.value`.

        Returns:
            str: The value of the `literal` attribute for the `allele-state` representation.

        """
        for rep in representations:
            focus = getattr(rep,"focus",None)
            if  focus and any(coding.code == "allele-state" for coding in getattr(focus,"coding",[])):
                literal = getattr(rep,"literal",None)
                if literal:
                    return literal.value
                else:
                    raise ValueError("Missing `literal.value` for the `allele-state` representation.")

    def translate_allele_profile_to_vrs_allele(
        self, expression: object, normalize: bool = True
    ):
        """Translate an AlleleProfile to a VRS Allele.

        Args:
            expression (object): An AlleleProfile object containing allele information.
            normalize (bool, optional): Whether to normalize the VRS Allele. Defaults to True.

        Raises:
            ValueError: If the expression contains invalid data or multiple locations/literals.

        Returns:
            models.Allele: A VRS Allele object constructed from the given AlleleProfile.

        """
        self._is_valid_allele_profile(expression)

        location_data = self._is_valid_sequence_location(expression.location)
        values_needed = {
            "refseq": location_data.sequenceContext.display,
            "start": location_data.coordinateInterval.startQuantity.value,
            "end": location_data.coordinateInterval.endQuantity.value,
        }

        # Ensure only one coding is present
        #TODO: possible incoperate this in the _is_valid_seuqence_locaiton, to only have one coding list
        coding_list = location_data.coordinateInterval.coordinateSystem.system.coding
        if len(coding_list) != 1:
            raise ValueError("Currently only supporting 1 coding in numberingSystem")

        # Retrieve coordinate system display if available
        values_needed["coordinate_system_display"] = coding_list[0].display

        seq = self._get_literal_value_for_allele_state(expression.representation)
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

#TODO: move to a different class
    # ------------------ MOLDEF ALLELE PROFILE Contained TO VRS ALLELE------------------#
    def _validate_accession(self, refseq_id: str) -> str:
        """Validate the given RefSeq ID to ensure it matches the expected format.

        Args:
            refseq_id (str): The RefSeq ID to be validated.

        Raises:
            ValueError: If the RefSeq ID does not match the expected format.

        Returns:
            str: The validated RefSeq ID.
        """
        refseq_pattern = re.compile(r"^(NC_|NG_|NM_|NP_)\d+\.\d+$")

        if not refseq_pattern.match(refseq_id):
            raise ValueError(f"Invalid accession number: {refseq_id}. Must be a valid NCBI RefSeq ID (e.g., NM_000769.4).")

        return refseq_id

    #TODO: edit the error messages
    def _validate_and_extract_code(self,expression):
        """Validate and extract the code from the given expression.

        Args:
            expression (object): The expression containing the code to be validated and extracted.

        Raises:
            ValueError: If the 'contained' field is missing or empty.
            ValueError: If the 'representation' field does not contain exactly one list item.
            ValueError: If the 'code' field is missing or empty.
            ValueError: If the 'coding' field is missing or empty.
            ValueError: If the 'code' value is missing inside 'coding'.

        Returns:
            str: The validated and extracted code.
        """

        if not expression.contained:
            raise ValueError("Error: 'contained' field is missing or empty.")

        contained_item = expression.contained[0]

        if not contained_item.representation or len(contained_item.representation) != 1:
            raise ValueError("Error: 'representation' must contain exactly one list item.")

        representation_item = contained_item.representation[0]

        if not representation_item.code:
            raise ValueError("Error: 'code' field is missing or empty.")

        code_item = representation_item.code[0]

        if not code_item.coding:
            raise ValueError("Error: 'coding' field is missing or empty.")

        extracted_code = code_item.coding[0].code

        if not extracted_code:
            raise ValueError("Error: 'code' value is missing inside 'coding'.")

        return self._validate_accession(extracted_code)

    def translate_contained_allele_profile_to_vrs_allele(self, expression: object, normalize: bool = True):
        """Translate a contained AlleleProfile to a VRS Allele.

        Args:
            expression (object): An AlleleProfile object containing allele information.
            normalize (bool, optional): Whether to normalize the VRS Allele. Defaults to True.

        Raises:
            ValueError: If the expression contains invalid data or multiple locations/literals.

        Returns:
            models.Allele: A VRS Allele object constructed from the given AlleleProfile.
        """
        self._is_valid_allele_profile(expression)

        location_data = self._is_valid_sequence_location(expression.location)
        values_needed = {
            "refseq": self._validate_and_extract_code(expression),
            "start": location_data.coordinateInterval.startQuantity.value,
            "end": location_data.coordinateInterval.endQuantity.value,
        }

        coding_list = location_data.coordinateInterval.coordinateSystem.system.coding

        if len(coding_list) != 1:
            raise ValueError("Currently only supporting 1 coding in numberingSystem")

        # Retrieve coordinate system display if available
        values_needed["coordinate_system_display"] = coding_list[0].display

        seq = self._get_literal_value_for_allele_state(expression.representation)
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


    # ------------------ VRS ALLELE to MOLDEF ALLELE PROFILE Contained ------------------#

    def vrs_allele_to_contained_allele_profile(self, expression):
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
                    "display": f"{sequence_type} Sequence",
                }
            ]
        )
        coordSystem = CodeableConcept(
            coding=[
                {
                    #TODO: double check that this is correct
                    "system": "http://loinc.org",
                    "code": "LA30100-4",
                    "display": "0-based interval counting",
                }
            ]
        )
        seq_context_display = Reference(display=refseq_id)

        focus_value = CodeableConcept(
            coding=[Coding(
                system="http://hl7.org/fhir/moleculardefinition-focus",
                code = "allele-state")]
        )
        MolDefReprLiteral = MolecularDefinitionRepresentationLiteral(
            value=str(altAllele)
        )

        MolDefRepresentation = MolecularDefinitionRepresentation(
            focus=focus_value,
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
        ########### TODO: need to edit this #######  
        coding_values_2 = Coding(
            system="http://www.ncbi.nlm.nih.gov/refseq",
            code=refseq_id,
            display="TBD-THIS IS A DEMO EXAMPLE"
        )

        code_values = CodeableConcept(coding=[coding_values_2])

        representation_sequence_value = MolecularDefinitionRepresentation(
            code=[code_values])

        sequence_profile = SequenceProfile(
            # id="example-sequence-nc000002-acc",
            moleculeType=molType,
            representation=[representation_sequence_value]
            )
        ########### ##################### #######  


        FHIRAllele = AlleleProfile(
            contained=[sequence_profile],
            identifier=[identifier],
            moleculeType = molType,
            #NOTE: molecularType got added and now need to represent it in a codeableconcept. Remember type is still also present but dont need for translation.
            # type=self._detect_sequence_type(sequence_id=refseq_id),
            location=[MolDefLocation],
            representation=[MolDefRepresentation],
        )
        return FHIRAllele
