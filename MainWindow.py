from tkinter import *
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


from analysis import Analysis
from model import Model


# Обработчик нажатия на клавишу "Закрыть" в окне добавления графика
def click_button_close(subWindow):
    subWindow.destroy()


class MainWindow(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

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

        b_stat = Button(text="Статистики", command=self.click_button_statistics, width="26", height="2")
        b_stat.place(x=1120, y=170)

        self.combobox_graph = []
        self.graph_list = []
        self.analysis_model_list = []

    # Обработчик нажатия на клавишу "Добавить" в окне добавления графика
    def click_button_add(self, subWindow):

        if self.c2.get() == "РТС индекс":
            model = Model(1)

        if self.c2.get() == "Сбербанк":
            model = Model(3)

        if self.c2.get() == "Газпром":
            model = Model(4)

        if self.c2.get() == "ВТБ":
            model = Model(5)

        if self.c2.get() == "РТС - GBM":
            model = Model(2)

        if self.c2.get() == "Сбербанк - GBM":
            model = Model(6)

        if self.c2.get() == "Газпром - GBM":
            model = Model(7)

        if self.c2.get() == "ВТБ - GBM":
            model = Model(8)

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

    # Обработка нажатия на кнопку "Диспресия"
    @staticmethod
    def dispersion_click_button(analysis):

        check_result = analysis.calculation_dispersion()
        messagebox.showinfo("Дисперсия", "Дисперсия: " + str(check_result))

    # Обработка нажатия на кнопку "Среднее значение"
    @staticmethod
    def average_value_click_button(analysis):

        check_result = analysis.calculation_average_value()
        messagebox.showinfo("Среднее значение", "Среднее значение: " + str(check_result))

    # Обработка нажатия на кнопку "Асимметрия"
    @staticmethod
    def asymmetry_click_button(analysis):

        result = analysis.calculation_asymmetry()
        messagebox.showinfo("Ассиметрия", "Ассиметрия: " + str(result))

    # Обработка нажатия на кнопку "Стандартное отклонение"
    @staticmethod
    def standard_deviation(analysis):

        result = analysis.calculation_standard_deviation()
        messagebox.showinfo("Стандартное отклонение", "Стандартное отклонение: " + str(result))

    # Обработка нажатия на кнопку "Коэффициент асимметрии"
    @staticmethod
    def asymmetry_coefficient_click_button(analysis):

        result = analysis.calculation_asymmetry_coefficient()
        messagebox.showinfo("Коэффициент асимметрии", "Коэффициент асимметрии: " + str(result))

    # Обработка нажатия на кнопку "Эксцесс"
    @staticmethod
    def excess_click_button(analysis):

        result = analysis.calculation_excess()
        messagebox.showinfo("Эксцесс", "Эксцесс: " + str(result))

    # Обработка нажатия на кнопку "Куртозис"
    @staticmethod
    def kurtosis_click_button(analysis):

        result = analysis.calculation_kurtosis()
        messagebox.showinfo("Куртозис", "Куртозис: " + str(result))

    # Обработка нажатия на кнопку "Стандартный коэфифциент"
    @staticmethod
    def standard_ratio_click_button(analysis):

        result = analysis.calculation_standard_ratio()
        messagebox.showinfo("Стандартный коэфифциент", "Стандартный коэфифциент: " + str(result))

    # Обработка нажатия на кнопку "Среднеквадратичная ошибка"
    @staticmethod
    def standard_error_click_button(analysis):

        result = analysis.calculation_standard_error()
        messagebox.showinfo("Среднеквадратичная ошибка", "Среднеквадратичная ошибка: " + str(result))

    # Обработка нажатия на кнопку "Среднее абсолютное отклонение"
    @staticmethod
    def mean_absolute_deviation_click_button(analysis):

        result = analysis.calculation_mean_absolute_deviation()
        messagebox.showinfo("Среднее абсолютное отклонение", "Среднее абсолютное отклонение: " + str(result))

    # Обработка нажатия на кнопку "Минимальный Х"
    @staticmethod
    def x_min_click_button(analysis):

        result = analysis.calculation_min_x()
        messagebox.showinfo("Минимальный Х", "Минимальный Х: " + str(result))

    # Обработка нажатия на кнопку "Максимальный Х"
    @staticmethod
    def x_max_click_button(analysis):

        result = analysis.calculation_max_x()
        messagebox.showinfo("Максимальный Х", "Максимальный Х: " + str(result))

    def check_empty_c1(self):
        if self.c1.get() == "":
            messagebox.showinfo("Ошибка", "Не указан номер графика")
            return 1
        else:
            return 0

    # Рассчет взаимной корелляции
    def click_button_nested_correlation(self, subWindow):

        if self.check_empty_c1():
            return

        analyzed_model_1 = self.get_model(self.c1.get())
        analysis_model = self.get_analysis(analyzed_model_1)

        if self.c3.get() == "":
            return

        if self.c3.get() == "Сбербанк":
            analyzed_model_2 = Model(3)

        if self.c3.get() == "Газпром":
            analyzed_model_2 = Model(4)

        if self.c3.get() == "ВТБ":
            analyzed_model_2 = Model(5)
        analyzed_model_2.calculation()
        nested_correlation_model = analysis_model.calculation_nested_correlation(analyzed_model_1,analyzed_model_2)
        nested_correlation_model.graph = int(self.c2.get())
        nested_correlation_model.normalisation_axis()
        self.draw_graph(nested_correlation_model)

        subWindow.destroy()

    # Возвращаем модель анализа
    def get_analysis(self,analyzed_model):
        for i in self.analysis_model_list:
            if i.model == analyzed_model:
                return i

        analysis_model = Analysis(analyzed_model)
        self.analysis_model_list.append(analysis_model)

        return analysis_model

    # Рассчет статистик
    def statistics_calculation(self, subWindow, choice_of_calculation):

        if self.check_empty_c1():
            return

        analyzed_model = self.get_model(self.c1.get())
        analysis_model = self.get_analysis(analyzed_model)

        if choice_of_calculation == 2:
            self.average_value_click_button(analysis_model)

        if choice_of_calculation == 3:
            self.dispersion_click_button(analysis_model)

        if choice_of_calculation == 5:
            self.standard_deviation(analysis_model)

        if choice_of_calculation == 6:
            self.asymmetry_click_button(analysis_model)

        if choice_of_calculation == 7:
            self.asymmetry_coefficient_click_button(analysis_model)

        if choice_of_calculation == 8:
            self.excess_click_button(analysis_model)

        if choice_of_calculation == 9:
            self.kurtosis_click_button(analysis_model)

        if choice_of_calculation == 10:
            self.standard_ratio_click_button(analysis_model)

        if choice_of_calculation == 11:
            self.mean_absolute_deviation_click_button(analysis_model)

        if choice_of_calculation == 12:
            self.x_min_click_button(analysis_model)

        if choice_of_calculation == 13:
            self.x_max_click_button(analysis_model)
        subWindow.destroy()

    # Окно статистик
    def click_button_statistics(self):
        a = Toplevel()
        a.title('Статистики')
        a.geometry('900x500')

        label1 = Label(a, text="Номер графика для анализа", height=1, width=25, font='Arial 14')
        label1.place(x=10, y=10)
        self.c1 = ttk.Combobox(a, values=self.combobox_graph, height=4, width="24")
        self.c1.place(x=10, y=30)

        label2 = Label(a, text="Место для вывода анализа", height=1, width=24, font='Arial 14')
        label2.place(x=300, y=10)
        self.c2 = ttk.Combobox(a, values=[u"1", u"2", u"3", u"4"], height=4, width="24")
        self.c2.place(x=300, y=30)

        label3 = Label(a, text="Данные для взаимной корелляции", height=1, width=29, font='Arial 14')
        label3.place(x=300, y=70)
        self.c3 = ttk.Combobox(a, values=[u"Сбербанк", u"Газпром", u"ВТБ"], height=3, width="24")
        self.c3.place(x=300, y=90)

        button_nested_correlation = Button(a, text="Взаимная корелляция",
                                           command=lambda: self.click_button_nested_correlation(a),
                                           width="26", height="2")
        button_nested_correlation.place(x=300, y=150)

        choice_of_calculation = IntVar()
        choice_of_calculation.set(0)
        average_value = Radiobutton(a, text='Среднее значение', variable=choice_of_calculation, value=2)
        dispersion = Radiobutton(a, text='Дисперсия', variable=choice_of_calculation, value=3)
        standard_deviation = Radiobutton(a, text='Стандартное отклоение', variable=choice_of_calculation, value=5)
        asymmetry = Radiobutton(a, text='Асимметрия', variable=choice_of_calculation, value=6)
        asymmetry_coefficient = Radiobutton(a, text='Коэффициент асимметрии', variable=choice_of_calculation, value=7)
        excess = Radiobutton(a, text='Эксцесс', variable=choice_of_calculation, value=8)
        kurtosis = Radiobutton(a, text='Куртозис', variable=choice_of_calculation, value=9)
        standard_ratio = Radiobutton(a, text='Стандартный коэфифциент', variable=choice_of_calculation, value=10)
        mean_absolute_deviation = Radiobutton(a, text='Среднее абсолютное отклонение', variable=choice_of_calculation,
                                              value=11)
        x_min = Radiobutton(a, text='Минимальный Х', variable=choice_of_calculation, value=12)
        x_max = Radiobutton(a, text='Максимальный Х', variable=choice_of_calculation, value=13)

        average_value.place(x=10, y=60)
        dispersion.place(x=10, y=80)
        standard_deviation.place(x=10, y=100)
        asymmetry.place(x=10, y=120)
        asymmetry_coefficient.place(x=10, y=140)
        excess.place(x=10, y=160)
        kurtosis.place(x=10, y=180)
        standard_ratio.place(x=10, y=200)
        mean_absolute_deviation.place(x=10, y=220)
        x_min.place(x=10, y=240)
        x_max.place(x=10, y=260)

        b1 = Button(a, text="Вычислить",
                    command=lambda: self.statistics_calculation(a, choice_of_calculation.get()), width="15", height="2")
        b1.place(x=600, y=450)
        b2 = Button(a, text="Закрыть", command=lambda: click_button_close(a), width="15", height="2")
        b2.place(x=750, y=450)

        a.grab_set()  # Перехватывает все события происходящие в приложении
        a.focus_set()  # Захватывает и удерживает фокус

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
        self.c2 = ttk.Combobox(a, values=[u"РТС индекс", u"Сбербанк", u"Газпром", u"ВТБ", u"РТС - GBM"
                                          , u"Сбербанк - GBM", u"Газпром - GBM", u"ВТБ - GBM"], height=8)
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
