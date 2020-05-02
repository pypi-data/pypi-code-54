import docker
import os


def load_volume(volume_path, volume_name):
    client = docker.from_env()
    client.images.pull("alpine:3")

    directory_path = os.path.dirname(os.path.abspath(volume_path))
    archive_path = os.path.basename(volume_path)

    client.volumes.create(name=volume_name)

    client.containers.run(
        'alpine:3',
        name="truckman",
        auto_remove=True,
        volumes={
           directory_path: {"bind": "/in/", "mode": "ro"},
           volume_name: {"bind": "/out/", "mode": "rw"}
        },
        command="tar -xf /in/{} -C /out".format(archive_path)
    )
