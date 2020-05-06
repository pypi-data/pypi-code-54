import cv2
import os
import numpy as np
from PIL import Image
import pylevenshtein as pylev
from .package_tools.datahandler import Data


class Add:
    """
    Class to deal with new users.
    """

    nationality = ""
    first_name = ""
    middle_name = ""
    last_name = ""
    gender = ""
    age = 0
    lev = 0
    confidence = 0
    details = []
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    def __init__(self):
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.nationality = ""
        self.gender = ""
        self.age = 0
        self.lev = 0
        self.confidence = 0
        self.details = []
        self.travelled = False
        self.current_location = ""
        self.load_done = False
        self.flush_done = False
        self.check_done = False

        self.datahandler = Data()

    def load(self, details, cur_loc):
        """
        Loads data and sets values within the class.

        Parameters
        ----------
        details : list
            A list of details of the user.
        cur_loc : Current Location
            Written in [Airport Name], [Country]
        """
        if self.flush_done:
            self.first_name = details[0]
            self.middle_name = details[1]
            self.last_name = details[2]
            self.nationality = details[3]
            self.gender = details[4]
            self.age = details[5]
            self.travelled = details[6]
            self.current_location = cur_loc
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.load_done = True

            self.details = details
            self.details.pop()
            return "Loaded."
        else:
            return NotImplementedError("Error: Please Flush First.")

    def check(self):
        """
        Checks if user is in database.
        """
        if not self.load_done:
            raise NotImplementedError("Error: Please Load Details First.")
        else:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("..\\trainer\\trainer.yml")
            cascadepath = "..\\cascade\\haarcascade_frontalface_default.xml"
            facecascade = cv2.CascadeClassifier(cascadepath)

            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cam.set(3, 640)
            cam.set(4, 480)

            minw = 0.1 * cam.get(3)
            minh = 0.1 * cam.get(4)

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = facecascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minw), int(minh)),
            )

            confidence = 0

            yield "Taking picture. Stand in front of camera."

            face_detected = False

            idnum = 0
            while True:
                if face_detected:
                    yield "Face detected."
                    break
                else:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        idnum, self.confidence = recognizer.predict(gray[y:y + h, x:x + w])
                        self.confidence = round(100 - confidence)
                        face_detected = True
            output_details = self.datahandler.get_user_details(idnum)

            if output_details[1] is None:
                output_name = output_details[0] + " " + output_details[2]
            else:
                output_name = output_details[0] + " " + output_details[1] + "" + output_details[2]
            if self.middle_name is None:
                input_name = self.first_name + " " + self.last_name
            else:
                input_name = self.first_name + " " + self.middle_name + " " + self.last_name

            lev = pylev.levenshtein.distc(output_name, input_name)
            return_output = [idnum, self.confidence, output_details, lev]

            yield "Face identified."
            return return_output

    def user_add(self):
        """
        Adds user to database.
        """
        if self.load_done:
            camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            camera.set(3, 640)
            camera.set(4, 480)
            face_detector = cv2.CascadeClassifier('..\\cascade\\haarcascade_frontalface_default.xml')
            count = 0
            new_id = int(self.datahandler.get_idnum())
            self.details.append(new_id)
            self.datahandler.write_user_details(self.details)

            while True:
                ret, img = camera.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    count += 1
                    cv2.imwrite("..\\data\\images\\" + self.nationality + "\\User." + str(new_id) + '.' + str(count) +
                                ".jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('image', img)
                    output = str(count) + " pictures taken."
                    yield output
                if count >= 40:
                    break

            camera.release()
            cv2.destroyAllWindows()

            yield "Added " + self.first_name + " to the database. Train model."

        else:
            raise NotImplementedError("Error: Please Load Details First.")

    def getimagesandlabels(self, path):
        """
        System function. No calling.
        """
        imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
        facesamples = []
        idnum = 0
        ids = []
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        for imagePath in imagepaths:
            pil_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(pil_img, 'uint8')
            idnum = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                facesamples.append(img_numpy[y:y + h, x:x + w])
        ids.append(idnum)
        return facesamples, ids

    def train(self):
        """
        Trains yml model.
        """
        if not self.load_done:
            raise NotImplementedError("Error: Please Load Details First.")
        else:
            path = self.nationality
            faces, ids = self.getimagesandlabels(path)
            self.recognizer.train(faces, np.array(ids))
            self.recognizer.write('trainer/trainer.yml')

    def flush(self):
        self.nationality = ""
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.gender = ""
        self.age = 0
        self.lev = 0
        self.confidence = 0
        self.details = []
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.travelled = "No"

        self.flush_done = True
        self.load_done = False
        self.check_done = False
