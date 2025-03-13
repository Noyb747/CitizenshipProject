import json
import os

def readdir(dir_structure, base_path="."):
    for name, content in dir_structure.items():
        current_path = os.path.join(base_path, name)
        if isinstance(content, str):
            with open(current_path, "wb") as wfile:
                wfile.write(bytes.fromhex(content))
        elif isinstance(content, dict):
            os.makedirs(current_path, exist_ok=True)
            readdir(content, base_path=current_path)

def savef(path):
    if os.path.isfile(path):
        with open(path, "rb") as file:
            return file.read().hex()
    elif os.path.isdir(path):
        directory_content = {}
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            directory_content[entry] = savef(full_path)
        return directory_content
    else:
        raise ValueError(f"Unsupported file type: {path}")

def savef2(path):
    base_name = os.path.basename(path.rstrip(os.sep))
    return {base_name: savef(path)}

filen = input("f > ").strip()
mode = input("d/e > ").strip().lower()

if mode == "d":
    with open(filen, "r") as file:
        dir_structure = json.load(file)
    readdir(dir_structure)
elif mode == "e":
    dir_structure = savef2(filen)
    output_file = filen + ".zipped"
    with open(output_file, "w") as file:
        json.dump(dir_structure, file)
