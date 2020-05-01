"""
S3 storage

Store data in S3
"""
import os
import sys
import json
import gzip

try:
    # python2
    from urlparse import urlparse
    import cStringIO
    BytesIO = cStringIO.StringIO
except:
    # python3
    from urllib.parse import urlparse
    import io
    BytesIO = io.BytesIO

from .datastore import MetaflowDataStore, DataException, only_if_not_done
from ..metadata import MetaDatum
from .util.s3util import aws_retry, get_s3_client

class S3DataStore(MetaflowDataStore):
    TYPE='s3'

    s3 = None
    ClientError = None

    def __init__(self, *args, **kwargs):
        self.reset_client()
        super(S3DataStore, self).__init__(*args, **kwargs)

    @classmethod
    def reset_client(cls, hard_reset=False):
        # the s3 client is shared across all S3DataStores
        # so we don't open N connections to S3 unnecessarily
        if cls.s3 is None or hard_reset:
            cls.s3, cls.ClientError = get_s3_client()

    @aws_retry
    def _get_s3_object(self, path, return_buf=False):
        url = urlparse(path)
        buf = BytesIO()
        if self.monitor:
            with self.monitor.measure("metaflow.s3.get_object"):
                self.s3.download_fileobj(url.netloc, url.path.lstrip('/'), buf)
        else:
           self.s3.download_fileobj(url.netloc, url.path.lstrip('/'), buf) 
        if return_buf:
            buf.seek(0)
            return buf
        else:
            return buf.getvalue()

    @aws_retry
    def _put_s3_object(self, path, blob=None, buf=None):
        url = urlparse(path)
        if buf is None:
            buf = BytesIO(blob)
        if self.monitor:
            with self.monitor.measure("metaflow.s3.put_object"):
                self.s3.upload_fileobj(buf, url.netloc, url.path.lstrip('/'))
        else:
            self.s3.upload_fileobj(buf, url.netloc, url.path.lstrip('/'))

    @aws_retry
    def _head_s3_object(self, path):
        url = urlparse(path)
        try:
            return self.s3.head_object(Bucket=url.netloc, Key=url.path.lstrip('/'))
        except self.ClientError as err:
            error_code = int(err.response['Error']['Code'])
            if error_code == 404:
                return None
            else:
                raise

    @classmethod
    def get_latest_tasks(cls,
                         flow_name,
                         run_id=None,
                         steps=None,
                         pathspecs=None):
        run_prefix = cls.make_path(flow_name, run_id)

        from metaflow import S3
        with S3() as s3:
            task_urls = []
            # Note: When `pathspecs` is specified, we avoid the eventually
            # consistent `s3.list_paths` operation, and directly construct the
            # task_urls list.
            if pathspecs:
                task_urls = [cls.make_path(flow_name, pathspec=pathspec)
                             for pathspec in pathspecs]
            elif steps:
                task_objs = s3.list_paths(
                    [cls.make_path(flow_name, run_id, step) for step in steps])
                task_urls = [task.url for task in task_objs]
            else:
                step_objs = s3.list_paths([run_prefix])
                task_objs = s3.list_paths([step.url for step in step_objs])
                task_urls = [task.url for task in task_objs]
            urls = []
            for task_url in task_urls:
                for attempt in range(5):
                    metadata_filename = \
                        cls.get_metadata_filename_for_attempt(attempt)
                    urls.append(os.path.join(task_url, metadata_filename))
                    # Note for potential future optimization:
                    # Find the list of latest attempt for each task first, and
                    # follow up with a call to get done and metadata.
                    attempt_filename = \
                        cls.get_filename_for_attempt(attempt)
                    urls.append(os.path.join(task_url, attempt_filename))
                    done_filename = cls.get_done_filename_for_attempt(attempt)
                    urls.append(os.path.join(task_url, done_filename))

            results = s3.get_many(urls, return_missing=True)

            all_data_blobs = {}
            latest_attempt = {}
            done_attempts = set()

            for result in results:
                if result.exists:
                    path = result.url
                    step_name, task_id, fname = path.split('/')[-3:]
                    _, attempt = cls.parse_filename(fname)
                    if cls.is_done_filename(fname):
                        done_attempts.add((step_name, task_id, attempt))
                    elif cls.is_attempt_filename(fname):
                        # files are in sorted order, so overwrite is ok.
                        latest_attempt[(step_name, task_id)] = attempt
                    else:
                        # is_metadata_filename(fname) == True.
                        all_data_blobs[(step_name, task_id, attempt)] = \
                            result.blob
            latest_attempts = set((step_name, task_id, attempt)
                                   for (step_name, task_id), attempt
                                       in latest_attempt.items())
            latest_and_done = latest_attempts & done_attempts

        return [(step_name, task_id, attempt,
                 all_data_blobs[(step_name, task_id, attempt)])
                 for step_name, task_id, attempt in latest_and_done]

    @classmethod
    def get_artifacts(cls, artifacts_to_prefetch):
        artifact_list = []
        from metaflow import S3
        with S3() as s3:
            for obj in s3.get_many(artifacts_to_prefetch):
                sha = obj.key.split('/')[-1]
                artifact_list.append((sha, cls.decode_gzip_data(obj.path)))
        return artifact_list

    @only_if_not_done
    def save_metadata(self, name, data):
        """
        Save a task-specific metadata dictionary as JSON.
        """
        filename = self.filename_with_attempt_prefix('%s.json' % name,
                                                     self.attempt)
        path = os.path.join(self.root, filename)
        self._put_s3_object(path, json.dumps(data).encode('utf-8'))

    def has_metadata(self, name, with_attempt=True):
        attempt = self.attempt if with_attempt else None
        filename = self.filename_with_attempt_prefix('%s.json' % name,
                                                     attempt)
        path = os.path.join(self.root, filename)
        return bool(self._head_s3_object(path))

    def load_metadata(self, name):
        """
        Load a task-specific metadata dictionary as JSON.
        """
        filename = self.filename_with_attempt_prefix('%s.json' % name,
                                                     self.attempt)
        path = os.path.join(self.root, filename)
        return json.loads(self._get_s3_object(path).decode('utf-8'))

    def object_path(self, sha):
        root = os.path.join(self.data_root, sha[:2])
        return os.path.join(root, sha)

    @only_if_not_done
    def save_data(self, sha, transformable_object):
        """
        Save a content-addressed data blob if it doesn't exist already.
        """
        path = self.object_path(sha)
        if not self._head_s3_object(path):
            buf = BytesIO()
            # NOTE compresslevel makes a huge difference. The default
            # level of 9 can be impossibly slow.
            with gzip.GzipFile(fileobj=buf,
                               mode='wb',
                               compresslevel=3) as f:
                f.write(transformable_object.current())
            transformable_object.transform(lambda _: buf)
            buf.seek(0)
            self._put_s3_object(path, buf=buf)
        return path

    def load_data(self, sha):
        """
        Load a content-addressed data blob.
        """
        path = self.object_path(sha)
        buf = self._get_s3_object(path, return_buf=True)
        return self.decode_gzip_data(None, buf) # filename=None

    @only_if_not_done
    def save_log(self, logtype, bytebuffer):
        """
        Save a log file represented as a bytes object.
        """
        path = self.get_log_location(logtype)
        self._put_s3_object(path, bytebuffer)
        return path

    def load_log(self, logtype, attempt_override=None):
        """
        Load a task-specific log file represented as a bytes object.
        """
        path = self.get_log_location(logtype, attempt_override)
        return self._get_s3_object(path)

    @only_if_not_done
    def done(self):
        """
        Write a marker indicating that datastore has finished writing to
        this path.
        """
        filename = self.get_done_filename_for_attempt(self.attempt)
        path = os.path.join(self.root, filename)
        self._put_s3_object(path, b'')

        self.metadata.register_metadata(
            self.run_id, self.step_name, self.task_id,
            [MetaDatum(field='attempt-done', value=str(self.attempt), type='attempt-done')])

        self._is_done_set = True

    def is_done(self):
        """
        A flag indicating whether this datastore directory was closed
        succesfully with done().
        """
        filename = self.get_done_filename_for_attempt(self.attempt)
        path = os.path.join(self.root, filename)
        return bool(self._head_s3_object(path))
