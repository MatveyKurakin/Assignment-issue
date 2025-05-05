import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
from gen_func import *
import time

class Window:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        # Создание основного окна
        self.root = tk.Tk()
        self.root.title("Приближенный метод")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        #####################################

        self.path_img_n = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_k = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_n_max = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_c_max = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_c_min = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_d_max = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_d_min = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_b_max = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_lambda = os.path.join(base_path, 'images', 'empty.png')
        self.path_img_empty = os.path.join(base_path, 'images', 'empty.png')

        self.background_color = "#E3F2FD" # "#F0F0F0"
        self.entry_color = "#F5F9FF" # "#FFFFFF"
        self.button_color = "#5ba5fa" # "#5D6D7E"
        self.matrix_color_up = "#d9dadb"
        self.matrix_color_left = "#e1e3e6"
        self.matrix_color_cell = "#FDF6E3"
        self.matrix_color_param = "#4A6B8A"
        self.select_color_1 = "#E74C3C"
        self.select_color_2 = "lightblue"

        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background=self.background_color)

        self.coef_img_size = 0.04

        self.img_size = round(self.coef_img_size * self.root.winfo_screenheight())
        self.ing_width = 1
        self.img_height = round(self.coef_img_size * self.root.winfo_screenheight())

        #####################################

        self.coef_matrix_width = 0.003
        self.coef_matrix_height = 0.002

        self.matrix_width = round(self.coef_matrix_width * self.root.winfo_screenwidth())
        self.matrix_height = round(self.coef_matrix_height * self.root.winfo_screenheight())

        #####################################

        self.coef_base_font_size = 0.015
        self.coef_head_font_size = 0.017
        self.coef_notebook_font_size = 0.015
        self.coef_notebook_frame_font_size = 0.013
        self.coef_entry_width = 0.006

        self.base_font_size = round(self.coef_base_font_size * self.root.winfo_screenheight())
        self.head_font_size = round(self.coef_head_font_size * self.root.winfo_screenheight())
        self.notebook_font_size = round(self.coef_notebook_font_size * self.root.winfo_screenheight())
        self.notebook_frame_font_size = round(self.coef_notebook_frame_font_size * self.root.winfo_screenheight())
        self.entry_width = round(self.coef_entry_width * self.root.winfo_screenwidth())

        self.font_style = ("Arial", self.base_font_size)
        self.font_style_head = ("Arial", self.head_font_size, "bold")
        self.font_style_notebook = ('Helvetica', self.notebook_font_size)
        self.font_style_notebook_frame = ("Arial", self.notebook_frame_font_size)

        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.left_frame.grid(row=0, column=0, sticky='ns', pady=(10, 0))

        self.right_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.right_frame.grid(row=0, column=1, padx=10, sticky='nsew', pady=(10, 0))

        #####################################

        ### n

        tk.Label(self.left_frame, text="Входные параметры", bg=self.background_color, font=self.font_style_head).grid(row=0,
                                                                                                       columnspan=4)

        self.original_image = Image.open(self.path_img_n)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_n = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_n)  # put the image on a label
        self.label.grid(row=1, column=0)  # put the label in the grid

        tk.Label(self.left_frame, text="n:", bg=self.background_color, font=self.font_style).grid(row=1, column=1)
        self.entry_n = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_n.insert(0, "15")
        self.entry_n.grid(row=1, column=2)
        self.entry_n.bind("<KeyRelease>", self.change_entry)

        tk.Label(self.left_frame, text="не более 15", bg=self.background_color, font=self.font_style).grid(row=1, column=3, sticky="w")

        ### k

        self.original_image = Image.open(self.path_img_k)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_k = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color,
                              image=self.img_k)  # put the image on a label
        self.label.grid(row=2, column=0)  # put the label in the grid

        tk.Label(self.left_frame, text="k:", bg=self.background_color, font=self.font_style).grid(row=2, column=1)
        self.entry_k = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_k.insert(0, "1")
        self.entry_k.grid(row=2, column=2)
        self.entry_k.bind("<KeyRelease>", self.change_entry)

        tk.Label(self.left_frame, text="не более 10", bg=self.background_color, font=self.font_style).grid(row=2, column=3, sticky="w")

        ### n_max

        self.original_image = Image.open(self.path_img_n_max)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_n_max = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color,
                              image=self.img_n_max)  # put the image on a label
        self.label.grid(row=3, column=0)  # put the label in the grid

        tk.Label(self.left_frame, text="N_max:", bg=self.background_color, font=self.font_style).grid(row=3, column=1)
        self.entry_n_max = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_n_max.insert(0, "10")
        self.entry_n_max.grid(row=3, column=2)
        self.entry_n_max.bind("<KeyRelease>", self.check_n_max)

        tk.Label(self.left_frame, text="не более 100000", bg=self.background_color, font=self.font_style).grid(row=3, column=3, sticky="w")

        ### c_min

        self.original_image = Image.open(self.path_img_c_min)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_c_min = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_c_min)
        self.label.image = self.img_c_min
        self.label.grid(row=4, column=0)

        tk.Label(self.left_frame, text="c_min:", bg=self.background_color, font=self.font_style).grid(row=4, column=1)
        self.entry_c_min = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_c_min.insert(0, "100")
        self.entry_c_min.grid(row=4, column=2)

        tk.Label(self.left_frame, text="не менее 0", bg=self.background_color, font=self.font_style).grid(row=4, column=3, sticky="w")

        ### c_max

        self.original_image = Image.open(self.path_img_c_max)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_c_max = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_c_max)
        self.label.image = self.img_c_max
        self.label.grid(row=5, column=0)

        tk.Label(self.left_frame, text="c_max:", bg=self.background_color, font=self.font_style).grid(row=5, column=1)
        self.entry_c_max = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_c_max.insert(0, "999")
        self.entry_c_max.grid(row=5, column=2)

        tk.Label(self.left_frame, text="не более 99999", bg=self.background_color, font=self.font_style).grid(row=5, column=3, sticky="w")

        '''### d_min

        self.original_image = Image.open(self.path_img_d_min)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_d_min = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_d_min)
        self.label.image = self.img_d_min
        self.label.grid(row=6, column=0)

        tk.Label(self.left_frame, text="d_min:", bg=self.background_color, font=self.font_style).grid(row=6, column=1)
        self.entry_d_min = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_d_min.insert(0, "0")
        self.entry_d_min.grid(row=6, column=2)

        tk.Label(self.left_frame, text="не менее 0", bg=self.background_color, font=self.font_style).grid(row=6, column=3, sticky="w")

        ### d_max

        self.original_image = Image.open(self.path_img_d_max)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_d_max = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_d_max)
        self.label.image = self.img_d_max
        self.label.grid(row=7, column=0)

        tk.Label(self.left_frame, text="d_max:", bg=self.background_color, font=self.font_style).grid(row=7, column=1)
        self.entry_d_max = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_d_max.insert(0, "1")
        self.entry_d_max.grid(row=7, column=2)

        tk.Label(self.left_frame, text="не более 99999", bg=self.background_color, font=self.font_style).grid(row=7, column=3, sticky="w")

        ### b_max

        self.original_image = Image.open(self.path_img_b_max)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_b_max = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_b_max)
        self.label.image = self.img_b_max
        self.label.grid(row=8, column=0)

        tk.Label(self.left_frame, text="b_max:", bg=self.background_color, font=self.font_style).grid(row=8, column=1)
        self.entry_b_max = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_b_max.insert(0, "1")
        self.entry_b_max.grid(row=8, column=2)

        tk.Label(self.left_frame, text="не более 99999", bg=self.background_color, font=self.font_style).grid(row=8, column=3, sticky="w")

        ### lambda

        self.original_image = Image.open(self.path_img_lambda)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.img_lambda = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.img_lambda)
        self.label.image = self.img_lambda
        self.label.grid(row=9, column=0)

        tk.Label(self.left_frame, text="lambda:", bg=self.background_color, font=self.font_style).grid(row=9, column=1)
        self.entry_lambda = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width)
        self.entry_lambda.insert(0, "1")
        self.entry_lambda.grid(row=9, column=2)

        tk.Label(self.left_frame, text="не более 99999", bg=self.background_color, font=self.font_style).grid(row=9,
                                                                                                              column=3,
                                                                                                              sticky="w")'''
        #####################################

        tk.Label(self.left_frame, text="Расстановка по строкам", bg=self.background_color, font=self.font_style_head).grid(row=10,
                                                                                                            columnspan=4)

        self.entry_is_sort_matrix_y = tk.StringVar(value=0)

        self. r_sort_y_1 = tk.Radiobutton(self.left_frame, text="Без расстановки", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_y, value=0, font=self.font_style)
        self.r_sort_y_1.grid(row=11, columnspan=4, sticky="w")

        self.r_sort_y_2 = tk.Radiobutton(self.left_frame, text="Возрастание по строкам", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_y, value=1, font=self.font_style)
        self.r_sort_y_2.grid(row=12, columnspan=4, sticky="w")

        self.r_sort_y_3 = tk.Radiobutton(self.left_frame, text="Убывание по строкам", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_y, value=2, font=self.font_style)
        self.r_sort_y_3.grid(row=13, columnspan=4, sticky="w")

        #####################################

        tk.Label(self.left_frame, text="Расстановка по столбцам", bg=self.background_color, font=self.font_style_head).grid(row=14,
                                                                                                             columnspan=4)

        self.entry_is_sort_matrix_x = tk.StringVar(value=0)

        self.r_sort_x_1 = tk.Radiobutton(self.left_frame, text="Без расстановки", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_x, value=0, font=self.font_style)
        self.r_sort_x_1.grid(row=15, columnspan=4, sticky="w")

        self.r_sort_x_2 = tk.Radiobutton(self.left_frame, text="Возрастание по столбцам", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_x, value=1, font=self.font_style)
        self.r_sort_x_2.grid(row=16, columnspan=4, sticky="w")

        self.r_sort_x_3 = tk.Radiobutton(self.left_frame, text="Убывание по столбцам", bg=self.background_color,
                                    variable=self.entry_is_sort_matrix_x, value=2, font=self.font_style)
        self.r_sort_x_3.grid(row=17, columnspan=4, sticky="w")

        #####################################

        self.button_generate = tk.Button(self.left_frame, text="Сгенерировать", font=self.font_style,
                                         bg=self.button_color,
                                         command=self.generate_matrix)
        self.button_generate.grid(row=18, column=0, columnspan=4, pady=10)

        tk.Label(self.left_frame, text="Результат", bg=self.background_color, font=self.font_style_head).grid(row=19, columnspan=4)

        self.original_image = Image.open(self.path_img_empty)
        self.resized_image = self.original_image.resize((self.ing_width, self.img_height), Image.LANCZOS)
        self.my_image = ImageTk.PhotoImage(self.resized_image)
        self.label = tk.Label(self.left_frame, bg=self.background_color, image=self.my_image)
        self.label.image = self.my_image
        self.label.grid(row=20, column=0)

        tk.Label(self.left_frame, text="Сумма", bg=self.background_color, font=self.font_style).grid(row=20, column=1)
        self.sum_entry = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=(self.entry_width*2))
        self.sum_entry.grid(row=20, column=2, columnspan=2)

        '''label = tk.Label(self.left_frame, bg=self.background_color, image=self.my_image)
        label.image = self.my_image
        label.grid(row=21, column=0)

        tk.Label(self.left_frame, text="Наивный", bg=self.background_color, font=self.font_style).grid(row=21, column=1)
        self.sum_entry_greedy_d = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width * 2)
        self.sum_entry_greedy_d.grid(row=21, column=2, columnspan=2)

        label = tk.Label(self.left_frame, bg=self.background_color, image=self.my_image)
        label.image = self.my_image
        label.grid(row=22, column=0)

        tk.Label(self.left_frame, text="Погрешность", bg=self.background_color, font=self.font_style).grid(row=22, column=1)
        self.error = tk.Entry(self.left_frame, bg=self.entry_color, font=self.font_style, width=self.entry_width * 2)
        self.error.grid(row=22, column=2, columnspan=2)'''

        self.button_generate = tk.Button(self.left_frame, text="Расчитать", font=self.font_style, bg=self.button_color,
                                    command=self.calculate_matrix)
        self.button_generate.grid(row=21, column=0, columnspan=4, pady=10)

        #####################################

        style = ttk.Style()
        style.configure("TNotebook")
        style.configure("TNotebook.Tab", padding=[20, 10], font=self.font_style_notebook, background=self.background_color,
                        foreground="black")

        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.grid(row=3, column=2, sticky='nsew')

        self.frame_c = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.frame_d = [ttk.Frame(self.notebook, style="Custom.TFrame")]
        self.frame_lambda = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.frame_res = ttk.Frame(self.notebook, style="Custom.TFrame")

        self.notebook.add(self.frame_c, text="Матрица C")
        self.notebook.add(self.frame_d[0], text="D1")
        self.notebook.add(self.frame_lambda, text="λ")
        self.notebook.add(self.frame_res, text="X")

        self.c_matrix = [[]]
        self.d_matrix = [[[]]]
        self.b = []
        self.l = []

        matrix = np.zeros((int(self.entry_n.get()), int(self.entry_n.get())))
        matrix_d = np.zeros((int(self.entry_k.get()), int(self.entry_n.get()), int(self.entry_n.get())))
        vector = np.ones(int(self.entry_k.get()))
        self.create_c_matrix(matrix, self.frame_c)
        self.create_d_matrix(matrix_d, vector, self.frame_d)
        self.create_lambda(vector, self.frame_lambda)

        # self.show_matrix_on_frame(matrix, matrix, self.frame_veng_max)
        self.show_matrix_on_frame(matrix, matrix, self.frame_res)

        self.root.mainloop()

        self.root.destroy()

    def change_entry(self, event):
        n = int(self.entry_n.get())
        k = int(self.entry_k.get())
        n_max = int(self.entry_n_max.get())
        c_min = int(self.entry_c_min.get())
        c_max = int(self.entry_c_max.get()) + 1

        if not self.validate_entry(n, k, n_max, c_min, c_max):
            return

        self.c_matrix = [[]]
        self.d_matrix = [[[]]]
        self.b = []

        matrix = np.zeros((int(self.entry_n.get()), int(self.entry_n.get())))
        matrix_d = np.zeros((int(self.entry_k.get()), int(self.entry_n.get()), int(self.entry_n.get())))
        vector = np.ones(int(self.entry_k.get()))

        self.create_c_matrix(matrix, self.frame_c)

        for tab_id in self.notebook.tabs():
            tab_text = self.notebook.tab(tab_id, "text")
            if tab_text.startswith('D') or tab_text == 'X' or tab_text == 'λ':
                tab_widget = self.notebook.nametowidget(tab_id)
                self.notebook.forget(tab_id)
                tab_widget.destroy()

        self.frame_d = []
        self.frame_lambda = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.frame_res = ttk.Frame(self.notebook, style="Custom.TFrame")

        for i in range(int(self.entry_k.get())):
            self.frame_d.append(ttk.Frame(self.notebook, style="Custom.TFrame"))
        for i in range(int(self.entry_k.get())):
            self.notebook.add(self.frame_d[i], text=f"D{i+1}")
        self.notebook.add(self.frame_lambda, text="λ")
        self.notebook.add(self.frame_res, text="X")

        self.create_d_matrix(matrix_d, vector, self.frame_d)
        self.create_lambda(vector, self.frame_lambda)
        self.show_matrix_on_frame(matrix, matrix, self.frame_res)

    def create_c_matrix(self, matrix, frame):
        self.c_matrix = [[0 for _ in range(matrix.shape[0])] for _ in range(matrix.shape[0])]
        for widget in frame.winfo_children():
            widget.destroy()

        # label = tk.Label(frame, text="Дни", font=self.font_style_notebook_frame, bg=self.matrix_color_up, width=int(self.matrix_width * matrix.shape[0]*1.06), height=self.matrix_height, borderwidth=1,
        #                  relief="solid")
        # label.grid(row=0, column=1, columnspan=matrix.shape[1])

        # label = tk.Label(frame, text="Подразделения", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height*2, borderwidth=1,
        #                  relief="solid")
        # label.grid(row=0, column=0, rowspan=2)

        for i in range(len(matrix)):
            label = tk.Label(frame, text=i + 1, font=self.font_style_notebook_frame, bg=self.matrix_color_up, width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1, relief="solid")
            label.grid(row=1, column=i + 1)

        for i in range(len(matrix)):
            # label = tk.Label(frame, text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height,
            #                  borderwidth=1,
            #                  relief="solid")
            # label.grid(row=i + 2, column=0)
            label = tk.Label(frame, text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left,
                             width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=0)
            for j in range(len(matrix[i])):
                self.c_matrix[i][j] = tk.Entry(frame, font=self.font_style_notebook_frame, bg=self.matrix_color_cell, width=self.matrix_width,
                                 borderwidth=1,
                                 relief="solid")
                self.c_matrix[i][j].insert(0, int(matrix[i][j]))
                self.c_matrix[i][j].grid(row=i + 2, column=j + 1, ipady=11)  # Сдвигаем на 1 вниз для числа

    def create_d_matrix(self, matrix, vector, frame):
        self.d_matrix = [[[0 for _ in range(matrix.shape[2])] for _ in range(matrix.shape[1])] for _ in range(len(frame))]
        self.b = [1 for _ in range(len(frame))]
        for l in range(matrix.shape[0]):
            for widget in frame[l].winfo_children():
                widget.destroy()

            # label = tk.Label(frame[l], text="Дни", font=self.font_style_notebook_frame, bg=self.matrix_color_up, width=int(self.matrix_width * matrix.shape[1]*1.06), height=self.matrix_height, borderwidth=1,
            #                  relief="solid")
            # label.grid(row=0, column=1, columnspan=matrix.shape[1])

            # label = tk.Label(frame[l], text="Подразделения", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height*2, borderwidth=1,
            #                  relief="solid")
            # label.grid(row=0, column=0, rowspan=2)

            label = tk.Label(frame[l], text="b", font=self.font_style_notebook_frame,
                             bg=self.matrix_color_param, width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=1, column=matrix.shape[1]+2, padx=10)

            for i in range(matrix.shape[1]):
                label = tk.Label(frame[l], text=i + 1, font=self.font_style_notebook_frame, bg=self.matrix_color_up, width=self.matrix_width, height=self.matrix_height,
                                 borderwidth=1, relief="solid")
                label.grid(row=1, column=i + 1)

            for i in range(matrix.shape[1]):
                # label = tk.Label(frame[l], text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height,
                #                  borderwidth=1,
                #                  relief="solid")
                # label.grid(row=i + 2, column=0)
                label = tk.Label(frame[l], text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left,
                                 width=self.matrix_width, height=self.matrix_height,
                                 borderwidth=1,
                                 relief="solid")
                label.grid(row=i + 2, column=0)
                for j in range(matrix.shape[2]):
                    self.d_matrix[l][i][j] = tk.Entry(frame[l], font=self.font_style_notebook_frame, bg=self.matrix_color_cell, width=self.matrix_width,
                                     borderwidth=1,
                                     relief="solid")
                    self.d_matrix[l][i][j].insert(0, int(matrix[l][i][j]))
                    self.d_matrix[l][i][j].grid(row=i + 2, column=j + 1, ipady=11)  # Сдвигаем на 1 вниз для числа

            self.b[l] = tk.Entry(frame[l], font=self.font_style_notebook_frame, bg=self.matrix_color_cell,
                                              width=self.matrix_width,
                                              borderwidth=1,
                                              relief="solid")
            self.b[l].insert(0, int(vector[l]))
            self.b[l].grid(row=2, column=matrix.shape[1]+2, ipady=11)

    def create_lambda(self, vector, frame):
        self.l = [1 for _ in range(vector.shape[0])]
        for widget in frame.winfo_children():
            widget.destroy()

        label = tk.Label(frame, text="λ", font=self.font_style_notebook_frame, bg=self.matrix_color_up,
                         width=self.matrix_width, height=self.matrix_height,
                         borderwidth=1,
                         relief="solid")
        label.grid(row=0, column=1)

        for i in range(vector.shape[0]):
            label = tk.Label(frame, text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left,
                             width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 1, column=0)
            self.l[i] = tk.Entry(frame, font=self.font_style_notebook_frame,
                                              bg=self.matrix_color_cell, width=self.matrix_width,
                                              borderwidth=1,
                                              relief="solid")
            self.l[i].insert(0, int(vector[i]))
            self.l[i].grid(row=i + 1, column=1, ipady=11)  # Сдвигаем на 1 вниз для числа

    def get_c_matrix(self):
        c = np.zeros((len(self.c_matrix),len(self.c_matrix)))
        for i in range(len(self.c_matrix)):
            for j in range(len(self.c_matrix)):
                c[i][j] = int(self.c_matrix[i][j].get())
        return c

    def get_d_matrix(self):
        d = np.zeros((len(self.d_matrix),len(self.c_matrix),len(self.c_matrix)))
        for i in range(len(self.d_matrix)):
            for j in range(len(self.c_matrix)):
                for l in range(len(self.c_matrix)):
                    d[i][j][l] = int(self.d_matrix[i][j][l].get())
        return d

    def get_b(self):
        b = np.zeros(len(self.d_matrix))
        for i in range(len(self.d_matrix)):
            b[i] = int(self.b[i].get())
        return b

    def get_l(self):
        l = np.zeros(len(self.d_matrix))
        for i in range(len(self.d_matrix)):
            l[i] = int(self.l[i].get())
        return l

    def show_matrix_on_frame(self, matrix, res, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        # label = tk.Label(frame, text="Дни", font=self.font_style_notebook_frame, bg=self.matrix_color_up,
        #                  width=int(self.matrix_width * matrix.shape[0] * 1.06), height=self.matrix_height, borderwidth=1,
        #                  relief="solid")
        # label.grid(row=0, column=1, columnspan=matrix.shape[1])

        # label = tk.Label(frame, text="Подразделения", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height*2, borderwidth=1,
        #                  relief="solid")
        # label.grid(row=0, column=0, rowspan=2)

        for i in range(len(matrix)):
            label = tk.Label(frame, text=i + 1, font=self.font_style_notebook_frame, bg=self.matrix_color_up, width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1, relief="solid")
            label.grid(row=1, column=i + 1)

        for i in range(len(matrix)):
            # label = tk.Label(frame, text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left, width=int(self.matrix_width*2.5), height=self.matrix_height,
            #                  borderwidth=1,
            #                  relief="solid")
            # label.grid(row=i + 2, column=0)
            label = tk.Label(frame, text=f"{i + 1}", font=self.font_style_notebook_frame, bg=self.matrix_color_left,
                             width=self.matrix_width, height=self.matrix_height,
                             borderwidth=1,
                             relief="solid")
            label.grid(row=i + 2, column=0)
            for j in range(len(matrix[i])):
                color = self.matrix_color_cell
                if(res[i][j] == 1):
                    color = self.select_color_1
                if(res[i][j] == 2):
                    color = self.select_color_2
                label = tk.Label(frame, text=int(matrix[i][j]), font=self.font_style_notebook_frame, bg=color, width=self.matrix_width, height=self.matrix_height,
                                 borderwidth=1,
                                 relief="solid")
                label.grid(row=i + 2, column=j + 1)

    def generate_matrix(self):
        n = int(self.entry_n.get())
        k = int(self.entry_k.get())
        n_max = int(self.entry_n_max.get())
        c_min = int(self.entry_c_min.get())
        c_max = int(self.entry_c_max.get()) + 1

        if not self.validate_entry(n, k, n_max, c_min, c_max):
            return

        is_sort_matrix_y = self.entry_is_sort_matrix_y.get()
        is_sort_matrix_x = self.entry_is_sort_matrix_x.get()

        c = create_c(n, c_min, c_max)
        # d = self.get_d_matrix()
        # b = self.get_b()

        if (is_sort_matrix_y == "1"):
            c = increase_by_row(c)
        if (is_sort_matrix_y == "2"):
            c = de_increase_by_row(c)

        if (is_sort_matrix_x == "1"):
            c = increase_by_col(c)
        if (is_sort_matrix_x == "2"):
            c = de_increase_by_col(c)

        self.create_c_matrix(c, self.frame_c)
        # self.create_d_matrix(d, b, self.frame_d)

        res = np.zeros((int(self.entry_n.get()), int(self.entry_n.get())))
        self.show_matrix_on_frame(c, res, self.frame_res)

    def calculate_matrix(self):
        n = int(self.entry_n.get())
        k = int(self.entry_k.get())
        n_max = int(self.entry_n_max.get())
        c_min = int(self.entry_c_min.get())
        c_max = int(self.entry_c_max.get()) + 1

        self.validate_entry(n, k, n_max, c_min, c_max)

        n = int(self.entry_n.get())
        k = int(self.entry_k.get())
        n_max = int(self.entry_n_max.get())
        c = self.get_c_matrix()
        d = self.get_d_matrix()
        b = self.get_b()
        l = self.get_l()

        sum, res = main(n, k, n_max, c, d, b, l)

        self.show_matrix_on_frame(c, res, self.frame_res)

        self.sum_entry.delete(0, tk.END)
        self.sum_entry.insert(0, str(f"{round(sum, 2)}"))

    def validate_entry(self, n, k, n_max, c_min, c_max):
        try:
            n_max = int(self.entry_n_max.get())
            if not (1 <= n <= 15 and 1 <= k <= 10 and 1 <= n_max <= 100000 and 0 <= c_min < c_max <= 100000):
                raise ValueError
            self.sum_entry.delete(0, tk.END)
            self.sum_entry.config(foreground='black')
            return True
        except ValueError:
            self.sum_entry.delete(0, tk.END)
            self.sum_entry.insert(0, "ERROR")
            self.sum_entry.config(foreground='red')
            return False

    def check_n_max(self, event=None):
        try:
            n_max = int(self.entry_n_max.get())
            if not (1 <= n_max <= 100000):
                raise ValueError
            self.sum_entry.delete(0, tk.END)
            self.sum_entry.config(foreground='black')
            return True
        except ValueError:
            self.sum_entry.delete(0, tk.END)
            self.sum_entry.insert(0, "ERROR")
            self.sum_entry.config(foreground='red')
            return False
    def on_close(self):
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    window = Window()