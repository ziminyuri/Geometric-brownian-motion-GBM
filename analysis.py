import math
import copy

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

        # Параметры для гистограммы
        self.bar_graph = []                # Значения для графика гистограммы
        self.number_of_intervals = 40      # Количество интервалов для гистограмм
        self.max_bar_graph_value = 0

        # Параметры для автокорреляции
        self.l = model.n - 1         # Сдвиг

        # Параментр для Преобразования Фурье (Спектр)
        self.delta_t = 0.01

    # Рассчет среднего значения
    def calculation_average_value(self):

        self.average_value = np.mean(self.model.y)

        return self.average_value

    def check_stationarity_average_value(self):

        number_of_gaps = 10  # Количество промежутков

        gap_length = int(self.model.n / number_of_gaps)  # Длина промежутка

        average_value = 0

        delta_min_max = (2 * self.model.s_max) * 0.05

        for i in range(self.model.n):
            average_value = average_value + math.fabs(self.model.y[i])
            if i % gap_length == 0 and i > 0 or i == self.model.n - 1:
                average_value = average_value / gap_length
                self.all_average_value.append(average_value)
                average_value = 0

        flag_stationarity = True
        for i in range(self.all_average_value.__len__() - 1):

            if math.fabs(self.all_average_value[i] - self.all_average_value[i + 1]) > delta_min_max:
                flag_stationarity = False

        return flag_stationarity

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
    def calculation_nested_correlation(self):

        model = Model(16)                       # Модель графика взаимной корреляция
        analysis_model_n = self.model.n

        y_list_1 = copy.deepcopy(self.model.y)
        self.calculation_average_value()
        average_value1 = self.average_value

        self.model.calculation()
        y_list_2 = copy.deepcopy(self.model.y)
        self.calculation_average_value()
        average_value2 = self.average_value

        x = []
        y = []

        result_y_min = 0
        result_y_max = 0

        # Знаменатель
        sum_1 = 0
        sum_2 = 0

        for j in range(analysis_model_n - 1):
            temp_value_1 = (y_list_1[j] - average_value1)
            temp_value_1 = temp_value_1 ** 2
            sum_1 = sum_1 + temp_value_1

            temp_value_2 = (y_list_2[j] - average_value2)
            temp_value_2 = temp_value_2 ** 2
            sum_2 = sum_2 + temp_value_2

        denominator = sum_1 * sum_2
        denominator = math.sqrt(denominator)

        for i in range(self.l):

            numerator = 0

            for j in range(analysis_model_n - i - 1):
                temp_value = (y_list_1[j] - average_value1) * (y_list_2[j+i] - average_value2)
                numerator = numerator + temp_value

            result_y = numerator / denominator

            """
            if result_y_min > result_y:
                result_y_min = result_y

            if result_y_max < result_y:
                result_y_max = result_y
            """

            x.append(i)
            y.append(result_y)

        model.n = self.l
        model.y = np.array(y)
        model.x = np.array(x)

        mac_y = np.amax(model.y)
        mac_x = np.amin(model.y)

        # model.s_min = result_y_min
        # model.s_max = result_y_max
        # model.y = model.y * 99
        # model.normalization()

        model.axis_max = np.amax(model.y)
        model.axis_min = np.amin(model.y)

        return model