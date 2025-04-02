from statistical_test_realization import *

#проверка эксперемента через порог уровня значимости
res=0
for i in range (100):
    k=4
    generated_sample = generate_sample(2, 0.5, 1000) #список
    sample = np.array(generated_sample)
    # Выполняем хи-квадрат тест
    _, _, _, not_accept_h0 = criterion_test (sample, k, 0.05, 0.5, 2)
    if not_accept_h0 == True:
        res += 1
        
print(res)