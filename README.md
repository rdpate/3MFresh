# 3MFresh 🧼✨
*A lightweight Python script to clean `.3MF` files by removing unnecessary metadata and other data. This is designed primarily for Bambu Studio users but may be useful for other purposes.*

## 🔍 Why Use 3MFresh?
When downloading `.3MF` print profiles from **MakerWorld** or other sources, they often contain **metadata** that ties them to their original creator, model description, images, and other details.

This metadata can **persist even after modifying the file**, leading to confusion when using the profile for new prints. For example:
- A `.3MF` file may contain **optimized print settings for a specific filament**, but also **metadata** about the original model.
- If you **repurpose the print profile** by adding your own models, the **original metadata remains**—meaning the printer history and slicer still display **the old model's information**, rather than your custom project.

## 🚀 Features
- **Removes unnecessary `<metadata>` entries**, such as the original model name, creator, description, and images.
- **Keeps essential metadata**:
  - `<metadata name="Application">` *(e.g., "BambuStudio-01.10.02.76")*
  - `<metadata name="BambuStudio:3mfVersion">` *(e.g., version number)*
- **Deletes the `Auxiliaries` directory** (if present), which may contain thumbnails or extra data about the original project.
- **Preserves the `.3MF` file’s internal structure**, ensuring full compatibility with **Bambu Studio** and **Bambu Lab printers**.
- **Processes files in bulk** using an `input` directory.

By using **3MFresh**, you can **repurpose high-quality print profiles** without unwanted metadata, ensuring that your printer history and slicer interface accurately reflect **your custom models** rather than that of the original source.

## 📥 Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/brossow/3MFresh.git
   cd 3MFresh
   ```
   *Alternatively, you can download just the .py file and put it in its own directory. The first time you run the script, it will create any missing directories.*

2. **Ensure you have Python 3 installed.**
   Check by running:
   ```bash
   python --version
   ```

3. You're ready to go! No additional dependencies are required.

## 🛠 Usage
1. Place `.3MF` files into the **`input`** directory.
2. Run the script (e.g., using Terminal on a Mac or the command prompt in Windows):
   ```bash
   python process_3mf.py
   ```
3. Cleaned files will be in a timestamped subdirectory in the **`processed`** directory, and original files will be moved to a subdirectory in **`originals`**. This ensures files aren't accidentally overwritten.

## 📌 Notes
- The script **preserves essential metadata** (`Application` and `BambuStudio:3mfVersion`) but **removes all other metadata**.
- The **`Auxiliaries` directory is deleted** if found inside the `.3MF` archive.
- The script has been tested successfully with numerous 3MF files, but it comes with **no guarantees**, **no support**, and **you use it at your own risk**. Always make backups.
- If you encounter problems, open a detailed issue report.

## 🤝 Contributing
Pull requests are welcome! If you’d like to contribute, please **fork** the repository and submit a PR.

## 📝 License
This project is licensed under the MIT License. See `LICENSE` for details.