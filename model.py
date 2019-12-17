import numpy as np
import csv
import copy

# Функция импорта котировок
def import_value(filename):
    cost_rts = []
    date_rts = []

    csv.register_dialect('pipes', delimiter=';')
    with open(filename, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, dialect='pipes')

        for row in reader:
            try:
                r = float(row[2])
                cost_rts.append(r)
                date_rts.append(row[0])
            except:
                pass

    new_data_rts = []
    for i in date_rts:
        temp = i[:4] + "-" + i[4:6] + "-" + i[6:8]
        new_data_rts.append(temp)

    return new_data_rts, cost_rts


class Model:
    def __init__(self, option):
        self.option = option
        self.n = 0

        self.y_axis_min = 0
        self.y_axis_max = 0

        self.y_gaps_10 = []  # Промежутки исходных данных

        self.graph = 0

    # Расчет геометрического Броуновского движения
    def gbm(self):
        all_y = []
        for i in range (len(self.y_gaps_10)):
            y = copy.deepcopy(self.y_gaps_10[i])
            n = len(y)

            returns = []
            for i in range(1, n):
                value = (y[i] - y[i - 1]) / y[i - 1]
                returns.append(value)
            returns = np.array(returns)
            average_value = np.mean(returns)
            standard_deviation = np.std(returns)

            T = n
            mu = average_value
            sigma = standard_deviation
            S0 = y[0]
            dt = 1
            N = round(T / dt)
            t = np.linspace(0, T, N)
            W = np.random.standard_normal(size=N)
            W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
            X = (mu - 0.5 * sigma ** 2) * t + sigma * W
            S = S0 * np.exp(X)  ### geometric brownian motion ###

            y = S.tolist()
            all_y += y

        n = len(all_y)
        self.x = np.arange(n)
        self.y = np.array(all_y)

    # Расчет промежутков
    def highlight_gaps(self):
        interval = int(self.n / 10)
        for i in range(10):
            a = i * interval
            b = (i + 1) * interval
            y = self.y[a:b]
            self.y_gaps_10.append(y)

    def calculation(self):

        # РТС
        if self.option == 1:
            filename = "input_files/SPFB.RTS_161210_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.x = np.arange(self.n)
            self.highlight_gaps() # Разбиваем данные на 10 равных промежутков

        # Сбербанк
        if self.option == 3:
            filename = "input_files/SBER_161212_191210.csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.x = np.arange(self.n)

        # Газпром
        if self.option == 4:
            filename = "input_files/GAZP_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.x = np.arange(self.n)

        # ВТБ
        if self.option == 5:
            filename = "input_files/VTBR_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.x = np.arange(self.n)

        # GBM РТС
        if self.option == 2:
            filename = "input_files/SPFB.RTS_161210_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.highlight_gaps()  # Разбиваем данные на 10 равных промежутков
            self.gbm()

        # GBM Сбербанк
        if self.option == 6:
            filename = "input_files/SBER_161212_191210.csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.highlight_gaps()  # Разбиваем данные на 10 равных промежутков
            self.gbm()

        # GBM Газпром
        if self.option == 7:
            filename = "input_files/GAZP_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.highlight_gaps()  # Разбиваем данные на 10 равных промежутков
            self.gbm()

        # GBM ВТБ
        if self.option == 8:
            filename = "input_files/VTBR_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)
            self.n = len(self.y)
            self.highlight_gaps()  # Разбиваем данные на 10 равных промежутков
            self.gbm()

    # Нормализация осей
    def normalisation_axis(self):
        self.y_axis_max = np.amax(self.y) * 1.2
        self.y_axis_min = np.amin(self.y) * 0.8

    # Выделяем в ручную тренд методом скользящего окна
    def highlight_trends(self, analyzed_model):

        size_of_window = 50
        analysis_model_n = len(analyzed_model.y)
        sum_value_of_window = 0
        y = np.copy(analyzed_model.y)

        for i in range(analysis_model_n - size_of_window):
            for j in range(size_of_window):
                sum_value_of_window += y[i + j]

            average = sum_value_of_window / size_of_window
            y[i] = average
            sum_value_of_window = 0

        for i in range(analysis_model_n - size_of_window, analysis_model_n):
            for j in range(size_of_window):
                sum_value_of_window += y[i - j]

            average = sum_value_of_window / size_of_window
            y[i] = average
            sum_value_of_window = 0

        self.y = np.copy(y)
        self.x = np.arange(len(self.y))

