import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
from gen_func import *
import time

def generate_matrix_and_vector(new_c=None):

    N = int(entry_n.get())
    c_min = int(entry_c_min.get())
    c_max = int(entry_c_max.get()) + 1
    k = float(entry_k.get())

    is_sort_matrix_y = entry_is_sort_matrix_y.get()
    is_sort_matrix_x = entry_is_sort_matrix_x.get()

    # Проверка на корректность диапазонов
    if c_min >= c_max or k < 1.0 or N < 1 or N > 15 or k < 0 or c_min < 0:
        sum_entry_veng_max.delete(0, tk.END)
        sum_entry_veng_max.insert(0, "ERROR")

        # sum_entry_greedy.delete(0, tk.END)
        # sum_entry_greedy.insert(0, "ERROR")

        sum_entry_greedy_d.delete(0, tk.END)
        sum_entry_greedy_d.insert(0, "ERROR")
        raise ValueError("Минимальное значение должно быть меньше максимального.")

    c = create_c(N, c_min, c_max)
    if(new_c is not None):
        c = new_c

    if(is_sort_matrix_y == "1"):
        c = increase_by_row(c)
    if(is_sort_matrix_y == "2"):
        c = de_increase_by_row(c)

    if (is_sort_matrix_x == "1"):
        c = increase_by_col(c)
    if (is_sort_matrix_x == "2"):
        c = de_increase_by_col(c)

    show_c(c)

    cur_time = time.time()
    total_optimal_max, optimal_max, perm_1, perm_2 = optimal(c, k)
    time_optimal = time.time() - cur_time
    res_optimal_max = np.zeros(c.shape)
    for i in range(len(perm_1)):
        res_optimal_max[perm_1[i]][i] = 1
        res_optimal_max[perm_2[i]][i] = 2

    cur_time = time.time()
    total_naive_max, naive_max, perm_1, perm_2 = naive(c, k)
    time_naive = time.time() - cur_time
    res_naive_max = np.zeros(c.shape)
    for i in range(len(perm_1)):
        res_naive_max[perm_1[i]][i] = 1
        res_naive_max[perm_2[i]][i] = 2

    sum_entry_veng_max.delete(0, tk.END)
    sum_entry_veng_max.insert(0, str(f"{round(optimal_max, 2)}"))

    sum_entry_veng_max_res.delete(0, tk.END)
    sum_entry_veng_max_res.insert(0, str(f"{round(total_optimal_max, 2)}"))

    sum_entry_veng_max_time.delete(0, tk.END)
    sum_entry_veng_max_time.insert(0, str(f"{round(time_optimal, 2)} сек."))

    sum_entry_greedy_d.delete(0, tk.END)
    sum_entry_greedy_d.insert(0, str(f"{round(naive_max, 2)}"))

    sum_entry_greedy_d_res.delete(0, tk.END)
    sum_entry_greedy_d_res.insert(0, str(f"{round(total_naive_max, 2)}"))

    sum_entry_greedy_d_time.delete(0, tk.END)
    sum_entry_greedy_d_time.insert(0, str(f"{round(time_naive, 2)} сек."))

    error.delete(0, tk.END)
    error.insert(0, str(f"{round((optimal_max - naive_max), 2)}"))

    error_res.delete(0, tk.END)
    error_res.insert(0, str(f"{round((total_naive_max - total_optimal_max), 2)}"))

    show_matrix_on_frame(c, res_optimal_max, frame_veng_max)
    show_matrix_on_frame(c, res_naive_max, frame_greedy_d)

    tk.Label(left_frame, bg=select_color_1, image=img_c_min).grid(row=26, column = 0)
    tk.Label(left_frame, text="Первое арт. подразделение", bg=background_color, font=font_style).grid(row=26, column = 1, columnspan=3, sticky="w")
    tk.Label(left_frame, bg=select_color_2, image=img_c_min).grid(row=27, column=0)
    tk.Label(left_frame, text="Второе арт. подразделение", bg=background_color, font=font_style).grid(row=27, column=1, columnspan=3, sticky="w")

