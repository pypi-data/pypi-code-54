# This file is part of AdMincer,
# Copyright (C) 2019-present eyeo GmbH
#
# AdMincer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# AdMincer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AdMincer. If not, see <http://www.gnu.org/licenses/>.

"""Tests for converting annotations from CVAT to YOLO format."""


import pytest

import admincer.convert as co
import admincer.index as idx


def test_process_cvat_no_output_dir(convert_src):
    co.process_cvat_xml(str(convert_src.join('14_task11.xml')))

    results = idx.reg_index(str(convert_src.join('task11')))
    assert results['1_cut_1.png'] == [(976, 461, 1278, 711, 'textad')]
    assert results['1_cut_0.png'] == [(233, 714, 962, 805, 'bannerad')]
    names = 'bannerad\ntextad'
    assert convert_src.join('task11', 'class.names').read() == names


def test_process_cvat_with_output_dir_and_copy(convert_src):
    co.process_cvat_xml(str(convert_src.join('14_task11.xml')),
                        (str(convert_src.join('converted'))), False, True)

    results = idx.reg_index(str(convert_src.join('converted')))
    assert results['1_cut_0.png'] == [(233, 714, 962, 805, 'bannerad')]
    assert convert_src.join('converted', '1_cut_0.png').check(exists=1)
    assert convert_src.join('task11', '1_cut_0.png').check(exists=1)
    assert convert_src.join('converted', '1_cut_1.png').check(exists=1)
    assert convert_src.join('task11', '1_cut_1.png').check(exists=1)
    assert convert_src.join('converted', 'no_ads.png').check(exists=1)


def test_process_cvat_with_outputdir_names_copy(convert_src_names):
    convert_src_names.join('converted', 'foo.names').write('bar', ensure=True)

    co.process_cvat_xml(str(convert_src_names.join('14_task11.xml')),
                        str(convert_src_names.join('converted')), False, True)
    co.process_cvat_xml(str(convert_src_names.join('15_task12.xml')),
                        str(convert_src_names.join('converted')), False, True)

    results = idx.reg_index(str(convert_src_names.join('converted')))
    assert results['2_cut_0.png'] == [(957, 807, 1262, 1348, 'bannerad')]
    assert results['5_cut_1.png'] == [(975, 257, 1219, 468, 'popupad')]
    assert convert_src_names.join('converted', '2_cut_0.png').check(exists=1)
    assert convert_src_names.join('task12', '2_cut_0.png').check(exists=1)
    assert convert_src_names.join('converted', '5_cut_1.png').check(exists=1)
    assert convert_src_names.join('task12', '5_cut_1.png').check(exists=1)

    names = 'bar\nbannerad\ntextad\npopupad'
    assert convert_src_names.join('converted', 'foo.names').read() == names
    assert convert_src_names.join('task12', 'class.names').read() == names


def test_image_missing(bad_convert_src, caplog):
    co.process_cvat_xml(str(bad_convert_src.join('14_task11.xml')))
    assert 'image cannot be found.' in caplog.records[0].msg

    results = idx.reg_index(str(bad_convert_src.join('task11')))
    assert results['1_cut_0.png'] == [(233, 714, 962, 805, 'bannerad')]


def test_convert_2names(convert_src_names, caplog):
    convert_src_names.join('task11', 'other.names').write('foo')

    with pytest.raises(Exception) as info:
        co.process_cvat_xml(
            str(convert_src_names.join('14_task11.xml')),
            str(convert_src_names.join('converted')), False, True)

    assert str(info.value).startswith('Multiple .names files')
