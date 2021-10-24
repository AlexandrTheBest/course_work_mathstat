import math
import random
import numpy as np
import matplotlib.pyplot as plt


class MyRandom:
    theta = None
    is_discrete = None

    def __init__(self, theta):
        self.theta = theta

    def generate_number(self):
        pass

    def generate_sampling(self, size):
        sampling = list()
        for i in range(size):
            sampling += [self.generate_number()]
        return sampling

    def plot_distribution_function(self):
        pass

    def plot_probability_function(self):
        pass

    def plot_frequency_polygon(self, data: list, file_name):
        if self.is_discrete:
            x_list = data
            frequency = []
            for x in data:
                frequency += [data.count(x) / len(data)]
        else:
            data = sorted(list(set(data)))
            N = self.theta * 5
            delta = (data[-1] - data[0]) / N

            left = data[0]
            right = data[0] + delta
            count = 0
            x_list = []
            frequency = []
            i = 0
            while i <= len(data):
                if i < len(data) and left <= data[i] < right:
                    count += 1
                    i += 1
                else:
                    x_list.append((left + right) / 2)
                    frequency.append(count / (len(data) * delta))
                    if i == len(data):
                        break
                    else:
                        count = 0
                        left = right
                        right = right + delta

        plt.plot(x_list, frequency, label='полигон частот')
        plt.legend()
        plt.xlabel('x')
        plt.savefig(file_name, dpi=400, bbox_inches='tight')
        plt.close()

    @staticmethod
    def to_latex(sampling):
        latex_data = str()
        for i, x in enumerate(sampling):
            latex_data += f'{x}&'
            if (i + 1) % 10 == 0:
                latex_data += '\n'
        latex_data = latex_data[:-1] + '\\\\\n'
        return latex_data

    @staticmethod
    def plot_empirical_function(sample, file_name):
        sample.sort()
        new_sample = list()

        for i in sample:
            if i not in new_sample:
                new_sample.append(i)

        Y = 0
        plt.plot([new_sample[0] - 0.1, new_sample[0]], [0, 0], c="blue", label=r'$\mathscr{F}_n(t)$')
        for i in range(len(new_sample)):
            Y += sample.count(new_sample[i]) / len(sample)
            plt.plot([new_sample[i], new_sample[i] + 0.1 if i == len(new_sample) - 1 else new_sample[i + 1]], [Y, Y],
                     c="blue")
        # plt.show()
        plt.legend()
        plt.xlabel('x')
        plt.savefig(file_name, dpi=400, bbox_inches='tight')
        plt.close()


class Poisson(MyRandom):
    is_discrete = True

    def generate_number(self):
        exp_value = math.exp(-self.theta)
        x = 0
        prod = random.random()  # random.uniform(0, 1)
        while prod > exp_value:
            prod *= random.random()
            x += 1
        return x

    def plot_distribution_function(self):
        x_list = np.linspace(0, 2.5 * self.theta, 50)
        y_list = []
        for x in x_list:
            x = math.ceil(x)
            sum = 0
            for i in range(x):
                sum += (self.theta ** i) * math.exp(-self.theta) / math.factorial(i)
            y_list += [sum]

        plt.plot([x_list[0] - 0.1, x_list[0]], [0, 0], c="red", label=r'$F(t)$')
        for i in range(len(x_list)):
            Y = y_list[i]
            plt.plot([x_list[i], x_list[i] + 0.1 if i == len(x_list) - 1 else x_list[i + 1]], [Y, Y],
                     c="red")

    def plot_probability_function(self):
        x_list = range(math.floor(2.5 * self.theta))
        y_list = []
        for x in x_list:
            x = math.floor(x)
            y_list += [(self.theta ** x) * math.exp(-self.theta) / math.factorial(x)]

        plt.plot(x_list, y_list, c="red", label=r'$f(t)$')


class Uniform(MyRandom):
    a = None
    is_discrete = False

    def __init__(self, theta, a):
        super().__init__(theta)
        self.a = a

    def generate_number(self):
        return random.random() * self.theta + self.a

    def plot_distribution_function(self):
        x_list = [0, self.a, self.a + self.theta, self.a + self.theta + 2]
        y_list = [0, 0, 1, 1]
        plt.plot(x_list, y_list, c="red", label=r'$F(t)$')

    def plot_probability_function(self):
        x_list = [0, self.a]
        y_list = [0, 0]
        plt.plot(x_list, y_list, c="red", label=r'$f(t)$')
        x_list = [self.a, self.a + self.theta]
        y_list = [1 / self.theta, 1 / self.theta]
        plt.plot(x_list, y_list, c="red")
        x_list = [self.a + self.theta, self.a + self.theta + 2]
        y_list = [0, 0]
        plt.plot(x_list, y_list, c="red")


