from .mixins import BaseRequest, Keyable, Projectable
from ..response import GetResponse

class GetRequest(BaseRequest, Keyable, Projectable):
    def execute(self):
        response = self.client.get_item(**self.build())
        return GetResponse(response, self.reconstructor)

