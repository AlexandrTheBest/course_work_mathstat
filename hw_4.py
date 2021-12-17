import numpy as np
import scipy.stats as scs


def kolmogorov_uniform(selection, lamb, theta=16, a=7.2):
    size = len(selection)
    sorted_selection = sorted(selection)
    D_n_plus = []
    D_n_minus = []

    for k in range(1, size + 1):
        F_x = scs.uniform.cdf(sorted_selection[k - 1], loc=a, scale=theta)
        D_n_plus.append(np.abs(k / size - F_x))
        D_n_minus.append(np.abs(F_x - (k - 1) / size))

    D_n = max(max(D_n_plus), max(D_n_minus))
    if size < 20:
        S_n = (6 * size * D_n + 1) / (6 * np.sqrt(size))
    else:
        S_n = np.sqrt(size) * D_n

    if S_n >= lamb:
        return '\\(S_{\\chi^2} = ' + f'{S_n}\\). Отвергаем'
    else:
        return '\\(S_{\\chi^2} = ' + f'{S_n}\\). Принимаем'


S_CHI = [3.841,
         5.991,
         7.815,
         9.488,
         11.070,
         12.592,
         14.067,
         15.507,
         16.919,
         18.307,
         19.675,
         21.026,
         22.362,
         23.685,
         24.996,
         26.296,
         27.587]


def chi_square_uniform(selection, theta=16, a=7.2):
    N = len(selection)
    sorted_selection = sorted(selection)
    k = int(1 + np.floor(np.log2(N)))
    all_n_i = [0] * k
    step = theta / k
    for i in range(k):
        for x in sorted_selection:
            if a + step * i <= x < a + step * (i + 1):
                all_n_i[i] += 1

    P_i = 1 / k
    S_chi = 0
    for i in range(k):
        S_chi += (((all_n_i[i] / N) - P_i) ** 2) / P_i
    S_chi *= N
    if S_chi > S_CHI[k - 1]:
        return '\\(S_{\\chi^2} = ' + f'{S_chi}\\). Отвергаем'
    else:
        return '\\(S_{\\chi^2} = ' + f'{S_chi}\\). Принимаем'


def chi_square_poisson(selection, theta=4.5):
    N = len(selection)
    sorted_selection = sorted(selection)
    k = int(1 + np.floor(np.log2(N)))
    all_n_i = [0] * k
    all_P_i = []
    step = max(sorted_selection) / k

    for i in range(k):
        all_P_i += [
            scs.poisson.cdf(step * (i + 1), mu=theta) - scs.poisson.cdf(-1 if i == 0 else step * i, mu=theta)]
        for x in sorted_selection:
            if step * i <= x < step * (i + 1):
                all_n_i[i] += 1
            if i == k - 1 and x == step * (i + 1):
                all_n_i[i] += 1

    all_P_i[k - 1] = 1 - scs.poisson.cdf(step * (k - 1), mu=theta)
    S_chi = 0
    for i in range(k):
        S_chi += (((all_n_i[i] / N) - all_P_i[i]) ** 2) / all_P_i[i]
    S_chi *= N
    if S_chi > S_CHI[k - 1]:
        return '\\(S_{\\chi^2} = ' + f'{S_chi}\\). Отвергаем'
    else:
        return '\\(S_{\\chi^2} = ' + f'{S_chi}\\). Принимаем'


def poisson_maximum_likelihood_estimation(selection: list):
    return sum(selection) / len(selection)


def uniform_maximum_likelihood_estimation(selection: list, a=7.2):
    return max(selection) - a


def kolmogorov_complex_uniform(selection, lamb):
    selection_theta = selection[::2]
    selection_kolmogorov = selection[1::2]
    theta = uniform_maximum_likelihood_estimation(selection_theta)
    return kolmogorov_uniform(selection_kolmogorov, theta=theta, lamb=lamb)


def chi_square_complex_poisson(selection):
    selection_theta = selection[::2]
    selection_chi_square = selection[1::2]
    theta = poisson_maximum_likelihood_estimation(selection_theta)
    return chi_square_poisson(selection_chi_square, theta=theta)


def chi_square_complex_uniform(selection):
    selection_theta = selection[::2]
    selection_chi_square = selection[1::2]
    theta = uniform_maximum_likelihood_estimation(selection_theta)
    return chi_square_uniform(selection_chi_square, theta=theta)


def uniformity_criterion(d_data, lamb):
    return_data = ''
    try:
        while True:
            n = d_data.pop(0)
            m = d_data.pop(0)
            D = d_data.pop(0) * (np.sqrt((n + m) / (n * m)))
            t_lamb = np.sqrt((1 / n) + (1 / m)) * lamb
            if D > t_lamb:
                return_data += 'n = {:6d} | m = {:6d} | D = {:6.4f} | t = {:6.4f} | Reject.\n'.format(int(n), int(m), D,
                                                                                                      t_lamb)
            else:
                return_data += 'n = {:6d} | m = {:6d} | D = {:6.4f} | t = {:6.4f} | Not reject.\n'.format(int(n),
                                                                                                          int(m), D,
                                                                                                          t_lamb)
    except IndexError:
        return return_data


# Открываем файлы для записи результатов
# with open('uniform_kolmomgorov_simple.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 16; \\lambda_\\alpha = 1.36\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'uniform_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [float(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, kolmogorov_uniform(data, lamb=1.36)))
#
# with open('uniform_chi_square_simple.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 16\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'uniform_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [float(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, chi_square_uniform(data)))
#
# with open('poisson_chi_square_simple.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 4.5\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'poisson_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [int(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, chi_square_poisson(data)))
#
# with open('uniform_kolmogorov_complex.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 16; \\lambda_\\alpha = 1.36\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'uniform_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [float(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, kolmogorov_complex_uniform(data, lamb=1.36)))
#
# with open('poisson_chi_square_complex.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 4.5\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'poisson_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [int(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, chi_square_complex_poisson(data)))
#
# with open('uniform_chi_square_complex.txt', 'w', encoding='utf-8') as write_file:
#     write_file.write('\\(\\theta = 16\\)\\\\\n')
#     # Проходимся по всем файлам с выборками объемов n
#     for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
#         with open(f'uniform_n_{n}.txt', 'r', encoding='utf-8') as read_file:
#             # Читаем выборки, преобразуя их в список чисел
#             data = [float(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]
#             write_file.write('Выборка объема {:^6d} - {}\\\\\n'.format(n, chi_square_complex_uniform(data)))

with open('poisson_uniformity_criterion.txt', 'w', encoding='utf-8') as write_file:
    with open(f'poisson_D_n_m.txt', 'r', encoding='utf-8') as read_file:
        # Читаем выборки, преобразуя их в список чисел
        data = [float(x) for xx in read_file.read().replace('n =', '').replace('| m =', '').replace('| D =', '').split()
                for x in xx.split('&')]
        write_file.write(uniformity_criterion(data, lamb=1.36))

with open('uniform_uniformity_criterion.txt', 'w', encoding='utf-8') as write_file:
    with open(f'uniform_D_n_m.txt', 'r', encoding='utf-8') as read_file:
        # Читаем выборки, преобразуя их в список чисел
        data = [float(x) for xx in read_file.read().replace('n =', '').replace('| m =', '').replace('| D =', '').split()
                for x in xx.split('&')]
        write_file.write(uniformity_criterion(data, lamb=1.36))
