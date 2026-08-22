import hashlib
import pathlib

from data_handler import readData, writeData


def store_hash(hashDict: dict, hash: str, path: str):
    hashDict[path] = hash
    writeData(hashDict, 'entries.json')


def calculate_hash(file_content: bytes) -> str:
    sha256 = hashlib.sha256()
    sha256.update(file_content)
    s_hash = sha256.hexdigest()
    return s_hash


def extract_bytes(file: pathlib.Path) -> bytes:
    return file.read_bytes()


def main():
    current_hashes = readData('entries.json')
    print("-- File Integrity Monitor --")
    print(f"Tracked files: {len(current_hashes)}")
    opt = input("Options: l-log cwd / rl-recursive-log / c-compare hashes with current / q-quit\nEnter option: ")
    match opt:
        case "l":
            cwd = pathlib.Path.cwd()
            for file in cwd.iterdir():
                if file.is_file():
                    file_bytes = extract_bytes(file)
                    file_hash = calculate_hash(file_bytes)
                    store_hash(current_hashes, file_hash, str(file))
                    print(f"Logged: {file} with hash: {file_hash}")
        case "rl":
            cwd = pathlib.Path.cwd()
            for file in cwd.rglob("*"):
                if file.is_file():
                    file_bytes = extract_bytes(file)
                    file_hash = calculate_hash(file_bytes)
                    store_hash(current_hashes, file_hash, str(file))
                    print(f"Logged: {file} with hash: {file_hash}")
        case "c":
            for path, stored_hash in current_hashes.items():  
                file_path = pathlib.Path(path)
                if file_path.exists():
                    current_hash = calculate_hash(extract_bytes(file_path))
                    if current_hash != stored_hash:
                        print(f"File modified: {path}")
                    else:
                        print(f"File unchanged: {path}")
                else:
                    print(f"File deleted: {path}")
        case "q":
            print("Exiting...")

if __name__ == "__main__":
    main()
