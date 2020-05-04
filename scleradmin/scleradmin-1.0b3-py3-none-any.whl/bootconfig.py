import configparser

def bootPropsConfig(artifact, resources, targetDir, scalaVersion = "2.13.1"):
    """Create the configuration to install an artifact and its dependencies"""

    scala = {}
    scala["version"] = scalaVersion

    app = {}
    app["org"] = artifact.org
    app["name"] = artifact.name
    app["version"] = artifact.version
    app["class"] = "com.scleradb.pathgen.Main"
    app["cross-versioned"] = "binary"
    if resources:
        app["resources"] = ", ".join(resources)

    repositories = {}
    repositories["local"] = None
    repositories["typesafe-ivy-releases"] = "http://repo.typesafe.com/typesafe/ivy-releases/, [organization]/[module]/[revision]/[type]s/[artifact](-[classifier]).[ext]"
    repositories["maven-central"] = None
    repositories["Sonatype OSS Snapshots"] = "https://oss.sonatype.org/content/repositories/snapshots"
    
    boot = {}
    boot["directory"] = targetDir
    
    log = {}
    log["level"] = "error"

    config = configparser.ConfigParser(allow_no_value = True, delimiters = ":")

    config["scala"] = scala
    config["app"] = app
    config["repositories"] = repositories
    config["boot"] = boot
    config["log"] = log

    return config

def writeConfig(config, targetPath):
    """Write the configuration into the specified file"""

    with open(targetPath, "wt") as f:
        config.write(f, space_around_delimiters = False)