def show_c(matrix):
    for widget in frame_c_and_x.winfo_children():
        widget.destroy()

    label = tk.Label(frame_c_and_x, text="Дни", font=font_style_notebook_frame, bg=matrix_color_1, width=int(matrix_width * matrix.shape[0]*1.06), height=matrix_height, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame_c_and_x, text="Подразделения", font=font_style_notebook_frame, bg=matrix_color_2, width=int(matrix_width*2.5), height=matrix_height*2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=i + 1, font=font_style_notebook_frame, bg=matrix_color_1, width=matrix_width, height=matrix_height,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=f"{i + 1}", font=font_style_notebook_frame, bg=matrix_color_2, width=int(matrix_width*2.5), height=matrix_height,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            label = tk.Label(frame_c_and_x, text=int(matrix[i][j]), font=font_style_notebook_frame, bg=matrix_color_3, width=matrix_width, height=matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)  # Сдвигаем на 1 вниз для числа


def show_matrix_on_frame(matrix, res, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    label = tk.Label(frame, text="Дни", font=font_style_notebook_frame, bg=matrix_color_1,
                     width=int(matrix_width * matrix.shape[0] * 1.06), height=matrix_height, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame, text="Подразделения", font=font_style_notebook_frame, bg=matrix_color_2, width=int(matrix_width*2.5), height=matrix_height*2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=i + 1, font=font_style_notebook_frame, bg=matrix_color_1, width=matrix_width, height=matrix_height,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=f"{i + 1}", font=font_style_notebook_frame, bg=matrix_color_2, width=int(matrix_width*2.5), height=matrix_height,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            color = matrix_color_3
            if(res[i][j] == 1):
                color = select_color_1
            if(res[i][j] == 2):
                color = select_color_2
            label = tk.Label(frame, text=int(matrix[i][j]), font=font_style_notebook_frame, bg=color, width=matrix_width, height=matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)

def example_matrix_3():
    entry_n.delete(0, tk.END)
    entry_n.insert(0, "3")

    entry_c_min.delete(0, tk.END)
    entry_c_min.insert(0, "2")

    entry_c_max.delete(0, tk.END)
    entry_c_max.insert(0, "5")

    #entry_k.delete(0, tk.END)
    #entry_k.insert(0, "5.0")

    c = np.array([[5, 4, 2],
                  [4, 5, 4],
                  [2, 4, 5]])
    generate_matrix_and_vector(c)

def example_matrix_5():
    entry_n.delete(0, tk.END)
    entry_n.insert(0, "5")

    entry_c_min.delete(0, tk.END)
    entry_c_min.insert(0, "2")

    entry_c_max.delete(0, tk.END)
    entry_c_max.insert(0, "10")

    #entry_k.delete(0, tk.END)
    #entry_k.insert(0, "5.0")

    c = np.array([[1, 2, 3, 8, 10],
                  [2, 3, 8, 10, 8],
                  [3, 8, 10, 8, 3],
                  [8, 10, 8, 3, 2],
                  [10, 8, 3, 2, 1]])
    generate_matrix_and_vector(c)

def on_close():
    root.destroy()
    sys.exit()


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Создание основного окна
root = tk.Tk()
root.title("Огневая мощь противника")


root.protocol("WM_DELETE_WINDOW", on_close)

#####################################

path_img_c_max = os.path.join(base_path, 'images', 'c_max.png')
path_img_c_min = os.path.join(base_path, 'images', 'c_min.png')
path_img_x_max = os.path.join(base_path, 'images', 'x_max.png')
path_img_k = os.path.join(base_path, 'images', 'x_min_1.png')
path_img_group = os.path.join(base_path, 'images', 'group.png')
path_img_empty = os.path.join(base_path, 'images', 'empty.png')

background_color = "#7BA05B"
entry_color = "#B8D8B0"
button_color = "#B0524A"
matrix_color_1 = "#918151" # left
matrix_color_2 = "#4F7942" # up
matrix_color_3 = "#f8f8d9" # center
select_color_1 = "lightcoral"
select_color_2 = "lightblue"

style = ttk.Style()
style.configure("Custom.TFrame", background=background_color)

coef_img_size = 0.04

img_size = round(coef_img_size * root.winfo_screenheight())

#####################################

coef_matrix_width = 0.003
coef_matrix_height = 0.002

matrix_width = round(coef_matrix_width * root.winfo_screenwidth())
matrix_height =round(coef_matrix_height * root.winfo_screenheight())

#####################################

coef_base_font_size = 0.015
coef_head_font_size = 0.017
coef_notebook_font_size = 0.015
coef_notebook_frame_font_size = 0.013
coef_entry_width = 0.006

base_font_size = round(coef_base_font_size * root.winfo_screenheight())
head_font_size = round(coef_head_font_size * root.winfo_screenheight())
notebook_font_size = round(coef_notebook_font_size * root.winfo_screenheight())
notebook_frame_font_size = round(coef_notebook_frame_font_size * root.winfo_screenheight())
entry_width = round(coef_entry_width * root.winfo_screenwidth())

font_style = ("Arial", base_font_size)
font_style_head = ("Arial", head_font_size, "bold")
font_style_notebook = ('Helvetica', notebook_font_size)
font_style_notebook_frame = ("Arial", notebook_frame_font_size)

main_frame = ttk.Frame(root, style="Custom.TFrame")
main_frame.grid(row=0, column=0, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

left_frame = ttk.Frame(main_frame, style="Custom.TFrame")
left_frame.grid(row=0, column=0, sticky='ns', pady=(10,0))

right_frame = ttk.Frame(main_frame, style="Custom.TFrame")
right_frame.grid(row=0, column=1, padx=10, sticky='nsew', pady=(10,0))

#####################################

tk.Label(left_frame, text="Входные параметры", bg=background_color, font=font_style_head).grid(row=0, columnspan=5)

original_image = Image.open(path_img_group)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_group = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, bg=background_color, image = img_group) # put the image on a label
label.grid(row = 1, column = 0) # put the label in the grid

tk.Label(left_frame, text="Число подразделений:", bg=background_color, font=font_style).grid(row=1, column=1, columnspan=2)
entry_n = tk.Entry(left_frame, bg = entry_color, font=font_style, width=entry_width)
entry_n.insert(0, "15")
entry_n.grid(row=1, column=3)

tk.Label(left_frame, text="не более 15", bg=background_color, font=font_style).grid(row=1, column=4, sticky="w")

original_image = Image.open(path_img_c_min)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_c_min = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, bg=background_color, image = img_c_min)
label.image = img_c_min
label.grid(row = 2, column = 0)

tk.Label(left_frame, text="Минимальная мощь:", bg=background_color, font=font_style).grid(row=2, column=1, columnspan=2)
entry_c_min = tk.Entry(left_frame, bg = entry_color, font=font_style, width=entry_width)
entry_c_min.insert(0, "10")
entry_c_min.grid(row=2, column=3)

tk.Label(left_frame, text="не менее 0", bg=background_color, font=font_style).grid(row=2, column=4, sticky="w")

original_image = Image.open(path_img_c_max)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_c_max = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, bg=background_color, image = img_c_max)
label.image = img_c_max
label.grid(row = 3, column = 0)

tk.Label(left_frame, text="Максимальная мощь:", bg=background_color, font=font_style).grid(row=3, column=1, columnspan=2)
entry_c_max = tk.Entry(left_frame, bg = entry_color, font=font_style, width=entry_width)
entry_c_max.insert(0, "99")
entry_c_max.grid(row=3, column=3)

tk.Label(left_frame, text="не более 99999", bg=background_color, font=font_style).grid(row=3, column=4, sticky="w")

original_image = Image.open(path_img_k)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_k = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, bg=background_color, image = img_k)
label.image = img_k
label.grid(row = 4, column = 0)

