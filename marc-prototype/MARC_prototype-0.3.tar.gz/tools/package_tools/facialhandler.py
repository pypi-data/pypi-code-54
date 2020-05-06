import cv2.cv2


class Face:
    def __init__(self):
        pass

    def detect(self):
        cascadepath = "..\\..\\cascade\\haarcascade_frontalface_default.xml"
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
        for (x, y, w, h) in faces:
            return gray[y:y + h, x:x + w]

    def predict(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("..\\..\\trainer\\trainer.yml")

        idnum, confidence = recognizer.predict(self.detect())
        confidence = round(100-confidence)
        return idnum, confidence
