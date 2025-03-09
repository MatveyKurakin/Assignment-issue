import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np
import sys
from gen_func import *

def generate_matrix_and_vector():

    N = int(entry_n.get())
    c_min = int(entry_c_min.get())
    c_max = int(entry_c_max.get()) + 1
    x_min = float(entry_x_min.get())
    x_max = float(entry_x_max.get())

    is_sort_y = entry_is_sort_y.get()
    is_sort_x = entry_is_sort_x.get()

    # Проверка на корректность диапазонов
    if c_min >= c_max or x_min >= x_max:
        raise ValueError("Минимальное значение должно быть меньше максимального.")

    # Генерируем случайную матрицу c и вектор x
    c = create_c(N, c_min, c_max)
    x = create_x(N,x_min,x_max)

    if(is_sort_y == "1"):
        c = increase_by_row(c)
    if(is_sort_y == "2"):
        c = de_increase_by_row(c)

    if (is_sort_x == "1"):
        print("---")
        c = increase_by_col(c)
    if (is_sort_x == "2"):
        c = de_increase_by_col(c)

    # Отображаем матрицу c и вектор x
    #display_matrix(c)
    #display_vector(x)
    show_c_and_x(c,x)

    g, potential_profit = create_g(c, x)

    row_ind, col_ind = veng_max(g)
    res_veng_max = np.zeros(g.shape)
    total_veng_max = potential_profit
    for i in range(len(row_ind)):
        res_veng_max[row_ind[i]][col_ind[i]] = 1
        total_veng_max += g[row_ind[i]][col_ind[i]]

    row_ind, col_ind = greedy(g)
    res_greedy = np.zeros(g.shape)
    total_greedy = potential_profit
    for i in range(len(row_ind)):
        res_greedy[row_ind[i]][col_ind[i]] = 1
        total_greedy += g[row_ind[i]][col_ind[i]]

    d, potential_profit = create_d(c, x)

    row_ind, col_ind = greedy(d)
    res_greedy_d = np.zeros(d.shape)
    total_greedy_d = potential_profit
    for i in range(len(row_ind)):
        res_greedy_d[row_ind[i]][col_ind[i]] = 1
        for j in range(i+1):
            total_greedy_d += d[row_ind[j]][col_ind[i]]

    sum_entry_veng_max.delete(0, tk.END)  # Очищаем текстовое поле
    sum_entry_veng_max.insert(0, str(f"{round(total_veng_max, 2)}"))

    sum_entry_greedy.delete(0, tk.END)  # Очищаем текстовое поле
    sum_entry_greedy.insert(0, str(f"{round(total_greedy, 2)}"))

    sum_entry_greedy_d.delete(0, tk.END)  # Очищаем текстовое поле
    sum_entry_greedy_d.insert(0, str(f"{round(total_greedy_d, 2)}"))
    # Пример вычисления матрицы res (здесь просто случайная матрица 0 и 1)

    # Отображаем матрицу c с закрашенными ячейками
    show_matrix_on_frame(c, res_veng_max, frame_veng_max)
    show_matrix_on_frame(c, res_greedy, frame_greedy)
    show_matrix_on_frame(c, res_greedy_d, frame_greedy_d)

