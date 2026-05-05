import json
import os
import configparser
from parameters import FORTRAN_WINDOW_SIZE, params, get_key

class ConfigReader:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ZEEMAN_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "Zeeman"))
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
    
    def resolve_smart_path(self,read_path, anchor_directory):
        """
        Takes a path read from the config file and turns it back into an absolute path
        so the GUI can display and use it properly.
        """
        if not read_path:
            return ""

        # 1. If it's already an absolute path (/home/../...), return it as-is
        if os.path.isabs(read_path):
            return os.path.normpath(read_path)

        # 2. If it's a relative path (inputs/wave.dat), glue it to the anchor directory
        full_path = os.path.join(anchor_directory, read_path)
        
        # 3. Clean up the slashes and return the absolute path
        return os.path.normpath(full_path)

    def merge_element_data(self, elements):
        return [
            [el, est, fit]
            for el, est, fit in elements
        ]

    def read(self):
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes="#")
        config.read(self.config_path)
        conf = config["Params"]
        data = {}
        filePaths = set()
        for meta in params:
            key = get_key(meta)
            if meta["type"] in ["file", "hiddenFile"]:
                filePaths.add(key)
                

        for raw_key, raw_value in conf.items():
            clean_key = raw_key.split(",")[0]
            value = json.loads(raw_value) if raw_value else []
            if clean_key in filePaths:
                value = self.resolve_smart_path(value, self.ZEEMAN_DIR)
            data[clean_key] = value

        # transform data to the style it needs to be for the ui classes
        data['wave_range_lists'] = self.merge_ranges(data['wave_range_lists'])
        data["elements"] = self.merge_element_data(data["elements"])
        return data