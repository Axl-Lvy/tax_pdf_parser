# PDF Sorter Application

## How To Build

To build and run this application, from source, you will need python 3.

```bash
# Install dependencies
$ pip install -r requirements.txt

# Run the application: python -m main.py
$ cd electron-markdownify

# Build the application
$ pyinstaller main.py --onefile --name PDFSorter.exe
```

## How To Use

You can find a .exe in [dist](./dist) folder. Just run it, select a file type, then choose the directory where PDFs ae stored.
Finally, press *Start !* only one time, otherwise you will have duplicates.

Please note that this application is using multi threading, and load all available cores by default.

