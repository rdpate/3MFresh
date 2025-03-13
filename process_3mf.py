import os
import zipfile
import shutil
from datetime import datetime

# Set up directories
BASE_DIR = os.getcwd()
INPUT_DIR = os.path.join(BASE_DIR, "input")
PROCESSED_BASE_DIR = os.path.join(BASE_DIR, "processed")
ORIGINALS_BASE_DIR = os.path.join(BASE_DIR, "originals")

# Generate timestamped subdirectories
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
PROCESSED_DIR = os.path.join(PROCESSED_BASE_DIR, timestamp)
ORIGINALS_DIR = os.path.join(ORIGINALS_BASE_DIR, timestamp)

# Ensure all required directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ORIGINALS_DIR, exist_ok=True)

# Metadata elements to retain (matches any content inside)
METADATA_WHITELIST = ("<metadata name=\"Application\"", "<metadata name=\"BambuStudio:3mfVersion\"")

# Process each 3MF file in the input directory
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".3mf"):
        print(f"Processing: {filename}")

        filepath = os.path.join(INPUT_DIR, filename)
        processed_3mf_path = os.path.join(PROCESSED_DIR, filename)

        # Temporary directory for extraction
        temp_dir = os.path.join(BASE_DIR, "temp_extracted")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        # Extract 3MF (ZIP) contents
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Remove 'Auxiliaries' directory if present
        aux_dir = os.path.join(temp_dir, "Auxiliaries")
        if os.path.exists(aux_dir):
            shutil.rmtree(aux_dir)
            print("Removed Auxiliaries directory.")

        # Modify '3D/3dmodel.model' to remove metadata
        model_file = os.path.join(temp_dir, "3D", "3dmodel.model")
        if os.path.exists(model_file):
            with open(model_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Remove metadata lines EXCEPT those in the whitelist
            new_lines = [
                line for line in lines
                if not (line.lstrip().startswith("<metadata") and not any(line.lstrip().startswith(w) for w in METADATA_WHITELIST))
            ]

            # Save the modified file
            with open(model_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            print(f"Removed metadata entries (except whitelisted) from {filename}.")

        # Repackage everything back into a new .3MF file
        with zipfile.ZipFile(processed_3mf_path, "w", zipfile.ZIP_DEFLATED) as new_zip:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, temp_dir)  # Preserve structure
                    new_zip.write(file_path, archive_name)

        # Move the original .3MF file to the 'originals' directory
        shutil.move(filepath, os.path.join(ORIGINALS_DIR, filename))
        print(f"Processed file saved: {processed_3mf_path}")

        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

print("Batch processing complete!")
