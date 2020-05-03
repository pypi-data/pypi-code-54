# Copyright [2018-2020] Peter Krenesky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ixian.utils.process import execute, get_dev_uid, get_dev_gid
from ixian.config import CONFIG
from ixian_docker.modules.docker.utils.volumes import convert_volume_flags


def run_builder(
    image, outputs=None, command="build", flags=None, env=None, volumes=None
):
    """Run a docker builder container.

    This function is a helper for using the docker builder pattern.

    The default command is is the `build` script. This script should perform
    a library specific build process. (e.g. npm install, webpack compile). The
    default command may be overridden to obtain a shell or run additional tools
    such as a package updater.

    Dependencies may be mounted in using `volumes`.

    Outputs are mounted into volumes tagged with `{tag}.{output}`. Build
    scripts should direct all output to these directories. The volumes can be
    mounted by other builders or containers. The volumes may also be converted
    into images with `image_from_volume('{tag}.{output}')`.

    :param image: builder image to use.
    :param outputs: list of outputs.  May be files or directories.
    :param command: command string to execute, default is "build".
    :param flags: additional docker build flags.
    :param env: additional env flags .
    :param volumes: list of volume mappings.
    """
    # TODO use docker-py

    env_flags = " ".join(["-e %s=%s" % item for item in (env or {}).items()])
    volume_flags = " ".join(convert_volume_flags(volumes or []))

    # mount outputs into volumes.
    # TODO move this into build_library_volume
    output_volume_flags = " ".join(
        [
            CONFIG.format(
                "-v {PROJECT_NAME}.{output}:{DOCKER.APP_DIR}/{output}",
                image=image,
                output=output,
            )
            for output in outputs or []
        ]
    )

    # run builder
    execute(
        CONFIG.format(
            "docker run -it " +
            # '--name container.npm ' +
            "-e APP_DIR={DOCKER.APP_DIR} "
            + "-e DEV_UID={uid} "
            + "-e DEV_GID={gid} "
            + "{flags} {env_flags} {output_volumes} {volumes} {image} {command}",
            image=image,
            command=command or "build",
            uid=get_dev_uid(),
            gid=get_dev_gid(),
            env_flags=env_flags,
            flags=flags or "",
            output_volumes=output_volume_flags,
            volumes=volume_flags,
        )
    )


def build_library_image(tag, image, env=None, volumes=None):
    """Create a library image from the output of a docker builder.

    This runs the builder without any outputs mapped. The builder will save
    to the container. The container will be committed into the new image.

    :param tag: tag for library image
    :param image: builder image to build library with.
    :param outputs: outputs expected for library.
    :param env: additional env flags for builder.
    :param volumes: list of volume mappings. Volumes may be used to add caches
        or dependencies to the build.
    """
    # commit the builder first to create a blank container for the new image.
    # This ensures that this command doesn't update the builder container and
    # taint it for other builds.
    execute(
        "docker commit {image} {library_image}".format(image=image, library_image=tag)
    )

    # run the builder and commit the changes
    run_builder(tag, env=env, volumes=volumes)
    execute(
        "docker commit {library_image} {library_image}".format(
            image=image, library_image=tag
        )
    )


def build_library_volumes(image, outputs, env=None, volumes=None):
    """Create volumes from the output of a docker builder.

    This runs the builder with volumes mounted for all outputs. The outputted
    library volumes can then be mounted and used by other builders or the
    runtime container.

    `outputs` should be specified as a list of docker volume mapping strings.
    Mappings may contain config variables.

    :param image: builder image to build library with.
    :param outputs: outputs expected for library.
    :param env: additional env flags for builder.
    :param volumes: list of volume mappings. Volumes may be used to add caches
        or dependencies to the build.
    """
    run_builder(image, outputs, env=env, volumes=volumes)
