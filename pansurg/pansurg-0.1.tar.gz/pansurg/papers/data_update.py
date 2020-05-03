import urllib.request
import tarfile
import json
from typing import List


class DataUpdate:
    """
    This class is responsible for getting the papers from the Alan Institute.
    Attributes:
        data (List[dict]) JSON data of the papers that need to be uploaded into the data
    """
    data: List[dict]

    def __init__(self) -> None:
        self._url = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/noncomm_use_subset.tar.gz"
        self.data = []

    def get_data(self) -> None:
        """
        Gets JSON data from the source from the self._url and populates the self.data.
        :return: None
        """
        ftp_stream = urllib.request.urlopen(self._url)
        tar_file = tarfile.open(fileobj=ftp_stream, mode="r|gz")

        for member in tar_file:
            if "xml" not in member.path:
                data = tar_file.extractfile(member=member)
                content = json.loads(data.read())
                self.data.append(content)
