# Copyright 2010-2020 The pygit2 contributors
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2,
# as published by the Free Software Foundation.
#
# In addition to the permissions in the GNU General Public License,
# the authors give you unlimited permission to link the compiled
# version of this file into combinations with other programs,
# and to distribute those combinations without any restriction
# coming from the use of this file.  (The General Public License
# restrictions do apply in other respects; for example, they cover
# modification of the file, and distribution when not linked into
# a combined executable.)
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

"""Tests for Diff objects."""

from itertools import chain
import textwrap

import pytest

import pygit2
from pygit2 import GIT_DIFF_INCLUDE_UNMODIFIED
from pygit2 import GIT_DIFF_IGNORE_WHITESPACE, GIT_DIFF_IGNORE_WHITESPACE_EOL
from pygit2 import GIT_DELTA_RENAMED


COMMIT_SHA1_1 = '5fe808e8953c12735680c257f56600cb0de44b10'
COMMIT_SHA1_2 = 'c2792cfa289ae6321ecf2cd5806c2194b0fd070c'
COMMIT_SHA1_3 = '2cdae28389c059815e951d0bb9eed6533f61a46b'
COMMIT_SHA1_4 = 'ccca47fbb26183e71a7a46d165299b84e2e6c0b3'
COMMIT_SHA1_5 = '056e626e51b1fc1ee2182800e399ed8d84c8f082'
COMMIT_SHA1_6 = 'f5e5aa4e36ab0fe62ee1ccc6eb8f79b866863b87'
COMMIT_SHA1_7 = '784855caf26449a1914d2cf62d12b9374d76ae78'


PATCH = """diff --git a/a b/a
index 7f129fd..af431f2 100644
--- a/a
+++ b/a
@@ -1 +1 @@
-a contents 2
+a contents
diff --git a/c/d b/c/d
deleted file mode 100644
index 297efb8..0000000
--- a/c/d
+++ /dev/null
@@ -1 +0,0 @@
-c/d contents
"""

PATCHID = 'f31412498a17e6c3fbc635f2c5f9aa3ef4c1a9b7'

DIFF_HEAD_TO_INDEX_EXPECTED = [
    'staged_changes',
    'staged_changes_file_deleted',
    'staged_changes_file_modified',
    'staged_delete',
    'staged_delete_file_modified',
    'staged_new',
    'staged_new_file_deleted',
    'staged_new_file_modified'
]

DIFF_HEAD_TO_WORKDIR_EXPECTED = [
    'file_deleted',
    'modified_file',
    'staged_changes',
    'staged_changes_file_deleted',
    'staged_changes_file_modified',
    'staged_delete',
    'staged_delete_file_modified',
    'subdir/deleted_file',
    'subdir/modified_file'
]

DIFF_INDEX_TO_WORK_EXPECTED = [
    'file_deleted',
    'modified_file',
    'staged_changes_file_deleted',
    'staged_changes_file_modified',
    'staged_new_file_deleted',
    'staged_new_file_modified',
    'subdir/deleted_file',
    'subdir/modified_file'
]

HUNK_EXPECTED = """- a contents 2
+ a contents
"""

STATS_EXPECTED = """ a   | 2 +-
 c/d | 1 -
 2 files changed, 1 insertion(+), 2 deletions(-)
 delete mode 100644 c/d
"""

def test_diff_empty_index(dirtyrepo):
    repo = dirtyrepo
    head = repo[repo.lookup_reference('HEAD').resolve().target]

    diff = head.tree.diff_to_index(repo.index)
    files = [patch.delta.new_file.path for patch in diff]
    assert DIFF_HEAD_TO_INDEX_EXPECTED == files

    diff = repo.diff('HEAD', cached=True)
    files = [patch.delta.new_file.path for patch in diff]
    assert DIFF_HEAD_TO_INDEX_EXPECTED == files

def test_workdir_to_tree(dirtyrepo):
    repo = dirtyrepo
    head = repo[repo.lookup_reference('HEAD').resolve().target]

    diff = head.tree.diff_to_workdir()
    files = [patch.delta.new_file.path for patch in diff]
    assert DIFF_HEAD_TO_WORKDIR_EXPECTED == files

    diff = repo.diff('HEAD')
    files = [patch.delta.new_file.path for patch in diff]
    assert DIFF_HEAD_TO_WORKDIR_EXPECTED == files

