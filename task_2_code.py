import numpy as np
import matplotlib.pyplot as plt
import os
import requests
from scipy.special import spherical_jn, spherical_yn

#Вычисление ЭПР 
class RCS:  
    
    def __init__(self, radius):
        self.radius = radius

    def calculate_rcs(self, f):
        wavelength = 3e8 / f
        k = 2 * np.pi / wavelength
        kr = k * self.radius

        def h_func(n, x):
            return spherical_jn(n, x) + 1j * spherical_yn(n, x)

        def a_func(n, kr):
            return spherical_jn(n, kr) / h_func(n, kr)

        def b_func(n, kr):
            b_numerator = kr * spherical_jn(n-1, kr) - n * spherical_jn(n, kr)
            b_denominator = kr * h_func(n-1, kr) - n * h_func(n, kr)
            return b_numerator / b_denominator

        result = 0
        for n in range(1, 30):
            term = ((-1) ** n) * (n + 0.5) * (b_func(n, kr) - a_func(n, kr))
            result += term

        return (wavelength ** 2 / np.pi) * (np.abs(result)**2)

#класс записи результата
class Output_results:
    
 
    def save_results(filename, f_values, results):
        with open(filename, 'w') as file:
            file.write('     f            rcs\n')
            for x, y in zip(f_values, results):
                file.write(f'{x:.4f}    {y:.4f}\n')

url = "https://jenyay.net/uploads/Student/Modelling/task_rcs_01.txt"
response = requests.get(url)
with open('file.txt', 'wb') as file:
    file.write(response.content)

with open('file.txt') as f:
    M = f.read().split()

D = float(M[61].strip('D=;'))
fmin = float(M[62].strip('fmin=;'))
fmax = float(M[63].strip('fmax=;'))

f = np.linspace(fmin, fmax, num=300)
rcs_calculator = RCS(D / 2)
results = []

for F in f:
    rcs = rcs_calculator.calculate_rcs(F)
    results.append(rcs)

if not os.path.exists('results'):
    os.makedirs('results')

Output_results.save_results('results/results.txt', f, results)

plt.plot(f, results)
plt.title('Задание №2')
plt.xlabel('f')
plt.ylabel('ЭПР')
plt.grid(True)
plt.show()
