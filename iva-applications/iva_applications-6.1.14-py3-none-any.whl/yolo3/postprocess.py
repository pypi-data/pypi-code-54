"""Postprocessing utils for YOLO3."""
from typing import Dict, Tuple, List
import numpy as np
import tensorflow as tf

from PIL import Image, ImageDraw, ImageFont
from iva_applications.yolo2.postprocess import get_spaced_colors


ANCHORS = [
        (10, 13), (16, 30), (33, 23),
        (30, 61), (62, 45), (59, 119),
        (116, 90), (156, 198), (373, 326)
]


MAX_OUT_SIZE = 80


def draw_boxes(img_names, boxes_dicts, class_names, model_size) -> Image:
    """
    Draws detected boxes.

    Parameters
    ----------
    img_names
        A list of input images names.
    boxes_dicts
        A class-to-boxes dictionary.
    class_names
        A class names list.
    model_size
        The input size of the model.

    Returns
    -------
        Image
    """
    colors = get_spaced_colors(len(class_names))
    for _, img_name, boxes_dict in zip(range(len(img_names)), img_names, boxes_dicts):
        img = Image.open(img_name)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font='/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
                                  size=(img.size[0] + img.size[1]) // 100)
        resize_factor = \
            (img.size[0] / model_size[0], img.size[1] / model_size[1])
        for cls, _ in enumerate(class_names):
            boxes = boxes_dict[cls]
            if np.size(boxes) != 0:
                color = colors[cls]
                for box in boxes:
                    xy_, confidence = box[:4], box[4]
                    xy_ = [xy_[i] * resize_factor[i % 2] for i in range(4)]
                    x_0, y_0 = xy_[0], xy_[1]
                    thickness = (img.size[0] + img.size[1]) // 200
                    for tick in np.linspace(0, 1, thickness):
                        xy_[0], xy_[1] = xy_[0] + tick, xy_[1] + tick
                        xy_[2], xy_[3] = xy_[2] - tick, xy_[3] - tick
                        draw.rectangle(xy_, outline=tuple(color))
                    text = '{} {:.1f}%'.format(class_names[cls],
                                               confidence * 100)
                    text_size = draw.textsize(text, font=font)
                    draw.rectangle(
                        [x_0, y_0 - text_size[1], x_0 + text_size[0], y_0],
                        fill=tuple(color))
                    draw.text((x_0, y_0 - text_size[1]), text, fill='black',
                              font=font)
                    print('{} {:.2f}%'.format(class_names[cls],
                                              confidence * 100))
        img = img.convert('RGB')
        return img


