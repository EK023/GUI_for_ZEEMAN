
params = [
        {"display": "res", "type": "int"},
        {"display": "vr", "type": "fit"},
        {"display": "vsini", "type": "fit"},
        {"display": "vmic", "type": "fit"},
        {"display": "vmac", "type": "fit"},
        {"display": "teff", "type": "fit"},
        {"display": "logg", "type": "fit"},
        {"display": "metal", "type": "fit"},
        {"display": "contpoly", "type": "int"},
        {"display": "n iter", "type": "int"},
        {"display": "save file", "type": "bool", "key": "savefile"}, # would be really nice to move to save_file and show_plot
        {"display": "show plot", "type": "bool", "key": "showplot"},
        {"display": "run format", "type": "choice", "options": ["fit","syn"]},
        {"display": "wave from text", "type": "bool", "key": "read_wave_from_text"},
        {"display": "mainpath", "type": "file", "folder": True},
        {"display": "vlinespath", "type": "file"},
        {"display": "model atm folder", "type": "file", "folder": True},
        {"display": "model atm file", "type": "file"},
        # they aren't actually displayed as ones before, more for the data handling when saving and loading data.
        {"display": "iterlist", "type": "iterlist"},
        {"display": "ranges", "type": "ranges"}, 
        {"display": "elements", "type": "elements"}, 
        {"display": "obsspecpath", "type": "hiddenFile"}

    ]

# Fortran array size and window size limits, used for splitting large ranges into smaller chunks for the Fortran code to handle. Adjust as needed based on your Fortran code's requirements.
FORTRAN_MAX_ALLOWED_RANGE = 200
FORTRAN_WINDOW_SIZE = 10

def get_key(row):
    return row.get("key", row["display"].replace(" ", "_"))

