"""
This module provides a function to upload an object string to Google Cloud Storage.
"""

import os

from google.cloud import storage


class _StorageUploader:
    def __init__(self, bucket=None):
        self._client = storage.Client()
        self._bucket = self._client.bucket(bucket or os.environ["STORAGE_BUCKET"])

    def __call__(self, obj_str, filepath):
        blob = self._bucket.blob(filepath)
        blob.upload_from_string(obj_str)


def to_storage(obj_str, filepath, bucket=None):
    _StorageUploader(bucket)(obj_str, filepath)
