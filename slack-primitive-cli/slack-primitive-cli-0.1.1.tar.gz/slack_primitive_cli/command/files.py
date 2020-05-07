import os
from typing import Any, Optional

import click
import slack
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup


@click.command(name="files.upload", help="Uploads or creates a file. See https://api.slack.com/methods/files.upload ")
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--channels", required=True)
@optgroup.group("File contents", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--file")
@optgroup.option("--content")
@click.option("--filename")
@click.option("--filetype")
@click.option("--initial_comment")
@click.option("--thread_ts")
@click.option("--title")
def upload(token, channels, file, content, filename, filetype, initial_comment, thread_ts, title):
    client = slack.WebClient(token=token)

    if filename is None and file is not None:
        filename = os.path.basename(file)

    def _update_kwargs(key: str, value: Optional[Any]):
        if value is not None:
            kwargs[key] = value

    kwargs = dict(channels=channels)
    _update_kwargs("file", file)
    _update_kwargs("content", content)
    _update_kwargs("filename", filename)
    _update_kwargs("filetype", filetype)
    _update_kwargs("initial_comment", initial_comment)
    _update_kwargs("thread_ts", thread_ts)
    _update_kwargs("title", title)

    # Noneの引数を渡すと、以下のエラーが発生するため、Noneの引数は`files_upload`メソッドに渡さないようにする
    # TypeError: Can not serialize value type: <class 'NoneType'>
    if title is not None:
        kwargs["title"] = title

    response = client.files_upload(**kwargs)
    print(response)
    return response


@click.command(name="files.delete", help="Deletes a file. See https://api.slack.com/methods/files.delete ")
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--file", required=True)
def delete(token, file):
    client = slack.WebClient(token=token)
    response = client.files_delete(file=file)
    print(response)
    return response
