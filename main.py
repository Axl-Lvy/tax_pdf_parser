"""
Main file. Execute from here to run the application.
"""

import customtkinter
from tkinter import filedialog
from src.parser import Parser
from src.parameters import type_choices


def main():
    """
    Main function. Create the app and run the main loop.

    :return:
    """

    customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("400x240")

    parser = Parser("ATD", app)

    def choose_directory():
        """
        The choose_directory function allows the user to select a directory from their computer.
        The function then sets the folder variable in parser to that directory.

        :return: Nothing
        """
        folder = filedialog.askdirectory(initialdir="./",
                                         title="Browse File")
        parser.folder = folder

    def start_analyze():
        """
        Starts analyzing the selected folder.
        :return: Nothing
        """
        parser.start()

    def choose_type(choice):
        """
        Save the type of file selected by the user through the dropdown menu.
        :param choice: str: The type of file to be saved.
        :return: Nothing.
        """
        parser.chosen_type = choice

    # Dropdown menu
    option_menu = customtkinter.CTkOptionMenu(app, values=type_choices, command=choose_type)
    option_menu.set(type_choices[0])
    option_menu.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

    # Choose directory menu
    button = customtkinter.CTkButton(master=app, text="Choose directory", command=choose_directory)
    button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    # Start button
    button = customtkinter.CTkButton(master=app,
                                     text="Start !",
                                     command=start_analyze,
                                     fg_color="#7B0000",
                                     hover_color="#540000"
                                     )
    button.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

    # Start the main loop
    app.mainloop()


if __name__ == "__main__":
    main()
