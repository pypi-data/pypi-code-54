# Copyright [2018-2020] Peter Krenesky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ixian_docker.utils.print import ProgressPrinter


def print_docker_transfer_events(events):
    """
    Print a stream of events from a docker push or pull.

    :param events:
    :return:
    """
    printer = ProgressPrinter()
    for event in events:
        if "id" in event:
            # layer events all have an id
            file_id = event["id"]
            if file_id not in printer.line_numbers:
                printer.add_line(file_id)
            printer.print(
                file_id, f"{file_id}: {event['status']} {event.get('progress', '')}",
            )

        else:
            # non-layer events occur after all layers are complete.
            # move cursor to the end (complete) and then print the status
            if not printer.is_complete:
                printer.complete()

            if "status" in event:
                print(event["status"])
            elif "errorDetail" in event:
                print(event["error"])
            else:
                # some events like push digest happen twice, they can be ignored.
                pass


def format_pull_status_minimal(status, seen_layers=None):
    """
    Minimally format a single status message from a docker pull or push.

    This is a minimal format. If seen_layers is provided, only the first update for download and
    extraction statuses are printed. This is a quieter format that reads easier in a text log.

    :param status: dict of status data
    :param seen_layers: set of layers that have already been seen.
    :return:
    """
    if "id" not in status:
        return status

    layer_id = status["id"]
    if status.startswith("Pulling from"):
        return f"{status}:{layer_id}"

    elif status in [
        "Pulling fs layer",
        "Pull complete",
        "Downloading",
        "Extracting",
        "Download complete",
    ]:
        if status in ["Downloading", "Extracting"]:
            seen = seen_layers[status]
            if layer_id in seen:
                return None
            else:
                layer_size = status["progressDetail"]["total"]
                status = f"{status} {format_bytes(layer_size)}"
                seen.add(layer_id)

        return f"{layer_id}: {status}"


def format_bytes(size):
    """
    human readable bytes size
    :param size: integer
    :return: string
    """
    power = 2 ** 10
    n = 0
    power_labels = {0: "B", 1: "kB", 2: "MB", 3: "GB", 4: "TB"}
    while size > power:
        size /= power
        n += 1
    if n:
        formatted_size = f"{size:.2f}"
    else:
        formatted_size = size
    return f"{formatted_size}{power_labels[n]}"
