from . import versionmap

class Artifact:
    """Installable artifact"""

    def __init__(self, org, name, version = None):
        self.org = org
        self.name = name
        self.version = version if version else versionmap.latest(org, name)

    def __eq__(self, x):
        return (self.org, self.name, self.version) == (x.org, x.name, x.version)

    def __hash__(self):
        return hash((self.org, self.name, self.version))

    def __repr__(self):
        return "Artifact({}, {}, {})".format(self.org, self.name, self.version)

    def __str__(self):
        return "{} : {} : {}".format(self.org, self.name, self.version)

def pathGen():
    """Classpath generator, \
       works with SBT launcher to install dependencies and emit classpaths"""

    return Artifact("com.scleradb", "sclera-install-pathgen")

def initArtifacts():
    """Initial minimal set of artifacts to get the shell running"""

    return [
        Artifact("com.scleradb", "sclera-config"),
        Artifact("com.scleradb", "sclera-core"),
        Artifact("com.scleradb", "sclera-shell")
    ]

def installed(bootDir):
    """Read the list of installed artifacts from boot dir"""

    for namedir in bootDir.iterdir():
        for versiondir in namedir.iterdir():
            yield Artifact("com.scleradb", namedir.name, versiondir.name)

def updated(artifact):
    return Artifact(artifact.org, artifact.name)

def parse(spec):
    """Parse the input artifact specification: <name> or <name>:<version>"""

    strs = spec.split(":")
    n = len(strs)

    org = "com.scleradb"
    version = None

    if n == 3:
        org = strs[0]
        name = strs[1]
        version = strs[2]
    elif n == 2:
        name = strs[0]
        version = strs[1]
    elif n == 1:
        name = strs[0]
    else:
        raise ValueError("Incorrect artifact specification: [{}]".format(spec))

    return Artifact(org, name, version)
