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
        #print(np.where(d[i] * x>0)[0])
        #print(np.where(d[i] * x>0)[1])
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
    #x = np.zeros(c.shape)
    iter_min_sum = 0
    is_exists = False
    #g = create_g_min(c, d, l)
    #x_first = veng_min(g)

    for i in range(n_0, n_max):
        g = create_g_min(c, d, l)
        #print("---")
        #print(np.where(x>0)[1])
        #print(g[np.where(x>0)])
        x = veng_min(g)
        #print(np.where(x > 0)[1])
        #print(g[np.where(x > 0)])
        w = create_w(d, x, b)
        l = l + 1 * w
        l[l < 0] = 0
        #print(np.sum(c * x), l, w)
        if np.any(w > 0):
            #print("BAD")
            continue
        if np.sum(c * x) < min_sum:
            min_sum = np.sum(c * x)
            x_min_sum = x
            iter_min_sum = i
            is_exists = True
        if (np.sum(np.abs(w)) < 0.001):
            break
    #print("===")
    #print(g[np.where(x_min_sum > 0)])
    #print(g[np.where(x_first > 0)])
    #print(np.sum(g*x_min_sum)-np.sum(g*x_first))
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
        #print(np.where(x>0)[1])
        #if(7510>i>7490):
            #print(i, ")", np.sum(c * x), l, w)
        if np.any(w > 0):
            #print("BAD")
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
    n_max = 100000
    n_0 = 0
    c_1 = np.array([
        [49, 20, 23, 68, 45, 89, 31, 11, 12, 43, 71, 92, 62, 96, 33],
        [27, 34, 33, 91, 46, 76, 94, 14, 94, 94, 60, 50, 78, 41, 87],
        [62, 74, 35, 13, 92, 91, 26, 27, 93, 11, 11, 94, 15, 14, 54],
        [72, 69, 17, 50, 49, 79, 37, 33, 32, 32, 96, 62, 30, 59, 49],
        [58, 34, 55, 41, 87, 10, 84, 80, 70, 80, 61, 63, 79, 58, 86],
        [52, 44, 15, 89, 24, 50, 68, 43, 71, 31, 31, 62, 39, 91, 12],
        [81, 56, 54, 26, 58, 72, 44, 69, 91, 83, 86, 74, 28, 69, 87],
        [13, 63, 38, 33, 55, 97, 24, 21, 11, 12, 51, 70, 26, 71, 23],
        [14, 89, 30, 87, 94, 96, 27, 15, 41, 99, 49, 59, 28, 64, 64],
        [91, 32, 43, 88, 48, 52, 81, 70, 24, 75, 69, 92, 59, 97, 63],
        [56, 75, 87, 48, 91, 55, 37, 23, 51, 51, 43, 75, 97, 95, 32],
        [43, 19, 39, 37, 45, 89, 13, 28, 26, 38, 44, 58, 60, 46, 29],
        [86, 46, 33, 12, 86, 42, 49, 29, 82, 91, 13, 35, 26, 98, 11],
        [34, 35, 65, 23, 35, 81, 68, 78, 66, 30, 77, 12, 97, 24, 51],
        [36, 32, 65, 86, 90, 53, 47, 53, 35, 26, 51, 78, 67, 14, 96]
    ])
    d_1 = np.array([[
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ]])
    b_1 = np.array([2])
    l_1 = np.array([1])

    c_2 = np.array([
        [56, 48, 18, 59, 21, 25, 78, 44, 63, 41, 21, 44, 24, 71, 42],
        [13, 37, 60, 33, 40, 72, 28, 47, 71, 69, 38, 67, 20, 69, 69],
        [65, 38, 35, 23, 35, 94, 55, 81, 85, 40, 17, 37, 46, 38, 75],
        [80, 81, 83, 61, 45, 96, 97, 18, 89, 38, 54, 15, 14, 27, 29],
        [44, 19, 72, 51, 42, 86, 16, 20, 97, 24, 11, 62, 42, 37, 91],
        [56, 60, 57, 10, 75, 35, 50, 85, 94, 51, 74, 10, 93, 20, 79],
        [65, 29, 37, 11, 81, 97, 39, 29, 68, 11, 59, 34, 60, 17, 62],
        [54, 71, 99, 13, 22, 45, 48, 80, 28, 71, 31, 15, 88, 39, 74],
        [68, 85, 45, 51, 83, 80, 36, 53, 61, 82, 30, 28, 26, 18, 78],
        [84, 99, 60, 94, 67, 50, 10, 80, 32, 55, 97, 96, 94, 99, 19],
        [20, 32, 24, 30, 12, 27, 69, 92, 78, 34, 83, 70, 73, 81, 27],
        [11, 44, 18, 54, 41, 80, 90, 20, 75, 65, 70, 53, 57, 19, 40],
        [30, 47, 91, 57, 42, 72, 42, 22, 48, 54, 36, 49, 83, 78, 45],
        [64, 16, 37, 71, 37, 83, 87, 39, 65, 46, 61, 91, 22, 62, 71],
        [84, 97, 18, 74, 95, 64, 59, 50, 86, 61, 38, 64, 54, 62, 96]
    ])
    d_2 = np.array([[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]])
    b_2 = np.array([1])
    l_2 = np.array([1])

    '''c = np.array([[5, 4, 3, 6],
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
    l = np.array([1, 1])'''
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
    #print(main_1_max(n, k, n_0, n_max, c, d, b, l))
    #print(main_phi_max(n, k, n_0, n_max, c, d, b, l))
    print(main_1_min(n, k, n_0, 10, c_1, d_1, b_1, l_1))
    #print(main_phi_min(n, k, n_0, n_max, c_1, d_1, b_1, l_1))