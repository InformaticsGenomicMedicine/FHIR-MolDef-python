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

class VRSAlleleToFHIRTranslator:

    def full_allele_translator(self,vrs_allele=None):
        return MolecularDefinition(
            identifier= self.map_identifiers(vrs_allele),
            contained=[self.map_contained(vrs_allele)],
            description = self.map_description(vrs_allele),
            extension = self.map_extensions(vrs_allele),
            location = self.map_location(vrs_allele),
            representation = self.map_lit_to_rep_lit_expr(vrs_allele)
        )

# --------------------------------------------------------------------------------------------
    # Mapping identifiers
    def map_identifiers(self,ao):
        identifiers = []
        identifiers.extend(self._map_id(ao))
        identifiers.extend(self._map_name(ao))
        identifiers.extend(self._map_aliases(ao))
        identifiers.extend(self._map_digest(ao))
        return identifiers or None
        #Put them all together to create a upper class identifers

    def _map_id(self,ao):
        value = getattr(ao,'id',None)
        if value:
            return [Identifier(value=value)]
        return []

    def _map_name(self,ao):
        value = getattr(ao,'name',None)
        if value:
            return [Identifier(value=value)]
        return []

    def _map_aliases(self,ao):
        value = getattr(ao,"aliases", None)
        if value:
            return [Identifier(value=alias) for alias in ao.aliases]
        return []

    def _map_digest(self, ao):
        value = getattr(ao,'digest',None)
        if value:
            # NOTE: url of vrs webpage that discribes the digest. This will be hard coded
            return [Identifier(value=value, system="https://vrs.ga4gh.org/en/stable/conventions/computed_identifiers.html#truncated-digest-sha512t24u")]
        return []

# --------------------------------------------------------------------------------------------
    # Mapping description
    def map_description(self,ao):
        return getattr(ao,'description', None)
        #vrs.descriptin will go to description.markdown

# --------------------------------------------------------------------------------------------
    # Validate that we are mapping a VRSAlelle to a FHIR Allele Profile

# --------------------------------------------------------------------------------------------
    # Mapping Extensions
    def map_extensions(self,source=None):
        vrs_exts = getattr(source,"extensions", None)
        if not vrs_exts:
            return None
        return [self._map_ext(ext_obj) for ext_obj in vrs_exts]

    #NOTE: Extension in extension will be transalted below. this will be a loop of loops
    def _map_ext(self, ext_obj):
        extension = Extension(
            id=ext_obj.id,
            url=ext_obj.name
        )

        self._assign_extension_value(extension, ext_obj.value)

        sub_exts = []
        sub_exts.extend(self._map_description_subext(ext_obj))
        sub_exts.extend(self._map_nested_extensions(ext_obj))

        if sub_exts:
            extension.extension = sub_exts

        return extension

    def _map_description_subext(self, ext_obj):
        if getattr(ext_obj, "description", None):
            return [Extension(url="description", valueString=ext_obj.description)]
        return []

    def _map_nested_extensions(self, ext_obj):
        if not getattr(ext_obj, "extensions", None):
            return []
        return [self._map_ext(nested) for nested in ext_obj.extensions]

    def _assign_extension_value(self, extension, value):
        if value is None:
            return

        type_map = {
            str: "valueString",
            bool: "valueBoolean",
            float: "valueDecimal"
        }

        for expected_type, attr_name in type_map.items():
            if isinstance(value, expected_type):
                setattr(extension, attr_name, value)
                return

        raise TypeError("Unsupported extension value type. Must be str, bool, or float.")

    def _map_location_extensions(self, source, url_base):
        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self._map_digest_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts

    def _map_lse_extensions(self, source, url_base):
        #NOTE location includes digest where literal sequence location expression doesnt
        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts
    
    def _map_refseq_extensions(self, source, url_base):
        #NOTE location includes digest where literal sequence location expression doesnt
        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self._map_digest_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts
    
    def _map_name_sub(self, source, url_base):
        if getattr(source, "name", None):
            return [Extension(
                url=f"{url_base}/name",
                valueString=source.name
            )]
        return []

    def _map_description_sub(self, source, url_base):
        if getattr(source, "description", None):
            return [Extension(
                url=f"{url_base}/description",
                valueString=source.description
            )]
        return []

    def _map_aliases_sub(self, source, url_base):
        aliases = getattr(source, "aliases", []) or []
        return [
            Extension(
                url=f"{url_base}/alias",
                valueString=alias
            )
            for alias in aliases
        ]

    def _map_digest_sub(self, source, url_base):
        if getattr(source, "digest", None):
            return [Extension(
                url=f"{url_base}/digest",
                valueString=source.digest
            )]
        return []


