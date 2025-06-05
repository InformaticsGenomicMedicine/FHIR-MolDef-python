from ga4gh.vrs.models import Allele, SequenceLocation, SequenceReference, sequenceString
from ga4gh.core.models import Extension

from api.seqrepo import SeqRepoAPI
from translators.vrs_json_pointers import allele_identifiers as ALLELE_PTRS
from translators.vrs_json_pointers import extension_identifiers as EXT_PTRS
from translators.vrs_json_pointers import sequence_location_identifiers as SEQ_LOC
from translators.vrs_json_pointers import literal_sequence_expression_identifiers as LSE


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
        recursive_extensions = top_ext.get('extensions', [])

        extension_objects = []
        for ext in recursive_extensions:
            sub_extensions = [
                Extension(
                    id=sub_ext.get('id'),
                    name=sub_ext.get('name'),
                    value=sub_ext.get('value'),
                    description= sub_ext.get('description')
                )
                for sub_ext in ext.get('extensions', [])
            ]

            extension_objects.append(
                Extension(
                    id=ext.get('id'),
                    name=ext.get('name'),
                    value=ext.get('value'),
                    description= ext.get('description'),
                    extensions=sub_extensions or None
                )
            )

        return SequenceLocation(
            id=top_ext['id'],
            name=top_ext['name'],
            description=top_ext['description'],
            extensions=extension_objects or None,
            digest=top_ext['digest'],
            aliases=top_ext['aliases'],
            type = "SequenceLocation",
            sequenceReference=self._map_sequence_reference(),
            start=coord['start'],
            end=coord['end'],
            # sequence= # This needs to come from the contained value above
            )

    def _capture_coordinates(self,ao):
        coordinates = {}
        for loc in ao.location:
            coordinates['start'] = loc.id.sequenceLocation.coordinateInterval.startQuantity
            coordinates['end'] = loc.id.sequenceLocation.coordinateInterval.endQuantity
        return coordinates

    def _map_sequence_reference(self,ao):
        top_ext = self._extract_location_fields(ao.representation)[0]
        recursive_extensions = top_ext.get('extensions', [])

        extension_objects = []
        
        for ext in recursive_extensions:
            sub_extensions = [
                Extension(
                    id=sub_ext.get('id'),
                    name=sub_ext.get('name'),
                    value=sub_ext.get('value'),
                    description= sub_ext.get('description')
                )
                for sub_ext in ext.get('extensions', [])
            ]

            extension_objects.append(
                Extension(
                    id=ext.get('id'),
                    name=ext.get('name'),
                    value=ext.get('value'),
                    description= ext.get('description'),
                    extensions=sub_extensions or None
                )
            )

        return SequenceReference(
            id =top_ext['id'] ,
            name = top_ext['name'],
            description =top_ext['description'] ,
            aliases = top_ext['aliases'],
            extensions=extension_objects or None,
            # sequence=sequenceString()
        )

#------------------------------------------------------------------------------------------------------------------------------------------------#
    
#------------------------------------------------------------------------------------------------------------------------------------------------#

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
                "id": getattr(rep.literal.id, "id", None),
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


