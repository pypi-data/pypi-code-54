import docker
from os import system

class Classifier:
    def __init__(self):
        self._clfContainer = self.startContainerFromImage("gwint/classifier:1")

    def __del__(self):
        self._clfContainer.stop()

    def classify(self, imgPath):
        containerID = self._clfContainer.id
        system(f'docker container cp {imgPath} {containerID}:/{imgPath}')
        output = \
            self._clfContainer.exec_run(["python", "docker-ann/classify", imgPath])

        return output[1].decode().strip()

    def startContainerFromImage(self, imageName):
        client = docker.from_env()
        container = \
            client.containers.run(imageName, "bin/bash", detach=True, tty=True)

        return container


if __name__ == "__main__":
    clf = Classifier()
    print(clf.classify("classify.py"))
