import tkinter as tk
from tkinter import ttk
from tkinter import *
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
    #display_matrix(c)
    #display_vector(x)
    show_c_and_x(c,x)

    d, potential_profit = create_g(c, x)

    row_ind, col_ind = veng_max(d)
    res_veng_max = np.zeros(d.shape)
    total_veng_max = potential_profit
    for i in range(len(row_ind)):
        res_veng_max[row_ind[i]][col_ind[i]] = 1
        total_veng_max += d[row_ind[i]][col_ind[i]]

    row_ind, col_ind = greedy(d)
    res_greedy = np.zeros(d.shape)
    total_greedy = potential_profit
    for i in range(len(row_ind)):
        res_greedy[row_ind[i]][col_ind[i]] = 1
        total_greedy += d[row_ind[i]][col_ind[i]]

    sum_entry.delete(0, tk.END)  # Очищаем текстовое поле
    sum_entry.insert(0, str(f"{round(total_veng_max,2)}, {round(total_greedy, 2)}"))
    # Пример вычисления матрицы res (здесь просто случайная матрица 0 и 1)

    # Отображаем матрицу c с закрашенными ячейками
    show_matrix_on_frame(c, res_veng_max, frame_veng_max)
    show_matrix_on_frame(c, res_greedy, frame_greedy)


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
def show_c_and_x(matrix, vector):
    for widget in frame_c_and_x.winfo_children():
        widget.destroy()

    label = tk.Label(frame_c_and_x, text="C", font=font_style, bg="yellow", width=10, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0)
    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=i + 1, font=font_style, bg="#D3D3D3", width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=0, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=f"Фирма {i + 1}", font=font_style, bg="#D3D3D3", width=10, height=2,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            label = tk.Label(frame_c_and_x, text=int(matrix[i][j]), font=font_style, bg="white", width=5, height=2,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)  # Сдвигаем на 1 вниз для числа


    label = tk.Label(frame_c_and_x, text="X", font=font_style, bg="#D3D3D3", width=5, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=len(matrix)+1, padx=10)

    for i in range(len(vector)):
        label = tk.Label(frame_c_and_x, text=vector[i], font=font_style, bg="white", width=5, height=2, borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=len(matrix)+1, padx=10)  # Сдвигаем на 1 вниз для числа

def show_matrix_on_frame(matrix, res, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    label = tk.Label(frame, text="C", font=font_style, bg="yellow", width=10, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0)
    for i in range(len(matrix)):
        label = tk.Label(frame, text=i + 1, font=font_style, bg="#D3D3D3", width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=0, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=f"Фирма {i + 1}", font=font_style, bg="#D3D3D3", width=10, height=2,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            color = "#90EE90" if res[i][j] == 1 else "white"
            label = tk.Label(frame, text=int(matrix[i][j]), font=font_style, bg=color, width=5, height=2,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)  # Сдвигаем на 1 вниз для числа
def on_close():
    root.destroy()
    sys.exit()

# Создание основного окна
root = tk.Tk()
root.title("Генерация матрицы и вектора")

root.protocol("WM_DELETE_WINDOW", on_close)

font_style = ("Arial", 16)

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

left_frame = ttk.Frame(main_frame, width=200)
left_frame.grid(row=0, column=0, sticky='ns')  # Заполнение по вертикали

# Создаем правый фрейм для Notebook
right_frame = ttk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky='nsew')

# Поля ввода с значениями по умолчанию
tk.Label(left_frame, text="Размер матрицы N:", font=font_style).grid(row=0, column=0)
entry_n = tk.Entry(left_frame, font=font_style)
entry_n.insert(0, "11")  # Значение по умолчанию
entry_n.grid(row=0, column=1)

tk.Label(left_frame, text="c_min:", font=font_style).grid(row=1, column=0)
entry_c_min = tk.Entry(left_frame, font=font_style)
entry_c_min.insert(0, "10")  # Значение по умолчанию
entry_c_min.grid(row=1, column=1)

tk.Label(left_frame, text="c_max:", font=font_style).grid(row=2, column=0)
entry_c_max = tk.Entry(left_frame, font=font_style)
entry_c_max.insert(0, "100")  # Значение по умолчанию
entry_c_max.grid(row=2, column=1)

tk.Label(left_frame, text="x_min:", font=font_style).grid(row=3, column=0)
entry_x_min = tk.Entry(left_frame, font=font_style)
entry_x_min.insert(0, "0")  # Значение по умолчанию
entry_x_min.grid(row=3, column=1)

tk.Label(left_frame, text="x_max:", font=font_style).grid(row=4, column=0)
entry_x_max = tk.Entry(left_frame, font=font_style)
entry_x_max.insert(0, "1")  # Значение по умолчанию
entry_x_max.grid(row=4, column=1)

# Кнопка для генерации матрицы и вектора
button_generate = tk.Button(left_frame, text="Сгенерировать", font=font_style, command=generate_matrix_and_vector)
button_generate.grid(row=5, columnspan=2)

tk.Label(left_frame, text="Ответ: ", font=font_style).grid(row=6, column=0)
sum_entry = tk.Entry(left_frame, font=font_style, width=20)
sum_entry.grid(row=6, column=1)

notebook = ttk.Notebook(right_frame)
notebook.grid(row=3, column=2, sticky='nsew')

frame_c_and_x = ttk.Frame(notebook)
frame_veng_max = ttk.Frame(notebook)
frame_greedy = ttk.Frame(notebook)

notebook.add(frame_c_and_x, text="Матрица C и вектор X")
notebook.add(frame_veng_max, text="Венгерский максимум")
notebook.add(frame_greedy, text="Жадный")

matrix= np.zeros((int(entry_n.get()),int(entry_n.get())))
vector= np.zeros(int(entry_n.get()))
show_c_and_x(matrix, vector)

show_matrix_on_frame(matrix, matrix, frame_veng_max)
show_matrix_on_frame(matrix, matrix, frame_greedy)

# Запуск основного цикла
root.mainloop()

root.destroy()