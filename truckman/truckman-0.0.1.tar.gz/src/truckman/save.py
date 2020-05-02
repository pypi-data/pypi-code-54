import docker
import os
import sys


def save_volume(volume_name):
    client = docker.from_env()
    client.images.pull("alpine:3")

    container = client.containers.create(
        'alpine:3',
        name="truckman",
        volumes={
           volume_name: {"bind": "/in/", "mode": "rw"},
           os.getcwd(): {"bind": "/out/", "mode": "rw"}
        },
        command="sleep 1000"
    )
    container.start()
    res = container.exec_run("tar cf - -C /in .".format(volume_name))
    container.stop()
    container.remove()
    sys.stdout.buffer.write(res.output)
