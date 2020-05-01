from contextlib import contextmanager

from .exceptions import DiskFullError
from .file import File


class DOSPath(object):
    """Encapsulate a path within an image."""
    def __init__(self, image, entry=None, name=None):
        self.image = image
        self.entry = entry
        self.name = name

    def __str__(self):
        if self.entry:
            return self.entry.name.decode()
        return self.name.decode()

    @property
    def size_blocks(self):
        """Return file size in blocks."""
        if self.entry:
            return self.entry.size
        raise FileNotFoundError("File not found: "+self.name)

    @property
    def size_bytes(self):
        """Return file size in bytes."""
        if self.entry is None:
            raise FileNotFoundError("File not found: "+self.name)

        size = 0
        block = self.entry.first_block()
        while block:
            size += block.data_size
            block = block.next_block()

        return size

    @contextmanager
    def open(self, mode='r', ftype=None):
        """Return new file object."""
        if mode not in ('r', 'w'):
            raise ValueError("Invalid mode, "+mode)

        if mode == 'r':
            if self.entry is None:
                raise FileNotFoundError("File not found: "+self.name)
        else:
            # open file for write
            if not self.image.writeable:
                raise PermissionError("Image is read-only")

            if self.entry:
                # truncate an existing file
                block = self.entry.first_block().next_block()

                while block:
                    # free all blocks after the first
                    self.image.bam.set_free(block.track, block.sector)
                    block = block.next_block()

                self.entry.size = 1
                self.entry.first_block().data_size = 0
            else:
                # no existing entry, create a new one
                if ftype is None:
                    raise ValueError("File type missing for new file")
                entry = self.image.get_free_entry()
                if entry is None:
                    raise DiskFullError()

                entry.file_type = ftype
                entry.name = self.name
                entry.size = 1
                self.entry = entry
                self.name = None

            if self.entry.file_type == 'REL':
                raise NotImplementedError("No relative file write support")

        yield File(self.entry, mode)

    @staticmethod
    def wildcard_match(fname, ftype, wildcard):
        """Return True if file matches a DOS wildcard."""

        if isinstance(wildcard, str):
            wildcard = wildcard.encode()

        if b'=' in wildcard:
            # file type
            if wildcard[-1] == ord('='):
                raise ValueError("Invalid wildcard, "+str(wildcard))
            wildcard, wftype = wildcard.split(b'=', 1)
            if ord(ftype[0]) != wftype[0]:
                return False

        for w, f in zip(wildcard, fname):
            if w == ord('?'):
                # matches any character
                continue
            if w == ord('*'):
                # matches rest of file name
                return True
            if w != f:
                return False

        if len(fname)+1 == len(wildcard) and wildcard.endswith(b'*'):
            # zero length match
            return True
        return len(fname) == len(wildcard)
