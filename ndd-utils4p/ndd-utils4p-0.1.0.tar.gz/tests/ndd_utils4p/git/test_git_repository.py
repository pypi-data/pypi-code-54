from datetime import datetime
from pathlib import Path

from expects import *
from git import Repo
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.git import GitRepository


class TestGitRepository(AbstractTest):

    def test_head_commit(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        commit_1 = repo.index.commit('Initial commit')
        expect(git_repository.head_commit()).to(equal(commit_1))

        commit_2 = repo.index.commit('Commit #2')
        expect(git_repository.head_commit()).to(equal(commit_2))

        new_branch = repo.create_head('new_branch')
        new_branch.checkout()
        commit_3 = repo.index.commit('Commit #3')
        expect(git_repository.head_commit()).to(equal(commit_3))

    def test_head_tags_names(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        repo.index.commit('Initial commit')
        expect(git_repository.head_tags_names()).to(equal([]))

        repo.create_tag('tag_1_1')
        expect(git_repository.head_tags_names()).to(equal(['tag_1_1']))

        repo.index.commit('Commit #2')
        expect(git_repository.head_tags_names()).to(equal([]))

        repo.create_tag('tag_2_1')
        expect(git_repository.head_tags_names()).to(equal(['tag_2_1']))

        repo.create_tag('tag_2_2')
        expect(git_repository.head_tags_names()).to(equal(['tag_2_1', 'tag_2_2']))

        new_branch = repo.create_head('new_branch')
        new_branch.checkout()
        repo.index.commit('Commit #3')
        expect(git_repository.head_tags_names()).to(equal([]))

    def test_has_untracked_files(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        repo.index.commit('Initial commit')
        expect(git_repository.has_untracked_files()).to(be_false)

        file_1 = tmp_path.joinpath('file_1.txt')
        file_1.write_text('file_1')
        expect(git_repository.has_untracked_files()).to(be_true)

        repo.index.add([file_1.as_posix()])
        expect(git_repository.has_untracked_files()).to(be_false)

        file_2 = tmp_path.joinpath('file_2.txt')
        file_2.write_text('file_2')
        expect(git_repository.has_untracked_files()).to(be_true)

    def test_has_unindexed_files(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        repo.index.commit('Initial commit')
        expect(git_repository.has_unindexed_files()).to(be_false)

        file_1 = tmp_path.joinpath('file_1.txt')
        file_1.write_text('file_1')
        expect(git_repository.has_unindexed_files()).to(be_false)

        repo.index.add([file_1.as_posix()])
        expect(git_repository.has_unindexed_files()).to(be_false)

        file_1.write_text('file_1 v2')
        expect(git_repository.has_unindexed_files()).to(be_true)

        repo.index.add([file_1.as_posix()])
        expect(git_repository.has_unindexed_files()).to(be_false)

        repo.index.commit('Commit #2')
        expect(git_repository.has_unindexed_files()).to(be_false)

    def test_has_uncommitted_files(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        repo.index.commit('Initial commit')
        expect(git_repository.has_uncommitted_files()).to(be_false)

        file_1 = tmp_path.joinpath('file_1.txt')
        file_1.write_text('file_1')
        expect(git_repository.has_uncommitted_files()).to(be_false)

        repo.index.add([file_1.as_posix()])
        expect(git_repository.has_uncommitted_files()).to(be_true)

        file_1.write_text('file_1 v2')
        expect(git_repository.has_uncommitted_files()).to(be_true)

        repo.index.add([file_1.as_posix()])
        expect(git_repository.has_uncommitted_files()).to(be_true)

        repo.index.commit('Commit #2')
        expect(git_repository.has_uncommitted_files()).to(be_false)

    def test_is_dirty(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        repo.index.commit('Initial commit')
        expect(git_repository.is_dirty()).to(be_false)

        # file not tracked
        file_1 = tmp_path.joinpath('file_1.txt')
        file_1.write_text('file_1')
        expect(git_repository.is_dirty()).to(be_true)

        # file not indexed
        file_1.write_text('file_1 v2')
        expect(git_repository.is_dirty()).to(be_true)

        # file not indexed
        repo.index.add([file_1.as_posix()])
        expect(git_repository.is_dirty()).to(be_true)

        # file committed
        repo.index.commit('Commit #2')
        expect(git_repository.is_dirty()).to(be_false)

        # file not tracked and file not indexed
        file_2 = tmp_path.joinpath('file_2.txt')
        file_2.write_text('file_2')
        file_3 = tmp_path.joinpath('file_3.txt')
        file_3.write_text('file_3')
        repo.index.add([file_2.as_posix()])
        expect(git_repository.is_dirty()).to(be_true)

    def test_head_metadata(self, tmp_path: Path):
        repo = Repo.init(tmp_path)
        git_repository = GitRepository(repo)

        commit = repo.index.commit('Initial commit')
        generated_after = datetime.now()
        metadata = git_repository.head_metadata()
        generated_before = datetime.now()

        generated_date = metadata.pop('generated_at')
        expect(generated_after <= generated_date).to(be_true)
        expect(generated_before >= generated_date).to(be_true)
        expect(metadata).to(equal({
            'commit_hash': commit.hexsha,
            'commit_date': commit.committed_datetime,
            'commit_tags': [],
            'dirty': False,
        }))

        repo.create_tag('tag_1')
        file_1 = tmp_path.joinpath('file_1.txt')
        file_1.write_text('file_1')

        generated_after = datetime.now()
        metadata = git_repository.head_metadata()
        generated_before = datetime.now()

        generated_date = metadata.pop('generated_at')
        expect(generated_after <= generated_date).to(be_true)
        expect(generated_before >= generated_date).to(be_true)
        expect(metadata).to(equal({
            'commit_hash': commit.hexsha,
            'commit_date': commit.committed_datetime,
            'commit_tags': ['tag_1'],
            'dirty': True,
        }))
