import json
import configparser

class ConfigWriter:
    def __init__(self, config_path, data):
        self.config_path = config_path
        self.write(data)

    def handle_fit(self,key, value, config):
        val = float(value.get("value"))
        enabled = value.get("enabled")
        config["Params"][f"{key},fit{key}"] = json.dumps([val, enabled])


    def handle_string(self, key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(value)


    def handle_bool(self,key, value, config):
        config["Params"][key.replace(" ", "_")] = json.dumps(value.get("enabled"))


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

    def write(self, data):
        fits = ["vr", "vsini", "vmic", "vmac", "teff", "logg", "metal"]
        string_keys = ["obsspecpath","mainpath", "vlinespath", "model atm folder"]
        bool_keys = ["save file", "show plot", "read_wave_from_text"]
        int_keys = ["n iter", "contpoly", "res"]
        data["read_wave_from_text"] = data.pop("wave from text")
        handlers = {}

        for k in fits:
            handlers[k] = self.handle_fit

        for k in string_keys:
            handlers[k] = self.handle_string

        for k in bool_keys:
            handlers[k] = self.handle_bool

        for k in int_keys:
            handlers[k] = self.handle_int

        config = configparser.ConfigParser(delimiters=(':'))
        config["Params"] = {}

        wave_ranges = []
        elements = []

        for key, value in data.items():

            if key.startswith("range_"):
                self.handle_range(value, wave_ranges)
                continue

            handler = handlers.get(key)

            if handler:
                handler(key, value, config)

        # sort the elements
        wave_ranges = sorted(wave_ranges, key=lambda x: x[0])
        # elements = sorted(elements, key=lambda x: x[0])
        config["Params"]["wave_range_lists"] = json.dumps(elements)

        with open(self.config_path, "w") as f:
            config.write(f)



    # def write(self, data):
    #     fits = ["vr", "vsini", "vmic", "vmac", "teff", "logg", "metal"]
    #     string_keys = ["obsspecpath","mainpath", "vlinespath", "model atm folder"]
    #     bool_keys = ["save file", "show plot", "read_wave_from_text"]
    #     int_keys = ["n iter", "contpoly", "res"]
    #     data["read_wave_from_text"] = data.pop("wave from text") 

    #     config = configparser.ConfigParser(delimiters=(':'))

    #     config['Params'] = {}
    #     elements = []
    #     for key, value in data.items():
    #         if key in fits:
    #             val = float(value.get("value"))
    #             enabled = value.get("enabled")
    #             config["Params"][f"{key},fit{key}"] = json.dumps([val, enabled])
    #         elif key == "elements":
    #             config["Params"]["elements"] = json.dumps(value)
    #         elif key in string_keys:
    #             config["Params"][key] = json.dumps(value)
    #         elif key in bool_keys:
    #             config["Params"][key.replace(" ", "_")] = json.dumps(value.get("enabled"))
    #         elif key in int_keys:
    #             val = int(round(float(value.get("value"))))
    #             config["Params"][key.replace(" ", "_")] = json.dumps(val)
    #         elif key.startswith("range_"):
    #             min_val = float(data[key].get("min"))
    #             max_val = float(data[key].get("max"))
    #             if max_val - min_val > 200:
    #                 newMax = min_val + 200
    #                 while newMax < max_val:
    #                     elements.append([min_val, newMax])
    #                     min_val = newMax
    #                     newMax = min_val + 200
    #                 elements.append([min_val, max_val])
    #             else:
    #                 elements.append([min_val, max_val])

    #     # sort the elements
    #     elements = sorted(elements, key=lambda x: x[0])
    #     config["Params"]["elements"] = json.dumps([elements]) # Check if the extra [] are needed
    #     with open(self.config_path, 'w') as f:
    #         config.write(f)