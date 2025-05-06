########################################################################
##########################   BaseTranslation   #########################
########################################################################
from fhir.resources.identifier import Identifier
from profiles.allele import Allele
from fhir.resources.extension import Extension

from resources.moleculardefinition import MolecularDefinition,MolecularDefinitionRepresentation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding

class FullVRSAlleleTranslator:
    def __init__(self, vrs_allele):
        self.vrs_allele = vrs_allele

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

    def map_extension(self, ext_obj=None, source=None):
        if ext_obj is None:
            source = source or self.vrs_allele

            if not getattr(source, "extensions", None):
                return None

            return [self.map_extension(ext_obj=ext, source=source) for ext in source.extensions]

        extension = Extension(
            id=ext_obj.id,
            url=ext_obj.name,
        )

        value = ext_obj.value

        type_to_attr = {
            str: 'valueString',
            bool: 'valueBoolean',
            dict: 'valueCode',
            float: 'valueDecimal',
        }

        for expected_type, attr_name in type_to_attr.items():
            if isinstance(value, expected_type):
                setattr(extension, attr_name, value)
                break

        sub_extensions = []

        if ext_obj.description:
            sub_extensions.append(
                Extension(
                    url="description",
                    valueString=ext_obj.description
                )
            )

        if ext_obj.extensions:
            for nested in ext_obj.extensions:
                sub_extensions.append(self.map_extension(ext_obj= nested, source=ext_obj))

        if sub_extensions:
            extension.extension = sub_extensions

        return extension

    def map_code(self):
        #TODO: noticed that there may potentially be multiple expressions will need to create a list of codeableconepts to do this translations. 
        for exp in self.vrs_allele.expressions:
            fhir_code = Coding(
                display=exp.syntax,
                code=exp.value,
                version=exp.syntax_version
            )

            return CodeableConcept(
                id=exp.id,
                extension=self.map_extension(source=exp),
                coding=[fhir_code]
            )

    def create_rep(self):
        rep = MolecularDefinitionRepresentation(code=[self.map_code()])
        return rep 

    #TODO: For right now use MolecularDefinition becuase it has much less restirctions then Allele
    def translate(self):
        return MolecularDefinition( 
            identifier=self.map_identifiers(),
            description=self.map_description(),
            extension=self.map_extension(),
            representation=[self.create_rep()]
        )
