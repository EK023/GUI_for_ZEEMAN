import json
import configparser

class ConfigReader:
    def __init__(self, config_path):
        self.config_path = config_path

    def merge_ranges(self, ranges):
        if not ranges:
            return []

        merged = []
        print( ranges[0], "first")
        current_min, current_max = ranges[0]

        for min_val, max_val in ranges[1:]:
            if min_val == current_max:
                # extend current range
                current_max = max_val
            else:
                merged.append([current_min, current_max])
                current_min, current_max = min_val, max_val

        merged.append([current_min, current_max])
        return merged
    
    def merge_element_data(self, elements, iterset):
        return [
            [el, est, fit, int(el in iterset)]
            for el, est, fit in elements
        ]

    def read(self):
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes="#")
        config.read(self.config_path)
        params = config["Params"]
        data = {}

        for key in params:
            # print(f"RAW VALUE: '{key}'", params)
            value = json.loads(params[key]) if params[key] else []
            data[key.split(",")[0]] = value

        iterset = set( data["iterlist"][0]) if data["iterlist"] else set()
        # print(data["contpoly"], int("contpoly" in iterset))
        # data["contpoly"] = [data["contpoly"], int("contpoly" in iterset)] # add the contpoly checkbox status from iterlist

        # transform data to the style it needs to be for the ui classes
        data['wave_range_lists'] = self.merge_ranges(data['wave_range_lists'])
        data["elements"] = self.merge_element_data(data["elements"],iterset)
        return data