def yolo_layer(inputs, n_classes, anchors, img_size):
    """
    Create Yolo final detection layer. Detect boxes with respect to anchors.

    Parameters
    ----------
    inputs
        Tensor input.
    n_classes
        Number of labels.
    anchors
        A list of anchor sizes.
    img_size
        The input size of the model.

    Returns
    -------
         Tensor output.
    """
    n_anchors = len(anchors)
    inputs = tf.placeholder(shape=inputs.shape, dtype='float32', name='detection_placeholder')
    shape = inputs.get_shape().as_list()
    grid_shape = shape[1:3]
    inputs = tf.reshape(inputs, [-1, n_anchors * grid_shape[0] * grid_shape[1],
                                 5 + n_classes])

    strides = (img_size[0] // grid_shape[0], img_size[1] // grid_shape[1])

    box_centers, box_shapes, confidence, classes = \
        tf.split(inputs, [2, 2, 1, n_classes], axis=-1)
    width = tf.range(grid_shape[0], dtype=tf.float32)
    heigth = tf.range(grid_shape[1], dtype=tf.float32)
    width_offset, heigth_offset = tf.meshgrid(width, heigth)
    width_offset = tf.reshape(width_offset, (-1, 1))
    heigth_offset = tf.reshape(heigth_offset, (-1, 1))
    x_y_offset = tf.concat([width_offset, heigth_offset], axis=-1)
    x_y_offset = tf.tile(x_y_offset, [1, n_anchors])
    x_y_offset = tf.reshape(x_y_offset, [1, -1, 2])
    box_centers = tf.nn.sigmoid(box_centers)
    box_centers = (box_centers + x_y_offset) * strides

    anchors = tf.tile(anchors, [grid_shape[0] * grid_shape[1], 1])
    box_shapes = tf.exp(box_shapes) * tf.to_float(anchors)

    confidence = tf.nn.sigmoid(confidence)

    classes = tf.nn.sigmoid(classes)

    inputs = tf.concat([box_centers, box_shapes,
                        confidence, classes], axis=-1)

    return inputs


def build_boxes(inputs):
    """Compute top left and bottom right points of the boxes."""
    center_x, center_y, width, height, confidence, classes = \
        tf.split(inputs, [1, 1, 1, 1, 1, -1], axis=-1)

    top_left_x = center_x - width / 2
    top_left_y = center_y - height / 2
    bottom_right_x = center_x + width / 2
    bottom_right_y = center_y + height / 2

    boxes = tf.concat([top_left_x, top_left_y,
                       bottom_right_x, bottom_right_y,
                       confidence, classes], axis=-1)

    return boxes


def non_max_suppression(inputs, n_classes, max_output_size, iou_threshold,
                        confidence_threshold):
    """
    Perform non-max suppression separately for each class.

    Parameters
    ----------
    inputs
        Tensor input.
    n_classes
        Number of classes.
    max_output_size
        Max number of boxes to be selected for each class.
    iou_threshold
        Threshold for the IOU.
    confidence_threshold
        Threshold for the confidence score.

    Returns
    -------
        A list containing class-to-boxes dictionaries for each sample in the batch.
    """
    batch = tf.unstack(inputs)
    boxes_dicts = []
    for boxes in batch:
        boxes = tf.boolean_mask(boxes, boxes[:, 4] > confidence_threshold)
        classes = tf.argmax(boxes[:, 5:], axis=-1)
        classes = tf.expand_dims(tf.to_float(classes), axis=-1)
        boxes = tf.concat([boxes[:, :5], classes], axis=-1)

        boxes_dict = dict()
        for cls in range(n_classes):
            mask = tf.equal(boxes[:, 5], cls)
            mask_shape = mask.get_shape()
            if mask_shape.ndims != 0:
                class_boxes = tf.boolean_mask(boxes, mask)
                boxes_coords, boxes_conf_scores, _ = tf.split(class_boxes,
                                                              [4, 1, -1],
                                                              axis=-1)
                boxes_conf_scores = tf.reshape(boxes_conf_scores, [-1])
                indices = tf.image.non_max_suppression(boxes_coords,
                                                       boxes_conf_scores,
                                                       max_output_size,
                                                       iou_threshold)
                class_boxes = tf.gather(class_boxes, indices)
                boxes_dict[cls] = class_boxes[:, :5]

        boxes_dicts.append(boxes_dict)

    return boxes_dicts


def build_detection_graph(
                output_tensors: Dict,
                input_shape: Tuple,
                class_names: List,
                anchors: List,
                iou_threshold: float,
                confidence_threshold: float):
    """Build YOLO3 tensorflow postprocessing graph for detection."""
    n_classes = len(class_names)
    keys = list(output_tensors.keys())
    detect0 = yolo_layer(output_tensors[keys[0]],
                         n_classes=n_classes,
                         anchors=anchors[6:9],
                         img_size=input_shape)
    detect1 = yolo_layer(output_tensors[keys[1]],
                         n_classes=n_classes,
                         anchors=anchors[3:6],
                         img_size=input_shape)
    detect2 = yolo_layer(output_tensors[keys[2]],
                         n_classes=n_classes,
                         anchors=anchors[0:3],
                         img_size=input_shape)
    output_tensors = tf.concat([detect0, detect1, detect2], axis=1)
    output_tensors = build_boxes(output_tensors)
    boxes_dicts = non_max_suppression(
        output_tensors, n_classes=n_classes,
        max_output_size=MAX_OUT_SIZE,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold)
    return boxes_dicts
