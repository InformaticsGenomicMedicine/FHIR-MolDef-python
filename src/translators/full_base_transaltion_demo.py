from fhir.resources.identifier import Identifier
from profiles.allele import Allele
from fhir.resources.extension import Extension
from fhir.resources.quantity import Quantity

from resources.moleculardefinition import MolecularDefinition,MolecularDefinitionRepresentation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from translators.allele_utils import (
    is_valid_vrs_allele,
)
from fhir.resources.reference import Reference

from resources.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from profiles.sequence import Sequence as FhirSequence

class FullVRSAlleleTranslator:
    def __init__(self, vrs_allele):
        self.vrs_allele = vrs_allele

    def validate_vrs_allele(self):
        #This is where VRS type is getting checked to make sure its a vrs allele
        return is_valid_vrs_allele(self.vrs_allele)
    
    #TODO: For right now use MolecularDefinition becuase it has much less restirctions then Allele
    def translate(self):
        return MolecularDefinition( 
            identifier=self.map_identifiers(),
            description=self.map_description(),
            extension=self.map_extensions(),
            representation=[self.create_rep()]
        )

    # ─── Identifier & Description Mappers ───
    def map_identifiers(self):
        identifiers = []

        if self.vrs_allele.id:
            identifiers.append(Identifier(value=self.vrs_allele.id))

        if self.vrs_allele.aliases:
            identifiers.extend([
                Identifier(value=alias) for alias in self.vrs_allele.aliases
            ])

        if self.vrs_allele.name:
            identifiers.append(Identifier(value=self.vrs_allele.name))

        if self.vrs_allele.digest:
            identifiers.append(Identifier(system=self.vrs_allele.digest))

        return identifiers or None

    def map_description(self):
        return self.vrs_allele.description or None
    
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
    
    # ─── Location Mappers  ───

    def map_location_extensions(self):
        location_extensions = []

        if self.vrs_allele.location.name:
            name_ext = Extension(
                url="http://example.org/fhir/StructureDefinition/sequence-location-name",
                valueString=self.vrs_allele.location.name
            )
            location_extensions.append(name_ext)

        if self.vrs_allele.location.description:
            description_ext = Extension(
                url="http://example.org/fhir/StructureDefinition/sequence-location-description",
                valueString=self.vrs_allele.location.description
            )
            location_extensions.append(description_ext)

        for alias in self.vrs_allele.location.aliases or []:
            alias_ext = Extension(
                url="http://example.org/fhir/StructureDefinition/sequence-location-alias",
                valueString=alias
            )
            location_extensions.append(alias_ext)

        for exp in self.vrs_allele.location.extensions or []:
            exts = self.map_extensions(source=exp)
            if exts:
                location_extensions.extend(exts)

        if self.vrs_allele.location.digest:
            digest_ext = Extension(
                url="http://example.org/fhir/StructureDefinition/sequence-location-digest",
                valueString=self.vrs_allele.location.digest
            )
            location_extensions.append(digest_ext)

        return location_extensions

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

    #TODO: revisit this: Need to figure out where sequence needs to go in locaiton compared to fhir. because if we place it in sequenceLocaiton.seuqenceContext its a 1..1 cardinality
    def map_sequence_location(self):
        representation_sequence = MolecularDefinitionRepresentation(literal=self.vrs_allele.location.sequence)

        sequence_profile = FhirSequence(
            representation=[representation_sequence],
        )
        seq_context = Reference(
            reference=f"#{sequence_profile.id}", type="MolecularDefinition"
        )
        MolecularDefinitionLocationSequenceLocation(
            SequenceContext = seq_context
        )
    
    #TODO: revisit this: The same as teh above statement. sequenceReference fits est with sequencelocation.seuqenctCtontext but this is a 1..1 cardinality. might need to create a loop to see if one is present then cant transalte the other.
    def map_sequence_reference_to_sequence_location(self):
        representation_sequence = MolecularDefinitionRepresentation(literal=self.vrs_allele.location.sequenceReference.sequence)
        sequence_profile = FhirSequence(
            id=self.vrs_allele.location.sequenceReference.id,
            description=self.vrs_allele.location.sequenceReference.discription,
            # extension=,
            moleculeType=self.vrs_allele.location.sequenceReference.moleculeType,
            representation=[representation_sequence],
        )
        seq_context = Reference(
            reference=f"#{sequence_profile.id}", type="MolecularDefinition"
        )
        MolecularDefinitionLocationSequenceLocation(
            SequenceContext = seq_context
        )
    
    #TODO: figure out how to put everything together
    # def map_location(self):
        # MolecularDefinitionLocation(
        #     id=self.vrs_allele.location.id
        #     extension=self.map_location_extensions()
        # )

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
    
    #TODO: revisit this, need to include the other values in represntation:
    def create_rep(self):
        
        rep = MolecularDefinitionRepresentation(code=self.map_code())
        return rep 
    
    def map_representation_extensions(self):
        representation_extensions = []

        if self.vrs_allele.state.name:
            name_ext = Extension(
                url="http://example.org/fhir/LiteralRepresntation/name",
                valueString=self.vrs_allele.state.name
            )
            representation_extensions.append(name_ext)

        if self.vrs_allele.state.description:
            description_ext = Extension(
                url="http://example.org/fhir/LiteralRepresntation/location-description",
                valueString=self.vrs_allele.state.description
            )
            representation_extensions.append(description_ext)

        for alias in self.vrs_allele.state.aliases or []:
            alias_ext = Extension(
                url="http://example.org/fhir/LiteralRepresntation/location-alias",
                valueString=alias
            )
            representation_extensions.append(alias_ext)

        for exp in self.vrs_allele.state.expressions or []:
            exts = self.map_extensions(source=exp)
            if exts:
                representation_extensions.extend(exts)

        if self.vrs_allele.state.digest:
            digest_ext = Extension(
                url="http://example.org/fhir/LiteralRepresntation/location-digest",
                valueString=self.vrs_allele.state.digest
            )
            representation_extensions.append(digest_ext)

        return representation_extensions
        
    def map_literal_representation(self):
        MolecularDefinitionRepresentationLiteral(
            id=self.vrs_allele.state.id, 
            #TODO: figure out how to have extension for things that are repeated
            # extension=self.map_representation_extensions()
            value=self.vrs_allele.state.sequence
        )