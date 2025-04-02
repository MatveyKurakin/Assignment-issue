import numpy as np
from scipy.optimize import linear_sum_assignment

M = 10**9
K = 0

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

def summ_matrix(c, summ_perm, k):
    summ = c.sum() - summ_perm * (k-1) / k
    return summ

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
    return col_ind, row_ind

def conjugate(c, perm_1):
    n = c.shape[0]
    c_copy = c.copy()
    for i in range(n):
        for j in range(n):
            if(perm_1[j]==i):
                c_copy[i][j] = 0
            else:
                c_copy[i][j] += M
    perm_2, _ = veng_max(c_copy)
    return perm_2

def additional(c, perm_star, gamma):
    n = c.shape[0]
    c_copy = c.copy()
    for i in range(n):
        for j in range(n):
            if (perm_star[j] == i):
                if(gamma & 2**j):
                    c_copy[i][j] += 2*M
                else:
                    c_copy[i][j] = 0
            else:
                c_copy[i][j] += M
    perm_1, _ = veng_max(c_copy)
    return perm_1

def naive(c, k):
    c_copy = c.copy()
    perm_1, _ = veng_max(c_copy)
    perm_2 = conjugate(c_copy, perm_1)
    summ = summ_perm(c, perm_1, perm_2)
    summ_res = summ_matrix(c.copy(), summ, k)
    return summ_res, summ, perm_1, perm_2


def optimal(c, k):
    n = c.shape[0]
    c_copy = c.copy()
    perm_res_1, _ = veng_max(c_copy)
    perm_res_2 = conjugate(c_copy, perm_res_1)
    summ = summ_perm(c, perm_res_1, perm_res_2)
    perm_star = perm_res_1
    for gamma in range(1, 2**n-2):
        c_copy = c.copy()
        perm_1 = additional(c_copy, perm_star, gamma)
        perm_2 = conjugate(c_copy, perm_1)
        cur_summ = summ_perm(c_copy, perm_1, perm_2)
        if(cur_summ > summ):
            summ = cur_summ
            perm_res_1 = perm_1
            perm_res_2 = perm_2
    summ_res = summ_matrix(c.copy(), summ, k)
    return summ_res, summ, perm_res_1, perm_res_2

def main():
    k = 10.5
    c = create_c(15, 100, 1000)
    print(naive(c.copy(), k))
    print(optimal(c.copy(), k))


if __name__ == "__main__":
    main()