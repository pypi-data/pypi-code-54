import sys
import os
import stat
import subprocess
import requests
import re
import pathlib
import logging
import pkg_resources

from . import artifacts
from . import bootconfig

launcherUrl = (
    "https://repo1.maven.org/maven2"
    "/org/scala-sbt/launcher/1.1.3/launcher-1.1.3.jar"
)

def run(args, platform = sys.platform):
    """Install, add/remove artifacts"""

    initArtifacts = artifacts.initArtifacts()
    pathGen = artifacts.pathGen()

    # home subdirectory structue
    dirs = scleraDirs(
        rootDirStr = args.root[0],
        isInstall = args.install,
        isOverwrite = args.overwrite
    )

    # install config file
    installResource("config/sclera.conf", dirs["config"] / "sclera.conf")

    logging.basicConfig(
        filename = dirs["log"] / "install.log",
        level = logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )

    # Already installed packages
    prevInstalled = set(artifacts.installed(dirs["boot"]))
    prevInstalled.discard(pathGen)

    logging.info("prevInstalled: {}".format(prevInstalled))

    addArtifacts = [artifacts.parse(p) for p in (args.add or [])]
    remArtifacts = [artifacts.parse(p) for p in (args.remove or [])]

    # check if packages can be removed
    for artifact in remArtifacts:
        if artifact in initArtifacts:
            raise ValueError(
                "Cannot remove reserved package {}".format(artifact.name)
            )
        if artifact in addArtifacts:
            raise ValueError(
                "Cannot both add and remove package {}".format(artifact.name)
            )
        if artifact not in prevInstalled:
            raise ValueError(
                "Cannot remove package {} (not installed)".format(artifact.name)
            )

    if not (args.install or args.update):
        # prune packages which are already present
        addArtifacts = [a for a in addArtifacts if a not in prevInstalled]
        if not addArtifacts and not remArtifacts:
            print("Nothing to be added or removed. Exiting.")
            return

    logging.info("Removing: {}".format(remArtifacts))

    # remove packages
    for artifact in remArtifacts:
        print("Removing: {} ...".format(artifact), end = " ", flush = True)

        try:
            removeArtifact(artifact = artifact, bootDir = dirs["boot"])
        except:
            print("Failed.", flush = True)
            raise

        print("Done.", flush = True)

        prevInstalled.remove(artifact)

    if args.install:
        # artifacts in addArtifacts mask those in initArtifacts
        addArtifacts = merge(initArtifacts, addArtifacts)

    if args.update:
        # update versions of previously installed artifacts
        updated = [artifacts.updated(a) for a in prevInstalled]
        addArtifacts = merge(updated, addArtifacts)
    else:
        # artifacts in addArtifacts mask those in prevInstalled
        # -- enables artifact version change
        addArtifacts = merge(prevInstalled, addArtifacts)

    # remove the masked artifacts
    # necessary because only one version of an artifact should be present
    maskedArtifacts = prevInstalled.difference(addArtifacts)

    logging.info("Removing: {}".format(maskedArtifacts))

    for artifact in maskedArtifacts:
        print("Removing: {} ...".format(artifact), end = " ", flush = True)

        try:
            removeArtifact(artifact = artifact, bootDir = dirs["boot"])
        except:
            print("Failed.", flush = True)
            raise

        print("Done.", flush = True)

        prevInstalled.remove(artifact)

    # download launcher, add pathgen
    print("Preparing to install ...", end = " ", flush = True)

    try:
        launcherPath = downloadFile(
            url = launcherUrl, targetDir = dirs["install"]
        )

        installPaths = installArtifact(
            launcherPath = launcherPath,
            artifact = pathGen,
            resources = [],
            targetDir = dirs["lib"],
            bootDir = dirs["boot"]
        )
    except:
        print("Failed.", flush = True)
        raise

    print("Done.", flush = True)

    logging.info("Launcher: {}".format(launcherPath))
    logging.info("{}: {}".format(pathGen.name, installPaths))

    # add packages
    logging.info("Adding: {}".format(addArtifacts))

    # add packages and collect the class paths
    paths = []
    for artifact in addArtifacts:
        print("{} {} ...".format(
            "Reinstalling" if artifact in prevInstalled else "Installing",
            artifact
        ), end = " ", flush = True)

        try:
            libPaths = installArtifact(
                launcherPath = launcherPath,
                artifact = artifact,
                resources = installPaths,
                targetDir = dirs["lib"],
                bootDir = dirs["boot"]
            )
        except:
            print("Failed.", flush = True)
            raise

        print("Done.", flush = True)

        for path in libPaths:
            if path not in paths:
                paths.append(path)

    paths.extend(str(dirs[x]) for x in ("config", "extlib"))
    scriptPath = installScript(
        paths = paths,
        rootDir = dirs["sclera"],
        targetDir = dirs["bin"],
        platform = platform
    )

    if args.install:
        initSclera(scriptPath)

    print("Sclera installed at: {}".format(dirs["sclera"]))
    print("Executable script: {}".format(scriptPath))

def scleraDirs(rootDirStr, isInstall, isOverwrite):
    """Sclera installation directory structure"""

    d = {}
    d["sclera"] = pathlib.Path(rootDirStr).resolve()
    d["bin"] = d["sclera"] / "bin"
    d["home"] = d["sclera"] / "home"
    d["config"] = d["sclera"] / "config"
    d["lib"] = d["sclera"] / "lib"
    d["extlib"] = d["sclera"] / "extlib"
    d["install"] = d["sclera"] / "install"
    d["boot"] = d["install"] / "boot"
    d["log"] = d["install"] / "log"

    if not isInstall and not d["sclera"].exists():
        raise ValueError("Please install Sclera first, using --install")

    if isInstall and not isOverwrite and d["sclera"].exists():
        raise ValueError(
            "Directory exists, cannot overwrite: {}".format(d["sclera"])
        )

    for targetDir in d.values():
        targetDir.mkdir(parents = True, exist_ok = True)

    return d

