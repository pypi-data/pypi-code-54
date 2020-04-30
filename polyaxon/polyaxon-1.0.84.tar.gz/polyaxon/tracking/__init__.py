#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Union, Sequence

from polyaxon.client import RunClient
from polyaxon.polyboard.artifacts import V1RunArtifact
from polyaxon.tracking.run import Run
from polyaxon_sdk import V1Operation

TRACKING_RUN = None


def init(
    owner: str = None,
    project: str = None,
    run_uuid: str = None,
    client: RunClient = None,
    track_code: bool = True,
    track_env: bool = False,
    refresh_data: bool = False,
    artifacts_path: str = None,
):
    global TRACKING_RUN

    TRACKING_RUN = Run(
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        client=client,
        track_code=track_code,
        refresh_data=refresh_data,
        track_env=track_env,
        artifacts_path=artifacts_path,
    )


def create(
    name: str = None,
    description: str = None,
    tags: Union[str, Sequence[str]] = None,
    content: Union[str, V1Operation] = None,
):
    global TRACKING_RUN
    TRACKING_RUN.create(
        name=name, description=description, tags=tags, content=content,
    )


def get_tensorboard_path():
    global TRACKING_RUN
    return TRACKING_RUN.get_tensorboard_path()


def get_outputs_path():
    global TRACKING_RUN
    return TRACKING_RUN.outputs_path


def get_artifacts_path():
    global TRACKING_RUN
    return TRACKING_RUN.artifacts_path