def show_c_and_x(matrix, vector):
    for widget in frame_c_and_x.winfo_children():
        widget.destroy()

    label = tk.Label(frame_c_and_x, text="Месяцы", font=font_style, bg="lightblue", width=int(5 * matrix.shape[0]*1.06), height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame_c_and_x, text="Группа", font=font_style, bg="lightpink", width=10, height=4, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=i + 1, font=font_style, bg="lightblue", width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=f"{i + 1}", font=font_style, bg="lightpink", width=10, height=2,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            label = tk.Label(frame_c_and_x, text=int(matrix[i][j]), font=font_style, bg="white", width=5, height=2,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)  # Сдвигаем на 1 вниз для числа


    label = tk.Label(frame_c_and_x, text="X", font=font_style, bg="#F09B59", width=5, height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=1, column=len(matrix)+1, padx=10)

    for i in range(len(vector)):
        label = tk.Label(frame_c_and_x, text=vector[i], font=font_style, bg="white", width=5, height=2, borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=len(matrix)+1, padx=10)  # Сдвигаем на 1 вниз для числа

def show_matrix_on_frame(matrix, res, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    label = tk.Label(frame, text="Месяцы", font=font_style, bg="lightblue",
                     width=int(5 * matrix.shape[0] * 1.06), height=2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame, text="Группа", font=font_style, bg="lightpink", width=10, height=4, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=i + 1, font=font_style, bg="lightblue", width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=f"{i + 1}", font=font_style, bg="lightpink", width=10, height=2,
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
font_style_1 = ("Arial", 18, "bold")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#style_left_frame = ttk.Style()
#style_left_frame.configure('Frame1.TFrame', background='white')

#left_frame = ttk.Frame(main_frame, style='Frame1.TFrame')
left_frame = ttk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky='ns')  # Заполнение по вертикали
for i in range(100):
    left_frame.grid_rowconfigure(i, weight=3)
    left_frame.grid_columnconfigure(i, weight=3)
# Создаем правый фрейм для Notebook
right_frame = ttk.Frame(main_frame)
right_frame.grid(row=0, column=1, padx=10, sticky='nsew')

#####################################

tk.Label(left_frame, text="Входные параметры", font=font_style_1).grid(row=0, columnspan=3)

img_group = tk.PhotoImage(master=left_frame, file = "group.png") # your image
label = tk.Label(left_frame, image = img_group) # put the image on a label
label.grid(row = 1, column = 0) # put the label in the grid

tk.Label(left_frame, text="Число групп:", font=font_style).grid(row=1, column=1)
entry_n = tk.Entry(left_frame, font=font_style)
entry_n.insert(0, "10")  # Значение по умолчанию
entry_n.grid(row=1, column=2)

img_c_min = tk.PhotoImage(master=left_frame, file = "c_min.png") # your image
label = tk.Label(left_frame, image = img_c_min) # put the image on a label
label.grid(row = 2, column = 0) # put the label in the grid

tk.Label(left_frame, text="c_min:", font=font_style).grid(row=2, column=1)
entry_c_min = tk.Entry(left_frame, font=font_style)
entry_c_min.insert(0, "10")  # Значение по умолчанию
entry_c_min.grid(row=2, column=2)

img_c_max = tk.PhotoImage(master=left_frame, file = "c_max.png") # your image
label = tk.Label(left_frame, image = img_c_max) # put the image on a label
label.grid(row = 3, column = 0) # put the label in the grid

tk.Label(left_frame, text="c_max:", font=font_style).grid(row=3, column=1)
entry_c_max = tk.Entry(left_frame, font=font_style)
entry_c_max.insert(0, "99")  # Значение по умолчанию
entry_c_max.grid(row=3, column=2)

img_x_min = tk.PhotoImage(master=left_frame, file = "x_min.png") # your image
label = tk.Label(left_frame, image = img_x_min) # put the image on a label
label.grid(row = 4, column = 0) # put the label in the grid

tk.Label(left_frame, text="x_min:", font=font_style).grid(row=4, column=1)
entry_x_min = tk.Entry(left_frame, font=font_style)
entry_x_min.insert(0, "0.00")  # Значение по умолчанию
entry_x_min.grid(row=4, column=2)

img_x_max = tk.PhotoImage(master=left_frame, file = "x_max.png") # your image
label = tk.Label(left_frame, image = img_x_max) # put the image on a label
label.grid(row = 5, column = 0) # put the label in the grid

tk.Label(left_frame, text="x_max:", font=font_style).grid(row=5, column=1)
entry_x_max = tk.Entry(left_frame, font=font_style)
entry_x_max.insert(0, "1.00")  # Значение по умолчанию
entry_x_max.grid(row=5, column=2)

#####################################

tk.Label(left_frame, text="Сортировка по строкам", font=font_style_1).grid(row=6, columnspan=3)

entry_is_sort_y = tk.StringVar(value=0)

r_sort_y_1 = tk.Radiobutton(left_frame, text="Не сортировать по строкам", variable=entry_is_sort_y, value=0, font=font_style)
r_sort_y_1.grid(row=7, columnspan=3, sticky="w")

r_sort_y_2 = tk.Radiobutton(left_frame, text="Возрастание по строкам", variable=entry_is_sort_y, value=1, font=font_style)
r_sort_y_2.grid(row=8, columnspan=3, sticky="w")

r_sort_y_3 = tk.Radiobutton(left_frame, text="Убывание по строкам", variable=entry_is_sort_y, value=2, font=font_style)
r_sort_y_3.grid(row=9, columnspan=3, sticky="w")

#####################################

tk.Label(left_frame, text="Сортировка по столбцам", font=font_style_1).grid(row=10, columnspan=3)

entry_is_sort_x = tk.StringVar(value=0)

r_sort_x_1 = tk.Radiobutton(left_frame, text="Не сортировать по столбцам", variable=entry_is_sort_x, value=0, font=font_style)
r_sort_x_1.grid(row=11, columnspan=3, sticky="w")

r_sort_x_2 = tk.Radiobutton(left_frame, text="Возрастание по столбцам", variable=entry_is_sort_x, value=1, font=font_style)
r_sort_x_2.grid(row=12, columnspan=3, sticky="w")

r_sort_x_3 = tk.Radiobutton(left_frame, text="Убывание по столбцам", variable=entry_is_sort_x, value=2, font=font_style)
r_sort_x_3.grid(row=13, columnspan=3, sticky="w")

#####################################

tk.Label(left_frame, text="Результат", font=font_style_1).grid(row=14, columnspan=3)

my_image = tk.PhotoImage(master=left_frame, file = "img_461138.png") # your image

label = tk.Label(left_frame, image = my_image) # put the image on a label
label.grid(row = 15, column = 0) # put the label in the grid

tk.Label(left_frame, text="Венгерский", font=font_style).grid(row=15, column=1)
sum_entry_veng_max = tk.Entry(left_frame, font=font_style, width=20)
sum_entry_veng_max.grid(row=15, column=2)

label = tk.Label(left_frame, image = my_image) # put the image on a label
label.grid(row = 16, column = 0) # put the label in the grid

tk.Label(left_frame, text="Жадный G", font=font_style).grid(row=16, column=1)
sum_entry_greedy = tk.Entry(left_frame, font=font_style, width=20)
sum_entry_greedy.grid(row=16, column=2)

label = tk.Label(left_frame, image = my_image) # put the image on a label
label.grid(row = 17, column = 0) # put the label in the grid

tk.Label(left_frame, text="Жадный D", font=font_style).grid(row=17, column=1)
sum_entry_greedy_d = tk.Entry(left_frame, font=font_style, width=20)
sum_entry_greedy_d.grid(row=17, column=2)

button_generate = tk.Button(left_frame, text="Сгенерировать", font=font_style, bg="lightgreen", command=generate_matrix_and_vector)
button_generate.grid(row=18, columnspan=3, pady=10)

#####################################

style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 10], font=('Helvetica', 16))

notebook = ttk.Notebook(right_frame)
notebook.grid(row=3, column=2, sticky='nsew')

frame_c_and_x = ttk.Frame(notebook)
frame_veng_max = ttk.Frame(notebook)
frame_greedy = ttk.Frame(notebook)
frame_greedy_d = ttk.Frame(notebook)

notebook.add(frame_c_and_x, text="Матрица C и вектор X")
notebook.add(frame_veng_max, text="Венгерский максимум")
notebook.add(frame_greedy, text="Жадный G")
notebook.add(frame_greedy_d, text="Жадный D")

matrix= np.zeros((int(entry_n.get()),int(entry_n.get())))
vector= np.zeros(int(entry_n.get()))
show_c_and_x(matrix, vector)

show_matrix_on_frame(matrix, matrix, frame_veng_max)
show_matrix_on_frame(matrix, matrix, frame_greedy)
show_matrix_on_frame(matrix, matrix, frame_greedy_d)

# Запуск основного цикла
root.mainloop()

root.destroy()