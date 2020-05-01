from ..utils import fixed_shape_resizer

configs = {
    'attention': {
        'display_name': 'Attention OCR',
        'model_default_args': {
            'trainer': {
                'batch_size': 32,
            },
            '@model.backbone.input': {
                'image_resizer': fixed_shape_resizer(102, 32),
                'data_augmentation_options': [],
            },
        },
        'model_meta_arch': 'attention',
        'backbones': {
            'inception_v3': {'trainer': {'initial_learning_rate': 0.004}},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'inception_v3': 'tensorflow/natural_rgb/inception_v3-classification-imagenet2012-2016_08_28.ckpt',
            }
        }
    },
}
