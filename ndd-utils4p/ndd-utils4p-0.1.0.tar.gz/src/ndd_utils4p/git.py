"""
Utilities dealing with Git.
"""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

import git


class GitRepository:
    """
    Utilities dealing with ``git.Repository``.
    """

    def __init__(self, repository: git.Repo):
        self.repository = repository

    def head_commit(self) -> git.Commit:
        """
        Returns:
            git.Commit: The head commit of the current branch
        """
        return self.repository.head.commit

    def head_tags(self) -> List[git.Tag]:
        """
        Returns:
            List[git.Tag]: The tags on the head commit of the current branch
        """
        head_commit = self.head_commit()
        return list(tag for tag in self.repository.tags if tag.commit == head_commit)

    def head_tags_names(self) -> List[str]:
        """
        Returns:
            List[str]: The names of the tags on the head commit of the current branch
        """
        return [tag.name for tag in self.head_tags()]

    def has_untracked_files(self) -> bool:
        """
        Test that there is no file which has been added to the index.
        Returns:
            bool: True if there are untracked files, False otherwise
        """
        return len(self.repository.untracked_files) > 0

    def has_unindexed_files(self) -> bool:
        """
        Test that there is no file which has been added to the index and then modified in the working tree.
        Returns:
            bool: True if the working tree and the index are different, False otherwise
        """
        return len(self.repository.index.diff(None)) > 0

    def has_uncommitted_files(self) -> bool:
        """
        Test that there is no file which has been added to the index but not committed.
        Returns:
            bool: True if the index and the local repository are different, False otherwise
        """
        return len(self.repository.index.diff(self.head_commit())) > 0

    def is_dirty(self) -> bool:
        """
        Returns:
            bool: True if at least a file is not tracked or not indexed or not committed, False otherwise
        """
        return self.has_untracked_files() or self.has_unindexed_files() or self.has_uncommitted_files()

    def head_metadata(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Metadata describing the head commit including:
                - generated_at (datetime): when these metadata where generated
                - commit_hash (str): the hash of the head commit
                - commit_date (datetime): the date of the head commit
                - commit_tags (List[str]): the tags associated with the head commit
                - dirty: True if at least a file is not tracked or not indexed or not committed, False otherwise
        """
        return {
            'generated_at': datetime.now(),
            'commit_hash': self.head_commit().hexsha,
            'commit_date': self.head_commit().committed_datetime,
            'commit_tags': self.head_tags_names(),
            'dirty': self.is_dirty(),
        }

    # def commits_behind(self) -> List[git.Commit]:
    #     """
    #     Returns:
    #          List[git.Commit]: The commits that are behind the origin
    #     """
    #     active_branch_name = self.repository.active_branch.name
    #     return list(self.repository.iter_commits(f'{active_branch_name}..{active_branch_name}@{{u}}'))
    #
    # def commits_ahead(self) -> List[git.Commit]:
    #     """
    #     Returns:
    #          List[git.Commit]: The commits that are ahead the origin
    #     """
    #     active_branch_name = self.repository.active_branch.name
    #     return list(self.repository.iter_commits(f'{active_branch_name}@{{u}}..{active_branch_name}'))
