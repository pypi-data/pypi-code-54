import cv2
import time
from datetime import datetime
import threading
from concurrent.futures import Future
import pandas as pd


class Detect:
    cam_names_dict = {}

    def __init__(self):
        self.cam_names_dict = {}
        path = "data\\csv\\img_taken_per_day.csv"
        self.df = pd.read_csv(path, index=False)
        self.cam_names_dict = {}

    def setup(self, cam_location_names):
        count = 0
        cam_location_names = cam_location_names
        for location in cam_location_names:
            count = str(count)
            globals()["Cam"+count] = cv2.VideoCapture(count, cv2.CAP_DSHOW)
            self.cam_names_dict["Cam"+count] = location
            count = int(count)
            count += 1

    def begin_scan(self, fps):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        facecascade = cv2.CascadeClassifier("cascade/haarcascade_frontalface_default.xml")
        len_of_cam_names_dict = len(self.cam_names_dict)

        while True:
            for i in range(0, len_of_cam_names_dict):
                i = str(i)
                cam = globals()["Cam" + i]
                ret, img = cam.read()
                minw = 0.1 * cam.get(3)
                minh = 0.1 * cam.get(4)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = facecascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minw), int(minh)),
                )

                for (x, y, w, h) in faces:
                    time_of_capture = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cv2.imwrite(
                        "data/detected_faces/" + "Cam" + i + "/" + time_of_capture + ".jpg",
                        gray[y:y + h, x:x + w]
                    )
                    yield "Face detected at " + self.cam_names_dict[
                        "Cam" + i] + "camera on " + time_of_capture + "."

                    row_num = 0
                    for row in self.df.iterrows():
                        row_num = row
                    row_num += 1

                    self.df.at[row_num, 0] = time_of_capture
                    self.df.at[row_num, 0] = time_of_capture
                    path = "data\\csv\\img_taken_per_day.csv"
                    with open(path, 'w') as f:
                        self.df.to_csv(f, header=False)

                time.sleep(fps)
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break

    def call_with_future(self, fn, future, args, kwargs):
        try:
            result = fn(*args, **kwargs)
            future.set_result(result)
        except Exception as exc:
            future.set_exception(exc)

    def threaded(self, fn):
        def wrapper(*args, **kwargs):
            future = Future()
            threading.Thread(target=self.call_with_future, args=(fn, future, args, kwargs)).start()
            return future
        return wrapper

    def interleaving_thread_scan(self, fps, list_cam_num):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        facecascade = cv2.CascadeClassifier("cascade/haarcascade_frontalface_default.xml")
        if not list_cam_num:
            list_cam_num = self.cam_names_dict.keys()

        @self.threaded
        def interleaving_thread_scan_begin(cam_num):
            yield "Begun scanning for Cam" + cam_num
            while True:
                cam = globals()["Cam"+cam_num]
                ret, img = cam.read()
                minw = 0.1 * cam.get(3)
                minh = 0.1 * cam.get(4)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = facecascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minw), int(minh)),
                )

                for (x, y, w, h) in faces:
                    time_of_capture = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cv2.imwrite(
                        "data/detected_faces/" + time_of_capture + "/" + cam_num + ".jpg",
                        gray[y:y + h, x:x + w]
                    )
                    yield "Face detected at " + \
                          self.cam_names_dict["Cam"+cam_num] + "camera on " + time_of_capture + "."

                    row_num = 0
                    for row in self.df.iterrows():
                        row_num = row
                    row_num += 1

                    self.df.at[row_num, 0] = time_of_capture
                    self.df.at[row_num, 0] = time_of_capture
                    path = "data\\csv\\img_taken_per_day.csv"
                    with open(path, 'w') as f:
                        self.df.to_csv(f, header=False)
                time.sleep(fps)

            scanner_list = []
            for i in list_cam_num:
                globals()["Scanner" + i] = interleaving_thread_scan_begin(i)
                scanner_list.append(globals()["Scanner" + i])

            while True:
                for scanner in scanner_list:
                    if not scanner:
                        pass
                    else:
                        yield scanner
