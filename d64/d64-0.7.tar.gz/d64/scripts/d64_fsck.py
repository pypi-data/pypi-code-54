import argparse
import sys

from collections import defaultdict
from pathlib import Path

from d64.d64_image import D64Image
from d64.block import Block


IMAGE = None
FIX = False
YES = False
VERBOSE = False


USED_BLOCKS = defaultdict(set)


def remember_used(track, sector):
    """Note block usage for later reconciliation."""
    global USED_BLOCKS

    USED_BLOCKS[track].add(sector)


def fix_error(text, fixer=None, **kwargs):
    """Report, and optionally repair, an error."""
    print("ERROR: "+text)
    if FIX and fixer:
        if YES:
            return fixer(**kwargs)
        response = input("Fix? ")
        if response.lower() in ('y', 'yes'):
            return fixer(**kwargs)
    return 1


def check_misc():
    """Check various DOS fields and report disk name & id."""
    errors = 0

    print("\nChecking DOS information...")
    if IMAGE.dos_version != ord('2'):
        msg = "Unknown DOS version, "+chr(IMAGE.dos_version)
        errors += fix_error(msg, fix_dos_version)
    elif VERBOSE:
        print("DOS version: "+chr(IMAGE.dos_version))

    if IMAGE.dos_type[0] != IMAGE.dos_type[1]:
        msg = "Mismatch in DOS formats, ${:02x} & ${:02x}".format(IMAGE.dos_type[0], IMAGE.dos_type[1])
        errors += fix_error(msg, fix_dos_types)
    elif VERBOSE:
        print("DOS formats match, ${:02x} & ${:02x}".format(IMAGE.dos_type[0], IMAGE.dos_type[1]))

    block = Block(IMAGE, IMAGE.DIR_TRACK, 0)
    bad_link = True
    if not block.is_final:
        try:
            next = block.next_block()
            if next.track == IMAGE.DIR_TRACK and next.sector == 1:
                bad_link = False
        except ValueError:
            # invalid track/sector
            pass
    if bad_link:
        ts = block.get(0, 2)
        msg = "Invalid link to directory block, {}:{}".format(*ts)
        errors += fix_error(msg, fix_dir_link)
    elif VERBOSE:
        print("Link to directory block OK, {}:1".format(IMAGE.DIR_TRACK))

    print("Disk name: {}   Disk id: {}".format(IMAGE.name.decode(), IMAGE.id.decode()))
    if errors == 0:
        print("OK")

    return errors


def check_bam():
    """Check Block Availability Map."""
    errors = 0

    print("\nChecking Block Availability Map...")
    for track in range(1, IMAGE.MAX_TRACK+1):
        total, bits = IMAGE.bam.get_entry(track)
        counted = bits.count('1')
        if total != counted:
            msg = "Mismatch in track {} total and bits, {} & {} ({})".format(track, total, counted, bits)
            errors += fix_error(msg, fix_bam_entry, track=track)
        if VERBOSE:
            print("Track: {:2d}   Free blocks: {:2d}   Free bits: {}".format(track, total, bits))

    if not IMAGE.bam.is_allocated(IMAGE.DIR_TRACK, 0):
        msg = "Track {}:0 not allocated".format(IMAGE.DIR_TRACK)
        errors += fix_error(msg, fix_unalloc_block, block=Block(IMAGE.DIR_TRACK, 0))
    elif VERBOSE:
        print("Block {}:0 allocated".format(IMAGE.DIR_TRACK))
    remember_used(IMAGE.DIR_TRACK, 0)

    if errors == 0:
        print("OK")

    return errors


def check_directory():
    """Check directory integrity."""
    errors = 0

    print("\nChecking directory structure...")
    block = Block(IMAGE, D64Image.DIR_TRACK, 1)

    while True:
        if not IMAGE.bam.is_allocated(block.track, block.sector):
            msg = "Track {}:{} not allocated".format(block.track, block.sector)
            errors += fix_error(msg, fix_unalloc_block, block)
        elif VERBOSE:
            print("Block {}:{} allocated".format(block.track, block.sector))
        remember_used(block.track, block.sector)
        if block.is_final:
            if block.data_size != 0xfe:
                msg = "Block {}:{} has invalid data size, {}".format(block.track, block.sector, block.data_size)
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
            elif VERBOSE:
                print("Block {}:{} checked".format(block.track, block.sector))
            break
        if VERBOSE:
            print("Block {}:{} checked".format(block.track, block.sector))
        try:
            block = block.next_block()
        except ValueError:
            ts = block.get(0, 2)
            msg = "Invalid link in directory, {}:{}".format(*ts)
            errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
            break

    entry = 1
    for path in IMAGE.iterdir():
        raw_ftype = path.entry._file_type()
        if raw_ftype & 7 > 4:
            msg = "Entry {:2d}, invalid file type, ${:02x}".format(entry, raw_ftype)
            errors += fix_error(msg, fix_ftype, entry=path.entry, type='PRG')
        elif VERBOSE:
            print("Entry {:2d} has valid file type, ${:02x} ({})".format(entry, raw_ftype, path.entry.file_type))
        try:
            first_block = path.entry.first_block()
            if VERBOSE:
                print("Entry {:2d} link to first block OK, {}:{}".format(entry, first_block.track, first_block.sector))
        except ValueError:
            # invalid track/sector
            ts = block.get(0, 2)
            msg = "Entry {:2d}, invalid link to first data block, {}:{}".format(entry, *ts)
            # missing file contents, delete the entry
            errors += fix_error(msg, fix_ftype, entry=path.entry, type=0)
        entry += 1

    if errors == 0:
        print("OK")

    return errors


