import json
import numpy
import datetime
import decimal
import GrabCarAssignmentdorachua.OurCustomEncoder


def data_to_json(data):
        json_data = json.dumps(data,cls=GrabCarAssignmentdorachua.OurCustomEncoder)
        return json_data