import base64
import hashlib

import dill
import numpy as np


def hash_file(filename):
    hash_ = hashlib.sha256()

    with open(filename, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_.update(chunk)

    return hash_.hexdigest()


def get_influences(response, model_set, features):
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
    anchor_data = base64.b64decode(response["data"])
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