def merge(prevArtifacts, nextArtifacts):
    """Merge artifact lists with nextArtifacts masking prevArtifacts"""

    artifactList = list(nextArtifacts.copy())
    artifactList.extend(prevArtifacts)

    merged = []
    excludedNames = set()
    for artifact in artifactList:
        if artifact.name not in excludedNames:
            merged.append(artifact)
            excludedNames.add(artifact.name)

    return merged

def installResource(resourcePath, targetPath):
    """Read the resource embedded as `resourcePath` and write to `targetPath`"""

    content = pkg_resources.resource_string(__name__, resourcePath)
    with open(targetPath, "wt") as f:
        f.write(content.decode("utf-8"))

def downloadFile(url, targetDir, target = None, chunkSize = 4096):
    """Download content from the url and save in the specified directory"""

    if target is None:
        target = url.split("/")[-1]
    targetPath = targetDir / target

    # Check if the content has already been downloaded
    if targetPath.exists():
        return targetPath

    logging.info("Downloading {} to {}".format(url, targetPath))

    try:
        response = requests.get(url, stream = True)
        with open(targetPath, "wb") as f:
            for chunk in response.iter_content(chunk_size = chunkSize): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    except Exception as e:
        targetPath.unlink(missing_ok = True)
        logging.error(e)
        raise Exception(os.linesep.join([
            "Could not download dependencies from the internet.",
            "Please see the log for details:",
            logging.getLoggerClass().root.handlers[0].baseFilename
        ]))

    return targetPath

def removeArtifact(artifact, bootDir):
    """Remove the artifact's boot config dir and file"""

    targetArtifactDir = bootDir / artifact.name

    if targetArtifactDir.exists():
        targetVersionDir = targetArtifactDir / artifact.version

        if targetVersionDir.exists():
            for targetPath in targetVersionDir.iterdir():
                targetPath.unlink(missing_ok = False)
            targetVersionDir.rmdir()

        targetArtifactDir.rmdir()

def installArtifact(launcherPath, artifact, resources, targetDir, bootDir):
    """Create the artifact's boot config and install the artifact"""

    bootPropsPath = bootPropertiesPath(
        artifact = artifact,
        resources = resources,
        targetDir = targetDir,
        bootDir = bootDir
    )

    cmd = ["java", "-jar", launcherPath, "@{}".format(bootPropsPath.name)]
    logging.info("{}: Executing {}".format(artifact.name, cmd))

    proc = subprocess.run(
        cmd, capture_output = True, cwd = bootPropsPath.parent, text = True
    )

    logging.info(proc)

    if proc.returncode:
        removeArtifact(artifact, bootDir)

        logFile = ""
        try:
            logFile = "Log file: {}".format(
                logging.getLoggerClass().root.handlers[0].baseFilename
            )
        except:
            pass

        raise ValueError(os.linesep.join([
            "Could not install package {}.".format(artifact.name),
            "Please see the log for details.",
            logFile
        ]))

    return [path.strip() for path in proc.stdout.splitlines()]

def bootPropertiesPath(artifact, resources, targetDir, bootDir):
    """Create and store the boot properties file for the given artifact"""

    bootPropsConfig = bootconfig.bootPropsConfig(
        artifact = artifact, resources = resources, targetDir = targetDir
    )

    targetBootDir = bootDir / artifact.name / artifact.version
    targetBootDir.mkdir(parents = True, exist_ok = True)

    targetPath = targetBootDir / "{}.cfg".format(artifact.name)

    try:
        bootconfig.writeConfig(bootPropsConfig, targetPath)
    except:
        targetPath.unlink(missing_ok = True)
        raise

    return targetPath

def installScript(paths, rootDir, targetDir, platform):
    """Create and store the script in the specified directory"""

    (scriptName, preface, classPath, args) = \
        windowsSpec(paths) if platform == "win32" else posixSpec(paths)

    template = """\
        |{}
        |java -Xmx512m -classpath "{}" -DSCLERA_ROOT="{}" {} {} \
    """.format(
        preface, classPath, rootDir,
        "com.scleradb.interfaces.shell.Repl", args
    )

    marginRegex = re.compile(r"^\s*\|", re.MULTILINE)
    cmd = re.sub(marginRegex, "", template)

    targetPath = targetDir / scriptName

    with open(targetPath, "wt") as f:
        f.write(cmd)

    st = targetPath.stat()
    targetPath.chmod(st.st_mode | stat.S_IEXEC)

    return targetPath

def windowsSpec(paths):
    """Windows nuances for creating the executable script with java command"""

    classPath = ["%CLASSPATH%"]
    classPath.extend(paths)
    return ("sclera.cmd", "@ECHO OFF", ";".join(classPath), "%*")

def posixSpec(paths):
    """Posix nuances for creating the executable script with java command"""

    classPath = ["$CLASSPATH"]
    classPath.extend(paths)
    return ("sclera", "#!/bin/sh", ":".join(classPath), "$@")

def initSclera(scriptPath):
    """Initialize Sclera after installation"""

    cmd = ["{}".format(scriptPath), "--init"]
    logging.info("Executing {}".format(cmd))

    proc = subprocess.run(cmd, capture_output = True)
    logging.info(proc)
