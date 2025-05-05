import numpy as np
from scipy.optimize import linear_sum_assignment

M = 10**9
K = 0

def create_c(n, c_min=10, c_max=100):
    c = np.random.randint(c_min, c_max, size=(n, n))
    return c

def create_d(n, k, d_min=10, d_max=100):
    d = np.random.randint(d_min, d_max, size=(k, n, n))
    return d

def create_b(k = 1, b_max = 10):
    return np.random.randint(1, b_max, size=(k))

def increase_by_row(c):
    return np.sort(c, axis=1)

def increase_by_col(c):
    return np.sort(c, axis=0)

def de_increase_by_row(c):
    return np.sort(c, axis=1)[:, ::-1]

def de_increase_by_col(c):
    return np.sort(c, axis=0)[::-1]

def summ_perm(c, perm_1, perm_2):
    n = c.shape[0]
    sum = 0
    for i in range(n):
        for j in range(n):
            if(perm_1[j] == i or perm_2[j] == i):
                sum += c[i][j]
    return sum

def veng_max(c):
    cT = c.T
    max_cT = np.max(cT)
    cost_cT = cT
    cost_cT = max_cT - cT
    row_ind, col_ind = linear_sum_assignment(cost_cT)
    x = np.zeros(c.shape)
    x[col_ind[:], row_ind[:]] = 1
    return x

def create_g(c, d, l):
    g = np.array(c.copy(), dtype=np.float64)
    for i in range(d.shape[0]):
        g -= d[i] * l[i]
    return g

def create_w(d, x, b):
    w = np.zeros(d.shape[0])
    for i in range(d.shape[0]):
        w[i] = np.sum(d[i] * x) - b[i]
    return w

def main(n, k, n_max, c, d, b, l):
    for i in range(n_max):
        g = create_g(c, d, l)
        x = veng_max(g)
        w = create_w(d, x, b)
        if(np.sum(np.abs(w))<0.01):
            break
        w[w < 0] = 0
        l = l + 1 * w
    return np.sum(c * x), x


if __name__ == "__main__":
    n = 4
    k = 1
    n_max = 10
    c = np.array([[2,3,1,4],
                  [5,2,6,3],
                  [7,1,4,2],
                  [3,4,5,6]])
    d = np.array([[[1,0,0,0],
                  [0,1,0,0],
                  [0,0,0,0],
                  [0,0,0,0]]])
    b = np.array([1])
    l = np.array([1])
    x = main(n, k, n_max, c, d, b, l)
    print(x)