from .block import Block
from .exceptions import DiskFullError


class File(object):
    """Read and write access to files."""
    def __init__(self, entry, mode):
        self.entry = entry
        self.mode = mode
        self.block = entry.first_block()
        self.pos_block = 2

    def read(self, count=-1):
        """Read bytes from file."""
        ret = b''

        while count:
            remaining = self.block.data_size-(self.pos_block-2)
            if remaining == 0:
                break

            # read as much as is wanted from the current block
            length = remaining if count == -1 else min(count, remaining)
            ret += self.block.get(self.pos_block, self.pos_block+length)
            self.pos_block += length
            if count != -1:
                count -= length

            if self.block.is_final:
                # no more blocks, end of file
                break

            if self.pos_block == Block.SECTOR_SIZE:
                # end of block, move on to the next block
                self.block = self.block.next_block()
                self.pos_block = 2

        return ret

    def write(self, data):
        """Write data to a file."""
        written = 0

        while data:
            remaining_space = Block.SECTOR_SIZE-self.pos_block
            if remaining_space:
                length = min(remaining_space, len(data))
                self.block.set(self.pos_block, data[:length])
                self.pos_block += length
                self.block.data_size = self.pos_block-2
                written += length
                data = data[length:]
            else:
                # end of block, append a new one
                next_block = self.block.image.alloc_next_block(self.block.track, self.block.sector)
                if next_block is None:
                    raise DiskFullError()
                next_block.data_size = 0
                self.block.set_next_block(next_block)
                self.block = next_block
                self.pos_block = 2
                self.entry.size += 1

        return written
