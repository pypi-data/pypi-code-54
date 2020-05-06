import os
import cv2
import pandas as pd
from .package_tools.datahandler import Data


class Command:
    def __init__(self):
        self.path_to_database = "data/csv/database.json"
        self.path_to_images = "data/detected_faces/"
        self.datahandler = Data()

    def get_cam_data(self, date):
        path = self.path_to_images + date
        list_of_img_names = os.listdir(path)

        for img_name in list_of_img_names:
            path = self.path_to_images + date + "\\" + img_name
            cv2.imshow(img_name, path)

        return len(list_of_img_names)

    def get_totals(self):
        output_details_dict = self.datahandler.get_totals()
        return output_details_dict

"""    def cam_hits_per_day(self, date):
        path = "data/csv/img_taken_per_day.csv"
        df = pd.read_csv(path, index=False)
        cam_hits = df.iloc[[date]]
        output_details = cam_hits.values.tolist()
        return output_details""" # Under development
