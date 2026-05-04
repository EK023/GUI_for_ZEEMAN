import json
import configparser
from parameters import FORTRAN_WINDOW_SIZE

class ConfigReader:
    def __init__(self, config_path):
        self.config_path = config_path
    """
    First try to put together ranges that should belong to one page and then later merge the ones that are continuous.
    """
    def merge_ranges(self, raw_blocks):
        if not raw_blocks:
            return []

        if isinstance(raw_blocks[0][0], (float, int)): 
            raw_blocks = [raw_blocks]

        gui_pages_raw = []
        current_page_raw = []
        last_raw_block_len = 0

        for block in raw_blocks:
            if not block:
                continue

            is_continuation = False
            block = sorted(block, key=lambda x: x[0])
            if current_page_raw and last_raw_block_len == FORTRAN_WINDOW_SIZE:
                last_val = current_page_raw[-1][1]
                first_val = block[0][0]
                if first_val >= last_val:
                    is_continuation = True
            
            if is_continuation:
                current_page_raw.extend(block)
            else:
                if current_page_raw:
                    gui_pages_raw.append(current_page_raw)
                current_page_raw = list(block)
                
            last_raw_block_len = len(block)
            
        if current_page_raw:
            gui_pages_raw.append(current_page_raw)

        final_pages = []
        for page in gui_pages_raw:
            merged_page = []
            current_min, current_max = page[0]
            
            for min_val, max_val in page[1:]:
                if abs(min_val - current_max) < 1e-6:
                    current_max = max_val
                else:
                    merged_page.append([current_min, current_max])
                    current_min, current_max = min_val, max_val
                    
            merged_page.append([current_min, current_max])
            final_pages.append(merged_page)
            
        return final_pages

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
            value = json.loads(params[key]) if params[key] else []
            data[key.split(",")[0]] = value

        iterset = set( data["iterlist"][0]) if data["iterlist"] else set()
        # print(data["contpoly"], int("contpoly" in iterset))
        # data["contpoly"] = [data["contpoly"], int("contpoly" in iterset)] # add the contpoly checkbox status from iterlist

        # transform data to the style it needs to be for the ui classes
        data['wave_range_lists'] = self.merge_ranges(data['wave_range_lists'])
        data["elements"] = self.merge_element_data(data["elements"],iterset)
        return data