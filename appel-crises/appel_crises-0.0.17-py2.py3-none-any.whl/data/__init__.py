"""
Data module. This little python file only imports the json stored in the directory.
"""
import glob
import json
import os
from collections import namedtuple
from typing import Tuple, Dict, List

from appel_crises.settings import BASE_DIR

EmailTemplate = namedtuple('EmailTemplate', 'template_id, content, subject')


def load_json_file(filename: str):
    """Load from json file in this directory"""
    with open(os.path.join(BASE_DIR, "appel_crises", "data", filename)) as f:
        return json.load(f)


def load_json_dir(dirname: str):
    """Return an iterable of loaded content in this directory."""
    result = []
    for filename in glob.glob(os.path.join(dirname, '*.json')):
        with open(filename) as f:
            result.append(json.load(f))

    return result


def load_email_templates() -> List[EmailTemplate]:
    """Load the email templates"""
    path = os.path.join(BASE_DIR, "appel_crises", "data", "messages")

    return [EmailTemplate(**d) for d in load_json_dir(path)]


DISTRICT_TO_MP: Dict[str, Tuple[str, str, str, str]] = load_json_file(
    "district_to_mp.json"
)

POSTAL_CODE_TO_DISTRICT: Dict[str, List[str]] = load_json_file(
    "postal_code_to_district.json"
)

EMAIL_TEMPLATES: List[EmailTemplate] = load_email_templates()
