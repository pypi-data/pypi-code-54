"""Local test cases for client.py"""

from os import remove
from os.path import dirname

from mfiles.client import MFilesClient

DIR = dirname(__file__)
TEST_FILE_NAME = "mfiles_api_test_file.txt"

def test_upload():
    """Upload a file."""
    client = MFilesClient(server="https://doc.climeon.com/REST/",
                          vault="{15A2F1B9-78D6-402C-8F15-E800CAC3FCC4}")
    with open(TEST_FILE_NAME, mode="w+") as file_stream:
        file_stream.write("Automatic test of M-Files API")
    document_info = {
        "Document Type": "Report",
        "Document Title": TEST_FILE_NAME[:-4],
        "Distribution": "2.Restricted",
        "Workflow": "General doc workflow"
    }
    upload_info = client.upload_file(TEST_FILE_NAME, object_type="Document",
                                     object_class="General Document",
                                     extra_info=document_info)
    remove(TEST_FILE_NAME)
    assert TEST_FILE_NAME in upload_info["Files"][0]["EscapedName"]
