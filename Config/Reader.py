import json
import configparser

class ConfigReader:
    def __init__(self, config_path):
        self.config_path = config_path

    def read(self):
        config = configparser.ConfigParser(delimiters=(':'))
        config.read(self.config_path)
        params = config["Params"]
        data = {}

        for key in params:
            value = json.loads(params[key])
            data[key] = value

        return data