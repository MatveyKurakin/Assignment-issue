import tkinter as tk
from tkinter import ttk
import numpy as np
import sys
from gen_func import *

def generate_matrix_and_vector():

    N = int(entry_n.get())
    c_min = float(entry_c_min.get())
    c_max = float(entry_c_max.get())
    x_min = float(entry_x_min.get())
    x_max = float(entry_x_max.get())

    # Проверка на корректность диапазонов
    if c_min > c_max or x_min > x_max:
        raise ValueError("Минимальное значение должно быть меньше максимального.")

    # Генерируем случайную матрицу c и вектор x
    c = create_c(N, c_min, c_max)
    x = create_x(N,x_min,x_max)

    # Отображаем матрицу c и вектор x
    display_matrix(c)
    display_vector(x)

    d, potential_profit = create_d(c, x)

    row_ind, col_ind = veng_max(d)
    res = np.zeros(d.shape)
    total = potential_profit
    for i in range(len(row_ind)):
        res[row_ind[i]][col_ind[i]] = 1
        total += d[row_ind[i]][col_ind[i]]

    sum_entry.delete(0, tk.END)  # Очищаем текстовое поле
    sum_entry.insert(0, str(round(total,2)))
    # Пример вычисления матрицы res (здесь просто случайная матрица 0 и 1)

    # Отображаем матрицу c с закрашенными ячейками
    display_colored_matrix(c, res)


def display_matrix(matrix):
    matrix_window = tk.Toplevel(root)
    matrix_window.title("Матрица")
    matrix_window.grid_columnconfigure(0,weight=10)
    label = tk.Label(matrix_window, text="C", font=font_style, bg="yellow", width=5, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0)
    for i in range(len(matrix)):
        label = tk.Label(matrix_window, text=i + 1, font=font_style, bg="#D3D3D3", width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=0, column=i+1)

    for i in range(len(matrix)):
        label = tk.Label(matrix_window, text=f"Команда {i + 1}", font=font_style, bg="#D3D3D3", width=5, height=2,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            label = tk.Label(matrix_window, text=matrix[i][j], font=font_style, bg="white", width=5, height=2, borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j+1)  # Сдвигаем на 1 вниз для числа
def display_vector(vector):
    vector_window = tk.Toplevel(root)
    vector_window.title("Вектор")
    label = tk.Label(vector_window, text="X", font=font_style, bg="#D3D3D3", width=5, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1)
    for i in range(len(vector)):
        label = tk.Label(vector_window, text=i + 1, font=font_style, bg="#D3D3D3", width=5, height=2,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)

    for i in range(len(vector)):
        label = tk.Label(vector_window, text=vector[i], font=font_style, bg="white", width=5, height=2, borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=1)  # Сдвигаем на 1 вниз для числа


def display_colored_matrix(matrix, res):
    colored_window = tk.Toplevel(root)
    colored_window.title("Закрашенная матрица c")

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            color = "#90EE90" if res[i][j] == 1 else "white"
            label = tk.Label(colored_window, text=matrix[i][j], font=font_style, bg=color, width=5, height=2, borderwidth=1,
                             relief="solid")
            label.grid(row=i + 1, column=j)  # Сдвигаем на 1 вниз для числа

def on_close():
    root.destroy()
    sys.exit()

# Создание основного окна
root = tk.Tk()
root.title("Генерация матрицы и вектора")

root.protocol("WM_DELETE_WINDOW", on_close)

font_style = ("Arial", 16)

# Поля ввода с значениями по умолчанию
tk.Label(root, text="Размер матрицы N:", font=font_style).grid(row=0, column=0)
entry_n = tk.Entry(root, font=font_style)
entry_n.insert(0, "10")  # Значение по умолчанию
entry_n.grid(row=0, column=1)

tk.Label(root, text="c_min:", font=font_style).grid(row=1, column=0)
entry_c_min = tk.Entry(root, font=font_style)
entry_c_min.insert(0, "100")  # Значение по умолчанию
entry_c_min.grid(row=1, column=1)

tk.Label(root, text="c_max:", font=font_style).grid(row=2, column=0)
entry_c_max = tk.Entry(root, font=font_style)
entry_c_max.insert(0, "200")  # Значение по умолчанию
entry_c_max.grid(row=2, column=1)

tk.Label(root, text="x_min:", font=font_style).grid(row=3, column=0)
entry_x_min = tk.Entry(root, font=font_style)
entry_x_min.insert(0, "0")  # Значение по умолчанию
entry_x_min.grid(row=3, column=1)

tk.Label(root, text="x_max:", font=font_style).grid(row=4, column=0)
entry_x_max = tk.Entry(root, font=font_style)
entry_x_max.insert(0, "1")  # Значение по умолчанию
entry_x_max.grid(row=4, column=1)

# Кнопка для генерации матрицы и вектора
button_generate = tk.Button(root, text="Сгенерировать", font=font_style, command=generate_matrix_and_vector)
button_generate.grid(row=5, columnspan=2)

tk.Label(root, text="Ответ: ", font=font_style).grid(row=6, column=0)
sum_entry = tk.Entry(root, font=font_style, width=20)
sum_entry.grid(row=6, column=1)

# Запуск основного цикла
root.mainloop()

root.destroy()