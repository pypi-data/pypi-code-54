import requests
import configparser

versionMapUrl = (
    "https://raw.githubusercontent.com/scleradb"
    "/sclera-version-map/master/versions.ini"
)

versionMap = configparser.ConfigParser()
 
def latest(org, name):
    """Get the latest version of the artifact with the given org, name"""

    if not ("com.scleradb" in versionMap):
        response = requests.get(versionMapUrl)
        response.raise_for_status()

        versionMap.read_string(response.text, source = versionMapUrl)

    if (not org in versionMap) or (not name in versionMap[org]):
        raise Exception(
            "Please specify the version for {}:{}".format(org, name)
        )

    return versionMap[org][name]
