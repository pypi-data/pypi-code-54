# -*- coding=utf-8 -*-
"""YOLO2 preprocess."""
from typing import Dict, Tuple, Any, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from iva_applications.mscoco17.coco_dict import CONFIG_DICT
from iva_applications.mscoco17.config import CLASS_NAMES
from iva_applications.yolo2.postprocess import get_spaced_colors


def yxyxs2xyxys(yxyx_box: np.ndarray) -> np.ndarray:
    """
    Convert bounding box format from [y1, x1, y2, x2, score] to [x1, y1, x2, y2, score].

    Parameters
    ----------
    yxyx_box
        bounding box in format [y1, x1, y2, x2, score]

    Returns
    -------
    bounding box in format [x1, y1, x2, y2, score]
    """
    xyxy_box = np.zeros(yxyx_box.shape)
    xyxy_box[0] = yxyx_box[1]
    xyxy_box[1] = yxyx_box[0]
    xyxy_box[2] = yxyx_box[3]
    xyxy_box[3] = yxyx_box[2]
    xyxy_box[4] = yxyx_box[4]
    return xyxy_box


def xyxy2xywh(xyxy_box: np.ndarray) -> np.ndarray:
    """
    Convert bounding box format from [x1, y1, x2, y2] to [x, y, w, h].

    Parameters
    ----------
    xyxy_box
        bounding box in format [x1, y1, x2, y2]

    Returns
    -------
    bounding box in format [x, y, w, h]
    """
    xywh_box = np.zeros(xyxy_box.shape)
    xywh_box[0] = (xyxy_box[0] + xyxy_box[2]) / 2
    xywh_box[1] = (xyxy_box[1] + xyxy_box[3]) / 2
    xywh_box[2] = xyxy_box[2] - xyxy_box[0]
    xywh_box[3] = xyxy_box[3] - xyxy_box[1]
    return xywh_box


def xxyy2xywh(xxyy_box: np.ndarray) -> np.ndarray:
    """
    Convert bounding box format from [x1, x2, y1, y2] to [x, y, w, h].

    Parameters
    ----------
    xxyy_box
        bounding box in format [x1, x2, y1, y2]

    Returns
    -------
    bounding box in format [x, y, w, h]
    """
    xywh_box = np.zeros(xxyy_box.shape)
    xywh_box[0] = (xxyy_box[0] + xxyy_box[1]) / 2
    xywh_box[1] = (xxyy_box[2] + xxyy_box[3]) / 2
    xywh_box[2] = xxyy_box[1] - xxyy_box[0]
    xywh_box[3] = xxyy_box[3] - xxyy_box[2]
    return xywh_box


def coco80_to_coco91_class() -> List[int]:  # returns the coco class for each darknet class
    """
    Take darknet classes and transpose its numbers according to each coco class.

    Returns
    -------
    list of numbers in coco labels
    """
    keys = list(CONFIG_DICT.keys())
    keys_list = [int(key) for key in keys]
    return keys_list


def refine_output_by_thresh(boxes, scores, classes, confidence_threshold: float):
    """
    Filter predictions by their score value which is greater than the confidence threshold.

    Parameters
    ----------
    boxes
        boxes on the objects
    scores
        confidence scores for founded objects
    classes
        classes of founded objects
    confidence_threshold
        threshold used to filter the detections

    Returns
    -------
    tuple of filtered scores, boxes and corresponding classes
    """
    boxes_thresh_indices = [score > confidence_threshold for score in scores]
    boxes = boxes[0, boxes_thresh_indices, :]
    scores = scores[boxes_thresh_indices]
    classes = classes[boxes_thresh_indices]
    return scores, boxes, classes


def get_output_dict(scores, boxes, classes) -> dict:
    """
    Create a dictionary from the predictions.

    Parameters
    ----------
    scores
        confidence scores for the objects
    boxes
        boxes around the objects
    classes
        classes of detected objects

    Returns
    -------
    constructed dictionary of classes as keys and boxes, scores as values.
    """
    output_dict: Dict[int, np.ndarray] = {}
    for i, class_ in enumerate(classes):
        class_ = int(class_)
        output_dict.setdefault(class_, [])
        box_score_value = boxes[i]
        score_value = scores[i]
        dict_value = np.hstack((box_score_value, score_value))
        output_dict[class_].append(dict_value)
    for key in list(output_dict.keys()):
        output_dict[key] = np.array(output_dict[key])
    return output_dict


def filter_detections(detections: Dict[int, np.ndarray]) -> np.ndarray:
    """
    Pop empty classes and convert to Ground Truth format.

    Parameters
    ----------
    detections
        Postprocessing tensors result

    Returns
    -------
    Postprocessed tensors result without empty classes.
    """
    labels = []
    labels_which_detect = [None if detections[key].size == 0 else key for key in list(detections.keys())]
    for value in labels_which_detect:
        if value is not None:
            number_of_cl_detect = np.shape(detections[value][:, :5])[0]
            for row in range(number_of_cl_detect):
                labels.append((value, *detections[value][row, :5]))
    detections_as_array = np.asarray(labels)
    return detections_as_array


