from io import BytesIO

import joblib
import pytest
from monitaur import hash_file
from monitaur.exceptions import FileError
from monitaur.utils import generate_anchors, valid_model
from monitaur.virgil.alibi.tabular import AnchorTabular


def test_hash_file_returns_sha256_hash_of_a_file(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value = BytesIO(b"12345")

    result = hash_file("filename")

    mock_open.assert_called_once_with("filename", "rb")
    assert result == "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"


def test_valid_model():
    assert valid_model(".pickle", "tabular")
    assert valid_model(".h5", "image")

    with pytest.raises(FileError) as excinfo:
        valid_model(".h5", "tabular")
        assert (
            "Invalid model. Acceptable files: '.joblib', '.pickle'."
            == excinfo.value.message
        )

    with pytest.raises(FileError) as excinfo:
        valid_model("", "image")
        assert (
            "Invalid model. Acceptable files: '.joblib', '.tar', '.h5'."
            == excinfo.value.message
        )


def test_generate_anchors(mocker, training_data):
    mocker.patch.object(
        joblib, "load", return_value=b"Image-Base-64-encoded-return-data"
    )
    mocker.patch.object(AnchorTabular, "__init__", return_value=None)
    mocker.patch.object(AnchorTabular, "fit")

    assert generate_anchors(
        ".joblib",
        "job.joblib",
        [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeF",
            "Age",
        ],
        training_data,
        1,
    )
