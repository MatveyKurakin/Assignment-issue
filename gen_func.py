import numpy as np
from scipy.optimize import linear_sum_assignment
def create_x(n, x_min, x_max):
    x = np.random.uniform(x_min, x_max, size=n)
    x = np.round(x, 2)
    return x

def create_c(n, c_min, c_max):
    c = np.random.uniform(c_min, c_max, size=(n, n))
    c = np.round(c, 2)
    return c

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
    c = create_c(4, 100, 200)
    x = create_x(4,0,1)
    print("c:\n", c)
    print("x =", x)
    d, potential_profit = create_d(c, x)
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