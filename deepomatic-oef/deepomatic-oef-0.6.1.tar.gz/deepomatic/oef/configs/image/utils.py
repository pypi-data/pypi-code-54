import copy

def fixed_shape_resizer(width, height):
    return {'fixed_shape_resizer': {'convert_to_grayscale': False, 'height': height, 'resize_method': 'BILINEAR', 'width': width}}

def keep_aspect_ratio_resizer(min_size, max_size):
    return {'keep_aspect_ratio_resizer': {'convert_to_grayscale': False, 'max_dimension': max_size, 'min_dimension': min_size, 'pad_to_max_dimension': False, 'per_channel_pad_value': None, 'resize_method': 'BILINEAR'}}


def update_if_not_present(target_dict, default_dict):
    """
    This returns a copy of target_dict augmented with all the key-values present
    in default_dict but not in target_dict.

    Args:
        target_dict (dict): The dictionnary to augment.
        default_dict (dict): The default keys and values that will be injected in target_dict
                             if not present.

    Return:
        A dict augmented with the default keys from default_dict.
    """
    target_dict = copy.deepcopy(target_dict)
    target_dict.update({k: v for k, v in default_dict.items() if k not in target_dict})
    return target_dict
