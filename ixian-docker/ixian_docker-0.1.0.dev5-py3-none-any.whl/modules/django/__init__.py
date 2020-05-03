OPTIONS = {
    "name": "DJANGO",
    "tasks": "ixian_docker.modules.django.tasks",
    "config": "ixian_docker.modules.django.config.DjangoConfig",
    "dockerfile_template": "{DJANGO.MODULE_DIR}/Dockerfile.template",
    # Runtime volumes mounted in all environments.
    "volumes": [],
}
