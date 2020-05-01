from qbackup.sources.file import FileSource
from qbackup.targets.disk import FileTarget

from .filecopy import *


def test_single_file_copy():
    src = "AAA"
    tgt = "BBB"
    tsk = SingleFileDiskCopy(src, tgt)
    assert isinstance(tsk.source, FileSource)
    assert (isinstance(tsk.target, FileTarget))

    jstr = tsk.to_json()

    print(jstr)

    tsk1 = Task.from_json(jstr)
    assert isinstance(tsk1, SingleFileDiskCopy)
    assert tsk.source.name == tsk1.source.name
    assert tsk.target.name == tsk1.target.name

    tsk1.run()
    assert tsk1.status == Task.Status.DONE