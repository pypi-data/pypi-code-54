from .mixins import BaseRequest
from .search_attribute import DictAttribute
from ..response import SaveResponse

class PutRequest(BaseRequest):
    def execute(self):
        response = self.client.put_item(**self.build())
        return SaveResponse(response, self.reconstructor)

    def item(self, item_dict):
        """add the item_dict to the search_attributes"""
        self.add_attribute(DictAttribute, 'Item', item_dict)
        return self


