from ga4gh.vrs.models import Allele, SequenceLocation, SequenceReference

from api.seqrepo import SeqRepoAPI
from translators.vrs_json_pointers import allele_identifiers as ALLELE_PTRS
from translators.vrs_json_pointers import extension_identifiers as EXT_PTRS


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
        top_ext = self._capture_extension_values(ao)
        return SequenceLocation(
            id=top_ext['id'],
            name=top_ext['name'],
            description=top_ext['description'],
            extensions=self._capture_extension_values(ao),
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
        return SequenceReference()
#------------------------------------------------------------------------------------------------------------------------------------------------#
    def _capture_extension_values(self, ao):
        values = {}

        for ext in getattr(ao.location, "extension", []):
            url = getattr(ext, "url", "")
            val = getattr(ext, "valueString", None) or getattr(ext, "valueCode", None) or getattr(ext, "valueInteger", None)

            if EXT_PTRS['id'] in url:
                values['id'] = val
            elif EXT_PTRS['name'] in url:
                values['name'] = val
            elif EXT_PTRS['description'] in url:
                values['description'] = val
            elif EXT_PTRS['digest'] in url:
                values['digest'] = val
            elif EXT_PTRS['aliases'] in url:
                values.setdefault('aliases', []).append(val)
            elif EXT_PTRS['extension'] in url:
                values.setdefault('extension', []).append(self._capture_sub_extension_values(ext))

        return values


    def _capture_sub_extension_values(self, ext_obj):
        values = {}

        for sub_ext in getattr(ext_obj, "extension", []):
            url = getattr(sub_ext, "url", "")
            val = getattr(sub_ext, "valueString", None) or getattr(sub_ext, "valueCode", None) or getattr(sub_ext, "valueInteger", None)

            if EXT_PTRS['id'] in url:
                values['id'] = val
            elif EXT_PTRS['extensions'] in url:
                values.setdefault('extensions', []).append(self._capture_sub_extension_values(sub_ext))
            elif EXT_PTRS['name'] in url:
                values['name'] = val
            elif EXT_PTRS['description'] in url:
                values['description'] = val
            elif EXT_PTRS['digest'] in url:
                values['digest'] = val
            elif EXT_PTRS['aliases'] in url:
                values.setdefault('aliases', []).append(val)
            elif EXT_PTRS['value'] in url:
                values['value'] = val

        return values
