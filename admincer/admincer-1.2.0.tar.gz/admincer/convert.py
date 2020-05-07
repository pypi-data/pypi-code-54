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


import os
import logging
import shutil
import xml.etree.ElementTree as etree
import glob

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']


def _get_names_file(path):
        """If there is a single .names file, return it."""
        names_files = glob.glob(os.path.join(path, '*.names'))
        if len(names_files) > 1:
            raise Exception('Multiple .names files in {}'
                            .format(path))
        if len(names_files) == 1:
            return names_files[0]
        return None


def _get_names(filename):
    """Open a filename and return a line-by-line list of the contents."""
    if os.path.exists(str(filename)):
        return [line.strip() for line in open(filename)]
    return []


def _append_unique(base, new):
    """Append any new, unique items to a base list."""
    for item in new:
        if item not in base:
            base.append(item)
    return base


def _write_names(names, names_dst):
    """Write the contents of a list to a file."""
    with open(names_dst, 'w+', newline='\n') as f:
        f.write('\n'.join(names))


def copy_move_images(image_dirs, output_dir, copy, move):
    for image_dir in image_dirs:
        for dirpath, dirnames, filenames in os.walk(image_dir):
            for fn in filenames:
                if any(fn.endswith(ext) for ext in IMAGE_EXTENSIONS):
                    if copy:
                        shutil.copy(os.path.join(dirpath, fn), output_dir)
                    elif move:
                        shutil.move(os.path.join(dirpath, fn), output_dir)


def convert_annotations(img_tag, names):
    """Find each ad in an img_tag and convert them to yolo-format annotations.

    Parameters
    ----------
    img_tag : xml.etree.ElementTree.Element
        CVAT-style tag for an image
    names : list
        An ordered list of labels, which describe boxes in images

    Returns
    -------
    (yolo_annotations, names) : tuple(str, list)
        yolo_annotations is a string containing all yolo-style annotations
            for the given img_tag, separated by '\n' newline characters.
        names is a list containing all passed-in names, plus any new labels.

    """
    width = int(img_tag.get('width'))
    height = int(img_tag.get('height'))

    yolo_annotations = []

    for box in img_tag.findall('box'):
        label = box.get('label')
        xmin = float(box.get('xtl'))
        ymin = float(box.get('ytl'))
        xmax = float(box.get('xbr'))
        ymax = float(box.get('ybr'))

        if label not in names:
            names.append(label)
        label_id = names.index(label)
        yolo_x = (xmin + ((xmax - xmin) / 2)) / width
        yolo_y = (ymin + ((ymax - ymin) / 2)) / height
        yolo_w = (xmax - xmin) / width
        yolo_h = (ymax - ymin) / height

        yolo_annotations.append(
            f'{label_id} {yolo_x:.6f} {yolo_y:.6f} {yolo_w:.6f} {yolo_h:.6f}'
        )

    return ('\n'.join(yolo_annotations), names)


def process_cvat_xml(xml_file, output_dir=None, move=False, copy=False):
    """Convert annotations from CVAT to YOLO.

    Parameters
    ----------
    xml_file : str
        Filename of the xml file containing the CVAT annotations
    output_dir : str
        Path where the YOLO annotation .txt files will be written
    move : bool
        If true, the images will be moved to the output_dir
    copy : bool
        If true, the images will be copied to the output_dir

    """
    if move and copy:
        raise ValueError('Choose either "copy" or "move", not both')

    cvat_xml = etree.parse(xml_file)

    # Is there a .names file in the output_dir?
    names_out = []
    names_file_out = None
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        names_file_out = _get_names_file(output_dir)
        names_out = _get_names(names_file_out)

    # Is there a .names file alongside the XML file?
    names_file_up = _get_names_file(os.path.split(xml_file)[0])
    names_up = _get_names(names_file_up)

    # Is there a .names file alongside the images?
    image_folder = os.path.join(os.path.split(xml_file)[0],
                                os.path.split(cvat_xml.find('image')
                                              .get('name'))[0])
    names_file_in = _get_names_file(image_folder)
    names_in = _get_names(names_file_in)

    names = []
    names = _append_unique(names, names_out)
    names = _append_unique(names, names_up)
    names = _append_unique(names, names_in)

    image_dirs = set()

    for img_tag in cvat_xml.findall('image'):
        img_name = img_tag.get('name')
        image_path = os.path.join(os.path.split(xml_file)[0], img_name)
        image_dirs.add(os.path.dirname(image_path))

        if not os.path.exists(image_path):
            logging.warning('{} image cannot be found. Is `{}` image \
                            directory correct?'.
                            format(image_path, image_path))

        if output_dir is not None:
            yolo = os.path.basename(os.path.splitext(img_name)[0] + '.txt')
            yolo_dst = os.path.join(output_dir, yolo)

        else:
            yolo_dst = os.path.splitext(image_path)[0] + '.txt'

        yolo_annotations, names = convert_annotations(img_tag, names)

        with open(yolo_dst, 'w+', newline='\n') as yolo_file:
            yolo_file.write(yolo_annotations)

    # Write the class.names file to the output_dir or the image paths, and
    # overwrite any existing .names files
    if output_dir is not None:
        if names_file_out:
            _write_names(names, names_file_out)
        else:
            _write_names(names, os.path.join(output_dir, 'class.names'))
    else:
        for image_dir in image_dirs:
            _write_names(names, os.path.join(image_dir, 'class.names'))

    if names_file_up:
        _write_names(names, names_file_up)

    if names_file_in:
        _write_names(names, names_file_in)

    if output_dir is not None and copy or move:
        copy_move_images(image_dirs, output_dir, copy, move)
