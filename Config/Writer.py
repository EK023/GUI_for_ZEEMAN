import json
import configparser
from parameters import params, get_key, FORTRAN_MAX_ALLOWED_RANGE, FORTRAN_WINDOW_SIZE

class ConfigWriter:
    def __init__(self, config_path, data):
        self.config_path = config_path
        self.write(data)

    def handle_fit(self,key, value, config):
        try:
            val = float(value.get("value"))
        except (ValueError, TypeError):
            val = 0
        enabled = int(value.get("enabled"))
        config["Params"][f"{key},fit{key}"] = json.dumps([val, enabled])

    def handle_string(self, key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(value)

    def handle_bool(self,key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(int(value.get("enabled")))

    def handle_iterlist(self, key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(value)

    def handle_int(self,key, value, config):
        try:
            val = int(round(float(value.get("value"))))
        except (ValueError, TypeError):
            val = 0
        config["Params"][key.replace(" ", "_")] = json.dumps(val)

    def handle_range(self, value, wave_range_lists):

        for wave_range in value:
            wave_ranges = []
            for min_val, max_val in wave_range:
                while max_val - min_val > FORTRAN_MAX_ALLOWED_RANGE:
                        new_max = min_val + FORTRAN_MAX_ALLOWED_RANGE
                        wave_ranges.append([min_val, new_max])
                        min_val = new_max
                wave_ranges.append([min_val, max_val])
            wave_ranges = sorted(wave_ranges, key=lambda x: x[0])
            for i in range(0, len(wave_ranges), FORTRAN_MAX_ALLOWED_RANGE):
                wave_range_lists.append(wave_ranges[i:i+FORTRAN_WINDOW_SIZE])

    def handle_elements(self, dict, elements):
        for value in dict:
            el = value.get("element")
            est = float(value.get("estimate"))
            fit = int(value.get("fit"))
            elements.append([el, est, fit])

    def write(self, data):
        elements = []
        wave_range_lists = []

        SAVE_HANDLERS = {
            "fit": self.handle_fit,
            "bool": self.handle_bool,
            "int": self.handle_int,
            "file": self.handle_string,
            "choice": self.handle_string,
            "hiddenFile": self.handle_string,
            "ranges": lambda k, v, c: self.handle_range(v, wave_range_lists),
            "elements": lambda k, v, c: self.handle_elements(v, elements),
            "iterlist": self.handle_iterlist
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
        config["Params"]["wave_range_lists"] = json.dumps(wave_range_lists)

        with open(self.config_path, "w") as f:
            config.write(f)