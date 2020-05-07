import os

# import db
from lib import paths_management as paths
from lib import db

app_paths = paths.App_Paths()
db_path = os.path.join(app_paths.base_script_path, 'web_downloader.db')

curr_db = db.Database(db_path)
curr_db.create_db()