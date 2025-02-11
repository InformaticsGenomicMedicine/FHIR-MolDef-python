# from ga4gh.vrs.dataproxy import SeqRepoRESTDataProxy
from ga4gh.vrs.extras.translator import Translator
from ga4gh.vrs.dataproxy import create_dataproxy
from exception import SeqRepoDataProxyCreationError

class SeqRepoAPI:
    DEFAULT_LOCAL_URL = "seqrepo+file:///usr/local/share/seqrepo/2021-01-29/"
    HOST_URL = "seqrepo+https://services.genomicmedlab.org/seqrepo"

    def __init__(self, seqrepo_data_proxy_url: str = None) -> None:
        """Initialize the SeqRepoAPI instance with the specified SeqRepo REST service URL.

        Args:
            seqrepo_data_proxy_url (str): The base URL of the SeqRepo REST service.

        Attributes:
            seqrepo_dataproxy (ga4gh.vrs.dataproxy.SeqRepoDataProxy): The data proxy for SeqRepoRESTData.
                It allows retrieval of genomic sequence data.
            tlr (ga4gh.vrs.extras.translator.Translator): The translator for handling genomic variations.
                It provides functionalities such as translation, normalization, and identification.
        """
        
        if seqrepo_data_proxy_url is None:
            seqrepo_data_proxy_url = self.DEFAULT_LOCAL_URL

        try:
            self.seqrepo_dataproxy = create_dataproxy(uri=seqrepo_data_proxy_url)
        except Exception as e:
            try:
                self.seqrepo_dataproxy = create_dataproxy(uri=self.HOST_URL)
            except:
                raise SeqRepoDataProxyCreationError(f"Failed to create seqrepo data proxy.")

        self.tlr = Translator(
            data_proxy=self.seqrepo_dataproxy,
            translate_sequence_identifiers=True,
            normalize=True,
            identify=True,
        )
