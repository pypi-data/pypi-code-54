
import json
import sys

class CreateDashboard():

    options = {
        "apexchart": {
            "axies": "",
            "series": [],
            "options": "",
        }
    }

    data = []
    
    def add(self, name, data):
        """
            If exists in data merge data
        """
        if name in self.options:
            data = {** self.options[name], **data}
            self.data.append({name: data})
        else:
            self.data.append({name: data})
        
        return self
    
    def run(self):
        self.writeJsonToFile()

    def getArgFileName(self):
        args = sys.argv
        if len(args) > 1:
            if '--tmp-file' not in args[1]:
                raise Exception("argument --tmp-file not defined")
            split_key = args[1].split("=")

            if len(split_key) < 2:
                raise Exception("argument --tmp-file not defined")
            return split_key[1]
        else:
            raise Exception("argument --tmp-file not defined")

    def writeJsonToFile(self, filename= False):
        """
            Get file name
        """
        if not filename:
            filename = self.getArgFileName()

        """
            Write file json
        """
        with open(filename, 'w') as outfile:
            json.dump(self.data, outfile)

    def dumpJson(self):
        return json.dumps(self.data)