def hw_2():
    theta_poisson = 4.5
    theta_uniform = 16
    a_uniform = 7.2
    n_list = [5, 10, 100, 200, 400, 600, 800, 1000, 20000, 100000]
    poisson = Poisson(theta_poisson)
    uniform = Uniform(theta_uniform, a_uniform)
    poisson_empirical_values = {}
    uniform_empirical_values = {}
    for n in n_list:
        with open(f'poisson_n_{n}.txt', "w", encoding='utf-8') as write_file:
            sampling = poisson.generate_sampling(n)
            write_file.write(poisson.to_latex(sampling))
            write_file.close()
        poisson_empirical_values[n] = sampling
        poisson.plot_distribution_function()
        poisson.plot_empirical_function(sampling, f'poisson_n_{n}.png')
        poisson.plot_frequency_polygon(sampling, f'poisson_polygon_n_{n}.png')
        poisson.plot_probability_function()
        poisson.plot_frequency_polygon(sampling, f'poisson_polygon_probability_n_{n}.png')

    with open(f'poisson_D_n_m.txt', "w", encoding='utf-8') as write_file:
        for n in n_list:
            for m in n_list:
                max_deviation = 0
                for x in np.linspace(0, 2.5 * theta_poisson, 50):
                    f_n = len([item for item in poisson_empirical_values[n] if item < x]) / n
                    f_m = len([item for item in poisson_empirical_values[m] if item < x]) / m
                    if abs(f_n - f_m) > max_deviation:
                        max_deviation = abs(f_n - f_m)

                write_file.write(
                    'n = {:6d} | m = {:6d} | D = {:10.8f}\n'.format(n, m, math.sqrt((n * m) / (n + m)) * max_deviation))

    with open(f'poisson_X_S.txt', "w", encoding='utf-8') as write_file:
        for n in n_list:
            sample_average = 0
            for x in poisson_empirical_values[n]:
                sample_average += x
            sample_average /= n

            sample_variance = 0
            for x in poisson_empirical_values[n]:
                sample_variance += (x - sample_average) ** 2
            sample_variance /= n

            write_file.write(f'{n}&{sample_average}&{sample_variance}\\\\\n')

    for n in n_list:
        with open(f'uniform_n_{n}.txt', "w", encoding='utf-8') as write_file:
            sampling = uniform.generate_sampling(n)
            write_file.write(uniform.to_latex(sampling))
            write_file.close()
        uniform_empirical_values[n] = sampling
        uniform.plot_distribution_function()
        uniform.plot_empirical_function(sampling, f'uniform_n_{n}.png')
        uniform.plot_frequency_polygon(sampling, f'uniform_polygon_n_{n}.png')
        uniform.plot_probability_function()
        uniform.plot_frequency_polygon(sampling, f'uniform_polygon_probability_n_{n}.png')

    with open(f'uniform_D_n_m.txt', "w", encoding='utf-8') as write_file:
        for n in n_list:
            for m in n_list:
                max_deviation = 0
                for x in np.linspace(0, a_uniform + theta_uniform + 2, 50):
                    f_n = len([item for item in uniform_empirical_values[n] if item < x]) / n
                    f_m = len([item for item in uniform_empirical_values[m] if item < x]) / m
                    if abs(f_n - f_m) > max_deviation:
                        max_deviation = abs(f_n - f_m)

                write_file.write(
                    'n = {:6d} | m = {:6d} | D = {:10.8f}\n'.format(n, m, math.sqrt((n * m) / (n + m)) * max_deviation))

    with open(f'uniform_X_S.txt', "w", encoding='utf-8') as write_file:
        for n in n_list:
            sample_average = 0
            for x in uniform_empirical_values[n]:
                sample_average += x
            sample_average /= n

            sample_variance = 0
            for x in uniform_empirical_values[n]:
                sample_variance += (x - sample_average) ** 2
            sample_variance /= n

            write_file.write(f'{n}&{sample_average}&{sample_variance}\\\\\n')


hw_2()
