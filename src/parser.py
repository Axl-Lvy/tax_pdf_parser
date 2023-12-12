"""
Parser class file. This is where you can find all the logic of the app, including:
- Pdf reader.
- Text parser.
- Multithreading
"""

import os
import multiprocessing as mp
import fitz
from os import path
import shutil
from threading import Thread
import tkinter as tk
from src.parameters import cores_number


class Parser:
    def __init__(self, chosen_type: str, app: tk.Tk):
        """
        Constructor.


        :param self: Represents the instance of the object itself.
        :param chosen_type: str: Chosen type of file.
        :return: Nothing.
        """
        self.chosen_type = chosen_type
        self.folder = "./"
        self.last_starting_thread = 0
        self.threads = []
        self.app = app
        self.threads_life = []

    def monitor(self, thread_index: int, app: tk.Tk):
        if self.threads[thread_index].is_alive():
            # check the thread every 100ms
            app.after(100, lambda: self.monitor(thread_index, app))
        else:
            print(thread_index)
            self.threads_life[thread_index] = False
            if self.last_starting_thread < len(self.threads) - 1:
                self.last_starting_thread += 1
                self.threads[self.last_starting_thread].start()
                self.monitor(self.last_starting_thread, app)

    def start(self):
        """
        The start function parses all the pdf files in self.folder.
        It uses multiprocessing to speed up the parsing process.

        :param self: Refer to the object itself.
        :return: Nothing.
        """
        if True in self.threads_life:
            print("Already running !")
            return
        files_list = filter(lambda x: x.endswith(".pdf"), os.listdir(self.folder))
        self.threads = [AsyncParser(file_name, self.folder, self.chosen_type) for file_name in files_list]
        self.threads_life = [True for _ in self.threads]

        if cores_number == -1:
            t_max = mp.cpu_count()
        else:
            t_max = max(cores_number, mp.cpu_count())
        for i in range(min(len(self.threads), t_max)):
            self.threads[i].start()
            self.monitor(i, self.app)
            self.last_starting_thread = i
        return


class AsyncParser(Thread):
    def __init__(self, file_name: str, folder: str, chosen_type: str):
        super().__init__()
        self.file_name = file_name
        self.folder = folder
        self.chosen_type = chosen_type

    def run(self) -> None:
        """
        The run parses the PDF document into text.
        It then looks for the identification number.
        The original PDF is moved to folder named by the identification number.

        :param self: Represent the instance of the class.
        :return: Nothing.
        """
        # try:
        # Parse the pdf
        pdf_path = os.path.join(self.folder, self.file_name)
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()
        pdf_document.close()  # It is important to close the pdf before moving it

        # Look for the identification number
        next_line_important = False
        identification_number = ""
        for line in text.splitlines():
            compact_line = line.replace("  ", "").replace(" ", "").lower()
            if next_line_important and len(compact_line) == 13:
                identification_number = compact_line
                break
            elif compact_line.startswith("identifiant:"):
                identification_number = compact_line[12:]
                break
            else:
                next_line_important = compact_line in ["numérofiscal:", "numerofiscal:"]
        if identification_number == "":
            new_path = path.join("generated_data", "not_found", self.chosen_type)
        else:
            new_path = path.join("generated_data", identification_number, self.chosen_type)

        # Move the pdf
        try:
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        except Exception as e:
            print(e)
        shutil.copy(pdf_path, os.path.join(new_path, self.file_name))
        if identification_number == "":
            with open(path.join(new_path, self.file_name.replace(".pdf", ".txt")),
                      "w+",
                      encoding="utf-8") as text_file:
                text_file.write(text)
