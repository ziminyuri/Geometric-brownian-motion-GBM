import numpy as np
import math
import csv


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

    print(new_data_rts)
    # print(cost_rts)
    print(date_rts)

    return new_data_rts, cost_rts


class Model:
    def __init__(self, option):
        self.c = 1  # Константа
        self.t = 1  # Период

        self.option = option
        self.n = 0

        self.mu = 0.1
        self.sigma = 0.01


        self.y_axis_min = 0
        self.y_axis_max = 0

        self.graph = 0

    def calculation_average_value(self):
        self.average_value = np.mean(self.r_y)

    def random(self):
        self.r_y = np.random.uniform(0, self.c, self.n)

    def calculation(self):

        if self.option == 1:
            filename = "input_files/SPFB.RTS_161210_191210 (1).csv"
            self.date, self.y = import_value(filename)

        if self.option == 3:
            filename = "input_files/SBER_161212_191210.csv"
            self.date, self.y = import_value(filename)

        if self.option == 4:
            filename = "input_files/GAZP_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)

        if self.option == 5:
            filename = "input_files/VTBR_161212_191210 (1).csv"
            self.date, self.y = import_value(filename)

        self.n = len(self.y)
        self.x = np.arange(self.n)

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

