from tinydb import TinyDB, where, Query
from datetime import datetime
from cryptography.fernet import Fernet
import os


class Data:
    def __init__(self):
        cur_path = os.path.dirname(__file__)
#        path_to_database = os.path.relpath("data/csv/database.json", cur_path)
#        self.db = TinyDB(path_to_database)

        path_to_totals = os.path.relpath("data/csv/totals.json", cur_path)
        self.db_totals = TinyDB(path_to_totals)

    def get_idnum(self):
        idnum = len(self.db) + 1  # Total users + current user, since current user isn't part of db yet
        return idnum

    def write_user_details(self, details):
        idnum = self.get_idnum()
        self.db.insert({"ID": idnum, "First Name": details[0], "Middle Name": details[1], "Last Name": details[2],
                        "Nationality": details[3], "Gender": details[4], "Age": details[5], "Locations": "Init"})

        total_type = Query()
        total_added = self.db_totals.search(where("Total Added"))
        self.db_totals.update({"Total Added": total_added}, total_type == "Total Added")

    def get_user_details(self, idnum):
        output_details_dict = self.db.search(where("ID") == idnum)
        output_details_list = output_details_dict.values()
        output_details_list.drop([0])
        return output_details_list

    def write_current_location(self, idnum, cur_loc):
        prev_data_dict = self.db.search(where("ID") == idnum)
        prev_data = prev_data_dict.get("Locations")

        time_of_capture = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_value = prev_data + "; " + time_of_capture + " " + cur_loc
        self.db.update({"Locations": new_value}, where("ID") == idnum)
        total_type = Query()
        total_scanned = self.db_totals.search(where("Total Scanned"))
        self.db_totals.update({"Total Scanned": total_scanned}, total_type == "Total Scanned")

    def get_totals(self):
        totals_list = self.db_totals.all()
        return totals_list

    def decrypt(self):
        file = open("key.key", 'rb')
        key = file.read()
        file.close()

        with open("../data/csv/database.json", 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        with open('../data/csv/database.json', 'wb') as f:
            f.write(decrypted)

    def encrypt(self):
        file = open("key.key", 'rb')
        key = file.read()
        file.close()

        with open("../data/csv/database.json", 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open('../data/csv/database.json', 'wb') as f:
            f.write(encrypted)
