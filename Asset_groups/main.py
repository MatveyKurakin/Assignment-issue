import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
from gen_func import *

def generate_matrix_and_vector():

    N = int(entry_n.get())
    c_min = int(entry_c_min.get())
    c_max = int(entry_c_max.get()) + 1
    x_min = float(entry_x_min.get())
    x_max = float(entry_x_max.get())

    is_sort_matrix_y = entry_is_sort_matrix_y.get()
    is_sort_matrix_x = entry_is_sort_matrix_x.get()
    is_sort_vector = entry_is_sort_vector.get()

    if c_min >= c_max or x_min >= x_max or N < 1 or N > 15 or x_min < 0 or x_max > 1 or c_min < 0:
        sum_entry_veng_max.delete(0, tk.END)
        sum_entry_veng_max.insert(0, "ERROR")

        sum_entry_greedy_d.delete(0, tk.END)
        sum_entry_greedy_d.insert(0, "ERROR")
        raise ValueError("Минимальное значение должно быть меньше максимального.")

    c = create_c(N, c_min, c_max)
    x = create_x(N,x_min,x_max)

    if(is_sort_matrix_y == "1"):
        c = increase_by_row(c)
    if(is_sort_matrix_y == "2"):
        c = de_increase_by_row(c)

    if (is_sort_matrix_x == "1"):
        c = increase_by_col(c)
    if (is_sort_matrix_x == "2"):
        c = de_increase_by_col(c)

    if (is_sort_vector == "1"):
        x = increase(x)
    if (is_sort_vector == "2"):
        x = de_increase(x)

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

    d, potential_profit = create_d(c, x)

    row_ind, col_ind = greedy(d)
    res_greedy_d = np.zeros(d.shape)
    total_greedy_d = potential_profit
    for i in range(len(row_ind)):
        res_greedy_d[row_ind[i]][col_ind[i]] = 1
        for j in range(i+1):
            total_greedy_d += d[row_ind[j]][col_ind[i]]

    sum_entry_veng_max.delete(0, tk.END)
    sum_entry_veng_max.insert(0, str(f"{round(total_veng_max, 2)}"))

    sum_entry_greedy_d.delete(0, tk.END)
    sum_entry_greedy_d.insert(0, str(f"{round(total_greedy_d, 2)} ({round(total_greedy_d / total_veng_max*100, 2)}%)"))

    show_matrix_on_frame(c, res_veng_max, frame_veng_max)
    show_matrix_on_frame(c, res_greedy_d, frame_greedy_d)

def show_c_and_x(matrix, vector):
    for widget in frame_c_and_x.winfo_children():
        widget.destroy()

    label = tk.Label(frame_c_and_x, text="Месяцы", font=font_style_notebook_frame, bg="lightblue", width=int(matrix_width * matrix.shape[0]*1.06), height=matrix_height, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame_c_and_x, text="Группа", font=font_style_notebook_frame, bg="lightpink", width=matrix_width*2, height=matrix_height*2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=i + 1, font=font_style_notebook_frame, bg="lightblue", width=matrix_width, height=matrix_height,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame_c_and_x, text=f"{i + 1}", font=font_style_notebook_frame, bg="lightpink", width=matrix_width*2, height=matrix_height,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            label = tk.Label(frame_c_and_x, text=int(matrix[i][j]), font=font_style_notebook_frame, bg="white", width=matrix_width, height=matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)

    label = tk.Label(frame_c_and_x, text="X", font=font_style_notebook_frame, bg="#F09B59", width=matrix_width, height=matrix_height, borderwidth=1,
                     relief="solid")
    label.grid(row=1, column=len(matrix)+1, padx=10)

    for i in range(len(vector)):
        label = tk.Label(frame_c_and_x, text=vector[i], font=font_style_notebook_frame, bg="white", width=matrix_width, height=matrix_height, borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=len(matrix)+1, padx=10)

def show_matrix_on_frame(matrix, res, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    label = tk.Label(frame, text="Месяцы", font=font_style_notebook_frame, bg="lightblue",
                     width=int(matrix_width * matrix.shape[0] * 1.06), height=matrix_height, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=1, columnspan=matrix.shape[1])

    label = tk.Label(frame, text="Группа", font=font_style_notebook_frame, bg="lightpink", width=matrix_width*2, height=matrix_height*2, borderwidth=1,
                     relief="solid")
    label.grid(row=0, column=0, rowspan=2)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=i + 1, font=font_style_notebook_frame, bg="lightblue", width=matrix_width, height=matrix_height,
                         borderwidth=1, relief="solid")
        label.grid(row=1, column=i + 1)

    for i in range(len(matrix)):
        label = tk.Label(frame, text=f"{i + 1}", font=font_style_notebook_frame, bg="lightpink", width=matrix_width*2, height=matrix_height,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=i + 2, column=0)
        for j in range(len(matrix[i])):
            color = "#90EE90" if res[i][j] == 1 else "white"
            label = tk.Label(frame, text=int(matrix[i][j]), font=font_style_notebook_frame, bg=color, width=matrix_width, height=matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=j + 1)
def on_close():
    root.destroy()
    sys.exit()


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

root = tk.Tk()
root.title("Группы активов")

root.protocol("WM_DELETE_WINDOW", on_close)

#####################################

path_img_c_max = os.path.join(base_path, 'images', 'c_max.png')
path_img_c_min = os.path.join(base_path, 'images', 'c_min.png')
path_img_x_max = os.path.join(base_path, 'images', 'x_max.png')
path_img_x_min = os.path.join(base_path, 'images', 'x_min.png')
path_img_group = os.path.join(base_path, 'images', 'group.png')
path_img_empty = os.path.join(base_path, 'images', 'empty.png')

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

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

left_frame = ttk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky='ns')

