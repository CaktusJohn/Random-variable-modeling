import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def generate_sample(k, p, experiments):
    res = dict()  # Уникальные значения случайной величины в экспериментах
    for _ in range(experiments):
        successes = 0
        nu = 0  # Случайная величина (количество испытаний)
        while successes < k:
            nu += 1
            u = random.random()
            if u < p:
                successes += 1
        if nu in res:
            res[nu] += 1
        else:
            res[nu] = 1
    return res

def theoretical_probability(nu, k, p):
    """Вычисляет теоретическую вероятность для отрицательного биномиального распределения."""
    # Биномиальный коэффициент
    binomial_coeff = math.comb(nu - 1, k - 1) # кол-во сочетаний
    
    # Теоретическая вероятность
    probability = binomial_coeff * (p**k) * ((1 - p)**(nu - k))
    
    return probability

def sample_statistics(results, exp_n):
    """Вычисляет выборочные характеристики."""
    
    # Выборочное среднее
    mean = sum(value * freq for value, freq in results.items()) / exp_n

    # Выборочная дисперсия
    variance = sum(freq * (value - mean) ** 2 for value, freq in results.items()) / exp_n

    # Размах выборки
    values = list(results.keys())
    range_ = max(values) - min(values)

    # Медиана
    cumulative = 0  # Накопленная частота
    median = None
    # Определяем половину выборки
    half = exp_n / 2
    lower_median = None
    upper_median = None
    
    for value, freq in results.items():
        cumulative += freq

        # Для четного n фиксируем два центральных значения
        if lower_median is None and cumulative >= half:
            lower_median = value
        if cumulative > half:
            upper_median = value
            break

    # Если n нечётное, медиана — одно центральное значение
    if exp_n % 2 == 1:
        median = upper_median
    # Если n чётное, медиана — среднее двух центральных значений
    else:
        median = (lower_median + upper_median) / 2
        
    return mean, variance, range_, median

def theoretical_statistics(k, p):
    """Вычисляет теоретические характеристики."""
    mean = k / p  # Математическое ожидание
    variance = k * (1 - p) / (p ** 2)  # Дисперсия
    return mean, variance

def print_table_with_deviations(sorted_values, experiments, k, p):
    print(f"{'nu':<10}{'ni':<10}{'pi':<10}{'Теоритическая P':<20}{'Погрешность':<20}")
    print("-" * 70)
    
    for nu, ni in sorted_values.items():                                         #nu - значение случайной величины         
        pi = ni / experiments                                                    #ni - количество
        theoretical_p = theoretical_probability(nu, k, p)                        #pi - частота
        deviation = abs(pi - theoretical_p)
        print(f"{nu:<10}{ni:<10}{pi:<10.4f}{theoretical_p:<20.4f}{deviation:<20.4f}")

def plot_empirical_distribution(results, k, p): #Строит выборочную и теоретическую функции распределения.
    
    results[0] = 0  
    total_count = sum(results.values())
    sorted_results = sorted(results.items())
    x_empirical = [0]   
    y_empirical = [0]  

    cumulative = 0

    # Вычисляем выборочную функцию распределения
    for value, freq in sorted_results:
        cumulative += freq
        x_empirical.append(value)
        y_empirical.append(cumulative / total_count)

    # Расширяем диапазон для теоретической функции распределения
    max_x = max(max(x_empirical), k + 20)
    x_theoretical = np.arange(k, max_x + 1)
    
    y_theoretical = np.cumsum([theoretical_probability(nu, k, p) for nu in x_theoretical])
    x_theoretical = np.insert(x_theoretical, 0, 0)  
    y_theoretical = np.insert(y_theoretical, 0, 0)  

    # Построение графиков
    plt.step(x_empirical, y_empirical, where="post", label="Выборочная функция распределения", color="blue")
    plt.step(x_theoretical, y_theoretical, where="post", label="Теоретическая функция распределения", color="red")

    # Настройка графика
    plt.xlabel("x")
    plt.ylabel("P")
    plt.title("Функции распределения")
    plt.grid()
    plt.legend()
    plt.show()

    # Возвращаем выборочную и теоретическую функции распределения
    return dict(zip(x_empirical, y_empirical)), dict(zip(x_theoretical, y_theoretical))





def max_difference(empirical, theoretical):
    """Вычисляет максимальную разницу между выборочной и теоретической функциями распределения."""
    max_diff = 0
    # Для каждого значения находим разницу между выборочной и теоретической вероятностью
    for x in empirical:
        rounded_x = round(x, 6)  # Округляем до 6 знаков после запятой
        p_empirical = empirical.get(rounded_x, 0)  # Получаем вероятность из выборочного распределения
        p_theoretical = theoretical.get(rounded_x, 0)  # Получаем вероятность из теоретического распределения (по умолчанию 0)
        diff = abs(p_empirical - p_theoretical)  
        max_diff = max(max_diff, diff)  
    return max_diff


# Параметры эксперимента
experiments = 1000  # Количество экспериментов
p = 0.5  # Вероятность успеха
k = 3  # Количество успехов (орлов)

res = generate_sample(k, p, experiments)# Генерация ресультата эксперементов

sorted_val = dict(sorted(res.items()))  # Сортировка по ключам

# Вывод таблицы с отклонениями
print_table_with_deviations(sorted_val, experiments, k, p)

# Вычисление выборочных характеристик
mean, variance, range_, median = sample_statistics(sorted_val, experiments)

# Вычисление теоретических характеристик
theoretical_mean, theoretical_variance = theoretical_statistics(k, p)

# Вывод таблицы характеристик
print(f"\nТаблица характеристик:")
print(f"{'':<20}{'Выборочное':<15}{'Теоретическое':<15}{'Разница':<15}")
print(f"{'Среднее':<20}{mean:<15}{theoretical_mean:<15}{abs(mean - theoretical_mean):<15}")
print(f"{'Дисперсия':<20}{variance:<15}{theoretical_variance:<15}{abs(variance - theoretical_variance):<15}")
print(f"{'Размах':<20}{range_:<15}{'-':<15}{'-':<15}")
print(f"{'Медиана':<20}{median:<15}{'-':<15}{'-':<15}")

# Построение функции распределения
empirical, theoretical = plot_empirical_distribution(res, k, p)

# Вычисление максимальной разницы между теоретической и выборочной функциями распределения
D = max_difference(empirical, theoretical)
print(f"\nМера расхождения графиков теоретической и выборочной функции распределения: {D}")



