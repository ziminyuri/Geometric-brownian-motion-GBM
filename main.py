from tkinter import *
from MainWindow import MainWindow


def main():
    root = Tk()
    app = MainWindow(root)
    app.pack()
    root.title("Курсовой проект / Методы обработки эксперементальных данных")
    root.geometry('1400x820')
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
