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

    def handle_range(self, value, wave_ranges):
        min_val = float(value.get("min"))
        max_val = float(value.get("max"))
        while max_val - min_val > 200:
                new_max = min_val + 200
                wave_ranges.append([min_val, new_max])
                min_val = new_max

        wave_ranges.append([min_val, max_val])

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
        handlers = {}
        elements = []
        iterlist = []

        for meta in params:
            key = get_key(meta)
            t = meta["type"]
            match t:
                case "fit":
                    handlers[key] = self.handle_fit
                case "file" | "choice":
                    handlers[key] = self.handle_string
                case "bool":
                    handlers[key] = self.handle_bool
                case "int" | "contpoly":
                    handlers[key] = self.handle_int
            
        handlers["elements"] = lambda key, value, config: self.handle_elements(value, elements, iterlist)
        handlers["obsspecpath"] = self.handle_string
        config = configparser.ConfigParser(delimiters=(':'))
        config["Params"] = {}

        wave_ranges = []
        

        for key, value in data.items():
            if key.startswith("range_"):
                self.handle_range(value, wave_ranges)
                continue

            handler = handlers.get(key)

            if handler:
                handler(key, value, config)

        # sort the elements
        wave_ranges = sorted(wave_ranges, key=lambda x: x[0])
        config["Params"]["elements"] = json.dumps(elements)
        config["Params"]["iterlist"] = json.dumps([iterlist])
        config["Params"]["wave_range_lists"] = json.dumps(wave_ranges)
        

        with open(self.config_path, "w") as f:
            config.write(f)