right_frame = ttk.Frame(main_frame)
right_frame.grid(row=0, column=1, padx=10, sticky='nsew')

#####################################

tk.Label(left_frame, text="Входные параметры", font=font_style_head).grid(row=0, columnspan=4)

img_group = tk.PhotoImage(master=left_frame, file=path_img_group)
label = tk.Label(left_frame, image = img_group)
label.grid(row = 1, column = 0)

tk.Label(left_frame, text="Число групп:", font=font_style).grid(row=1, column=1)
entry_n = tk.Entry(left_frame, font=font_style, width=entry_width)
entry_n.insert(0, "15")
entry_n.grid(row=1, column=2)

tk.Label(left_frame, text="не более 15", font=font_style).grid(row=1, column=3, sticky="w")

original_image = Image.open(path_img_c_min)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_c_min = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, image = img_c_min)
label.image = img_c_min
label.grid(row = 2, column = 0)

tk.Label(left_frame, text="c_min:", font=font_style).grid(row=2, column=1)
entry_c_min = tk.Entry(left_frame, font=font_style, width=entry_width)
entry_c_min.insert(0, "10")
entry_c_min.grid(row=2, column=2)

tk.Label(left_frame, text="не менее 0", font=font_style).grid(row=2, column=3, sticky="w")

original_image = Image.open(path_img_c_max)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_c_max = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, image = img_c_max)
label.image = img_c_max
label.grid(row = 3, column = 0)

tk.Label(left_frame, text="c_max:", font=font_style).grid(row=3, column=1)
entry_c_max = tk.Entry(left_frame, font=font_style, width=entry_width)
entry_c_max.insert(0, "99")
entry_c_max.grid(row=3, column=2)

tk.Label(left_frame, text="не более 99999", font=font_style).grid(row=3, column=3, sticky="w")

original_image = Image.open(path_img_x_min)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_x_min = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, image = img_x_min)
label.image = img_x_min
label.grid(row = 4, column = 0)

tk.Label(left_frame, text="x_min:", font=font_style).grid(row=4, column=1)
entry_x_min = tk.Entry(left_frame, font=font_style, width=entry_width)
entry_x_min.insert(0, "0.00")
entry_x_min.grid(row=4, column=2)

tk.Label(left_frame, text="не менее 0.00", font=font_style).grid(row=4, column=3, sticky="w")

original_image = Image.open(path_img_x_max)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
img_x_max = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, image = img_x_max)
label.image = img_x_max
label.grid(row = 5, column = 0)

tk.Label(left_frame, text="x_max:", font=font_style).grid(row=5, column=1)
entry_x_max = tk.Entry(left_frame, font=font_style, width=entry_width)
entry_x_max.insert(0, "1.00")
entry_x_max.grid(row=5, column=2)

tk.Label(left_frame, text="не более 1.00", font=font_style).grid(row=5, column=3, sticky="w")

#####################################

tk.Label(left_frame, text="Расстановка по строкам", font=font_style_head).grid(row=6, columnspan=4)

entry_is_sort_matrix_y = tk.StringVar(value=0)

