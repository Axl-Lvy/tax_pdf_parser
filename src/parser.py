import os
from multiprocessing import Pool, cpu_count
import fitz
from os import path
import shutil
from typing import Sequence


class Parser:
    def __init__(self, chosen_type: str):
        """
        Constructor.


        :param self: Represents the instance of the object itself
        :param chosen_type: str: Chosen type of file
        :return: Nothing
        """
        self.chosen_type = chosen_type
        self.folder = "./"

    def parse_file(self, file_name):
        """
        The parse_file function takes a file name as an argument and parses the PDF document into text.
        It then looks for the identification number.
        The original PDF is moved to folder named by the identification number.

        :param self: Represent the instance of the class
        :param file_name: Specify the name of the file to be parsed
        :return: Nothing
        :doc-author: Trelent
        """
        try:
            # Parse the pdf
            pdf_path = path.join(self.folder, file_name)
            pdf_document = fitz.open(pdf_path)
            text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()
            pdf_document.close()  # It is important to close the pdf before moving it

            # Look for the identification number
            with open(path.join(self.folder, file_name.replace(".pdf", ".txt")), "w+", encoding="utf-8") as text_file:
                text_file.write(text)
            new_path = path.join(self.folder, "1")

            # Move the pdf
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            shutil.move(pdf_path, os.path.join(new_path, file_name))
            shutil.move(os.path.join(new_path, file_name), pdf_path)

        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        files_list = filter(lambda x: x.endswith(".pdf"), os.listdir(self.folder))
        with Pool(processes=cpu_count()) as pool:
            pool.map(self.parse_file, files_list)
        return
