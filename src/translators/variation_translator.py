### will be attempting to transalte spdi, and hgvs to FHIR Variation Profile
# Variation profile includes two representations
# alt and ref state

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs.dataproxy import create_dataproxy

from profiles.variation import Variation
from resources.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from translators.allele_utils import detect_sequence_type
from vrs_tools.hgvs_tools import HgvsToolsLite

class VariationTranslation:

    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)
        #most likely need to replace this
        self.hgvs_tools = HgvsToolsLite(data_proxy=self.dp)

    def _spdi_coordinate_interval(self):
        system = CodeableConcept(
                coding=[Coding(
                        system="http://loinc.org",
                        code =  "LA30100-4",
                        display =  "0-based interval counting",
                )
                ]
            )
        
        origin = CodeableConcept(
                coding=[Coding(
                        system="http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                        code =  "sequence-start",
                        display =  "Sequence start",
                )
                ]
            )

        normalizationMethod = CodeableConcept(
                coding=[Coding(
                        system="http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                        code =  "fully-justified", 
                        display = "Fully justified" 
                )
                ]
            )
        
        return system, origin, normalizationMethod
    
    def _hgvs_coordinate_interval(self):
        system = CodeableConcept(
                coding=[Coding(
                        system="http://loinc.org",
                        code =  "LA30102-0",
                        display =  "1-based character counting",
                )
                ]
            )
        
        origin = CodeableConcept(
                coding=[Coding(
                        system="http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                        code =  "feature-start",
                        display =  "Feature start",
                )
                ]
            )

        normalizationMethod = CodeableConcept(
                coding=[Coding(
                        system="http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                        code =  "right-shift", 
                        display = "Right shift" 
                )
                ]
            )
        
        return system, origin, normalizationMethod
    
    def _hgvs_position(self, sv):
        pos = sv.posedit.pos
        return pos.start.base, pos.end.base
    
    # TODO: This function was copied from another module. Consider moving it to `allele_utils.py`.
    # NOTE: The name `allele_utils` might not be ideal, since this function is also used in the
    #       variation module, which could cause confusion.
    def _refseq_to_fhir_id(self, refseq_accession):
        """Converts a RefSeq accession string to a standardized FHIR ID format.
        This method removes the version suffix (after the dot), strips out underscores,
        and converts the string to lowercase to ensure compatibility with FHIR resource IDs.

        Args:
            refseq_accession (str): A RefSeq accession string (e.g., 'NM_001256789.1').

        Returns:
            str: A formatted FHIR-compatible ID (e.g., 'nm001256789').
        """
        return refseq_accession.split(".", 1)[0].replace("_", "").lower()

    def _from_spdi(self,spdi):
        """Parse an SPDI string and convert it into a FHIR Variation Profile object.

        Args:
            spdi (str): A valid spdi string. "<sequence_accession>:<position>:<deleted_sequence_or_length>:<inserted_sequence>".

        Raises:
            TypeError: If the provided `spdi` argument is not a string.
            ValueError:  If the SPDI string does not contain four colon-separated fields or 
            cannot be parsed correctly.

        Returns:
            object: A FHIR Variation Profile object representing the parsed SPDI variant.
        """
        if not isinstance(spdi,str):
            raise TypeError("SPDI expression must be a string.")

        try:
            seq_acc,pos,del_seq_or_len,ins_seq = spdi.split(":",maxsplit=3)
        except:
            raise ValueError(f"Invalid SPDI expected four colon-separated fields: {spdi}")

        seq_acc = str(seq_acc).strip()

        start = int(pos)

        try:
            del_len = int(del_seq_or_len)
        except ValueError:
            del_len = len(del_seq_or_len)
        end = start + del_len

        alt_seq = str(ins_seq)

        aliases = self.dp.translate_sequence_identifier(seq_acc, "refseq")
        aliases = [a.split(":")[1] for a in aliases]
        ref_seq = self.dp.get_sequence(aliases[0],start,end)

        values = {
            "refget_accession": seq_acc,
            "start": start,
            "end": end,
            "ref_seq": ref_seq,
            "alt_seq": alt_seq
        }

        return self._create_variation_profile(values,fmt="spdi")

    def _from_hgvs(self,hgvs_expr):
        
        sv = self.hgvs_tools.parse(hgvs_expr)
        if not sv:
            return None

        if self.hgvs_tools.is_intronic(sv):
            raise ValueError("Intronic HGVS variants are not supported")

        start_pos, end_pos, alt_seq = self.hgvs_tools.get_position_and_state(sv)

        edit_type = self.hgvs_tools.get_edit_type(sv)

        if edit_type in {"del","delins","dup"}:
            ref_seq = self.dp.get_sequence(sv.ac,start_pos,end_pos)
        elif edit_type == "ins":
            ref_seq = sv.posedit.edit.ref or ""
        elif edit_type == "sub":
            ref_seq = sv.posedit.edit.ref
        elif edit_type == "identity":
            ref_seq = self.dp.get_sequence(sv.ac,start_pos,end_pos)
            if not ref_seq:
                ref_seq = sv.posedit.edit.alt or ""
        else:
            raise NotImplementedError(f"Unsupported HGVS edit type: {edit_type}")
        
        start,end = self._hgvs_position(sv)

        values = {
            "refget_accession": sv.ac,
            "start": start,
            "end": end,
            "ref_seq": ref_seq,
            "alt_seq": alt_seq,
            }

        return self._create_variation_profile(values, fmt="hgvs")

    def _create_variation_profile(self,values,fmt):
        """Create a FHIR Variation resource from parsed variant data (HGVS or SPDI).

        Args:
            values (dict): A dictionary containing variant attributes. (Refget Accession,Start,End,Reference Sequence, Alternative Sequence)

        Returns:
            object: A fully populated FHIR Variation object.
        """
        MOLTYPE_SYSTEM_DEFAULT_VALUE = "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecule-type"
        FOCUS_SYSTEM_DEFAULT_VALUE = "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus"

        sequence_type = detect_sequence_type(values["refget_accession"])

        mol_type = CodeableConcept(
            coding=[Coding(
                system =  MOLTYPE_SYSTEM_DEFAULT_VALUE,
                code =  sequence_type.lower(),
                display =  f"{sequence_type} Sequence",
                )])

        if fmt == "hgvs":
            coord_system_values, coord_system_origin, normalization_method = self._hgvs_coordinate_interval()
        elif fmt == "spdi":
            coord_system_values, coord_system_origin, normalization_method = self._spdi_coordinate_interval()

        fhir_id = self._refseq_to_fhir_id(refseq_accession=values["refget_accession"])

        sequence_context = Reference(
            reference=f"#ref-to-{fhir_id}",
            type = "MolecularDefinition",
            display= values['refget_accession']
        )

        coord_system = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
                system=coord_system_values,
                origin=coord_system_origin,
                normalizationMethod= normalization_method
            )

        start, end = Quantity(value=int(values["start"])),Quantity(value=int(values["end"]))

        coord_interval = MolecularDefinitionLocationSequenceLocationCoordinateInterval(
                coordinateSystem=coord_system,
                startQuantity=start,
                endQuantity=end,
            )

        seq_loc = MolecularDefinitionLocationSequenceLocation(
                sequenceContext=sequence_context, coordinateInterval=coord_interval
            )
        location = MolecularDefinitionLocation(sequenceLocation=seq_loc)

        ############################ Rep trans ########################
        ref_state_lit_value = MolecularDefinitionRepresentationLiteral(
            value=values["ref_seq"]
        )
        ref_state_rep = MolecularDefinitionRepresentation(
            focus= CodeableConcept(
                coding=[Coding(
                    system=FOCUS_SYSTEM_DEFAULT_VALUE,
                    code="reference-state",
                    display="Reference State"
                )]
            ),
            literal=ref_state_lit_value
        )

        alt_state_lit_value = MolecularDefinitionRepresentationLiteral(
            value=values["alt_seq"]
        )

        alt_state_rep = MolecularDefinitionRepresentation(
            focus= CodeableConcept(
                coding=[Coding(
                    system=FOCUS_SYSTEM_DEFAULT_VALUE,
                    code="alternative-state",
                    display="Alternative State"
                )]
            ),
            literal=alt_state_lit_value
        )
        ############################ Rep trans ########################

        return Variation(
            # id="PLACEHOLDER VALUE FOR NOW",
            #contained = this is where you might want to place the refseq accission but do this later.
            moleculeType = mol_type,
            location=[location],
            representation=[ref_state_rep,alt_state_rep]
        )

    def translate_from(self, var, fmt):
        """Translate a variant (HGVS or SPDI) into a FHIR Variation object.

        Args:
            var (str): A variant expression in HGVS or SPDI format.
            fmt (str): The input format of the variant. Must be either "hgvs" or "spdi".

        Raises:
            ValueError: If an unsupported format is provided (i.e., not "hgvs" or "spdi").

        Returns:
            object: A FHIR Variation object representing the parsed variant.
        """
        if fmt == "hgvs":
            return self._from_hgvs(var)
        elif fmt == "spdi":
            return self._from_spdi(var)
        else:
            raise ValueError("Only 'hgvs' and 'spdi' formats are supported.")