def config_dict_class_names_conversion(postprocess: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
    """
    Take result with darknet classes and transpose its numbers according to each coco class.

    Parameters
    ----------
    postprocess
        The postprocesed result

    Returns
    -------
        The result with transposed classes
    """
    reformated_dict = {}
    for key in list(postprocess.keys()):
        post_value = postprocess[key]
        label = CONFIG_DICT[str(key)]
        index = CLASS_NAMES.index(label)
        reformated_dict[index] = post_value
    return reformated_dict


def get_postprocessed_output(output: Dict[str, np.ndarray], image_size: Tuple[int, int],
                             confidence_threshold: float) -> np.ndarray:
    """
    Get the output of the ssd-mobilenet network.

    Parameters
    ----------
    output
        raw output of the runner
    image_size
        size of the input image
    confidence_threshold
        confidence threshold used to filter the predictions by the score
    Returns
    -------
    Output of ssd-mobilenet network.
    """
    orig_width, orig_height = image_size
    postprocessed_reformat = {}
    if len(output) != 0:
        boxes = output['detection_boxes:0']
        scores = output['detection_scores:0'][0]
        classes = output['detection_classes:0'][0]

        refined_scores, refined_boxes, refined_classes = refine_output_by_thresh(boxes, scores, classes,
                                                                                 confidence_threshold)
        output_dict = get_output_dict(refined_scores, refined_boxes, refined_classes)

        postprocessed_reformat = config_dict_class_names_conversion(output_dict)
        for key in list(postprocessed_reformat.keys()):
            length = postprocessed_reformat[key].shape[0]
            for number in range(length):
                # shuffle coordinates from original (ymin. xmin, ymax, xmax) to (xmin, ymin, xmax, ymax)
                box_ = yxyxs2xyxys(postprocessed_reformat[key][number])
                box_[0] *= orig_width
                box_[1] *= orig_height
                box_[2] *= orig_width
                box_[3] *= orig_height
                postprocessed_reformat[key][number] = box_

    postprocessed_filtered = filter_detections(postprocessed_reformat)
    return postprocessed_filtered


def draw_boxes(
        img_name: str,
        boxes: Any,
        font: str = '/usr/share/fonts/liberation/LiberationSans-Regular.ttf') -> Image:
    """
    Draws detected boxes.

    Parameters
    ----------
    img_name
        path to the image used to be drawn at
    boxes
        boxes that should be drawn
    font
        any font
    Returns
    -------
    image with drawn boxes
    """
    img = Image.open(img_name)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=font,
                              size=(img.size[0] + img.size[1]) // 100)
    colors = get_spaced_colors(len(CLASS_NAMES))
    if isinstance(boxes, dict):
        for cls in list(boxes.keys()):
            box_ = boxes[cls]
            box = box_[0]
            color = colors[cls]
            xy_coords, confidence = box[:4], box[4]
            xy_coords = np.asarray([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]])
            x0_coord, y0_coord = xy_coords[0], xy_coords[1]
            thickness = (img.size[0] + img.size[1]) // 200
            for tick in np.linspace(0, 1, thickness):
                xy_coords[0], xy_coords[1] = xy_coords[0] + tick, xy_coords[1] + tick
                xy_coords[2], xy_coords[3] = xy_coords[2] - tick, xy_coords[3] - tick
                draw.rectangle(xy_coords, outline=tuple(color))
            text = '{} {:.1f}%'.format(CLASS_NAMES[cls],
                                       confidence * 100)
            text_size = draw.textsize(text, font=font)
            draw.rectangle(
                [x0_coord, y0_coord - text_size[1], x0_coord + text_size[0], y0_coord],
                fill=tuple(color))
            draw.text((x0_coord, y0_coord - text_size[1]), text, fill='black',
                      font=font)
    elif isinstance(boxes, np.ndarray):
        confidence = 0
        for cls in range(boxes.shape[0]):
            box = boxes[cls]
            color = colors[int(box[0])]
            class_ = int(box[0])
            if box.shape[0] == 6:
                xy_coords, confidence = box[1:5], box[5]
            else:
                xy_coords = box[1:5]
            xy_coords = np.asarray([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]])
            x0_coord, y0_coord = xy_coords[0], xy_coords[1]
            thickness = (img.size[0] + img.size[1]) // 200
            for tick in np.linspace(0, 1, thickness):
                xy_coords[0], xy_coords[1] = xy_coords[0] + tick, xy_coords[1] + tick
                xy_coords[2], xy_coords[3] = xy_coords[2] - tick, xy_coords[3] - tick
                draw.rectangle([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]], outline=tuple(color))
            if box.shape[0] == 6:
                text = '{} {:.1f}%'.format(CLASS_NAMES[class_], confidence * 100)
            else:
                text = '{}'.format(CLASS_NAMES[class_])
            text_size = draw.textsize(text, font=font)
            draw.rectangle(
                [x0_coord, y0_coord - text_size[1], x0_coord + text_size[0], y0_coord],
                fill=tuple(color))
            draw.text((x0_coord, y0_coord - text_size[1]), text, fill='white',
                      font=font)
    else:
        raise TypeError('unsupported type of boxes %s' % type(boxes))
    img = img.convert('RGB')
    return img


def build_boxes_on_the_image(img_path: str, boxes):
    """
    Draw and display the images with the detections.

    Parameters
    ----------
    img_path
        path to the image
    boxes
        boxes that should be drawn
    Returns
    -------
    None
    """
    image_with_boxes = draw_boxes(img_path, boxes)
    image_with_boxes.show()
