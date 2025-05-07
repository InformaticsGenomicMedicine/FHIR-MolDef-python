from fhir.resources.identifier import Identifier
from profiles.allele import Allele
from fhir.resources.extension import Extension

from resources.moleculardefinition import MolecularDefinition,MolecularDefinitionRepresentation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from translators.allele_utils import (
    is_valid_vrs_allele,
)
class FullVRSAlleleTranslator:
    def __init__(self, vrs_allele):
        self.vrs_allele = vrs_allele

    def validate_vrs_allele(self):
        #This is where VRS type is getting checked to make sure its a vrs allele
        return is_valid_vrs_allele(self.vrs_allele)

    def map_identifiers(self):
        identifiers = []

        if self.vrs_allele.id:
            identifiers.append(Identifier(value=self.vrs_allele.id))

        if self.vrs_allele.aliases:
            identifiers.extend([
                Identifier(value=alias) for alias in self.vrs_allele.aliases
            ])

        if self.vrs_allele.description:
            identifiers.append(Identifier(value=self.vrs_allele.description))

        if self.vrs_allele.digest:
            identifiers.append(Identifier(system=self.vrs_allele.digest))

        return identifiers or None

    def map_description(self):
        return self.vrs_allele.name or None
    
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
    
    def create_rep(self):
        
        rep = MolecularDefinitionRepresentation(code=self.map_code())
        return rep 

    #TODO: For right now use MolecularDefinition becuase it has much less restirctions then Allele
    def translate(self):
        return MolecularDefinition( 
            identifier=self.map_identifiers(),
            description=self.map_description(),
            extension=self.map_extensions(),
            representation=[self.create_rep()]
        )
