import numpy as np
from scipy.optimize import linear_sum_assignment

'''
программа с мега интерфейсом
вводится матрица и вектор
считается матрица d~ и g
считается S3 и S1
все выводится красиво
жадный к d~ и g
венгеркий к g
выводится результат
размер N на N заполняется автоматически, N<=15
2 галочки элементы матрица по строкам и столбцам убывают или возрастают
в c максимум двузначные целые, чтобы красиво вывести
'''

def create_x(n, x_min=0, x_max=1):
    x = np.random.uniform(x_min, x_max, size=n)
    x = np.round(x, 2)
    return x

def create_c(n, c_min=10, c_max=100):
    c = np.random.randint(c_min, c_max, size=(n, n))
    return c

def increase_by_row(c):
    return np.sort(c, axis=1)

def increase_by_col(c):
    return np.sort(c, axis=0)

def de_increase_by_row(c):
    return np.sort(c, axis=1)[:, ::-1]

def de_increase_by_col(c):
    return np.sort(c, axis=0)[::-1]

def create_g(c, x):
    potential_profit=0
    d = np.zeros(c.shape)
    for i in range(c.shape[0]):
        for j in range(c.shape[1] - 1, -1, -1):
            potential_profit += x[i] * c[i][j]
            if(j == c.shape[1] - 1):
                d[i][j] = (1 - x[i]) * c[i][j]
            else:
                d[i][j] = d[i][j+1] + (1 - x[i]) * c[i][j]
    return d, potential_profit

def create_d(c, x):
    potential_profit=0
    d = np.zeros(c.shape)
    for i in range(c.shape[0]):
        for j in range(c.shape[1] - 1, -1, -1):
            potential_profit += x[i] * c[i][j]
            if(j == c.shape[1] - 1):
                d[i][j] = (1 - x[i]) * c[i][j]
            else:
                d[i][j] = d[i][j+1] + (1 - x[i]) * c[i][j]
    return d, potential_profit

def veng_max(d):
    dT = d.T
    max_dT = np.max(dT)
    cost_dT = max_dT - dT
    row_ind, col_ind = linear_sum_assignment(cost_dT)
    return col_ind, row_ind

def greedy(d):
    dT = d.T
    col_ind = []
    for j in range(dT.shape[0]):
        max_dT = 0
        max_dT_ind = 0
        for i in range(dT.shape[1]):
            if i not in col_ind and dT[j][i] > max_dT:
                max_dT = dT[j][i]
                max_dT_ind = i
        col_ind.append(max_dT_ind)
    return col_ind, np.arange(0, dT.shape[0])

def main():
    c = create_c(4, 10, 100)
    x = create_x(4,0,1)
    print("c:\n", c)
    print("x =", x)
    d, potential_profit = create_g(c, x)
    print("d:\n", d)
    print("t_sum =", potential_profit)

    row_ind, col_ind = veng_max(d)
    res = np.zeros(d.shape)
    total = potential_profit
    for i in range(len(row_ind)):
        res[row_ind[i]][col_ind[i]] = 1
        total += d[row_ind[i]][col_ind[i]]
    print("res:\n", res)
    print("total =", total)

if __name__ == "__main__":
    main()