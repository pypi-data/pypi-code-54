
import beebird
import pathlib

# imports all tasks in this folder
beebird.importTasks(pathlib.Path(__file__).parent, __name__)