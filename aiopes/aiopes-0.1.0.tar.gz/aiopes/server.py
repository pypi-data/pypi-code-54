class Server:
    def __init__(self, server_id, obj):
        self.obj = obj
        self.server_id = server_id

    async def list(self, **kwargs):
        """ https://api.pacifices.cloud/docs.html#servers-servers 
                Lists servers matching those parameters.
        """

        return await self.obj._get(url=self.obj.query_string(self.obj.ROUTES["servers"]["base"], kwargs))

    async def create(self, payload: dict):
        """ https://api.pacifices.cloud/docs.html#servers-servers-post
                Creates a new server.
                    - payload, this dict should be populated with details around the server.
        """

        return await self.obj._post(url=self.obj.ROUTES["servers"]["base"], json=payload)

    async def get(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-get 
                Retrieve a server’s information.
        """
        
        return await self.obj._get(url=self.obj.path_var(self.obj.ROUTES["servers"]["base"], self.server_id))

    async def delete(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-delete
                Destroy a server.
        """

        return await self.obj._delete(url=self.obj.path_var(self.obj.ROUTES["servers"]["base"], self.server_id))

    async def settings(self, payload: dict):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-put
                Change a server’s settings. Also performs an update on the server to ensure the server settings are applied.
                    - payload, this dict should be populated with details around the server.
        """

        return await self.obj._put(url=self.obj.path_var(self.obj.ROUTES["servers"]["base"], self.server_id), json=payload)

    async def logs(self, json=True):
        """ https://api.pacifices.cloud/docs.html#servers-server-logs-get
                Retrieve a server’s logs.
                    - json, should we return a dict or data.
        """

        if json:
            query_string = "?format=json"
        else:
            query_string = "?format=raw"

        return await self.obj._get(url=self.obj.ROUTES["servers"]["logs"] + query_string.format(self.server_id), return_json=json)

    async def player_history(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-player-history-get
                Get a history of the player count on the server.
        """

        return await self.obj._get(url=self.obj.ROUTES["servers"]["play_history"].format(self.server_id))
    
    async def player_count(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-player-count-get
                Get the current count of players in the server.
        """

        return await self.obj._get(url=self.obj.ROUTES["servers"]["player_count"].format(self.server_id))

    async def version(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-version-get
                Get the current server version and whether the server is up-to-date.
        """

        return await self.obj._get(url=self.obj.ROUTES["servers"]["version"].format(self.server_id))

    async def command(self, command):
        """ https://api.pacifices.cloud/docs.html#servers-server-command-post
                Send a command to a server.
                    - command, CSGO command.
        """

        return await self.obj._post(url=self.obj.ROUTES["servers"]["command"].format(self.server_id), json={"command": command})

    async def restart(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-restart-post
                Restart a server.
                    - server_id, PES's server ID.
        """

        return await self.obj._post(url=self.obj.ROUTES["servers"]["restart"].format(self.server_id))

    async def update(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-update-post
                Update a server.
                    - server_id, PES's server ID.
        """

        return await self.obj._post(url=self.obj.ROUTES["servers"]["update"].format(self.server_id))

    async def history(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-history-get
                Retrieve a server’s history.
                    - server_id, PES's server ID.
        """

        return await self.obj._get(url=self.obj.ROUTES["servers"]["history"].format(self.server_id))