def test_index_to_workdir(dirtyrepo):
    diff = dirtyrepo.diff()
    files = [patch.delta.new_file.path for patch in diff]
    assert DIFF_INDEX_TO_WORK_EXPECTED == files


def test_diff_invalid(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    with pytest.raises(TypeError): commit_a.tree.diff_to_tree(commit_b)
    with pytest.raises(TypeError): commit_a.tree.diff_to_index(commit_b)

def test_diff_empty_index_bare(barerepo):
    repo = barerepo
    head = repo[repo.lookup_reference('HEAD').resolve().target]

    diff = barerepo.index.diff_to_tree(head.tree)
    files = [patch.delta.new_file.path.split('/')[0] for patch in diff]
    assert [x.name for x in head.tree] == files

    diff = head.tree.diff_to_index(repo.index)
    files = [patch.delta.new_file.path.split('/')[0] for patch in diff]
    assert [x.name for x in head.tree] == files

    diff = repo.diff('HEAD', cached=True)
    files = [patch.delta.new_file.path.split('/')[0] for patch in diff]
    assert [x.name for x in head.tree] == files

def test_diff_tree(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]

    def _test(diff):
        assert diff is not None
        assert 2 == sum(map(lambda x: len(x.hunks), diff))

        patch = diff[0]
        hunk = patch.hunks[0]
        assert hunk.old_start == 1
        assert hunk.old_lines == 1
        assert hunk.new_start == 1
        assert hunk.new_lines == 1

        assert patch.delta.old_file.path == 'a'
        assert patch.delta.new_file.path == 'a'
        assert patch.delta.is_binary == False

    _test(commit_a.tree.diff_to_tree(commit_b.tree))
    _test(barerepo.diff(COMMIT_SHA1_1, COMMIT_SHA1_2))


def test_diff_empty_tree(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    diff = commit_a.tree.diff_to_tree()

    def get_context_for_lines(diff):
        hunks = chain(*map(lambda x: x.hunks, [p for p in diff]))
        lines = chain(*map(lambda x: x.lines, hunks))
        return map(lambda x: x.origin, lines)

    entries = [p.delta.new_file.path for p in diff]
    assert all(commit_a.tree[x] for x in entries)
    assert all('-' == x for x in get_context_for_lines(diff))

    diff_swaped = commit_a.tree.diff_to_tree(swap=True)
    entries = [p.delta.new_file.path for p in diff_swaped]
    assert all(commit_a.tree[x] for x in entries)
    assert all('+' == x for x in get_context_for_lines(diff_swaped))

def test_diff_revparse(barerepo):
    diff = barerepo.diff('HEAD', 'HEAD~6')
    assert type(diff) == pygit2.Diff

def test_diff_tree_opts(barerepo):
    commit_c = barerepo[COMMIT_SHA1_3]
    commit_d = barerepo[COMMIT_SHA1_4]

    for flag in [GIT_DIFF_IGNORE_WHITESPACE,
                 GIT_DIFF_IGNORE_WHITESPACE_EOL]:
        diff = commit_c.tree.diff_to_tree(commit_d.tree, flag)
        assert diff is not None
        assert 0 == len(diff[0].hunks)

    diff = commit_c.tree.diff_to_tree(commit_d.tree)
    assert diff is not None
    assert 1 == len(diff[0].hunks)

def test_diff_merge(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    commit_c = barerepo[COMMIT_SHA1_3]

    diff_b = commit_a.tree.diff_to_tree(commit_b.tree)
    assert diff_b is not None

    diff_c = commit_b.tree.diff_to_tree(commit_c.tree)
    assert diff_c is not None
    assert 'b' not in [patch.delta.new_file.path for patch in diff_b]
    assert 'b' in [patch.delta.new_file.path for patch in diff_c]

    diff_b.merge(diff_c)
    assert 'b' in [patch.delta.new_file.path for patch in diff_b]

    patch = diff_b[0]
    hunk = patch.hunks[0]
    assert hunk.old_start == 1
    assert hunk.old_lines == 1
    assert hunk.new_start == 1
    assert hunk.new_lines == 1

    assert patch.delta.old_file.path == 'a'
    assert patch.delta.new_file.path == 'a'

def test_diff_patch(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]

    diff = commit_a.tree.diff_to_tree(commit_b.tree)
    assert diff.patch == PATCH
    assert len(diff) == len([patch for patch in diff])

def test_diff_ids(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    patch = commit_a.tree.diff_to_tree(commit_b.tree)[0]
    delta = patch.delta
    assert delta.old_file.id.hex == '7f129fd57e31e935c6d60a0c794efe4e6927664b'
    assert delta.new_file.id.hex == 'af431f20fc541ed6d5afede3e2dc7160f6f01f16'

def test_diff_patchid(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    diff = commit_a.tree.diff_to_tree(commit_b.tree)
    assert diff.patch == PATCH
    assert diff.patchid.hex == PATCHID

def test_hunk_content(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    patch = commit_a.tree.diff_to_tree(commit_b.tree)[0]
    hunk = patch.hunks[0]
    lines = ('{0} {1}'.format(x.origin, x.content) for x in hunk.lines)
    assert HUNK_EXPECTED == ''.join(lines)
    for line in hunk.lines:
        assert line.content == line.raw_content.decode()

def test_find_similar(barerepo):
    commit_a = barerepo[COMMIT_SHA1_6]
    commit_b = barerepo[COMMIT_SHA1_7]

    #~ Must pass GIT_DIFF_INCLUDE_UNMODIFIED if you expect to emulate
    #~ --find-copies-harder during rename transformion...
    diff = commit_a.tree.diff_to_tree(commit_b.tree,
                                      GIT_DIFF_INCLUDE_UNMODIFIED)
    assert all(x.delta.status != GIT_DELTA_RENAMED for x in diff)
    assert all(x.delta.status_char() != 'R' for x in diff)
    diff.find_similar()
    assert any(x.delta.status == GIT_DELTA_RENAMED for x in diff)
    assert any(x.delta.status_char() == 'R' for x in diff)

def test_diff_stats(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]

    diff = commit_a.tree.diff_to_tree(commit_b.tree)
    stats = diff.stats
    assert 1 == stats.insertions
    assert 2 == stats.deletions
    assert 2 == stats.files_changed
    formatted = stats.format(format=pygit2.GIT_DIFF_STATS_FULL |
                                    pygit2.GIT_DIFF_STATS_INCLUDE_SUMMARY,
                             width=80)
    assert STATS_EXPECTED == formatted

def test_deltas(barerepo):
    commit_a = barerepo[COMMIT_SHA1_1]
    commit_b = barerepo[COMMIT_SHA1_2]
    diff = commit_a.tree.diff_to_tree(commit_b.tree)
    deltas = list(diff.deltas)
    patches = list(diff)
    assert len(deltas) == len(patches)
    for i, delta in enumerate(deltas):
        patch_delta = patches[i].delta
        assert delta.status == patch_delta.status
        assert delta.similarity == patch_delta.similarity
        assert delta.nfiles == patch_delta.nfiles
        assert delta.old_file.id == patch_delta.old_file.id
        assert delta.new_file.id == patch_delta.new_file.id

        # As explained in the libgit2 documentation, flags are not set
        #assert delta.flags == patch_delta.flags

def test_diff_parse(barerepo):
    diff = pygit2.Diff.parse_diff(PATCH)

    stats = diff.stats
    assert 2 == stats.deletions
    assert 1 == stats.insertions
    assert 2 == stats.files_changed

    deltas = list(diff.deltas)
    assert 2 == len(deltas)

def test_parse_diff_null(barerepo):
    with pytest.raises(Exception):
        barerepo.parse_diff(None)

def test_parse_diff_bad(barerepo):
    diff = textwrap.dedent(
    """
    diff --git a/file1 b/file1
    old mode 0644
    new mode 0644
    @@ -1,1 +1,1 @@
    -Hi!
    """)
    with pytest.raises(Exception):
        barerepo.parse_diff(diff)
