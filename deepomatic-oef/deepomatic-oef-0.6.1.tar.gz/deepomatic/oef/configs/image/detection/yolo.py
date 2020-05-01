from ..utils import fixed_shape_resizer

configs = {
    'yolo_v2': {
        'display_name': 'YOLO v2',
        'model_default_args': {
            'trainer': {
                'batch_size': 64,
            },
            '@model.backbone.input': {
                'image_resizer': fixed_shape_resizer(416, 416),
                'data_augmentation_options': [],
            },
            '@meta_arch.parameters': {
                'subdivisions': 16,
                'classification_loss': {'weighted_softmax': {'logit_scale': 1.0}}
            },

        },
        'model_meta_arch': 'yolo_v2',
        'backbones': {
            'darknet_19': {'trainer': {'initial_learning_rate': 0.01}},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'darknet_19': 'darknet/natural_rgb/darknet19-yolo-voc2007.weights',
            }
        }
    },
    'yolo_v3': {
        'display_name': 'YOLO v3',
        'model_default_args': {
            'trainer': {
                'batch_size': 64,
            },
            '@model.backbone.input': {
                'image_resizer': fixed_shape_resizer(416, 416),
                'data_augmentation_options': [],
            },
            '@meta_arch.parameters': {
                'subdivisions': 32,
                'classification_loss': {'weighted_sigmoid': {}}
            },
        },
        'model_meta_arch': 'yolo_v3',
        'backbones': {
            'darknet_53': {'trainer': {'initial_learning_rate': 0.01}},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'darknet_53': 'darknet/natural_rgb/darknet53-yolo-imagenet2012.weights',
            }
        }
    },
}
