import math

import numpy as np
from model import Model


class Analysis:
    def __init__(self, model):

        self.model = model                 # Модель, которую анализиурем

        self.all_average_value = []        # Все средние значения
        self.average_value = 0             # Среднее значения тренда
        self.dispersion = 0                # Дисперсия
        self.standard_deviation = 0        # Стандартное отклонение
        self.asymmetry = 0                 # Асимметрия
        self.asymmetry_coefficient = 0     # Коэффициент асимметрии
        self.standard_ratio = 0            # Стандартный коэффициент
        self.excess = 0                    # Эксцесс

        self.l = model.n - 1  # Сдвиг


    # Рассчет среднего значения
    def calculation_average_value(self):

        self.average_value = np.mean(self.model.y)

        return self.average_value

    # Рассчет дисперсии
    def calculation_dispersion(self, iteration_number):

        if iteration_number <= 0:
            return

        trend_list = np.copy(self.model.y)

        for i in range(iteration_number - 1):
            self.model.calculation()
            deep_copy_y = np.copy(self.model.y)
            trend_list += deep_copy_y

        trend_list = trend_list / iteration_number

        average_value = np.mean(trend_list)

        dispersion = 0
        for i in range(self.model.n):
            dispersion += (trend_list[i] - average_value) * (trend_list[i] - average_value)

        self.dispersion = dispersion / self.model.n

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

        model = Model(9)                       # Модель графика взаимной корреляция
        model.y = np.correlate(model_1.y, model_2.y)
        model.n = len(model.y)
        model.x = np.arange(model.n)

        return model