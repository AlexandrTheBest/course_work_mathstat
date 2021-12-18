import math

from hw_2 import Poisson
from hw_3 import poisson_evaluation_by_the_method_of_moments  # Выборочное среднее
import scipy.stats as scs

poisson_4_5 = Poisson(theta=4.5)
poisson_7 = Poisson(theta=7)

all_t_a = {5: 6.2,
           10: 5.6,
           100: 4.85,
           200: 4.75,
           400: 4.675,
           600: 4.64333,
           800: 4.62375,
           1000: 4.611,
           20000: 4.5247,
           100000: 4.51104}
with open('poisson_hw_5.txt', 'w', encoding='utf-8') as write_file:
    write_file.write('Theta = 4.5\n')
    for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
        xx = poisson_evaluation_by_the_method_of_moments(poisson_4_5.generate_sampling(n))
        t_a = all_t_a[n]
        write_file.write('N = {:<6d} | X = {:<6f} | tα = {:<6f} | {}\n'.format(
            n,
            xx,
            t_a,
            'Theta = 4.5' if xx < t_a else 'Theta = 7'))
        print('N = {:<6d} | X = {:<6f} | tα = {:<6f} | {}\n'.format(
            n,
            xx,
            t_a,
            'Theta = 4.5' if xx < t_a else 'Theta = 7'))

    write_file.write('\n\nTheta = 7\n')
    for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
        xx = poisson_evaluation_by_the_method_of_moments(poisson_7.generate_sampling(n))
        t_a = all_t_a[n]
        write_file.write('N = {:<6d} | X = {:<6f} | tα = {:<6f} | {}\n'.format(
            n,
            xx,
            t_a,
            'Theta = 4.5' if xx < t_a else 'Theta = 7'))
        print('N = {:<6d} | X = {:<6f} | tα = {:<6f} | {}\n'.format(
            n,
            xx,
            t_a,
            'Theta = 4.5' if xx < t_a else 'Theta = 7'))

theta_0 = 4.5
theta_1 = 7
with open('poisson_min_n_with_a_b.txt', 'w', encoding='utf-8') as write_file:
    for a in [0.1, 0.05, 0.02, 0.01, 0.005]:
        t_a = scs.norm.ppf(a, loc=0, scale=1)
        t_b = scs.norm.ppf(1 - a, loc=0, scale=1)
        n = math.ceil(((math.sqrt(theta_1) * (t_b - t_a * math.sqrt(theta_0 / theta_1))) / (theta_0 - theta_1)) ** 2)
        write_file.write('Alpha = {:<5.3f} | Beta = {:<5.3f} | min(n) = {:<6d}\n'.format(a, a, n))
