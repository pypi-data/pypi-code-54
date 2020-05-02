# csvutil.py - CSV Utilities for nccsv
import csv


class CSVData():
    def __init__(self, filename=None):
        if filename:
            if not filename.endswith(".csv"):
                filename += ".csv"
        self.filename = filename
        self.data = None
    # init

    def update_data(self, data):
        self.data = data
    # update_data

    def load(self):
        data_tmp = []
        with open(self.filename, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            for row in reader:
                data_tmp.append(row)
        self.data = data_tmp
        return data_tmp
    # load

    def save(self):
        with open(self.filename, "w") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"')
            writer.writerows(self.data)
    # save
# CSVData