tk.Label(left_frame, text="Коеф. снижения мощи:", bg=background_color, font=font_style).grid(row=4, column=1, columnspan=2)
entry_k = tk.Entry(left_frame, bg = entry_color, font=font_style, width=entry_width)
entry_k.insert(0, "5.00")
entry_k.grid(row=4, column=3)

tk.Label(left_frame, text="не менее 1.00", bg=background_color, font=font_style).grid(row=4, column=4, sticky="w")

#####################################

tk.Label(left_frame, text="Расстановка по строкам", bg=background_color, font=font_style_head).grid(row=6, columnspan=5)

entry_is_sort_matrix_y = tk.StringVar(value=0)

r_sort_y_1 = tk.Radiobutton(left_frame, text="Без расстановки", bg=background_color, variable=entry_is_sort_matrix_y, value=0, font=font_style)
r_sort_y_1.grid(row=7, columnspan=5, sticky="w")

r_sort_y_2 = tk.Radiobutton(left_frame, text="Возрастание по строкам", bg=background_color, variable=entry_is_sort_matrix_y, value=1, font=font_style)
r_sort_y_2.grid(row=8, columnspan=5, sticky="w")

r_sort_y_3 = tk.Radiobutton(left_frame, text="Убывание по строкам", bg=background_color, variable=entry_is_sort_matrix_y, value=2, font=font_style)
r_sort_y_3.grid(row=9, columnspan=5, sticky="w")

#####################################

tk.Label(left_frame, text="Расстановка по столбцам", bg=background_color, font=font_style_head).grid(row=10, columnspan=5)

entry_is_sort_matrix_x = tk.StringVar(value=0)

