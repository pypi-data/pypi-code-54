from .mixins import BaseRequest, Keyable, Returnable
from ..response import DeleteResponse

class DeleteRequest(BaseRequest, Keyable, Returnable):
    def execute(self):
        response = self.client.delete_item(**self.build())
        return DeleteResponse(response, self.reconstructor)