def check_files():
    """Check integrity of all files."""
    errors = 0

    print("\nChecking files...")
    for path in IMAGE.iterdir():
        # known valid, already checked
        block = path.entry.first_block()
        blocks_used = 0

        while block:
            remember_used(block.track, block.sector)
            blocks_used += 1
            if VERBOSE:
                print("File {!s}, link to block OK, {}:{}".format(path, block.track, block.sector))
            if not IMAGE.bam.is_allocated(block.track, block.sector):
                msg = "File {!s}, block {}:{} not allocated".format(path, block.track, block.sector)
                errors += fix_error(msg, fix_unalloc_block, block)
            elif VERBOSE:
                print("File {!s}, block {}:{} allocated".format(path, block.track, block.sector))

            try:
                block = block.next_block()
            except ValueError:
                # invalid track/sector
                ts = block.get(0, 2)
                msg = "File {!s}, invalid link to block, {}:{}".format(path, *ts)
                # truncate file
                errors += fix_error(msg, fix_data_size, block=block, size=0xfe)
                break

        if blocks_used != path.size_blocks:
            msg = "File {!s}, mismatch in blocks used, {} & {} (actual)".format(path, path.size_blocks, blocks_used)
            errors += fix_error(msg, fix_block_count, entry=path.entry, count=blocks_used)
        elif VERBOSE:
            print("File {!s} uses {:d} blocks".format(path, blocks_used))

    if errors == 0:
        print("OK")

    return errors


def check_allocation():
    global USED_BLOCKS
    errors = 0

    print("\nChecking block allocation...")
    for track in range(1, IMAGE.MAX_TRACK+1):
        max_sectors = IMAGE.max_sectors(track)
        _, bits = IMAGE.bam.get_entry(track)
        bam_used = {i for i, b in enumerate(bits) if b == '0' and i < max_sectors}
        delta = bam_used-USED_BLOCKS[track]
        if delta:
            delta_s = ', '.join([str(b) for b in delta])
            msg = "Track {}, sectors {} marked allocated when unused".format(track, delta_s)
            fixed_bits = ''.join(['1' if i in delta else b for i, b in enumerate(bits)])
            errors += fix_error(msg, fix_track_alloc, track=track, bits=fixed_bits)
        elif VERBOSE:
            print("Track {} OK".format(track))

    if errors == 0:
        print("OK")

    return errors


def check_image(image_path):
    """Check the integrity of an image, return the number of uncorrected errors."""
    global IMAGE

    IMAGE = D64Image(image_path)
    mode = 'r+b' if FIX else 'rb'
    try:
        IMAGE.open(mode)
        errors = check_misc()
        errors += check_bam()
        errors += check_directory()
        errors += check_files()
        errors += check_allocation()

        print()
        for line in IMAGE.directory():
            print(line)
    finally:
        IMAGE.close()

    return errors


def fix_dos_version():
    """Fix DOS version field."""
    IMAGE.dos_version = ord('2')
    if VERBOSE:
        print("Setting DOS version to 2")
    return 0


def fix_dos_types():
    """Fix DOS format type fields."""
    IMAGE.dos_type = ((ord('A'), ord('A')))
    if VERBOSE:
        print("Setting DOS formats to 'A'")
    return 0


def fix_dir_link():
    """Fix link to directory block."""
    dir_block = Block(IMAGE, IMAGE.DIR_TRACK, 1)
    block = Block(IMAGE, IMAGE.DIR_TRACK, 0)
    block.set_next_block(dir_block)
    if VERBOSE:
        print("Setting link to {}:1".format(IMAGE.DIR_TRACK))
    return 0


def fix_bam_entry(track):
    """Fix track entry in BAM."""
    total, bits = IMAGE.bam.get_entry(track)
    counted = bits.count('1')
    IMAGE.bam.set_entry(track, counted, bits)
    if VERBOSE:
        print("Setting track {} to {} & {}".format(track, counted, bits))
    return 0


def fix_unalloc_block(block):
    """Allocate an in-use block."""
    IMAGE.bam.set_allocated(block.track, block.sector)
    if VERBOSE:
        print("Allocating block {}:{}".format(block.track, block.sector))
    return 0


def fix_data_size(block, size):
    """Fix data used in a block."""
    block.data_size = size
    if VERBOSE:
        print("Setting data size of {}:{} to {}".format(block.track, block.sector, size))
    return 0


def fix_ftype(entry, type):
    """Fix entry file type."""
    entry.file_type = type
    if VERBOSE:
        print("Setting entry file type to "+entry.file_type)
    return 0


def fix_block_count(entry, count):
    """Fix entry size in blocks."""
    entry.size = count
    if VERBOSE:
        print("Setting block count to {:d}".format(count))
    return 0


def fix_track_alloc(track, bits):
    """Fix BAM entry for a track."""
    IMAGE.bam.set_entry(track, bits.count('1'), bits)
    if VERBOSE:
        print("Setting bits to "+bits)
    return 0


def main():
    global FIX
    global YES
    global VERBOSE

    parser = argparse.ArgumentParser(description='Check and fix Commodore disk images.')
    parser.add_argument('image', type=Path, help='image filename')
    parser.add_argument('--fix', '-f', action='store_true', help='Fix errors detected')
    parser.add_argument('--yes', '-y', action='store_true', help='Answer questions with "yes"')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()
    FIX = args.fix
    YES = args.yes
    VERBOSE = args.verbose

    try:
        errors = check_image(args.image)
    except KeyboardInterrupt:
        sys.exit("\nAbort, discarding all changes")

    if errors:
        sys.exit("\n{:d} unfixed errors".format(errors))
