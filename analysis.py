import math
import copy

import numpy as np
from model import Model


class Analysis:
    def __init__(self, model):

        self.model = model  # Модель, которую анализиурем

        self.all_average_value = []  # Все средние значения
        self.average_value = 0  # Среднее значения тренда
        self.dispersion = 0  # Дисперсия
        self.standard_deviation = 0  # Стандартное отклонение
        self.asymmetry = 0  # Асимметрия
        self.asymmetry_coefficient = 0  # Коэффициент асимметрии
        self.standard_ratio = 0  # Стандартный коэффициент
        self.excess = 0  # Эксцесс

        self.l = model.n - 1  # Сдвиг

    # Рассчет среднего значения
    def calculation_average_value(self):

        self.average_value = np.mean(self.model.y)

        print("Расчет среднего на 10 интервалах")

        for i in range(len(self.model.y_gaps_10)):
            average_value = np.mean(self.model.y_gaps_10[i])
            self.all_average_value.append(average_value)
            print("Среднее значение промежутка № " + str(i + 1) + " = " + str(average_value))

        return self.average_value

    # Рассчет дисперсии
    def calculation_dispersion(self):

        if self.average_value ==0:
            self.calculation_average_value()

        dispersion = 0
        for i in range(self.model.n):
            dispersion += (self.model.y[i] - self.average_value) * (self.model.y[i] - self.average_value)

        self.dispersion = dispersion / self.model.n

        for i in range(len(self.model.y_gaps_10)):
            y = copy.deepcopy(self.model.y_gaps_10[i])
            dispersion = 0
            for j in range(len(y)):
                dispersion += (y[j] - self.all_average_value[i]) * (y[j] - self.all_average_value[i])

            dispersion = dispersion / len(y)
            print("Дисперсия промежутка № " + str(i + 1) + " = " + str(dispersion))

        return self.dispersion

    # Рассчет стандартного отклонения
    def calculation_standard_deviation(self):

        if self.dispersion == 0:  # Если не была расчитана диспресия
            self.calculation_dispersion(1)

        self.standard_deviation = math.sqrt(self.dispersion)

        return self.standard_deviation

    # Рассчет асимметрии
    def calculation_asymmetry(self):

        if self.average_value == 0:
            self.calculation_average_value()

        sum_of_values = 0

        for i in range(self.model.n):
            temp_value = (self.model.y[i] - self.average_value)
            temp_value = temp_value * temp_value * temp_value
            sum_of_values = sum_of_values + temp_value

        self.asymmetry = sum_of_values / self.model.n

        return self.asymmetry

    # Рассчет коэффициента асимметрии
    def calculation_asymmetry_coefficient(self):

        if self.standard_deviation == 0:
            self.calculation_standard_deviation()

        if self.asymmetry == 0:
            self.calculation_asymmetry()

        sigma3 = self.standard_deviation * self.standard_deviation * self.standard_deviation
        self.asymmetry_coefficient = self.asymmetry / sigma3

        return self.asymmetry_coefficient

    # Рассчет эксцесса
    def calculation_excess(self):

        if self.average_value == 0:
            self.calculation_average_value()

        sum_of_values = 0

        for i in range(self.model.n):
            temp_value = (self.model.y[i] - self.average_value)
            temp_value = temp_value ** 4  # Возведение в степень 4
            sum_of_values = sum_of_values + temp_value

        self.excess = sum_of_values / self.model.n

        return self.excess

    # Рассчет куртозис
    def calculation_kurtosis(self):

        if self.standard_deviation == 0:
            self.calculation_standard_deviation()

        if self.excess == 0:
            self.calculation_excess()

        kurtosis = self.excess / self.standard_deviation ** 4
        kurtosis = kurtosis - 3

        return kurtosis

    # Рассчет стандартного коэфициента
    def calculation_standard_ratio(self):

        sum_of_values = 0

        for i in range(self.model.n):
            temp_value = self.model.y[i] ** 2
            sum_of_values = sum_of_values + temp_value

        self.standard_ratio = sum_of_values / self.model.n

        return self.standard_ratio

    # Рассчет среднеквадратичной ошибки
    def calculation_standard_error(self):
        if self.standard_ratio == 0:
            self.calculation_standard_ratio()

        standard_error = math.sqrt(self.standard_ratio)

        return standard_error

    # Рассчет среднего абсолютного отклонения
    def calculation_mean_absolute_deviation(self):

        if self.average_value == 0:
            self.calculation_average_value()

        sum_of_values = 0

        for i in range(self.model.n):
            sum_of_values = sum_of_values + math.fabs(self.model.y[i] - self.average_value)

        mean_absolute_deviation = sum_of_values / self.model.n

        return mean_absolute_deviation

    # Поиск минимального Х
    def calculation_min_x(self):
        x = np.amin(self.model.y)
        return x

    # Поиск максимального Х
    def calculation_max_x(self):
        x = np.amax(self.model.y)
        return x

    # Взаимной корреляция
    def calculation_nested_correlation(self, model_1, model_2):

        model = Model(9)  # Модель графика взаимной корреляция
        model.y = np.correlate(model_1.y, model_2.y, mode="full")
        model.n = len(model.y)
        model.x = np.arange(model.n)

        return model
