from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference

from profiles.sequence import Sequence as FhirSequence
from resources.moleculardefinition import (
    MolecularDefinition,
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from translators.allele_utils import (
    is_valid_vrs_allele,
)


class FullVRSAlleleTranslator:
    def __init__(self, vrs_allele):
        self.vrs_allele = vrs_allele

    def validate_vrs_allele(self):
        #This is where VRS type is getting checked to make sure its a vrs allele
        return is_valid_vrs_allele(self.vrs_allele)

    #TODO: For right now use MolecularDefinition becuase it has much less restirctions then Allele
    def translate(self):
        return MolecularDefinition(
            identifier=self.map_identifiers(source=self.vrs_allele),
            #TODO: need to double check this translation
            contained=[
                self.map_sequence_location_sequence(),
                self.map_sequence_reference_to_sequence_location()
            ],
            description=self.map_description(source=self.vrs_allele),
            extension=self.map_extensions(),
            location = [self.create_location()], #TODO: need to double check the translations 
            representation=[self.create_representation()]
        )

    # ─── Identifier & Description Mappers ───
    def map_identifiers(self, source):
        identifiers = []

        if getattr(source, "id", None):
            identifiers.append(Identifier(value=source.id))

        if getattr(source, "aliases", None):
            identifiers.extend([
                Identifier(value=alias) for alias in source.aliases
            ])

        if getattr(source, "name", None):
            identifiers.append(Identifier(value=source.name))

        if getattr(source, "digest", None):
            identifiers.append(Identifier(system=source.digest))

        return identifiers or None

    def map_description(source):
        return getattr(source, "description", None)

    # ─── Extension Mappers ───
    def map_extensions(self, source=None):
        source = source or self.vrs_allele
        vrs_exts = getattr(source, "extensions", None)
        if not vrs_exts:
            return None

        return [self._map_ext(ext_obj) for ext_obj in vrs_exts]

    def _map_ext(self, ext_obj):
        extension = Extension(
            id=ext_obj.id,
            url=ext_obj.name
        )

        self._assign_extension_value(extension, ext_obj.value)

        sub_exts = []

        if ext_obj.description:
            sub_exts.append(
                Extension(
                    url="description",
                    valueString=ext_obj.description
                )
            )

        if ext_obj.extensions:
            sub_exts.extend(
                self._map_ext(nested)
                for nested in ext_obj.extensions
            )

        if sub_exts:
            extension.extension = sub_exts

        return extension

    def _assign_extension_value(self,extension, value):
        type_map = {
            str: "valueString",
            bool: "valueBoolean",
            dict: "valueCode",
            float: "valueDecimal",
            #TODO: figure out how to handle list from vrs and Null values
        }
        for expected_type, attr_name in type_map.items():
            if isinstance(value, expected_type):
                setattr(extension, attr_name, value)
                return
        raise ValueError("Only support extension values of types: str, bool, dict, float.")

    def _map_named_extensions(self, source, url_base):
        exts = []

        if getattr(source, "name", None):
            exts.append(Extension(
                url=f"{url_base}/name",
                valueString=source.name
            ))

        if getattr(source, "description", None):
            exts.append(Extension(
                url=f"{url_base}/description",
                valueString=source.description
            ))

        for alias in getattr(source, "aliases", []) or []:
            exts.append(Extension(
                url=f"{url_base}/alias",
                valueString=alias
            ))
        # nested expressions: reuse existing map_extensions
        nested = self.map_extensions(source=source)
        if nested:
            exts.extend(nested)

        if getattr(source, "digest", None):
            exts.append(Extension(
                url=f"{url_base}/digest",
                valueString=source.digest
            ))
        return exts

    # ─── Location Mappers  ───
    def map_location_extensions(self):
        return self._map_named_extensions(
            source=self.vrs_allele.location,
            #NOTE: this is a made up URL
            url_base="http://example.org/fhir/StructureDefinition/sequence-location"
        )

    def map_coordiante_interval(self):
        start_quant = Quantity(value=int(self.vrs_allele.location.start))
        end_quant = Quantity(value=int(self.vrs_allele.location.start))
        coord_system = CodeableConcept(
            coding=[
                {
                    "system": "http://loinc.org",
                    "code": "LA30100-4",
                    "display": "0-based interval counting",
                }
            ]
        )
        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=coord_system
        )
        coord_interval = MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=start_quant,
            endQuantity=end_quant,
        )

        return coord_interval
    
    def map_sequence_location(self):
        return MolecularDefinitionLocationSequenceLocation(
            sequenceContext=Reference(reference=f"#{self.vrs_allele.location.id}", type="MolecularDefinition"),
            coordinateInterval = self.map_coordiante_interval()

        )
    
    # NOTE: I think vrs sequenceLocation.sequence and sequencelocation.sequenceReference should go into a SequenceContained values
    # This way we can put both sequenceLocation.sequence and sequenceLocation.sequenceRefernce in contained list. 

    # #TODO: revisit this: Need to figure out where sequence needs to go in locaiton compared to fhir. because if we place it in sequenceLocaiton.seuqenceContext its a 1..1 cardinality
    def map_sequence_location_sequence(self):
        representation_sequence = MolecularDefinitionRepresentation(literal=self.vrs_allele.location.sequence)

        sequence_profile = FhirSequence(
            representation=[representation_sequence],
        )
        return sequence_profile

    # #TODO: revisit this: The same as teh above statement. sequenceReference fits est with sequencelocation.seuqenctCtontext but this is a 1..1 cardinality. might need to create a loop to see if one is present then cant transalte the other.
    def map_sequence_reference_to_sequence_location(self):

        rep_lit_sequence =  MolecularDefinitionRepresentationLiteral(value = self.vrs_allele.location.sequenceReference.sequence,
                                                                     encoding = CodeableConcept(
                                                                         coding = Coding(
                                                                             system = "vrs 2.0 codes for alphabet",
                                                                             code =self.vrs_allele.location.sequenceReference.residueAlphabet
                                                                         )
                                                                     ))

        representation_sequence = MolecularDefinitionRepresentation(
            code = [
                CodeableConcept(
                    coding=Coding(
                        system = "GA4GH RefGet identifier for the referenced sequence",
                        code =self.vrs_allele.location.sequenceReference.refgetAccession
                    )
                )
            ],
            literal=rep_lit_sequence
            )

        molecular_tyep = CodeableConcept(
            coding= Coding(
                system = "vrs 2.0 codes for alphabet",
                code =self.vrs_allele.location.sequenceReference.moleculeType
                )
                )

        sequence_profile = FhirSequence(
            identifier=self.map_identifiers(self.vrs_allele.location.sequenceReference),
            description=self.map_description(self.vrs_allele.location.sequenceReference),
            extension=self.map_extensions(self.vrs_allele.location.sequenceReference),
            moleculeType=molecular_tyep,
            representation=[representation_sequence],
        )
        return sequence_profile


    # TODO: need to create a custom validation that if vrs_allele.location.sequenceReference.iriReference an error gets thrown as we cannot translate this yet

    def create_location(self):
        MolecularDefinitionLocation(
            id=self.vrs_allele.location.id,
            extension=self.map_location_extensions(),
            sequenceLocation=self.map_sequence_location()
        )

    # ─── Literal Representation Mappers ───

    def map_code(self):
        concepts = []

        if not getattr(self.vrs_allele, "expressions", None):
            return None

        for exp in self.vrs_allele.expressions:
            fhir_code = Coding(
                display=exp.syntax,
                code=exp.value,
                version=exp.syntax_version
            )

            cc = CodeableConcept(
                id=exp.id,
                extension=self.map_extensions(source=exp),
                coding=[fhir_code]
            )
            concepts.append(cc)

        return concepts

    def map_representation_extensions(self):
        return self._map_named_extensions(
            source=self.vrs_allele.state,
            #NOTE: this is a made up URL
            url_base="http://example.org/fhir/LiteralRepresentation"
        )

    def map_literal_representation(self):
        literal = MolecularDefinitionRepresentationLiteral(
            id=self.vrs_allele.state.id,
            extension=self.map_representation_extensions(),
            value=str(self.vrs_allele.state.sequence)
        )
        return literal

    def create_representation(self):
        represntation = MolecularDefinitionRepresentation(
            code = self.map_code(),
            literal = self.map_literal_representation()
        )
        return represntation
