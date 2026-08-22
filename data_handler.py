
from json import dump, load


def writeData(data, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        dump(data, f, indent=2)

def readData(file_path: str):
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
                return load(f)
    except FileNotFoundError:
        return {}
