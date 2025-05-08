#!/usr/bin/env python3
import os
import zipfile
import shutil
import subprocess
import sys

KEEP_BACKUP_ON_SUCCESS = True
BACKUP_SUFFIX = ".backup"

METADATA_WHITELIST = ("<metadata name=\"Application\"", "<metadata name=\"BambuStudio:3mfVersion\"")

def process_3mf(filename):
    backup = filename + BACKUP_SUFFIX
    if os.path.exists(backup):
        raise RuntimeError("backup exists: " + backup)
    shutil.copy(filename, backup)

    remove = []
    lines = None
    model_filename = "3D/3dmodel.model"
    with zipfile.ZipFile(filename) as zip:
        for x in zip.namelist():
            if x.startswith("Auxiliaries/"):
                remove.append(x)
        try:
            model = zip.open(model_filename)
        except KeyError:
            pass
        else:
            with model:
                lines = model.readlines()
            lines = [x.decode("utf-8") for x in lines]
            def is_kept_line(line):
                line = line.lstrip()
                if not line.startswith("<metadata"):
                    return True
                if any(line.startswith(x) for x in METADATA_WHITELIST):
                    return True
                return False
            lines = filter(is_kept_line, lines)
            lines = "".join(lines).encode("utf-8")
            remove.append(model_filename)

    if remove:
        subprocess.run(["zip", "--delete", "--no-wild", "--quiet", filename] + remove, check=True)

    if lines:
        with zipfile.ZipFile(filename, mode="a", compression=zipfile.ZIP_DEFLATED) as zip:
            zip.writestr(model_filename, lines)

    if not KEEP_BACKUP_ON_SUCCESS:
        os.remove(backup)

if __name__ == "__main__":
    for x in sys.argv[1:]:
        if x.endswith(".3mf"):
            process_3mf(x)
        else:
            sys.exit("unrecognized file: " + x)
