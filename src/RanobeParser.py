from RanobeLibParser import RanobeLibParser
from RanobeHubParser import RanobeHubParser

class RanobeParser:
    def __init__(self, url, begin=0, end=0):
        if str.find(url, "ranobelib") != -1:
            self.parser = RanobeLibParser(url, begin, end)
        elif str.find(url, "ranobehub") != -1:
            self.parser = RanobeHubParser(url, begin, end)
        else:
            raise Exception('Invalid link')

    def set_parsing_callback(self, callback):
        self.parser.set_parsing_callback(callback)

    def parse(self):
        return self.parser.parse()