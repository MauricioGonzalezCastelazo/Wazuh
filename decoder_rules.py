from API import API

class Decoder: 
    def __init__(self): 
        self.api = API("192.168.0.158")

    def read_log(self, txt): 
        pass

    def generate_decoder(self): 
        pass

    def addDecoder(self, type = "decoders", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def updateDecoder(self, type = "decoders", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

class Rule: 
    def __init__(self): 
        pass

    def create_rule(self): 
        pass

    def addRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def updateRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

