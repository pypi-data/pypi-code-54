import json
import pathlib
import random
import shutil
from typing import Optional, Dict

import cv2
import imagesize
import numpy as np
from rays_pycocotools import coco
from tqdm import tqdm

from raytils.datasets.coco_fields import CocoCategories, CocoInfo, CocoLicence, CocoDetectionAnnotation, CocoModes, \
    CocoList, CocoImage, combine_coco_objects


class Annotation:
    def __init__(self, class_name, bbox=None, mask=None, classifications=None):
        if classifications is None:
            classifications = []
        if bbox is None and mask is None:
            raise ValueError("No annotations provided either bbox or mask must be valid")
        if not isinstance(classifications, list):
            raise TypeError("Classifications parameter must be a list!")
        if not isinstance(class_name, str):
            raise TypeError("Class name parameter must be a string!")
        self.class_name = class_name
        self.classifications = classifications
        self._bbox = bbox
        self._mask = mask
        self.__segmentation = None
        self.__bbox_area = 0
        self.__mask_area = 0

    @property
    def area(self):
        _, _ = self.poly, self.bbox  # Getters may set area
        if self.__mask_area:
            return self.__mask_area
        if self.__bbox_area:
            return self.__bbox_area
        return 0

    @property
    def poly(self):
        # TODO: Find general purpose way of doing this (mask->segm, RLE->segm, RLEencoded->segm)
        # TODO: Currently only supports RLEencoded->segm
        if self.__segmentation:
            return self.__segmentation
        elif isinstance(self._mask, dict):
            if isinstance(self._mask['counts'], list):
                # Decode RLE to mask
                rle = coco.maskUtils.frPyObjects(self._mask, self._mask["size"][0], self._mask["size"][1])
                mask = coco.maskUtils.decode(rle)

                # Decode the binary mask
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                segmentation = [c.flatten().tolist() for c in contours if c.size > 4]

                if self._bbox is None:
                    self._bbox = list(coco.maskUtils.toBbox(rle))
                self.__mask_area = np.count_nonzero(mask)
                self.__segmentation = [segmentation]
                return segmentation
            raise ValueError("Mask is not a valid RLE dict")
        elif isinstance(self._mask, list) and len(self._mask) % 2 == 0:  # Mask must already be a poly
            self.__segmentation = [self._mask]
            return self.__segmentation

        raise ValueError("Invalid value for mask ({})".format(type(self._mask)))

    @property
    def bbox(self):
        if self._bbox:
            self.__bbox_area = self._bbox[-2] * self._bbox[-1]
            return self._bbox

        _ = self.poly  # Poly may set the bounding box

        if self._bbox is None:
            raise ValueError("Cannot automatically infer bounding box")

        return self._bbox


