import numpy as np
import math

class Model():
    def __init__(self):
        self.n = 1000        # Кол-во точек
        self.c = 5           # Константа

        self.average_value = 0

    def average_value(self):
        self.average_value = np.mean(self.r_y)

    # Рассчет дисперсии
    def calculation_dispersion(self):
        trend_list = np.copy(self.r_y)

        iteration_number = 1
        for i in range(iteration_number - 1):
            #self.model.calculation()
            #deep_copy_y = np.copy(self.model.y)
            #trend_list += deep_copy_y
            print("gds")

        dispersion = 0
        for i in range(self.n):
            dispersion += (trend_list[i] - self.average_value) * (trend_list[i] - self.average_value)

        self.dispersion = dispersion / self.n

    # Рассчет стандартного отклонения
    def calculation_standard_deviation(self):

        if self.dispersion == 0:  # Если не была расчитана диспресия
            self.calculation_dispersion(1)

        self.standard_deviation = math.sqrt(self.dispersion)

        # return self.standard_deviation

    def random(self):
        self.r_y = np.random.uniform(0, self.c, self.n)

    def calculation(self):
        pass