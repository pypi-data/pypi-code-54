from typing import Optional

from git import InvalidGitRepositoryError
from git import Repo
from ndd_utils4p.git import GitRepository
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

LOGGER = logging.getLogger(__name__)


def _create_repository(documentation_directory: str) -> Optional[Repo]:
    try:
        repository = Repo(documentation_directory, search_parent_directories=True)
        LOGGER.info('Git repository found in directory "%s" or any parent', documentation_directory)
        return repository
    except InvalidGitRepositoryError:
        LOGGER.info('Git repository not found in directory "%s" or any parent', documentation_directory)
        return None


def _is_repository_valid(repository: Repo) -> bool:
    try:
        if repository is not None and len(list(repository.iter_commits())) > 0:
            return True
    except ValueError:
        LOGGER.info('Git repository has no commit')
    return False


def config_inited_handler(application: Sphinx, config: Config):
    LOGGER.info('Starting git-context plugin configuration')

    documentation_directory = application.srcdir
    repository = _create_repository(documentation_directory)
    if not _is_repository_valid(repository):
        LOGGER.info('Skipping git-context plugin configuration')
        return

    git_repository = GitRepository(repository)
    config['git_context'] = git_repository.head_metadata()
    LOGGER.debug('Git context: %s', config['git_context'])

    git_context_setup = config['git_context_setup']

    if git_context_setup is None:
        LOGGER.debug('Using default git_context_setup function')
        default_git_context_setup(config)
    else:
        LOGGER.debug('Using custom git_context_setup function')
        git_context_setup(config)


def default_git_context_setup(config: Config):
    date_pattern = "%Y/%m/%d %H:%M:%S"
    git_context = config['git_context']

    if git_context['dirty']:
        generated_at = git_context['generated_at'].strftime(date_pattern)
        config['html_context']['last_updated'] = generated_at
        config['version'] = f'{generated_at}<br/>WORKING VERSION'
        config['release'] = f'{generated_at} WORKING VERSION'
    else:
        committed_at = git_context['commit_date'].strftime(date_pattern)
        config['html_context']['last_updated'] = committed_at

        if len(git_context['commit_tags']) > 0:
            tags_label = 'Tag' if len(git_context['commit_tags']) == 1 else 'Tags'
            tags = ', '.join(git_context['commit_tags'])
            config['version'] = tags
            config['release'] = f'{tags_label}: {tags} | Commit: {git_context["commit_hash"]}'
        else:
            config['version'] = f'Commit: {git_context["commit_hash"][:8]}'
            config['release'] = f'Commit: {git_context["commit_hash"]}'

    LOGGER.debug(f'Sphinx HTML last updated = %s', config['html_context']['last_updated'])
    LOGGER.debug(f'Sphinx release = %s', config['release'])
    LOGGER.debug(f'Sphinx version = %s', config['version'])


def setup(application: Sphinx):
    application.add_config_value('git_context', {}, 'env')
    application.add_config_value('git_context_setup', None, 'env')

    application.connect('config-inited', config_inited_handler)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
