class Validate:
    def __init__(self, obj):
        self.obj = obj

    async def create(self, payload: dict):
        """ https://api.pacifices.cloud/docs.html#servers-server-payload-validation-post
                Validate's a payload.
                    - payload, this dict should be populated with details around the server.
        """
        
        return await self.obj._post(url=self.obj.ROUTES["servers"]["validate"], json=payload)

    async def settings(self, payload: dict):
        """ https://api.pacifices.cloud/docs.html#servers-server-payload-validation-put
                Validate a payload used to update a server’s settings.
                    - payload, this dict should be populated with details around the server.
        """

        return await self.obj._put(url=self.obj.ROUTES["servers"]["validate"], json=payload)