# --------------------------------------------------------------------------------------------
    # Mapping Literal Sequence Expression

    def map_lit_to_rep_lit_expr(self,ao):
        rep = MolecularDefinitionRepresentation(
            code = self._map_codeable_concept(ao),
            literal= self._map_literal_representation(ao)
        )
        return rep

    def _map_coding(self, exp):
        #vrs.syntax -> rep.code.cc.coding.display
        #vrs.value -> rep.code.cc.coding.code
        #vrs.syntax_version -> rep.code.cc.coding.version
        return Coding(
            display = exp.syntax,
            code = exp.value,
            version = exp.syntax_version,
        )

    def _map_codeable_concept(self,ao):
        expressions = getattr(ao, "expressions", None)
        if not expressions:
            return None

        cc_list = []
        for exp in expressions:
            cc = CodeableConcept(
                id=exp.id,
                #NOTE: Extension in expression will be transalted below. this will be a loop of loops
                extension=self.map_extensions(source=exp),
                coding=[self._map_coding(exp)]
            )
            cc_list.append(cc)

        return cc_list

    def _map_representation_extensions(self,ao):
        return self._map_lse_extensions(
            source=ao.state,
            url_base="https://example.org/fhir/StructureDefinition/"
            )

    def _map_literal_representation(self,ao):
        state = getattr(ao, "state", None)

        id_ = getattr(state, "id", None)
        value = str(getattr(state, "sequence", ""))

        return MolecularDefinitionRepresentationLiteral(
            id=id_,
            extension=self._map_representation_extensions(ao),
            value=value
        )
        #vrs.lse.id -> moldefreplit.id
        # use extension: name goes to url, the value of the name goes into value[x]
        # same the above statement
        # same the above statement
        #NOTE: Extension in extension will be transalted below. this will be a loop of loops
        #NOTE: LSE type is a validation step
        #vrs.lse.sequence -> moldefreplit.value

# --------------------------------------------------------------------------------------------
    # Mapping Location
    def map_location(self,ao):
        return MolecularDefinitionLocation(
            id = ao.location.id,
            extension = self._map_location_extensions(source=ao),
            sequenceLocation=self._map_sequence_location(ao)
        )
    
    def _map_coordinate_interval(self,ao):
        start, end = Quantity(value=int(ao.location.start)),Quantity(value=int(ao.location.end))
        coord_system = CodeableConcept(
            coding=[Coding(
                system="http://loinc.org",
                code="LA30100-4",
                display="0-based interval counting"
                )]
            )
        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=coord_system
        )

        return MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=start,
            endQuantity=end,
        )
    
    def _map_sequence_location(self, ao):
        if getattr(ao.location, "sequence", ""):
            sequence_context = self._reference_location_sequence()
        elif getattr(ao.location, "referenceSequence", None):
            sequence_context = self._reference_sequence_reference()
        else:
            raise ValueError("Neither 'sequence' nor 'referenceSequence' is defined in ao.location, but one is required.")

        return MolecularDefinitionLocationSequenceLocation(
            sequenceContext=sequence_context, #NOTE: This is a required field. So if sequence and referenceSequence isn't present we need to substitute it with something. 
            coordinateInterval=self._map_coordinate_interval(ao)
        )
    
    def map_contained(self, ao):
        if getattr(ao.location, "sequence", ""):
            return self.build_location_sequence(ao)
        elif getattr(ao.location, "referenceSequence", None):
            return self.build_location_reference_sequence(ao)
        else:
            return None
        
    def build_location_sequence(self, ao):
        sequence_id = "vrs-location-sequence"
        sequence_value = getattr(ao.location, "sequence", "")

        rep_sequence = MolecularDefinitionRepresentationLiteral(value=sequence_value)

        return FhirSequence(
            id=sequence_id,
            representation=[rep_sequence]
        )
    
    def build_location_reference_sequence(self, ao):
        source = getattr(ao.location, "referenceSequence", None)
        if not source:
            return None

        seqref_id = getattr(source, "id", "")
        seqref_description = getattr(source, "description", "")
        seqref_refgetAccession = getattr(source, "refgetAccession", "")
        seqref_residueAlphabet = getattr(source, "residueAlphabet", "")
        seqref_sequence = getattr(source, "sequence", "")
        seqref_moleculeType = getattr(source, "moleculeType", "")

        rep_sequence = MolecularDefinitionRepresentationLiteral(
            value=seqref_sequence,
            encoding=CodeableConcept(
                coding=[Coding(
                    system="vrs 2.0 codes for alphabet",
                    code=seqref_residueAlphabet
                )]
            )
        )

        representation_sequence = MolecularDefinitionRepresentation(
            code=[CodeableConcept(
                coding=[Coding(
                    system="GA4GH RefGet identifier for the referenced sequence",
                    code=seqref_refgetAccession
                )]
            )],
            literal=rep_sequence
        )

        molecule_type = CodeableConcept(
            coding=[Coding(
                system="vrs 2.0 codes for alphabet",
                code=seqref_moleculeType
            )]
        )

        return FhirSequence(
            id=seqref_id,
            moleculeType=molecule_type,
            description=seqref_description,
            extension=self._map_refseq_extensions(source=source),
            representation=[representation_sequence]
        )
    
    def _reference_location_sequence(self):
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequence",
            display="VRS location.sequence as contained FHIR Sequence"
        )
    
    def _reference_sequence_reference(self):
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequenceReference",
            display = "VRS location.sequenceReference as contaiend FHIR Sequence"
        )
    #     #TODO: lets discuss ao.location.sequence 
    #     # sequence is a sequenceString with a cardinality of 0..1 and is described as The literal sequence encoded by the sequenceReference at these coordinates.
    #     # should map to location.seqLocation.seqContext
    #     # MolecularDefinitionLocationSequenceLocation(sequenceContext=Reference())