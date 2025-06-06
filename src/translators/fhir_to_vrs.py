from ga4gh.core.models import Extension
from ga4gh.vrs.models import (
    Allele,
    LiteralSequenceExpression,
    SequenceLocation,
    SequenceReference,
    sequenceString,
)

from api.seqrepo import SeqRepoAPI
from translators.vrs_json_pointers import allele_identifiers as ALLELE_PTRS
from translators.vrs_json_pointers import extension_identifiers as EXT_PTRS
from translators.vrs_json_pointers import literal_sequence_expression_identifiers as LSE
from translators.vrs_json_pointers import sequence_location_identifiers as SEQ_LOC


class FhirToVrsAllele:

    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy

    def full_allele_translator(self,ao):
        meta = self._map_meta(ao)
        return Allele(
            id=meta['id'],
            name=meta['name'],
            type="Allele",
            aliases=meta['aliases'],
            digest=meta['digest'],
            description=ao.description,
            location=self._map_sequence_location(ao),
            state = self._map_literal_sequence_expression(ao)
        )

    def _map_meta(self,ao):

        values = {}

        for identifier in ao.identifier:
            if ALLELE_PTRS['id'] in identifier.system:
                values['id'] = identifier.value
            if ALLELE_PTRS['name'] in identifier.system:
                values['name'] = identifier.value
            if ALLELE_PTRS['digest'] in identifier.system:
                values['digest'] = identifier.value
            if ALLELE_PTRS['aliases'] in identifier.system:
                values.setdefault('aliases', []).append(identifier.value)

        return values
#------------------------------------------------------------------------------------------------------------------------------------------------#

    def _map_sequence_location(self,ao):
        coord = self._capture_coordinates(ao)
        top_ext = self._extract_location_fields(ao.location)[0]

        extension_objects = self._map_extension(top_ext)
        #TODO: rename these
        seq, _ = self._capture_contained(ao)
        lit_seq = self._capture_seuqence_contained_valeus(seq)

        return SequenceLocation(
            id=top_ext['id'],
            name=top_ext['name'],
            description=top_ext['description'],
            extensions=extension_objects,
            digest=top_ext['digest'],
            aliases=top_ext['aliases'],
            type = "SequenceLocation",
            sequenceReference=self._map_sequence_reference(ao),
            start=coord['start'],
            end=coord['end'],
            sequence=sequenceString(lit_seq)# This needs to come from the contained value above
            )

    def _capture_coordinates(self, ao):
        loc = ao.location[0]
        return {
            'start': loc.sequenceLocation.coordinateInterval.startQuantity.value,
            'end': loc.sequenceLocation.coordinateInterval.endQuantity.value
        }

    def _map_sequence_reference(self,ao):
        top_ext = self._extract_location_fields(ao.location)[0]
        extension_objects = self._map_extension(ext=top_ext)
        #TODO: rename these
        _,sequenceReference = self._capture_contained(ao)

        refgetAccession,moleculeType,residueAlphabet,lit_seq = self._capture_sequenceReference_contained_values(sequenceReference)

        return SequenceReference(
            id =top_ext['id'] ,
            name = top_ext['name'],
            description =top_ext['description'],
            aliases = top_ext['aliases'],
            extensions=extension_objects,
            refgetAccession = refgetAccession, #top_ext['digest'], #need to capture this from contained value
            residueAlphabet = residueAlphabet,
            moleculeType=moleculeType,
            sequence=sequenceString(lit_seq)
        )

#------------------------------------------------------------------------------------------------------------------------------------------------#

    def _map_literal_sequence_expression(self,ao):
        top_ext = self._extract_literal_fields(ao.representation)[0]
        extension_objects = self._map_extension(top_ext)

        return LiteralSequenceExpression(
            id=top_ext['id'],
            name=top_ext['name'],
            description=top_ext['description'],
            aliases = top_ext['aliases'],
            extensions=extension_objects,
            sequence=sequenceString(self._capture_sequence(ao))
        )

    def _capture_sequence(self,ao):
        return ao.representation[0].literal.value
