from tkinter import *
from MainWindow import MainWindow
import matplotlib.pyplot as plt
import numpy as np
import math


def main():
    root = Tk()
    app = MainWindow(root)
    app.pack()
    root.title("Курсовой проект / Методы обработки эксперементальных данных")
    root.geometry('1400x820')
    root.resizable(False, False)
    root.mainloop()


def main1():
    T = 1
    mu = 0.01
    sigma = 0.01
    c = 20  # Случайная положительная константа
    dt = 0.001
    N = round(T / dt)
    t = np.linspace(0, T, N)

    # W = np.random.standard_normal(size=N)
    W = np.random.randn(N)
    print('dsf')
    cum = np.cumsum(W)
    print(W)
    print('fsd')
    print(cum)
    print('fsd')

    W = np.cumsum(W) * np.sqrt(dt)  # стандартное броуновское движение
    print(W)
    X = (mu - 0.5 * sigma ** 2) * t + sigma * W
    S = c * np.exp(X)  # геометрическое броуновское движение
    plt.plot(t, S)
    plt.show()


# Рассчет дисперсии
def calculation_dispersion(r_t, n, average_value):
    dispersion = 0
    for i in range(n):
        dispersion += (r_t[i] - average_value) * (r_t[i] - average_value)

    dispersion = dispersion / n

    return dispersion


# Рассчет стандартного отклонения
def calculation_standard_deviation(dispersion):
    standard_deviation = math.sqrt(dispersion)

    return standard_deviation


def main2():
    c = 20
    n = 10
    t = np.arange(0, n)

    r_t = np.random.uniform(0, c)
    mu = np.mean(r_t)
    print("mu")
    print(mu)

    dispersion = calculation_dispersion(r_t, n, mu)
    standard_deviation = calculation_standard_deviation(dispersion)
    sigma1 = standard_deviation

    sigma = np.std(r_t)
    print("sigma")
    print(sigma)

    X = (mu - 0.5 * sigma ** 2) * t + sigma * r_t
    S = c * np.exp(X)  # геометрическое броуновское движение
    plt.plot(t, S)
    plt.show()


if __name__ == '__main__':
    main()
