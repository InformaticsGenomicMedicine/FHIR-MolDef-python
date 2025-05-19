from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference

from api.seqrepo import SeqRepoAPI
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
from translators.allele_utils import detect_sequence_type, is_valid_vrs_allele


class VRSAlleleToFHIRTranslator:

    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy

    def full_allele_translator(self,vrs_allele=None):
        #TODO: change MolecularDefinition to AlleleProfile
        is_valid_vrs_allele(vrs_allele)

        return MolecularDefinition(
            identifier= self.map_identifiers(vrs_allele),
            contained=[self.map_contained(vrs_allele)],
            description = self.map_description(vrs_allele),
            extension = self.map_extensions(vrs_allele),
            location = [self.map_location(vrs_allele)],
            representation = [self.map_lit_to_rep_lit_expr(vrs_allele)]
        )


# --------------------------------------------------------------------------------------------
    # Mapping identifiers
    def map_identifiers(self,ao):
        """Putting all the Identifiers together"""
        identifiers = []
        identifiers.extend(self._map_id(ao))
        identifiers.extend(self._map_name(ao))
        identifiers.extend(self._map_aliases(ao))
        identifiers.extend(self._map_digest(ao))
        return identifiers or None

    def _map_id(self,ao):
        """Mapping a vrs.id to a fhir Identifier"""
        value = getattr(ao,'id',None)
        if value:
            return [Identifier(value=value)]
        return []

    def _map_name(self,ao):
        """Mapping a vrs.name to a fhir Identifier"""
        value = getattr(ao,'name',None)
        if value:
            return [Identifier(value=value)]
        return []

    def _map_aliases(self,ao):
        """Mapping a vrs.aliases to a fhir Identifier"""
        value = getattr(ao,"aliases", None)
        if value:
            return [Identifier(value=alias) for alias in ao.aliases]
        return []

    def _map_digest(self, ao):
        """Mapping a vrs.digest to a fhir Identifier, hard coded system in this to reference the vrs digest in system"""
        value = getattr(ao,'digest',None)
        if value:
            # NOTE: url of vrs webpage that discribes the digest. This will be hard coded
            return [Identifier(value=value, system="https://vrs.ga4gh.org/en/stable/conventions/computed_identifiers.html#truncated-digest-sha512t24u")]
        return []

# --------------------------------------------------------------------------------------------
    # Mapping description
    def map_description(self,ao):
        """vrs.description will go to fhir description.markdown. This can be used in mulitple areas of the translation"""
        return getattr(ao,'description', None)

# --------------------------------------------------------------------------------------------
    # Validate that we are mapping a VRSAlelle to a FHIR Allele Profile

# --------------------------------------------------------------------------------------------
    # Mapping Extensions

    def map_extensions(self,source=None):
        """
        Maps VRS extension objects from the source to their FHIR representation using the _map_ext method.
        """
        vrs_exts = getattr(source,"extensions", None)
        if not vrs_exts:
            return None
        return [self._map_ext(ext_obj) for ext_obj in vrs_exts]

    def _map_ext(self, ext_obj):
        """
        Maps a VRS extension object to a FHIR Extension instance.
        """
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
        """Creates a FHIR Extension for the description attribute of the given extension object, if present. Note here description acts as a sub-extension"""
        if getattr(ext_obj, "description", None):
            return [Extension(url="description", valueString=ext_obj.description)]
        return []

    def _map_nested_extensions(self, ext_obj):
        """
        Returns a list of mapped extensions from the given object if it has extensions, otherwise returns an empty list. Note this is how we work with nested extensions if they are present.
        """
        if not getattr(ext_obj, "extensions", None):
            return []
        return [self._map_ext(nested) for nested in ext_obj.extensions]

    def _assign_extension_value(self, extension, value):
        """
        Assigns a value to the appropriate attribute of a FHIR extension based on the value's type (str, bool, or float).

        TODO: need to figure out how we are going to map dictionary, list and null values. 
        """

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
# --------------------------------------------------------------------------------------------
    # Mapping Sub-Extensions

    def _map_location_extensions(self, source, url_base):
        """
        Aggregates and returns a list of location-related extension mappings from the given source object.
        """

        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self._map_digest_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts

    def _map_lse_extensions(self, source, url_base):
        """
        Aggregates and returns a list of FHIR extension mappings for a given source object using various sub-mapping methods.
        NOTE location includes digest where literal sequence location expression doesnt
        """

        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts

    def _map_refseq_extensions(self, source, url_base):
        """
        Aggregates and returns a list of RefSeq-related FHIR extensions mapped from the source object.
        NOTE location includes digest where literal sequence location expression doesnt
        """
        exts = []
        exts.extend(self._map_name_sub(source, url_base))
        exts.extend(self._map_description_sub(source, url_base))
        exts.extend(self._map_aliases_sub(source, url_base))
        exts.extend(self._map_digest_sub(source, url_base))
        exts.extend(self.map_extensions(source=source) or [])
        return exts

    def _map_name_sub(self, source, url_base):
        """
        Creates a FHIR Extension for the 'name' attribute if present in the source object.
        
        """
        """"""
        if getattr(source, "name", None):
            return [Extension(
                url=f"{url_base}/name",
                valueString=source.name
            )]
        return []

    def _map_description_sub(self, source, url_base):
        """
        Map the 'description' attribute from the source object to a FHIR Extension if present.
        For this particualr extension we are hard coding the url because that is required by fhir. This URL is made up. 
        """

        if getattr(source, "description", None):
            return [Extension(
                url=f"{url_base}/description",
                valueString=source.description
            )]
        return []

    def _map_aliases_sub(self, source, url_base):
        """
        Creates a list of FHIR Extension objects for each alias found in the source object.
        """
        aliases = getattr(source, "aliases", []) or []
        return [
            Extension(
                url=f"{url_base}/alias",
                valueString=alias
            )
            for alias in aliases
        ]

    def _map_digest_sub(self, source, url_base):
        """
        Creates a FHIR Extension for the 'digest' attribute of the source object if it exists.
        """
        if getattr(source, "digest", None):
            return [Extension(
                url=f"{url_base}/digest",
                valueString=source.digest
            )]
        return []
