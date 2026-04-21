import json
import configparser
from parameters import params, get_key

class ConfigWriter:
    def __init__(self, config_path, data):
        self.config_path = config_path
        self.write(data)

    def handle_fit(self,key, value, config):
        val = float(value.get("value"))
        enabled = int(value.get("enabled"))
        config["Params"][f"{key},fit{key}"] = json.dumps([val, enabled])

    def handle_string(self, key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(value)

    def handle_bool(self,key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(int(value.get("enabled")))

    def handle_int(self,key, value, config):
        val = int(round(float(value.get("value"))))
        config["Params"][key.replace(" ", "_")] = json.dumps(val)

    def handle_range(self, value, wave_range_lists):
        wave_ranges = []
        fortran_window_size = 10
        fortran_max_allowed_range = 200
        for min_val, max_val in value:
            while max_val - min_val > fortran_max_allowed_range:
                    new_max = min_val + fortran_max_allowed_range
                    wave_ranges.append([min_val, new_max])
                    min_val = new_max

            wave_ranges.append([min_val, max_val])
        # sort the elements
        wave_ranges = sorted(wave_ranges, key=lambda x: x[0])
        for i in range(0, len(wave_ranges), fortran_window_size):
            wave_range_lists.append(wave_ranges[i:i+fortran_window_size])



    def handle_elements(self, dict, elements, iterlist):
        for value in dict:
            el = value.get("element")
            est = float(value.get("estimate"))
            fit = int(value.get("fit"))
            iter = value.get("iterlist")
            if iter:
                iterlist.append(el)
            elements.append([el, est, fit])

    def write(self, data):
        elements = []
        iterlist = []
        wave_range_lists = []

        SAVE_HANDLERS = {
            "fit": self.handle_fit,
            "bool": self.handle_bool,
            "int": self.handle_int,
            "file": self.handle_string,
            "choice": self.handle_string,
            "hiddenFile": self.handle_string,
            "ranges": lambda k, v, c: self.handle_range(v, wave_range_lists),
            "elements": lambda k, v, c: self.handle_elements(v, elements, iterlist),
        }

        config = configparser.ConfigParser(delimiters=(':'))
        config["Params"] = {}

        for meta in params:
            key = get_key(meta)
            t = meta["type"]
            value = data.get(key)

            handler = SAVE_HANDLERS.get(t)

            if handler and value is not None:
                handler(key, value, config)

        config["Params"]["elements"] = json.dumps(elements)
        config["Params"]["iterlist"] = json.dumps([iterlist])
        config["Params"]["wave_range_lists"] = json.dumps(wave_range_lists)
        

        with open(self.config_path, "w") as f:
            config.write(f)