r_sort_x_1 = tk.Radiobutton(left_frame, text="Без расстановки", bg=background_color, variable=entry_is_sort_matrix_x, value=0, font=font_style)
r_sort_x_1.grid(row=11, columnspan=5, sticky="w")

r_sort_x_2 = tk.Radiobutton(left_frame, text="Возрастание по столбцам", bg=background_color, variable=entry_is_sort_matrix_x, value=1, font=font_style)
r_sort_x_2.grid(row=12, columnspan=5, sticky="w")

r_sort_x_3 = tk.Radiobutton(left_frame, text="Убывание по столбцам", bg=background_color, variable=entry_is_sort_matrix_x, value=2, font=font_style)
r_sort_x_3.grid(row=13, columnspan=5, sticky="w")

#####################################

tk.Label(left_frame, text="Проверка работы", bg=background_color, font=font_style_head).grid(row=18, columnspan=5)

button_generate = tk.Button(left_frame, text="Матрица 3x3", font=font_style, bg=button_color, command=example_matrix_3)
button_generate.grid(row=19, column=2, columnspan=1, pady=10)

button_generate = tk.Button(left_frame, text="Матрица 5x5", font=font_style, bg=button_color, command=example_matrix_5)
button_generate.grid(row=19, column=3, columnspan=1, pady=10)

#####################################

tk.Label(left_frame, text="Результат", bg=background_color, font=font_style_head).grid(row=20, columnspan=5)

'''original_image = Image.open(path_img_empty)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
my_image = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, bg=background_color, image = my_image)
label.image = my_image
label.grid(row = 19, column = 0)'''

tk.Label(left_frame, text="S_max", bg=background_color, font=font_style).grid(row=21, column=2)
tk.Label(left_frame, text="S", bg=background_color, font=font_style).grid(row=21, column=3)
tk.Label(left_frame, text="Время", bg=background_color, font=font_style).grid(row=21, column=4)

tk.Label(left_frame, text="σ* и σ₀", bg=background_color, font=font_style).grid(row=22, column=0, columnspan=2, sticky="w")
sum_entry_greedy_d = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_greedy_d.grid(row=22, column=2)
sum_entry_greedy_d_res = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_greedy_d_res.grid(row=22, column=3)
sum_entry_greedy_d_time = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_greedy_d_time.grid(row=22, column=4)

'''label = tk.Label(left_frame, bg=background_color, image = my_image)
label.image = my_image
label.grid(row = 21, column = 0)'''

tk.Label(left_frame, text="σ₁ и σ₂", bg=background_color, font=font_style).grid(row=23, column=0, columnspan=2, sticky="w")
sum_entry_veng_max = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_veng_max.grid(row=23, column=2)
sum_entry_veng_max_res = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_veng_max_res.grid(row=23, column=3)
sum_entry_veng_max_time = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
sum_entry_veng_max_time.grid(row=23, column=4)

'''label = tk.Label(left_frame, bg=background_color, image = my_image)
label.image = my_image
label.grid(row = 22, column = 0)'''

tk.Label(left_frame, text="Погрешность", bg=background_color, font=font_style).grid(row=24, column=0, columnspan=2, sticky="w")
error = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
error.grid(row=24, column=2)
error_res = tk.Entry(left_frame, bg = entry_color, font=font_style, width=int(entry_width*1.2))
error_res.grid(row=24, column=3)

button_generate = tk.Button(left_frame, text="Сгенерировать", font=font_style, bg=button_color, command=generate_matrix_and_vector)
button_generate.grid(row=25, columnspan=5, pady=10)

#####################################

style = ttk.Style()
style.configure("TNotebook")
style.configure("TNotebook.Tab", padding=[20, 10], font=font_style_notebook, background=background_color, foreground="black")

notebook = ttk.Notebook(right_frame)
notebook.grid(row=3, column=2, sticky='nsew')

frame_c_and_x = ttk.Frame(notebook, style="Custom.TFrame")
frame_veng_max = ttk.Frame(notebook, style="Custom.TFrame")
frame_greedy_d = ttk.Frame(notebook, style="Custom.TFrame")

notebook.add(frame_c_and_x, text="Матрица C")
notebook.add(frame_greedy_d, text="σ* и σ₀")
notebook.add(frame_veng_max, text="σ₁ и σ₂")

matrix = np.zeros((int(entry_n.get()),int(entry_n.get())))
show_c(matrix)

show_matrix_on_frame(matrix, matrix, frame_veng_max)
show_matrix_on_frame(matrix, matrix, frame_greedy_d)

root.mainloop()

root.destroy()