# --------------------------------------------------------------------------------------------
    # Mapping Literal Sequence Expression

    def map_lit_to_rep_lit_expr(self,ao):
        """
        Maps an allele object to a MolecularDefinitionRepresentation with focus, code, and literal fields populated.
        # NOTE: focus_value this is hard coded because its required by AlleleProfile
        """
        focus_value = CodeableConcept(
            coding=[
                Coding(
                    system="http://hl7.org/fhir/moleculardefinition-focus",
                    code="allele-state",
                )
            ]
        )

        rep = MolecularDefinitionRepresentation(
            focus=focus_value,
            code = self._map_codeable_concept(ao),
            literal= self._map_literal_representation(ao)
        )
        return rep

    def _map_coding(self, exp):
        """
        Maps a VRS expression to a FHIR Coding object using its syntax, value, and syntax_version attributes.
        NOTE: mappings look like this: 
            vrs.syntax -> rep.code.cc.coding.display
            vrs.value -> rep.code.cc.coding.code
            vrs.syntax_version -> rep.code.cc.coding.version
        """

        return Coding(
            display = exp.syntax,
            code = exp.value,
            version = exp.syntax_version,
        )

    def _map_codeable_concept(self,ao):
        """
        Maps the 'expressions' attribute of the input object to a list of FHIR CodeableConcept instances.
        NOTE: we are using extenion method from above as well as the map_coding method 
        """
        expressions = getattr(ao, "expressions", None)
        if not expressions:
            return None

        cc_list = []
        for exp in expressions:
            cc = CodeableConcept(
                id=exp.id,
                extension=self.map_extensions(source=exp),
                coding=[self._map_coding(exp)]
            )
            cc_list.append(cc)

        return cc_list

    def _map_representation_extensions(self,ao):
        """
        Maps representation extensions from the given allele object (ao) using the _map_lse_extensions helper.
        NOTE: extension here is using one of the custom extension methods. 
        """

        return self._map_lse_extensions(
            source=ao.state,
            url_base="https://example.org/fhir/StructureDefinition/"
            )

    def _map_literal_representation(self,ao):
        """
        Maps a VRS Allele Object's literal sequence expression (LSE) state to a MolecularDefinitionRepresentationLiteral instance.
        NOTE: extension here is using one of the custom extension methods. 
            vrs.lse.id -> moldefreplit.id
            This extension the name goes to url adn the value of the name goes to the value[x] (this is the same for the other attributes)
            vrs.lse.sequence -> moldefreplit.value
        """
        state = getattr(ao, "state", None)

        id_ = getattr(state, "id", None)
        value = str(getattr(state, "sequence", ""))

        return MolecularDefinitionRepresentationLiteral(
            id=id_,
            extension=self._map_representation_extensions(ao),
            value=value
        )

