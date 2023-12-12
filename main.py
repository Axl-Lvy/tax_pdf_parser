import customtkinter
from tkinter import filedialog
from src.parser import Parser
from src.parameters import type_choices


def main():
    """
    Main function
    :return:
    """

    customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("400x240")

    parser = Parser(type_choices)

    def choose_directory():
        folder = filedialog.askdirectory(
            initialdir="./",
            title="Browse File"
        )
        parser.folder = folder

    def start_analyze():
        parser.start()

    def choose_type(choice):
        print("option menu dropdown clicked:", choice)

    option_menu = customtkinter.CTkOptionMenu(app, values=type_choices, command=choose_type)
    option_menu.set(type_choices[0])
    option_menu.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(master=app, text="Choose directory", command=choose_directory)
    button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(master=app, text="Start !", command=start_analyze,
                                     fg_color="#7B0000",
                                     hover_color="#540000"
                                     )
    button.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

    app.mainloop()


if __name__ == "__main__":
    main()
