import numpy as np
import math

class Model():
    def __init__(self, c, n):
        self.n = n       # Кол-во точек
        self.c = c       # Константа

        self.x = np.arange(0, self.n)

        self.average_value = 0
        self.dispersion = 0
        self.standard_deviation = 0

        self.y_axis_min = 0
        self.y_axis_max = 0

        self.graph = 0

    def calculation_average_value(self):
        self.average_value = np.mean(self.r_y)

    # Рассчет дисперсии
    def calculation_dispersion(self):

        dispersion = 0
        for i in range(self.n):
            dispersion += (self.r_y[i] - self.average_value) * (self.r_y[i] - self.average_value)

        self.dispersion = dispersion / self.n

    # Рассчет стандартного отклонения
    def calculation_standard_deviation(self):
        self.standard_deviation = math.sqrt(self.dispersion)

    def random(self):
        self.r_y = np.random.uniform(0, self.c, self.n)

    def calculation(self):

        self.random()                           # Сгенирировали случайный процесс
        self.calculation_average_value()                    # Расчсчтиали среднее значение
        self.calculation_dispersion()           # Посчитали дипсперсии для расчета стандартного отклонения
        self.calculation_standard_deviation()   # Расчитали стандартное отклонение

        y = []
        degree_standard_deviation = self.standard_deviation ** 2
        argument_1 = self.average_value - (degree_standard_deviation / 2)
        for i in range(self.n):
            argument_exp = (argument_1 * i) + (self.standard_deviation * self.r_y[i])
            argument = math.exp(argument_exp)
            y.append(self.c * argument)

        self.y = np.array(y)

    def normalisation_axis(self):
        self.y_axis_max = np.amax(self.y)
        self.y_axis_min = np.amin(self.y)