#------------------------------------------------------------------------------------------------------------------------------------------------#
    def _map_extension(self, ext):
        recursive_extensions = ext.get('extensions', [])
        extension_objects = []

        for ext_dict in recursive_extensions:
            sub_extensions = self._map_extension(ext_dict)

            extension_objects.append(
                Extension(
                    id=ext_dict.get('id'),
                    name=ext_dict.get('name'),
                    value=ext_dict.get('value'),
                    description=ext_dict.get('description'),
                    extensions=sub_extensions or None
                )
            )
        return extension_objects or None

    def _extract_location_fields(self,location_obj):
        results = []

        for loc in location_obj:
            result = {
                "id": getattr(loc, "id", None),
                "name": None,
                "description": None,
                "digest": None,
                "aliases": [],
                "extensions": []
            }

            for ext in getattr(loc, "extension", []):
                url = getattr(ext, "url", "") or ""
                val = getattr(ext, "valueString", None)

                if SEQ_LOC["name"] in url:
                    result["name"] = val
                elif SEQ_LOC["description"] in url:
                    result["description"] = val
                elif SEQ_LOC["digest"] in url:
                    result["digest"] = val
                elif SEQ_LOC["aliases"] in url:
                    result["aliases"].append(val)
                elif getattr(ext, "id", None):
                    nested = self._extract_nested_extensions([ext])
                    if nested:
                        result["extensions"].extend(nested)
            results.append(result)

        return results

    def _extract_literal_fields(self,representation_obj):
        results = []

        for rep in representation_obj:
            literal = getattr(rep, "literal", None)
            if literal is None:
                continue

            result = {
                "id": getattr(rep.literal, "id", None),
                "name": None,
                "description": None,
                "aliases": [],
                "extensions": []
            }


            for ext in getattr(literal, "extension", []):
                url = getattr(ext, "url", "") or ""
                val = getattr(ext, "valueString", None)

                if LSE["name"] in url:
                    result["name"] = val
                elif LSE["description"] in url:
                    result["description"] = val
                elif LSE["aliases"] in url:
                    result["aliases"].append(val)
                elif getattr(ext, "id", None):
                    nested = self._extract_nested_extensions([ext])
                    if nested:
                        result["extensions"].extend(nested)
            results.append(result)

        return results

    def _extract_nested_extensions(self,extension_list):
        results = []

        for ext in extension_list or []:
            ext_id = getattr(ext, "id", None)

            if ext_id:
                block = {"id": ext_id}

                inner = getattr(ext, "extension", []) or []
                nested_blocks = []

                for inner_ext in inner:
                    inner_url = getattr(inner_ext, "url", "") or ""
                    inner_val = getattr(inner_ext, "valueString", None)

                    if EXT_PTRS["name"] in inner_url:
                        block["name"] = inner_val
                    elif EXT_PTRS["value"] in inner_url:
                        block["value"] = inner_val
                    elif EXT_PTRS["description"] in inner_url:
                        block["description"] = inner_val
                    elif getattr(inner_ext, "id", None):
                        nested_blocks.extend(self._extract_nested_extensions([inner_ext]))

                if nested_blocks:
                    block["extensions"] = nested_blocks

                results.append(block)

        return results

#------------------------------------------------------------------------------------------------------------------------------------------------#
    def _capture_contained(self,ao):

        contained = ao.contained

        contained_values = {
            "vrs-location-sequence": None,
            "vrs-location-sequenceReference": None
        }

        for values in contained:
            if values.id == "vrs-location-sequence":
                contained_values['vrs-location-sequence'] = values
            elif values.id == "vrs-location-sequenceReference":
                contained_values['vrs-location-sequenceReference'] = values
            else:
                raise ValueError("contained values didn't include vrs-location-sequence or vrs-location-sequenceReference")

        return contained_values['vrs-location-sequence'], contained_values['vrs-location-sequenceReference']

    def _capture_seuqence_contained_valeus(self,sequence):
        
        return sequence.representation[0].literal.value

    def _capture_sequenceReference_contained_values(self,sequenceReference):

        return sequenceReference.representation[0].code[0].coding[0].code, sequenceReference.moleculeType.coding[0].code, sequenceReference.representation[0].literal.encoding.coding[0].code, sequenceReference.representation[0].literal.value