def log_metric(name, value, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_metric(
        name=name, value=value, step=step, timestamp=timestamp,
    )


def log_metrics(step=None, timestamp=None, **metrics):
    global TRACKING_RUN
    TRACKING_RUN.log_metrics(step=step, timestamp=timestamp, **metrics)


def log_image(data, name=None, step=None, timestamp=None, rescale=1, dataformats="CHW"):
    global TRACKING_RUN
    TRACKING_RUN.log_image(
        data=data,
        name=name,
        step=step,
        timestamp=timestamp,
        rescale=rescale,
        dataformats=dataformats,
    )


def log_image_with_boxes(
    tensor_image,
    tensor_boxes,
    name=None,
    step=None,
    timestamp=None,
    rescale=1,
    dataformats="CHW",
):
    global TRACKING_RUN
    TRACKING_RUN.log_image_with_boxes(
        tensor_image=tensor_image,
        tensor_boxes=tensor_boxes,
        name=name,
        step=step,
        timestamp=timestamp,
        rescale=rescale,
        dataformats=dataformats,
    )


def log_mpl_image(data, name=None, close=True, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_mpl_image(
        data=data, name=name, close=close, step=step, timestamp=timestamp,
    )


def log_video(data, name=None, fps=4, step=None, timestamp=None, content_type=None):
    global TRACKING_RUN
    TRACKING_RUN.log_video(
        data=data,
        name=name,
        fps=fps,
        step=step,
        timestamp=timestamp,
        content_type=content_type,
    )


def log_audio(
    data, name=None, sample_rate=44100, step=None, timestamp=None, content_type=None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_audio(
        data=data,
        name=name,
        sample_rate=sample_rate,
        step=step,
        timestamp=timestamp,
        content_type=content_type,
    )


def log_text(name, text, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_text(
        name=name, text=text, step=step, timestamp=timestamp,
    )


def log_html(name, html, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_html(
        name=name, html=html, step=step, timestamp=timestamp,
    )


def log_np_histogram(name, values, counts, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_np_histogram(
        name=name, values=values, counts=counts, step=step, timestamp=timestamp,
    )


def log_histogram(name, values, bins, max_bins=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_histogram(
        name=name,
        values=values,
        bins=bins,
        max_bins=max_bins,
        step=step,
        timestamp=timestamp,
    )


def log_model(path, name=None, framework=None, spec=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_model(
        path=path,
        name=name,
        framework=framework,
        spec=spec,
        step=step,
        timestamp=timestamp,
    )


def log_dataframe(path, name=None, content_type=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_dataframe(
        path=path, name=name, content_type=content_type, step=step, timestamp=timestamp,
    )


def log_artifact(path, name=None, artifact_kind=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_artifact(
        path=path,
        name=name,
        artifact_kind=artifact_kind,
        step=step,
        timestamp=timestamp,
    )


def log_roc_auc_curve(name, fpr, tpr, auc=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_roc_auc_curve(
        name=name, fpr=fpr, tpr=tpr, auc=auc, step=step, timestamp=timestamp,
    )


def log_sklearn_roc_auc_curve(name, y_preds, y_targets, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_sklearn_roc_auc_curve(
        name=name, y_preds=y_preds, y_targets=y_targets, step=step, timestamp=timestamp,
    )


def log_pr_curve(
    name, precision, recall, average_precision=None, step=None, timestamp=None
):
    global TRACKING_RUN
    TRACKING_RUN.log_pr_curve(
        name=name,
        precision=precision,
        recall=recall,
        average_precision=average_precision,
        step=step,
        timestamp=timestamp,
    )


def log_sklearn_pr_curve(name, y_preds, y_targets, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_sklearn_pr_curve(
        name=name, y_preds=y_preds, y_targets=y_targets, step=step, timestamp=timestamp,
    )


def log_curve(name, x, y, annotation=None, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_sklearn_pr_curve(
        name=name, x=x, y=y, annotation=annotation, step=step, timestamp=timestamp,
    )


def log_plotly_chart(name, figure, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_plotly_chart(
        name=name, figure=figure, step=step, timestamp=timestamp,
    )


def log_bokeh_chart(name, figure, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_bokeh_chart(
        name=name, figure=figure, step=step, timestamp=timestamp,
    )


def log_mpl_plotly_chart(name, figure, step=None, timestamp=None):
    global TRACKING_RUN
    TRACKING_RUN.log_mpl_plotly_chart(
        name=name, figure=figure, step=step, timestamp=timestamp,
    )


def set_description(description):
    global TRACKING_RUN
    TRACKING_RUN.set_description(description=description)


def set_name(name):
    global TRACKING_RUN
    TRACKING_RUN.set_name(name=name)


def log_status(status, reason=None, message=None):
    global TRACKING_RUN
    TRACKING_RUN.log_status(
        status=status, reason=reason, message=message,
    )


def log_inputs(reset=False, **inputs):
    global TRACKING_RUN
    TRACKING_RUN.log_inputs(reset=reset, **inputs)


def log_outputs(reset=False, **outputs):
    global TRACKING_RUN
    TRACKING_RUN.log_outputs(reset=reset, **outputs)


def log_tags():
    global TRACKING_RUN
    TRACKING_RUN.log_tags()


def log_succeeded():
    global TRACKING_RUN
    TRACKING_RUN.log_succeeded()


def log_stopped():
    global TRACKING_RUN
    TRACKING_RUN.log_stopped()


def log_failed(message=None, traceback=None):
    global TRACKING_RUN
    TRACKING_RUN.log_failed(message=message, traceback=traceback)


def log_code_ref():
    global TRACKING_RUN
    TRACKING_RUN.log_code_ref()


def log_data_ref(name: str, hash: str = None, path: str = None, content=None):
    global TRACKING_RUN
    TRACKING_RUN.log_data_ref(name=name, content=content, hash=hash, path=path)


def log_file_ref(path: str, hash: str = None, content=None):
    global TRACKING_RUN
    TRACKING_RUN.log_file_ref(
        path=path, hash=hash, content=content,
    )


def log_dir_ref(path: str):
    global TRACKING_RUN
    TRACKING_RUN.log_dir_ref(path=path)


def log_artifact_lineage(body: List[V1RunArtifact]):
    global TRACKING_RUN
    TRACKING_RUN.log_artifact_lineage(body)


def set_artifacts_path(artifacts_path: str):
    global TRACKING_RUN
    TRACKING_RUN.set_artifacts_path(artifacts_path)
