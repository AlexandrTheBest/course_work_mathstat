# Функции подсчета оценок для распределения Пуассона
def poisson_evaluation_by_the_method_of_moments(selection: list):
    return sum(selection) / len(selection)


def poisson_maximum_likelihood_estimation(selection: list):
    return sum(selection) / len(selection)


def poisson_optimal_estimation(selection: list):
    return sum(selection) / len(selection)


# Функции подсчета оценок для равномерного распределения II
def uniform_evaluation_by_the_method_of_moments(selection: list, a=7.2):
    return 2 * (sum(selection) / len(selection) - a)


def uniform_maximum_likelihood_estimation(selection: list):
    return max(selection)


def uniform_optimal_estimation(selection: list):
    return ((len(selection) + 1) / len(selection)) * max(selection)


# Открываем файл для записи результатов вычисления оценок
with open('poisson_estimations.txt', 'w', encoding='utf-8') as write_file:
    write_file.write('~~~~~~~~~~~~~~~~~~~~~θ = 4.5~~~~~~~~~~~~~~~~~~~~~\n')
    # Проходимся по всем файлам с выборками объемов n
    for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
        with open(f'poisson_n_{n}.txt', 'r', encoding='utf-8') as read_file:
            # Читаем выборки, преобразуя их в список чисел
            data = [int(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]

            write_file.write('╔===============================================╗\n'
                             '║             ВЫБОРКА ОБЪЕМА {:^6d}             ║\n'
                             '╠===============================================╣\n'
                             '║Метод моментов:                      θ = {:<6f}║\n'
                             '║Метод максимального правдоподобия:   θ = {:<6f}║\n'
                             '║Оптимальная оценка:                  θ = {:<6f}║\n'
                             '╚===============================================╝\n\n'.format(
                n,
                poisson_evaluation_by_the_method_of_moments(data),
                poisson_maximum_likelihood_estimation(data),
                poisson_optimal_estimation(data)
            ))

# Открываем файл для записи результатов вычисления оценок
with open('uniform_estimations.txt', 'w', encoding='utf-8') as write_file:
    write_file.write('~~~~~~~~~~~~~~~~~a = 7.2, θ = 16~~~~~~~~~~~~~~~~~\n')
    # Проходимся по всем файлам с выборками объемов n
    for n in [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]:
        with open(f'uniform_n_{n}.txt', 'r', encoding='utf-8') as read_file:
            # Читаем выборки, преобразуя их в список чисел
            data = [float(x) for xx in read_file.read().replace(r'\\', '').split() for x in xx.split('&')]

            write_file.write('╔===============================================╗\n'
                             '║             ВЫБОРКА ОБЪЕМА {:^6d}             ║\n'
                             '╠===============================================╣\n'
                             '║Метод моментов:                      θ = {:<6f}║\n'
                             '║Метод максимального правдоподобия:   θ = {:<6f}║\n'
                             '║Оптимальная оценка:                  θ = {:<6f}║\n'
                             '╚===============================================╝\n\n'.format(
                n,
                uniform_evaluation_by_the_method_of_moments(data),
                uniform_maximum_likelihood_estimation(data),
                uniform_optimal_estimation(data)
            ))
