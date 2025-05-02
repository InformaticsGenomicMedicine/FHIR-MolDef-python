########################################################################
##########################   BaseTranslation   #########################
########################################################################



from fhir.resources.identifier import Identifier
from profiles.allele import Allele
from fhir.resources.extension import Extension

# from resources.moleculardefinition import MolecularDefinition

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
    

    def map_extension(self):
        #TODO: figure out what mulitple extensions in a VRS allele object would look like
        ext_obj = self.vrs_allele.extension[0] #This is inputing only one extesnsion

        extension = Extension(
            id=ext_obj.id,
            url=ext_obj.name,
        )

        value = ext_obj.value 

        type_to_attr = {
            str: 'valueString',
            bool: 'valueBoolean',
            dict: 'valueCode',
            float: 'valueDecimal'
            #TODO: Need to figure out what list in extensions.values wold mapp to in FHIR values[x]
            }
        
        for expected_type, attr_name in type_to_attr.items():
            if isinstance(value, expected_type):
                setattr(extension, attr_name, value) 
                break

        sub_extensions = []
        if ext_obj.description:
            sub_extensions.append(
                Extension(
                    url= "description",
                    valueString=ext_obj.description
                )
            )

        if ext_obj.extensions:
            for nested in ext_obj.extensions:
                sub_extensions.append(self.build_extension(nested))
        
        if sub_extensions:
            extension.extension = sub_extensions

            return extension
    #TODO: Continue development expressions
    def translate(self):
        return Allele(
            identifier=self.map_identifiers(),
            description=self.map_description(),
            extension=self.map_extension(),
        )
    
if __name__ == "__main__":

    # vrs_allele_instance =  #TODO: input data here whenc created
    translator = FullVRSAlleleTranslator(vrs_allele_instance)
    fhir_allele = translator.translate()
    print(fhir_allele)
