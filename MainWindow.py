from tkinter import *
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model import Model


# Обработчик нажатия на клавишу "Закрыть" в окне добавления графика
def click_button_close(subWindow):
    subWindow.destroy()


class MainWindow(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.graph = []

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

        b3 = Button(text="Анализ", command=self.click_button_anylise, width="26", height="2")
        b3.place(x=1120, y=120)

        self.combobox_graph = []
        self.graph_list = []

    # Обработчик нажатия на клавишу "Добавить" в окне добавления графика
    def click_button_add(self, subWindow):

        if self.c2.get() == "РТС индекс":
            model = Model(1)

        else:
            model = Model(2)

            c = self.input_c.get()
            n = self.input_n.get()

            if c != '':
                c = float(c)
            else:
                c = 1

            if n != "":
                n = int(n)
            else:
                n = 0

        model.calculation()
        model.normalisation_axis()

        if self.c3.get() != "":
            model.graph = int(self.c3.get())
        else:
            model.graph = 1

        self.append_graph_to_list_and_combobox(model)
        self.draw_graph(model)

        subWindow.destroy()

    # Обработка нажатие на кнопку "Выделить тренды"
    def highlight_trends(self, subWindow):
        if self.c2.get() != "":
            analyse_model = self.get_model(self.c2.get())
            model = Model(3)
            model.highlight_trends(analyse_model)
            model.normalisation_axis()

            if self.c3.get() != "":
                model.graph = int(self.c3.get())
            else:
                model.graph = 1

            self.draw_graph(model)

        subWindow.destroy()

    # Получаем объект модели из списка объектов моделей
    def get_model(self, search_model):
        for i in self.graph_list:
            if i.graph == int(search_model):
                return i

    # Добавление в комбобокс построенных графиков и в список объектов моделей
    def append_graph_to_list_and_combobox(self, model):
        flag = 0

        for i in self.combobox_graph:
            if i == str(model.graph) and flag == 0:
                flag = 1

        if flag == 0:
            self.combobox_graph.append(str(model.graph))
            self.combobox_graph.sort()

        for i in self.graph_list:
            if i.graph == model.graph:
                i = model
                return

        self.graph_list.append(model)

    # Окно анализа
    def click_button_anylise(self):
        a = Toplevel()
        a.title('Анализ')
        a.geometry('450x200')

        label2 = Label(a, text="График функции", height=1, width=14, font='Arial 14')
        label2.place(x=10, y=10)
        self.c2 = ttk.Combobox(a, values=self.combobox_graph, height=2)
        self.c2.place(x=10, y=30)

        label3 = Label(a, text="Место вывода графика", height=1, width=20, font='Arial 14')
        label3.place(x=10, y=60)
        self.c3 = ttk.Combobox(a, values=[u"1", u"2", u"3", u"4"], height=4)
        self.c3.place(x=10, y=80)

        b1 = Button(a, text="Выделить тренды", command=lambda: self.highlight_trends(a), width="13", height="2")
        b1.place(x=285, y=20)
        b2 = Button(a, text="Закрыть", command=lambda: click_button_close(a), width="13", height="2")
        b2.place(x=285, y=150)

        a.grab_set()  # Перехватывает все события происходящие в приложении
        a.focus_set()  # Захватывает и удерживает фокус

    # Окно добавления графика
    def click_button_add_model(self):
        a = Toplevel()
        a.title('Добавить график')
        a.geometry('450x200')

        label2 = Label(a, text="График функции", height=1, width=14, font='Arial 14')
        label2.place(x=10, y=10)
        self.c2 = ttk.Combobox(a, values=[u"РТС индекс", u"GBM"], height=2)
        self.c2.place(x=10, y=30)

        label3 = Label(a, text="Место вывода графика", height=1, width=20, font='Arial 14')
        label3.place(x=10, y=60)
        self.c3 = ttk.Combobox(a, values=[u"1", u"2", u"3", u"4"], height=4)
        self.c3.place(x=10, y=80)

        b1 = Button(a, text="Добавить", command=lambda: self.click_button_add(a), width="13", height="2")
        b1.place(x=150, y=150)
        b2 = Button(a, text="Закрыть", command=lambda: click_button_close(a), width="13", height="2")
        b2.place(x=285, y=150)

        a.grab_set()  # Перехватывает все события происходящие в приложении
        a.focus_set()  # Захватывает и удерживает фокус

    """
    def get_model(self, number_of_trend):
        for i in self.graph:
            g = i.graph
            if g == int(number_of_trend):
                return i
    """

    def draw_graph(self, model):

        chart_number = str(model.graph)
        x = len(model.x)
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
