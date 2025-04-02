import matplotlib as plt
import random
import numpy as np
import scipy.stats as stats
from scipy.stats import nbinom



def generate_sample(n, p, experiments):
    res = []  # значения случайной величины в экспериментах
    for _ in range(experiments):
        successes = 0
        nu = 0  # Случайная величина (количество испытаний)
        while successes < n:
            nu += 1
            u = random.random()
            if u < p:
                successes += 1
        res.append(nu)
    res = sorted(res)
    return res


def criterion_test(generated_sample, k, alpha, p, n): #функция проверки гипотезы, alpha - вероятность ошибки первого рода
                                                #(упорядоченный набор значений случайной величины, кол во интервалов, уровень значимости)
    perc = np.linspace(0, 100, k+1) #вычисление перцентилей для разбиения данных на интервалы (k+1 включает 0 и 100)
    perc = perc[1:-1]
    intervals = np.percentile(generated_sample, perc) # вычисляет границы интервалов
    intervals = np.concatenate(([-np.inf], intervals, [np.inf])) #добавление первого и последнего интервала   
    frequency = np.histogram(generated_sample, bins = intervals)[0] #считает частоту попадания значений в каждый интервал, граница включается в правый
    
    cdf_vals = nbinom.cdf(intervals - n - 1, n, p) #вычисляется значение теоретической функции распределения в границах интервалов
    int_prob = np.diff(cdf_vals)#вычисляются вероятности попадания в каждый интервал (разность между значениями функции распределения)
    teoretic_freq = int_prob * len(generated_sample) #теоретические частоты
    
    mask = teoretic_freq != 0
    r0 = np.sum((frequency[mask] - teoretic_freq[mask]) ** 2 / teoretic_freq[mask])  #мера расхождения частот
    
    F = 1 - stats.chi2.cdf(r0, df=k-1) #значение обратной функции распредеения хи в точке R0
    
    return int_prob, intervals, F, F <= alpha
    

    