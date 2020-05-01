from deepomatic.oef.configs.utils import dict_inject
from ..utils import keep_aspect_ratio_resizer, update_if_not_present
from ..backbones import backbones

common_config = {
    'trainer': {
        'batch_size': 1,
    },
    '@model.backbone.input': {
        'image_resizer': keep_aspect_ratio_resizer(1024, 1024),
        'data_augmentation_options': [{'random_horizontal_flip': {'keypoint_flip_permutation': []}}],
    },
    '@meta_arch.parameters': {
        'first_stage_anchor_generator': {
            'grid_anchor_generator': {
                'aspect_ratios': [
                    0.5,
                    1.0,
                    2.0
                ],
                'height': 256,
                'height_offset': 0,
                'height_stride': 16,
                'scales': [
                    0.25,
                    0.5,
                    1.0,
                    2.0
                ],
                'width': 256,
                'width_offset': 0,
                'width_stride': 16
            }
        },
        'first_stage_box_predictor_conv_hyperparams': {
            'activation': 'RELU',
            'initializer': {
                'truncated_normal_initializer': {
                    'mean': 0.0,
                    'stddev': 0.01
                }
            },
            'op': 'CONV',
            'regularize_depthwise': False,
            'regularizer': {
                'l2_regularizer': {
                    'weight': 0.0
                }
            }
        },
        'second_stage_post_processing': {
            'batch_non_max_suppression': {
                'iou_threshold': 0.6,
                'max_detections_per_class': 100,
                'max_total_detections': 300,
                'score_threshold': 0.0
            },
            'logit_scale': 1.0,
            'score_converter': 'SOFTMAX'
        },
    }
}

configs = {
    'faster_rcnn': {
        'display_name': 'Faster RCNN',
        'model_default_args': dict_inject(common_config, {
            '@meta_arch': {
                'initial_crop_size': 14,
                'maxpool_kernel_size': 2,
                'maxpool_stride': 2,
            },
            '@meta_arch.parameters': {
                'second_stage_box_predictor': {
                    'mask_rcnn_box_predictor': {
                        'box_code_size': 4,
                        'dropout_keep_probability': 1.0,
                        'fc_hyperparams': {
                            'activation': 'RELU',
                            'initializer': {
                                'variance_scaling_initializer': {
                                    'factor': 1.0,
                                    'mode': 'FAN_AVG',
                                    'uniform': True
                                }
                            },
                            'op': 'FC',
                            'regularize_depthwise': False,
                            'regularizer': {
                                'l2_regularizer': {
                                    'weight': 0.0
                                }
                            }
                        },
                        'mask_height': 15,
                        'mask_prediction_conv_depth': 256,
                        'mask_prediction_num_conv_layers': 2,
                        'mask_width': 15,
                        'masks_are_class_agnostic': False,
                        'predict_instance_masks': False,
                        'predict_keypoints': False,
                        'share_box_across_classes': False,
                        'use_dropout': False
                    }
                },
                'second_stage_classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            },
        }),
        'model_meta_arch': 'faster_rcnn',
        'backbones': update_if_not_present({
            'inception_resnet_v2': {'trainer': {'initial_learning_rate': 0.0002}},
            'inception_v2': {'trainer': {'initial_learning_rate': 0.0002}},
            'nasnet_large': {'trainer': {'initial_learning_rate': 0.0003}},
            'pnasnet_large': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_50_v1': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_101_v1': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_152_v1': {'trainer': {'initial_learning_rate': 0.0003}},
        }, {
            # We use those default parameters for all other backbones
            k: {'trainer': {'initial_learning_rate': 0.0002}} for k in backbones
        }),
        'pretrained_parameters': {
            'natural_rgb': update_if_not_present({
                # See: https://github.com/Deepomatic/thoth/issues/230
                # 'inception_resnet_v2': 'tensorflow/natural_rgb/inception_resnet_v2-faster_rcnn-coco-2018_01_28.tar.gz',
                # See: https://github.com/Deepomatic/thoth/issues/276
                # 'nasnet_large': 'tensorflow/natural_rgb/nasnet_large-faster_rcnn-coco-2018_01_28.tar.gz',
                'resnet_50_v1': 'tensorflow/natural_rgb/resnet_50_v1-faster_rcnn-coco-2020_04_14.tar.gz',
                'resnet_101_v1': 'tensorflow/natural_rgb/resnet_101_v1-faster_rcnn-coco-2020_04_14.tar.gz',
            }, {
                # We use the backbone checkpoint for all other backbones
                k: None for k in backbones
            })
        }
    },
    'rfcn': {
        'display_name': 'RFCN',
        'model_default_args': dict_inject(common_config, {
            '@meta_arch.parameters': {
                'second_stage_box_predictor': {
                    'rfcn_box_predictor': {
                        'box_code_size': 4,
                        'conv_hyperparams': {
                            'activation': 'RELU',
                            'initializer': {
                                'truncated_normal_initializer': {
                                    'mean': 0.0,
                                    'stddev': 0.01
                                }
                            },
                            'op': 'CONV',
                            'regularize_depthwise': False,
                            'regularizer': {
                                'l2_regularizer': {
                                    'weight': 0.0
                                }
                            }
                        },
                        'crop_height': 18,
                        'crop_width': 18,
                        'depth': 1024,
                        'num_spatial_bins_height': 3,
                        'num_spatial_bins_width': 3
                    }
                },
                'second_stage_classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            },
        }),
        'model_meta_arch': 'rfcn',
        'backbones': update_if_not_present({
            'inception_resnet_v2': {'trainer': {'initial_learning_rate': 0.0003}},
            'inception_v2': {'trainer': {'initial_learning_rate': 0.0003}},
            'nasnet_large': {'trainer': {'initial_learning_rate': 0.0003}},
            'pnasnet_large': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_50_v1': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_101_v1': {'trainer': {'initial_learning_rate': 0.0003}},
            'resnet_152_v1': {'trainer': {'initial_learning_rate': 0.0003}},
        }, {
            # We use those default parameters for all other backbones
            k: {'trainer': {'initial_learning_rate': 0.0003}} for k in backbones
        }),
        'pretrained_parameters': {
            'natural_rgb': update_if_not_present({
                'resnet_101_v1': 'tensorflow/natural_rgb/resnet_101_v1-rfcn-coco-2018_01_28.tar.gz',
            }, {
                # We use the backbone checkpoint for all other backbones
                k: None for k in backbones
            })
        }
    },
}
