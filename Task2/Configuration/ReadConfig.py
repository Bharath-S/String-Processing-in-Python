import json

class ParseJson:
    """
    This class reads the configuration file and parses it accordingly.
    """

    def __init__(self, filePath):
        """
        Constructor of the class
        """
        self.jsonFileName = filePath
        self.parsedData = self.parseJson()

    def parseJson(self):
        """
        json parser
        """
        with open(self.jsonFileName) as f_in:
            return json.load(f_in)

    def getDictionaryFile(self):
        """
        Dictionary file
        """
        return self.parsedData["Dictionary"]

    def getInputFile(self):
        """
        Input file containing the matrix
        """
        return self.parsedData["Input_Matrix"]
        
    def getAlgoVersion(self):
        """
        Algorithm Version
        """
        return self.parsedData["Algorithm_Version"]