# --------------------------------------------------------------------------------------------
    # Mapping Location
    def map_location(self,ao):
        """
        Maps an vrs locaiton to a MolecularDefinitionLocation FHIR resource.
        NOTE:
            location.id mapes to FHIR location id
            extension: we are using a custom extension for location
            sequenceLocation: this is a mandatory field, and we use either use the sequenceReference or Sequence in locaiton to populate this field.
        """
        """"""
        return MolecularDefinitionLocation(
            id = ao.location.id,
            extension = self._map_location_extensions(source=ao,
                                                      url_base="https://example.org/fhir/StructureDefinition/"),
            sequenceLocation=self._map_sequence_location(ao)
        )

    def _map_coordinate_interval(self,ao):
        """
        Maps an vrs allele start and end to FHIR MolecularDefinitionLocationSequenceLocationCoordinateInterval.
        NOTE: 
            vrs only uses 0-based interbas indexting so this is hard coded. 
        """

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
        """
        Maps a VRS Allele Object's location to a MolecularDefinitionLocationSequenceLocation, handling sequence context resolution.
        """
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
        """
        Maps the contained attribute of an allele object to the appropriate FHIR location representation based on its sequence or sequenceReference.
        """
        if getattr(ao.location, "sequence", ""):
            return self.build_location_sequence(ao)
        elif getattr(ao.location, "referenceSequence", None):
            return self.build_location_reference_sequence(ao)
        else:
            return None

    #NOTE:This is the same code as what is put in allele_translator.py
    def _translate_sequence_id(self, dp, expression):
        """Translate a sequence ID using SeqRepo and return the RefSeq ID.

        Args:
            dp (SeqRepo DataProxy): The data proxy used to translate the sequence.
            sequence_id (str): The sequence ID to be translated.

        Raises:
            ValueError: If translation fails or if format is unexpected.

        Returns:
            str: A valid RefSeq identifier (e.g., NM_000123.3).
        """
        sequence = f"ga4gh:{expression.location.get_refget_accession()}"
        translated_ids = dp.translate_sequence_identifier(sequence, namespace="refseq")
        if not translated_ids:
            raise ValueError(f"No RefSeq ID found for sequence ID '{sequence}'.")

        translated_id = translated_ids[0]
        if not translated_id.startswith("refseq:"):
            raise ValueError(f"Unexpected ID format in '{translated_id}'")

        _, refseq_id = translated_id.split(":")
        return refseq_id

    def build_location_sequence(self, ao):
        """
        Builds a SequenceProfile object when location.sequence is present. NOTE: moleculeType is a requirement in SequenceProfile so we need to catpure this and we do so by using 
        _translate_sequence_id. 
        TODO: need to decide if we want system present, currently there is nothing there. 
        """
        sequence_id = "vrs-location-sequence"
        sequence_value = str(getattr(ao.location, "sequence", ""))

        rep_literal = MolecularDefinitionRepresentationLiteral(value=sequence_value)
        rep_sequence = MolecularDefinitionRepresentation(literal=rep_literal)
        refgetAccession = self._translate_sequence_id(dp= self.dp, expression = ao)
        sequence_type = detect_sequence_type(refgetAccession)

        molecule_type = CodeableConcept(
            coding=[Coding(
                system="TBD", #TODO: THIS IS NOT Correct double check, note sure if we need this.
                code=sequence_type
            )]
        )
        return FhirSequence(
            id=sequence_id,
            moleculeType=molecule_type,
            representation=[rep_sequence]
        )

    def build_location_reference_sequence(self, ao):
        """
        Builds a SequenceProfile object when location.sequenceReference is present. Again we need to create a SequenceProfile and place this in the contained in the ALleleProfile that we are translating. 
        """
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
                    system="vrs 2.0 codes for alphabet",#TODO: Double check
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
                system="vrs 2.0 codes for moleculeType",#TODO: Double check
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
        """Createing reference objects for location.sequence"""
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequence",
            display="VRS location.sequence as contained FHIR Sequence"
        )

    def _reference_sequence_reference(self):
        """Createing reference objects for location.sequenceReference"""
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequenceReference",
            display = "VRS location.sequenceReference as contaiend FHIR Sequence"
        )
    #     #TODO: lets discuss ao.location.sequence
    #     # sequence is a sequenceString with a cardinality of 0..1 and is described as The literal sequence encoded by the sequenceReference at these coordinates.
    #     # should map to location.seqLocation.seqContext
    #     # MolecularDefinitionLocationSequenceLocation(sequenceContext=Reference())
