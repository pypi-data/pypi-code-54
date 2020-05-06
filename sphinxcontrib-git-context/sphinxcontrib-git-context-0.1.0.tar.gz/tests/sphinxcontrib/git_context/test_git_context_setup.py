import shutil
from pathlib import Path
from typing import Callable

from expects import *
from git import Repo
from ndd_test4p.test_cases import AbstractTest
from sphinx.application import Sphinx

DEFAULT_DATE_REGEX = r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}'
COMMIT_DATE_REGEX = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2}'
GENERATED_AT_REGEX = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}'
SHORT_HASH_REGEX = r'[0-9a-f]{8}'
FULL_HASH_REGEX = r'[0-9a-f]{40}'


class TestGitRepository(AbstractTest):

    def test_with_default_settings_and_no_git_repository(self, tmp_path: Path):
        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path)
        expect(index_content).to(contain('<p>version default_version</p>'))
        expect(index_content).to(contain('<p>release default_release</p>'))

    def test_with_default_settings_and_no_commit(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            Repo.init(git_root_path.as_posix())

        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(contain('<p>version default_version</p>'))
        expect(index_content).to(contain('<p>release default_release</p>'))

    def test_with_default_settings_and_one_commit_and_dirty(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.index.commit('Commit #1')

        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version {DEFAULT_DATE_REGEX}&lt;br/&gt;WORKING VERSION</p>'))
        expect(index_content).to(match(rf'<p>release {DEFAULT_DATE_REGEX} WORKING VERSION</p>'))

    def test_with_default_settings_and_one_commit_and_clean(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.git.add(all=True)
            repository.index.commit('Commit #1')

        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version Commit: {SHORT_HASH_REGEX}</p>'))
        expect(index_content).to(match(rf'<p>release Commit: {FULL_HASH_REGEX}</p>'))

    def test_with_default_settings_and_one_tag_and_dirty(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.index.commit('Commit #1')
            repository.create_tag('tag_1')

        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version {DEFAULT_DATE_REGEX}&lt;br/&gt;WORKING VERSION</p>'))
        expect(index_content).to(match(rf'<p>release {DEFAULT_DATE_REGEX} WORKING VERSION</p>'))

    def test_with_default_settings_and_one_tag_and_clean(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.git.add(all=True)
            repository.index.commit('Commit #1')
            repository.create_tag('tag_1')

        fixture_dir_path = self._test_data_subdirectory_path('default')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(r'<p>version tag_1</p>'))
        expect(index_content).to(match(rf'<p>release Tag: tag_1 \| Commit: {FULL_HASH_REGEX}</p>'))

    # ------------------------------------------------------------------------------------------------------------------

    def test_with_custom_settings_and_no_git_repository(self, tmp_path: Path):
        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path)
        expect(index_content).to(contain('<p>version default_version</p>'))
        expect(index_content).to(contain('<p>release default_release</p>'))

    def test_with_custom_settings_and_no_commit(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            Repo.init(git_root_path.as_posix())

        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(contain('<p>version default_version</p>'))
        expect(index_content).to(contain('<p>release default_release</p>'))

    def test_with_custom_settings_and_one_commit_and_dirty(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.index.commit('Commit #1')

        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version commit_tags=”” commit_date=”{COMMIT_DATE_REGEX}”</p>'))
        expect(index_content).to(
            match(rf'<p>release generated_at=”{GENERATED_AT_REGEX}” commit_hash=”{FULL_HASH_REGEX}” dirty=”True”</p>'))

    def test_with_custom_settings_and_one_commit_and_clean(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.git.add(all=True)
            repository.index.commit('Commit #1')

        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version commit_tags=”” commit_date=”{COMMIT_DATE_REGEX}”</p>'))
        expect(index_content).to(
            match(rf'<p>release generated_at=”{GENERATED_AT_REGEX}” commit_hash=”{FULL_HASH_REGEX}” dirty=”False”</p>'))

    def test_with_custom_settings_and_one_tag_and_dirty(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.index.commit('Commit #1')
            repository.create_tag('tag_1')

        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version commit_tags=”tag_1” commit_date=”{COMMIT_DATE_REGEX}”</p>'))
        expect(index_content).to(
            match(rf'<p>release generated_at=”{GENERATED_AT_REGEX}” commit_hash=”{FULL_HASH_REGEX}” dirty=”True”</p>'))

    def test_with_custom_settings_and_one_tag_and_clean(self, tmp_path: Path):
        def git_operations(git_root_path: Path):
            repository = Repo.init(git_root_path.as_posix())
            repository.git.add(all=True)
            repository.index.commit('Commit #1')
            repository.create_tag('tag_1')

        fixture_dir_path = self._test_data_subdirectory_path('custom')
        index_content = self._run_sphinx(fixture_dir_path, tmp_path, git_operations)
        expect(index_content).to(match(rf'<p>version commit_tags=”tag_1” commit_date=”{COMMIT_DATE_REGEX}”</p>'))
        expect(index_content).to(
            match(rf'<p>release generated_at=”{GENERATED_AT_REGEX}” commit_hash=”{FULL_HASH_REGEX}” dirty=”False”</p>'))

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _run_sphinx(fixture_dir_path: Path, tmp_path: Path, git_operations: Callable[[Path], None] = None):
        source_dir_path = tmp_path.joinpath('source')
        build_dir_path = tmp_path.joinpath('build')
        shutil.copytree(fixture_dir_path.as_posix(), source_dir_path.as_posix())

        if git_operations is not None:
            git_operations(tmp_path)

        sphinx = Sphinx(
            source_dir_path.as_posix(),
            source_dir_path.as_posix(),
            build_dir_path.as_posix(),
            build_dir_path.as_posix(),
            'html')
        sphinx.build()

        index_file_path = build_dir_path.joinpath('index.html')
        index_content = index_file_path.read_text()
        return index_content
