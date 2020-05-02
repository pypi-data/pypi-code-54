from ..response import SearchResponse
from .mixins import BaseRequest, Filterable, Projectable, Limitable

class ScanRequest(
        BaseRequest,
        Filterable,
        Projectable,
        Limitable):
    def execute(self):
        response = self.client.scan(**self.build())
        return SearchResponse(response, self.reconstructor)
