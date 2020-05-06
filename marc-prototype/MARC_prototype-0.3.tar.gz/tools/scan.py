from .package_tools.datahandler import Data
from .package_tools.facialhandler import Face


class Scan:

    def __init__(self, ):
        self.idnum = 0
        self.datahandler = Data()

    def scan(self):

        face_handler = Face()

        self.idnum, confidence = face_handler.predict()

        if not face_handler.predict():
            yield "Failed to detect face"

        output_details = self.datahandler.get_user_details(self.idnum)
        yield "Returning details."
        yield output_details, confidence

    def pin_location(self, cur_loc):
        yield "Adding " + cur_loc + " to data."
        self.datahandler.write_current_location(self.idnum, cur_loc)
        yield "Added."
