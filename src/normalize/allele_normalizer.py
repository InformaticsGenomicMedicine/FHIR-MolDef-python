# NOTE: This is just a temporary class for now.
from ga4gh.core import ga4gh_identify
from ga4gh.vrs import normalize as vrs_normalize

from api.seqrepo_api import SeqRepoAPI


class AlleleNormalizer:
    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy

    def post_normalize_allele(self, allele):
        """Normalize the VRS allele and assign GA4GH identifiers.

        Args:
            allele (models.Allele): The VRS allele to be normalized.

        Returns:
            models.Allele: The normalized VRS allele with GA4GH identifiers.

        """
        # Translating the sequence id to ga4gh format
        seq_id = self.dp.translate_sequence_identifier(
            allele.location.sequence_id._value, "ga4gh"
        )[0]
        allele.location.sequence_id = seq_id
        # Using the ga4gh normalize function to normalize the allele. (Coming form biocommons.normalize())
        allele = vrs_normalize(allele, self.dp)
        # Setting the allele id to a  GA4GH digest-based id for the object, as a CURIE
        allele._id = ga4gh_identify(allele)
        # Setting the location id to a GA4GH digest-based id for the object, as a CURIE
        allele.location._id = ga4gh_identify(allele.location)
        return allele

