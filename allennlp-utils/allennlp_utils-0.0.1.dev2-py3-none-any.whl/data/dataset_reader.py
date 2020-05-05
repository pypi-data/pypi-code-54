from typing import Iterable

from allennlp.data import DatasetReader, Instance


@DatasetReader.register("utils-atis")
class ATISDatasetReader(DatasetReader):
    """
    read the ATIS dataset for slot filling and intent detection task
    """
    def __init__(self):
        super(ATISDatasetReader, self).__init__()
        pass

    def text_to_instance(self, *inputs) -> Instance:
        pass

    def _read(self, file_path: str) -> Iterable[Instance]:
        pass