# Import required libraries
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs import models

from moldefresource.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from normalize.allele_normalizer import AlleleNormalizer
from profiles.alleleprofile import AlleleProfile


class AlleleFactory:
    """The goal of this module is to simplify the creation of AlleleProfiles, eliminating the need to build them step by step or through the unpackaging process.
    These AlleleProfiles will come with pre-filled attributes, allowing you to input just five key attributes: id, startQuantity, endQuantity, reference sequence, and literal value.
    This function specifically creates an AlleleProfile for Literal Value representation.
    """

    def __init__(self):
        self.normalize = AlleleNormalizer()

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

    def create_fhir_allele(
        self, id_value: str, start: int, end: int, reference_sequence: str, literal_value: str
    ):
        """Creates a FHIR (Fast Healthcare Interoperability Resources) AlleleProfile instance. This method simplifies the creation of a FHIR AlleleProfile resource by abstracting the underlying FHIR structure and data mapping.

        Args:
            id_value (str): The unique identifier for the AlleleProfile instance.
            start (int):  The start position of the allele (0-based).
            end (int):  The end position of the allele (0-based).
            reference_sequence (str): The RefSeq identifier.
            literal_value (str): The alternative sequence.

        Returns:
            AlleleProfile: A fully constructed FHIR AlleleProfile resource.

        """
        coding_val = Coding(
            system="http://loinc.org",
            code="LA30100-4",
            display="0-based interval counting",
        )

        codeconcept_val = CodeableConcept(
            coding=[coding_val],
            text="0-based interval counting",
        )

        MolDefLocSeqLocCoordIntCoord = (
            MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
                system=codeconcept_val
            )
        )
        # Create the coordinateInterval and build the interval with start and end quantities.
        MolDefLocSeqLocCoordInt = (
            MolecularDefinitionLocationSequenceLocationCoordinateInterval(
                coordinateSystem=MolDefLocSeqLocCoordIntCoord,
                startQuantity=Quantity(value=start),
                endQuantity=Quantity(value=end),
            )
        )

        refseq = reference_sequence.split(".")[0].lower()

        # Wrap the coordianteInterval into the sequenceLocation and add the sequenceContext.
        MolDefLocSeqLoc = MolecularDefinitionLocationSequenceLocation(
            sequenceContext=Reference(
                reference=f"MolecularDefinition/example-sequence-{refseq}-url",
                type="MolecularDefinition",
                display=reference_sequence,
            ),
            coordinateInterval=MolDefLocSeqLocCoordInt,
        )
        # Create the MolecularDefinitionLocation object, including the sequenceLocation
        Location = MolecularDefinitionLocation(sequenceLocation=MolDefLocSeqLoc)

        # Create a Coding instance to specify the focus.
        focus_coding_val = Coding(
            system="http://hl7.org/fhir/moleculardefinition-focus",
            code="allele-state",
            display="Allele State",
        )
        # Wrapt the coding value into the CodeableConcept.
        focus_codeconcept_val = CodeableConcept(
            coding=[focus_coding_val],
        )

        # Define the literal value using MolecularDefinitionRepresentationLiteral.
        MolDefRepLit = MolecularDefinitionRepresentationLiteral(value=literal_value)

        # Integrate these into the MolecularDefinitionRepresentation.
        Representation = MolecularDefinitionRepresentation(
            literal=MolDefRepLit, focus=focus_codeconcept_val
        )

        # Spcifies the profile URL in the Meta data type
        meta_val = Meta(profile=["http://hl7.org/fhir/StructureDefinition/allelesliced"])

        seq_type = self._detect_sequence_type(reference_sequence)
        # Defines the type of sequence, such as dna, rna, or aa.
        moltype_coding_val = Coding(
            system="http://hl7.org/fhir/sequence-type",
            code=seq_type.lower(),
            display=f"{seq_type} Sequence",
        )

        # Wrap the moleculeType in the CodeableConcept data type.
        moltype_codeconcept_val = CodeableConcept(
            coding=[moltype_coding_val],
        )
        # Incorporates the Location and Representation components created earlier.
        return AlleleProfile(
            id=id_value,
            meta=meta_val,
            moleculeType=moltype_codeconcept_val,
            location=[Location],
            representation=[Representation],
        )

    def create_vrs_allele(
        self,
        start: int,
        end: int,
        reference_sequence: str,
        alternative_sequence: str,
        normalize: bool = True,
    ):
        """Creates a Variant Representation Specification (VRS) Allele object.This method simplifies the creation of a VRS Allele so users do not need to directly interact with the underlying Python implementation of vrs-python.

        Args:
            start (int): The start position of the allele.
            end (int): The end position of the allele.
            reference_sequence (str): The reference sequence identifier.
            alternative_sequence (str): The alternative sequence.
            normalize (bool, optional): Weather to normalize the vrs allele or not. Defaults to True.

        Returns:
            models.Allele: A VRS Allele object, either in normalized form or as originally constructed.

        """
        interval = models.SequenceInterval(
            start=models.Number(value=start), end=models.Number(value=end)
        )
        location = models.SequenceLocation(
            sequence_id=f"refseq:{reference_sequence}", interval=interval
        )

        state = models.LiteralSequenceExpression(sequence=alternative_sequence)

        allele = models.Allele(location=location, state=state)

        if normalize:
            return self.normalize.post_normalize_allele(allele)
        else:
            return allele
