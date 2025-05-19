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
    # cost_cT = cT
    cost_cT = max_cT - cT
    row_ind, col_ind = linear_sum_assignment(cost_cT)
    x = np.zeros(c.shape)
    x[col_ind[:], row_ind[:]] = 1
    return x

def veng_min(c):
    cT = c.T
    max_cT = np.max(cT)
    cost_cT = cT
    row_ind, col_ind = linear_sum_assignment(cost_cT)
    x = np.zeros(c.shape)
    x[col_ind[:], row_ind[:]] = 1
    return x

def create_g_max(c, d, l):
    g = np.array(c.copy(), dtype=np.float64)
    for i in range(d.shape[0]):
        g -= d[i] * l[i]
    return g

def create_g_min(c, d, l):
    g = np.array(c.copy(), dtype=np.float64)
    for i in range(d.shape[0]):
        g += d[i] * l[i]
    return g

def create_w(d, x, b):
    w = np.zeros(d.shape[0])
    for i in range(d.shape[0]):
        w[i] = np.sum(d[i] * x) - b[i]
    return w

def main(n, k, n_0, n_max, c, d, b, l):
    for i in range(n_0, n_max):
        g = create_g_max(c, d, l)
        x = veng_max(g)
        w = create_w(d, x, b)
        if(np.sum(np.abs(w))<0.01):
            break
        w[w < 0] = 0
        l = l + 1 * w
    return np.sum(c * x), x


def main_1_max(n, k, n_0, n_max, c, d, b, l):
    max_sum = 0
    x_max_sum = np.zeros(c.shape)
    iter_max_sum = 0
    is_exists = False

    for i in range(n_0, n_max):
        g = create_g_max(c, d, l)
        x = veng_max(g)
        w = create_w(d, x, b)
        l = l + 1 * w
        l[l < 0] = 0
        if np.any(w > 0):
            continue
        if np.sum(c * x) > max_sum:
            max_sum = np.sum(c * x)
            x_max_sum = x
            iter_max_sum = i
            is_exists = True
        if (np.sum(np.abs(w)) < 0.001):
            break
    return max_sum, x_max_sum, iter_max_sum, is_exists

def main_phi_max(n, k, n_0, n_max, c, d, b, l):
    max_sum = 0
    x_max_sum = np.zeros(c.shape)
    iter_max_sum = 0
    is_exists = False

    for i in range(n_0, n_max):
        g = create_g_max(c, d, l)
        x = veng_max(g)
        w = create_w(d, x, b)
        phi = 1/(i+1)
        l = l + phi * w
        l[l < 0] = 0
        if np.any(w > 0):
            continue
        if np.sum(c * x) > max_sum:
            max_sum = np.sum(c * x)
            x_max_sum = x
            iter_max_sum = i
            is_exists = True
        if (np.sum(np.abs(w)) < 0.001):
            break
    return max_sum, x_max_sum, iter_max_sum, is_exists

def main_1_min(n, k, n_0, n_max, c, d, b, l):
    min_sum = 10**9
    x_min_sum = np.zeros(c.shape)
    iter_min_sum = 0
    is_exists = False

    for i in range(n_0, n_max):
        g = create_g_min(c, d, l)
        x = veng_min(g)
        w = create_w(d, x, b)
        l = l + 1 * w
        l[l < 0] = 0
        if np.any(w > 0):
            continue
        if np.sum(c * x) < min_sum:
            min_sum = np.sum(c * x)
            x_min_sum = x
            iter_min_sum = i
            is_exists = True
        if (np.sum(np.abs(w)) < 0.001):
            break
    return min_sum, x_min_sum, iter_min_sum, is_exists

def main_phi_min(n, k, n_0, n_max, c, d, b, l):
    min_sum = 10**9
    x_min_sum = np.zeros(c.shape)
    iter_min_sum = 0
    is_exists = False

    for i in range(n_0, n_max):
        g = create_g_min(c, d, l)
        x = veng_min(g)
        w = create_w(d, x, b)
        phi = 1 / (i + 1)
        l = l + phi * w
        l[l < 0] = 0
        if np.any(w > 0):
            continue
        if np.sum(c * x) < min_sum:
            min_sum = np.sum(c * x)
            x_min_sum = x
            iter_min_sum = i
            is_exists = True
        if (np.sum(np.abs(w)) < 0.001):
            break
    return min_sum, x_min_sum, iter_min_sum, is_exists

if __name__ == "__main__":
    n = 4
    k = 2
    n_max = 10
    n_0 = 0
    #phi = 1/(n_0+1)
    c = np.array([[5, 4, 3, 6],
                  [3, 5, 3, 3],
                  [3, 4, 5, 3],
                  [3, 2, 5, 5]])
    d = np.array([[[2, 1, 2, 1],
                   [1, 0, 1, 1],
                   [0, 0, 2, 1],
                   [0, 0, 0, 1]],
                  [[2, 1, 2, 1],
                   [1, 1, 1, 1],
                   [2, 0, 0, 1],
                   [2, 0, 1, 1]]
                  ])
    b = np.array([4, 3])
    l = np.array([1, 1])
    '''
    c = np.array([[5, 4, 3],
                [4, 5, 3],
                [3, 4, 5]
                ])
    d = np.array([[[2, 1, 2],
                   [1, 1, 1],
                   [0, 0, 0],
                   ]])
    b = np.array([2])
    l = np.array([1])'''
    print(main_1_max(n, k, n_0, n_max, c, d, b, l))
    print(main_phi_max(n, k, n_0, n_max, c, d, b, l))
    print(main_1_min(n, k, n_0, n_max, c, d, b, l))
    print(main_phi_min(n, k, n_0, n_max, c, d, b, l))