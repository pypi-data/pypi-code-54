BASE_URL = "https://api.pacifices.cloud/v1/" # Base URL of PES's API

ROUTES = {
    "servers": {
        "base": BASE_URL + "servers",
        "validate": BASE_URL + "servers/validate",
        "logs": BASE_URL + "servers/{}/logs",
        "play_history": BASE_URL + "servers/{}/player-history",
        "player_count": BASE_URL + "servers/{}/player-count",
        "version": BASE_URL + "servers/{}/version",
        "command": BASE_URL + "servers/{}/command",
        "restart": BASE_URL + "servers/{}/restart",
        "update": BASE_URL + "servers/{}/update",
        "history": BASE_URL + "servers/{}/history",
    },
    "locations": BASE_URL + "locations",
    "mapgroups": BASE_URL + "mapgroups",
    "mods": BASE_URL + "mods",
    "plugins": BASE_URL + "plugins",
    "tickrates": BASE_URL + "tickrates",
    "gamemodes": BASE_URL + "gamemodes",
    "files": BASE_URL + "files",
}