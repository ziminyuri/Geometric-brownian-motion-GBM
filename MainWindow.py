from tkinter import *
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model import Model


class MainWindow(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.graph = []
        self.analysis_model = []  # Список, где храним модели анализа

        label1 = Label(text="График №1", height=1, width=15, font='Arial 18')
        label1.place(x=165, y=5)

        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim([0, 1000])
        ax.set_ylim([-100, 100])
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=5, y=35)

        label2 = Label(text="График №2", height=1, width=15, font='Arial 18')
        label2.place(x=700, y=5)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=550, y=35)

        label3 = Label(text="График №3", height=1, width=15, font='Arial 18')
        label3.place(x=165, y=360)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=5, y=400)

        label4 = Label(text="График №4", height=1, width=15, font='Arial 18')
        label4.place(x=700, y=360)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=550, y=400)

        b2 = Button(text="Добавить", command=self.click_button_add_model, width="26", height="2")
        b2.place(x=1120, y=70)

        b3 = Button(text="Анализ", command=self.click_button_add_model, width="26", height="2")
        b3.place(x=1120, y=120)

        self.combobox_value = []  # ComboBox графиков для анализа

    # Обработчик нажатия на клавишу "Добавить" в окне добавления графика
    def click_button_add(self):

        c = self.input_c.get()
        n = self.input_n.get()

        if c != '':
            c = float(c)
        else:
            c = 1

        if n != "":
            n = int(n)
        else:
            n = 1000

        model = Model(c, n)
        model.calculation()
        model.normalisation_axis()
        model.graph = 1

        self.draw_graph(model)

    # Обработчик нажатия на клавишу "Закрыть" в окне добавления графика
    def click_button_close(self):
        pass

    # Окно добавления графика
    def click_button_add_model(self):
        a = Toplevel()
        a.title('Добавить график')
        a.geometry('300x200')

        # Ввод n
        label_n = Label(a, text="Количество значений", height=1, width=18, font='Arial 14')
        label_n.place(x=10, y=10)
        self.input_n = Entry(a, width=15)
        self.input_n.place(x=10, y=30)

        # Ввод c
        label_c = Label(a, text="Введите с", height=1, width=9, font='Arial 14')
        label_c.place(x=10, y=60)
        self.input_c = Entry(a, width=15)
        self.input_c.place(x=10, y=80)

        b1 = Button(a, text="Добавить", command=lambda: self.click_button_add(), width="13", height="2")
        b1.place(x=40, y=150)
        b2 = Button(a, text="Закрыть", command=self.click_button_close, width="13", height="2")
        b2.place(x=170, y=150)

        a.grab_set()  # Перехватывает все события происходящие в приложении
        a.focus_set()  # Захватывает и удерживает фокус

    def get_model(self, number_of_trend):
        for i in self.graph:
            g = i.graph
            if g == int(number_of_trend):
                return i

    def draw_graph(self, model):

        chart_number = str(model.graph)
        x = model.n
        y_min = model.y_axis_min
        y_max = model.y_axis_max

        x_list = model.x
        y_list = model.y

        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim([0, x])
        ax.set_ylim([y_min, y_max])

        ax.plot(x_list, y_list, color='red', label='Линия 1')

        if chart_number == "1":
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().place(x=5, y=35)

        if chart_number == "2":
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().place(x=550, y=35)

        if chart_number == "3":
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().place(x=5, y=400)

        if chart_number == "4":
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().place(x=550, y=400)