r_sort_y_1 = tk.Radiobutton(left_frame, text="Без расстановки", variable=entry_is_sort_matrix_y, value=0, font=font_style)
r_sort_y_1.grid(row=7, columnspan=4, sticky="w")

r_sort_y_2 = tk.Radiobutton(left_frame, text="Возрастание по строкам", variable=entry_is_sort_matrix_y, value=1, font=font_style)
r_sort_y_2.grid(row=8, columnspan=4, sticky="w")

r_sort_y_3 = tk.Radiobutton(left_frame, text="Убывание по строкам", variable=entry_is_sort_matrix_y, value=2, font=font_style)
r_sort_y_3.grid(row=9, columnspan=4, sticky="w")

#####################################

tk.Label(left_frame, text="Расстановка по столбцам", font=font_style_head).grid(row=10, columnspan=4)

entry_is_sort_matrix_x = tk.StringVar(value=0)

r_sort_x_1 = tk.Radiobutton(left_frame, text="Без расстановки", variable=entry_is_sort_matrix_x, value=0, font=font_style)
r_sort_x_1.grid(row=11, columnspan=4, sticky="w")

r_sort_x_2 = tk.Radiobutton(left_frame, text="Возрастание по столбцам", variable=entry_is_sort_matrix_x, value=1, font=font_style)
r_sort_x_2.grid(row=12, columnspan=4, sticky="w")

r_sort_x_3 = tk.Radiobutton(left_frame, text="Убывание по столбцам", variable=entry_is_sort_matrix_x, value=2, font=font_style)
r_sort_x_3.grid(row=13, columnspan=4, sticky="w")

#####################################

tk.Label(left_frame, text="Расстановка вектора X", font=font_style_head).grid(row=14, columnspan=4)

entry_is_sort_vector = tk.StringVar(value=0)

r_sort_x_1 = tk.Radiobutton(left_frame, text="Без расстановки", variable=entry_is_sort_vector, value=0, font=font_style)
r_sort_x_1.grid(row=15, columnspan=4, sticky="w")

r_sort_x_2 = tk.Radiobutton(left_frame, text="Возрастание", variable=entry_is_sort_vector, value=1, font=font_style)
r_sort_x_2.grid(row=16, columnspan=4, sticky="w")

r_sort_x_3 = tk.Radiobutton(left_frame, text="Убывание", variable=entry_is_sort_vector, value=2, font=font_style)
r_sort_x_3.grid(row=17, columnspan=4, sticky="w")

#####################################

tk.Label(left_frame, text="Результат", font=font_style_head).grid(row=18, columnspan=4)

original_image = Image.open(path_img_empty)
resized_image = original_image.resize((img_size, img_size), Image.LANCZOS)
my_image = ImageTk.PhotoImage(resized_image)
label = tk.Label(left_frame, image = my_image)
label.image = my_image
label.grid(row = 19, column = 0)

tk.Label(left_frame, text="Венгерский", font=font_style).grid(row=19, column=1)
sum_entry_veng_max = tk.Entry(left_frame, font=font_style, width=entry_width * 2)
sum_entry_veng_max.grid(row=19, column=2, columnspan=2)

label = tk.Label(left_frame, image = my_image)
label.image = my_image
label.grid(row = 21, column = 0)

tk.Label(left_frame, text="Жадный", font=font_style).grid(row=21, column=1)
sum_entry_greedy_d = tk.Entry(left_frame, font=font_style, width=entry_width * 2)
sum_entry_greedy_d.grid(row=21, column=2, columnspan=2)

button_generate = tk.Button(left_frame, text="Сгенерировать", font=font_style, bg="lightgreen", command=generate_matrix_and_vector)
button_generate.grid(row=22, columnspan=4, pady=10)

#####################################

style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 10], font=font_style_notebook)

notebook = ttk.Notebook(right_frame)
notebook.grid(row=3, column=2, sticky='nsew')

frame_c_and_x = ttk.Frame(notebook)
frame_veng_max = ttk.Frame(notebook)
frame_greedy_d = ttk.Frame(notebook)

notebook.add(frame_c_and_x, text="Матрица C и вектор X")
notebook.add(frame_veng_max, text="Венгерский")
notebook.add(frame_greedy_d, text="Жадный")

matrix= np.zeros((int(entry_n.get()),int(entry_n.get())))
vector= np.zeros(int(entry_n.get()))
show_c_and_x(matrix, vector)

show_matrix_on_frame(matrix, matrix, frame_veng_max)
show_matrix_on_frame(matrix, matrix, frame_greedy_d)

root.mainloop()

root.destroy()