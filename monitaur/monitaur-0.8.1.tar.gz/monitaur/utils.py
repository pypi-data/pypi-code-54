import base64
import hashlib
import pickle

import dill
import joblib
import numpy as np
from monitaur.exceptions import FileError
from monitaur.virgil.alibi.tabular import AnchorTabular


def hash_file(filename):
    hash_ = hashlib.sha256()

    with open(filename, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_.update(chunk)

    return hash_.hexdigest()


def get_influences(anchor_binary_data, model_set, features):
    """
    Downloads trained model and respective influences from s3.
    Then calculates influences for a given transaction.

    Args:
        model_set: A UUID string for the monitaur model set.
        response: Json dumped anchor data from the API

    Returns:
        dict of influences
    """

    influence_threshold = 0.95

    # write explainers for the model to anchors file
    anchors_filename = f"{model_set}.anchors"
    anchor_data = base64.b64decode(anchor_binary_data["data"])

    with open(anchors_filename, "wb") as f:
        f.write(anchor_data)

    # load explainer from s3 download
    with open(anchors_filename, "rb") as f:
        explainer = dill.load(f)

    # determine influences for transaction
    inputs = list(features.values())
    reshaped_inputs = np.asarray(inputs).reshape(1, len(inputs))
    influences = explainer.explain(reshaped_inputs, threshold=influence_threshold)

    return influences["names"]


def valid_model(extension, model_class):
    """
    Validates a trained model based on the model_class.

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        model_class: 'tabular' or 'image'.

    Returns:
        True if valid
    """

    if model_class == "tabular" and extension not in [".joblib", ".pickle"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.pickle'.")
    if model_class == "image" and extension not in [".joblib", ".tar", ".h5"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.tar', '.h5'.")

    return True


def generate_anchors(
    extension, trained_model, feature_names, training_data, model_set_id
):
    """
    Generates anchor

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        trained_model: Instantiated model (.joblib, .pickle, '.tar', '.h5).
        feature_names: Model inputs.
        training_data: Training data (x training).
        model_set_id: A UUID string for the monitaur model set received from the API.

    Returns:
        binary
    """

    if extension == ".joblib":
        trained_model_file = joblib.load(trained_model)
    else:
        trained_model_file = pickle.load(trained_model)

    predict_fn = lambda x: trained_model_file.predict_proba(x)  # NOQA
    explainer = AnchorTabular(predict_fn, feature_names)
    explainer.fit(training_data)

    filename_anchors = f"{model_set_id}.anchors"

    with open(filename_anchors, "wb") as f:
        dill.dump(explainer, f)

    with open(filename_anchors, "rb") as f:
        return (filename_anchors, (base64.b64encode(f.read())).decode("utf-8"))