class COCOCreator:
    """ Class for creating annotation files in COCO format through a simple interface

    Attributes:
        mode: Coco annotation file type e.g "detection" or "keypoints"
        data_splits: Dictionary describing the export format (useful for splitting into training/testing splits)
        random_splits: Shuffle the imported data between data_splits if true
    """

    # TODO: Finish implementation
    #  - Add support for multiple different file imports (from coco files, labelbox, csv, json, images etc)
    #  - Add support for different segmentation types
    #  - Add support for different modes (Keypoint, Panoptic, Instance Segm etc)
    def __init__(self, mode: str, data_splits: Optional[Dict[str, float]] = None, random_splits=True):
        if not CocoModes.is_valid(mode):
            raise ValueError(f"Mode '{mode}' isn't a valid COCO format\n\tMust be one of: {CocoModes.modes}")
        self.__mode = mode
        if self.__mode != CocoModes.DETECTION:
            raise NotImplementedError(f"Export of {self.__mode} coco files is not currently implemented")
        if data_splits is None:
            data_splits = {"coco": 1.0}
        if 0 > sum(data_splits.values()) > 1.0:
            raise ValueError(f"Cannot split dataset into '{data_splits}' data splits are not between 0 and 1!")
        self.data_splits = data_splits
        self.random_splits = random_splits
        self.__image_path_ann_lut = {}
        self.__extra_fields_lut = {}
        self.classes = CocoCategories()
        self.info = CocoInfo(contributor="Raymond Kirk", url="https://github.com/RaymondKirk")
        self.license = CocoLicence(licence_id=0, name="Contact Author", url="https://github.com/RaymondKirk")
        self.licenses = CocoList([self.license])

    def map_classes(self, map_dict):
        """Replace classes in keys of map_dict with value"""
        for key, annotations in self.__image_path_ann_lut.items():
            for ann in annotations:
                if ann.class_name in map_dict:
                    ann.class_name = map_dict[ann.class_name]
        for old, new in map_dict.items():
            self.classes.remove(old)
            self.classes.add(new)

    def add_detection_annotation(self, image_path, class_name, bbox=None, mask=None, classifications=None):
        if self.__mode != CocoModes.DETECTION:
            raise ValueError(f"Cannot call add_detection_annotation when creating a {self.__mode} coco file")
        image_path = str(image_path)  # Ensure it's a string not Path object
        if image_path not in self.__image_path_ann_lut:
            self.__image_path_ann_lut[image_path] = []
        self.__image_path_ann_lut[image_path].append(Annotation(class_name, bbox, mask, classifications))
        self.classes.add(class_name)

    def add_label_me_folder(self, folder_path):
        """Converts a LabelMe (https://github.com/wkentaro/labelme) instance segmentation folder to COCO"""
        if isinstance(folder_path, str):
            folder_path = pathlib.Path(folder_path).resolve()

        json_files = list(folder_path.glob("*.json"))

        if not len(json_files):
            raise IOError("No '.json' files in the label me folder '{}'!".format(folder_path))

        for file in tqdm(json_files, postfix=f"Detections from LabelMe Folder {folder_path}"):
            label_data = json.load(file.open("rb"))
            image_path = (folder_path / label_data["imagePath"]).resolve()
            if not image_path.is_file():
                raise IOError("File '{}' does not exists!".format(image_path))

            for shape in label_data['shapes']:
                if "points" not in shape:
                    raise NotImplementedError("Only LabelMe files labelled as polygons are supported")
                points_list = [item for xy in shape['points'] for item in xy]
                x1, x2 = min([xy[0] for xy in shape['points']]), max([xy[0] for xy in shape['points']])
                y1, y2 = min([xy[1] for xy in shape['points']]), max([xy[1] for xy in shape['points']])
                w, h = x2 - x1, y2 - y1
                label_no_digits = ''.join(i for i in shape["label"] if not i.isdigit())
                # TODO: Calculate mask area instead of bbox
                self.add_detection_annotation(image_path, label_no_digits, bbox=[x1, y1, w, h], mask=points_list)

    def add_extra_info(self, image_path, **kwargs):
        """Adds extra info to a CocoImage field. Useful for things such as depth.
            If adding extra file paths you must also copy the files before or after exporting.
        """
        if image_path not in self.__image_path_ann_lut:
            raise ValueError(f"Annotations for '{image_path}' have not been added yet. Please add them first.")

        if image_path not in self.__extra_fields_lut:
            self.__extra_fields_lut[image_path] = {}
        for field_name, field_info in kwargs.items():
            self.__extra_fields_lut[image_path][field_name] = field_info

    def export(self, dataset_root: pathlib.Path):
        if self.__mode == CocoModes.DETECTION:
            return self.export_detection(dataset_root)
        raise NotImplementedError(f"Mode  '{self.__mode}' is not currently supported.")

    def export_detection(self, output_dir: pathlib.Path):
        if isinstance(output_dir, str):
            output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        class_name_to_idx = self.classes.classes_to_idx

        image_id = 0
        annotation_id = 0

        # Split files randomly into n-sized data split sections
        data_split_keys = list(self.data_splits.keys())
        data_split_values = [self.data_splits[k] for k in data_split_keys]
        split_sizes = [int(len(self.__image_path_ann_lut) * v) for v in data_split_values]
        idx_splits = [0] + [sum(split_sizes[:l]) for l in range(1, len(split_sizes) + 1)]
        file_path_keys = list(self.__image_path_ann_lut.keys())
        if self.random_splits:
            random.shuffle(file_path_keys)
        split_keys = {data_split_keys[i]: file_path_keys[idx_splits[i]:idx_splits[i + 1]]
                      for i in range(0, len(idx_splits) - 1)}

        for split_name, file_paths in split_keys.items():
            images = CocoList()
            annotations = CocoList()
            export_file_name = output_dir / "{}.json".format(split_name)

            export_file_name.parent.mkdir(parents=True, exist_ok=True)

            image_path_lut = {k: self.__image_path_ann_lut[k] for k in file_paths}
            for image_file, image_annotation in tqdm(image_path_lut.items(), postfix=f" Exporting {export_file_name}"):
                width, height = imagesize.get(str(image_file))

                # Copy the files to new COCO dataset
                new_image_file = f"data/{pathlib.Path(image_file).name}"
                new_image_file_location = output_dir / new_image_file
                new_image_file_location.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy(str(image_file), str(new_image_file_location))

                images.append(CocoImage(
                    image_id=image_id,
                    width=width,
                    height=height,
                    file_name=new_image_file,
                    image_license=self.license.id,
                    flickr_url="",
                    coco_url="",
                    date_captured="",
                    **self.__extra_fields_lut.get(image_file, {})
                ))

                for ann in image_annotation:
                    annotations.append(CocoDetectionAnnotation(
                        annotation_id=annotation_id,
                        image_id=image_id,
                        category_id=class_name_to_idx[ann.class_name],
                        segmentation=ann.poly,
                        area=ann.area,
                        bbox=ann.bbox,
                        iscrowd=0,
                        classifications=ann.classifications
                    ))
                    annotation_id += 1

                image_id += 1

            coco_file = combine_coco_objects([self.info, images, annotations, self.classes, self.licenses])

            with export_file_name.open('w') as fh:
                json.dump(coco_file, fh, indent=4, sort_keys=True)
