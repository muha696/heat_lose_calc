import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from heat_lose import HeatLoses
import pandas as pd



class PipeSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет тепловых потерь в трубопроводах")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)

        self.pipes = []
        self.branches = []

        self.create_input_widgets()
        self.create_canvas()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

    def create_input_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Параметры трубопровода")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(input_frame, text="Температура прямой воды, °C:").grid(row=0, column=0, sticky="w")
        self.temp_p = ttk.Entry(input_frame)
        self.temp_p.grid(row=0, column=1, padx=5, pady=5)
        self.temp_p.insert(0, "90")

        ttk.Label(input_frame, text="Температура обратной воды, °C:").grid(row=1, column=0, sticky="w")
        self.temp_o = ttk.Entry(input_frame)
        self.temp_o.grid(row=1, column=1, padx=5, pady=5)
        self.temp_o.insert(0, "50")

        ttk.Label(input_frame, text="Расход, т/ч:").grid(row=2, column=0, sticky="w")
        self.flow_entry = ttk.Entry(input_frame)
        self.flow_entry.grid(row=2, column=1, padx=5, pady=5)
        self.flow_entry.insert(0, "100")

        ttk.Label(input_frame, text="Диаметр трубопровода, мм:").grid(row=3, column=0, sticky="w")
        self.dn = tk.StringVar(input_frame)
        self.dn_menu = ttk.Combobox(input_frame, textvariable=self.dn, values=[str(i) for i in [133, 159, 165, 219, 273, 325, 377,
                                                             426, 530, 630, 720]])
        self.dn_menu.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Толщина стенки ПУ, мм").grid(row=4, column=0, sticky="w")
        self.su = ttk.Entry(input_frame)
        self.su.grid(row=4, column=1, padx=5, pady=5)
        self.su.insert(0, "12")

        ttk.Label(input_frame, text="Коэффициент теплоизоляции прямого трубопровода:").grid(row=5, column=0, sticky="w")
        self.lamizp = ttk.Entry(input_frame)
        self.lamizp.grid(row=5, column=1, padx=5, pady=5)
        self.lamizp.insert(0, "0.033")

        ttk.Label(input_frame, text="Коэффициент теплоизоляции обратного трубопровода:").grid(row=6, column=0, sticky="w")
        self.lamizo = ttk.Entry(input_frame)
        self.lamizo.grid(row=6, column=1, padx=5, pady=5)
        self.lamizo.insert(0, "0.033")

        ttk.Label(input_frame, text="Коэффициент местных тепловых потерь").grid(row=7, column=0, sticky="w")
        self.mu = ttk.Entry(input_frame)
        self.mu.grid(row=7, column=1, padx=5, pady=5)
        self.mu.insert(0, "0")

        input_frame_air = ttk.LabelFrame(self.root, text="Параметры потребителя")
        input_frame_air.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(input_frame_air, text="Потребление потребителя, Гкал/ч:").grid(row=2, column=0, sticky="w")
        self.q_cons = ttk.Entry(input_frame_air)
        self.q_cons.grid(row=2, column=1, padx=5, pady=5)
        self.q_cons.insert(0, "0")

        input_frame_air = ttk.LabelFrame(self.root, text="Параметры окружающей среды")
        input_frame_air.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(input_frame_air, text="Температура грунта, °C:").grid(row=2, column=0, sticky="w")
        self.temp_gr = ttk.Entry(input_frame_air)
        self.temp_gr.grid(row=2, column=1, padx=5, pady=5)
        self.temp_gr.insert(0, "5")

        ttk.Label(input_frame_air, text="Теплопроводность грунта:").grid(row=3, column=0, sticky="w")
        self.lam_gr = ttk.Entry(input_frame_air)
        self.lam_gr.grid(row=3, column=1, padx=5, pady=5)
        self.lam_gr.insert(0, "1.92")

        self.sections_frame = ttk.LabelFrame(self.root, text="Участки трубопровода")
        self.sections_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(self.sections_frame, text="Название участка").grid(row=0, column=0, sticky="w")
        self.section_length_name = ttk.Entry(self.sections_frame)
        self.section_length_name.grid(row=0, column=1, padx=5, pady=5)
        self.section_length_name.insert(0, "")

        ttk.Label(self.sections_frame, text="Длина участка, м:").grid(row=1, column=0, sticky="w")
        self.section_length_entry = ttk.Entry(self.sections_frame)
        self.section_length_entry.grid(row=1, column=1, padx=5, pady=5)
        self.section_length_entry.insert(0, "1")

        self.add_section_button = ttk.Button(self.sections_frame, text="Добавить участок", command=self.add_section)
        self.add_section_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_last_btn = ttk.Button(self.sections_frame, text="Удалить выделенный", command=self.delete_section)
        self.delete_last_btn.grid(row=1, column=2, padx=5, pady=5)

        self.load_sections_button = ttk.Button(self.sections_frame, text="Загрузить из Excel",
                                               command=self.load_sections_from_excel)
        self.load_sections_button.grid(row=2, column=2, padx=5, pady=5)

        self.sections_listbox = tk.Listbox(self.sections_frame, height=5)
        self.sections_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        action_frame = ttk.LabelFrame(self.root, text="Действия")
        action_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        self.calcbtn = ttk.Button(action_frame, text="Расчитать", command=self.calc_lose)
        self.calcbtn.grid(row=4, column=0, pady=5)

        self.excelbtn = ttk.Button(action_frame, text="Экспорт в эксель", state="disabled", command=self.export_to_excel)
        self.excelbtn.grid(row=4, column=1, pady=5, sticky="w")

        self.save_graph = ttk.Button(action_frame, text="Сохранить график", state="disabled")
        self.save_graph.grid(row=4, column=2, pady=5, sticky="w")


    def create_canvas(self):
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.ax.spines['bottom'].set_linewidth(1.5)
        self.ax.spines['left'].set_linewidth(1.5)
        self.ax.spines['right'].set_linewidth(1.5)
        self.ax.spines['top'].set_linewidth(1.5)
        self.ax.set_xlabel("Длина, м")
        self.ax.set_ylabel("Температура воды, °C")
        self.ax.grid(True, linestyle='--', color='k', linewidth=1)

    def add_section(self):
        name = self.section_length_name.get()
        length = self.section_length_entry.get()
        if length:
            self.sections_listbox.insert(tk.END, f"{name} - {length} м")

    def delete_section(self):
        selected_indices = self.sections_listbox.curselection()
        for index in reversed(selected_indices):
            self.sections_listbox.delete(index)

    def load_sections_from_excel(self):
        """Загрузить участки из Excel файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if not file_path:
            return  # пользователь отменил

        try:
            df = pd.read_excel(file_path)

            # Проверяем, что в файле есть нужные столбцы
            if 'Название участка' not in df.columns or 'Длина' not in df.columns:
                messagebox.showerror("Ошибка", "Файл должен содержать столбцы 'Название' и 'Длина'!")
                return

            # Очищаем старые данные
            self.sections_listbox.delete(0, tk.END)

            # Добавляем новые данные
            for _, row in df.iterrows():
                name = str(row['Название участка'])
                length = str(row['Длина'])
                self.sections_listbox.insert(tk.END, f"{name} - {length} м")

            messagebox.showinfo("Успешно", "Участки загружены из Excel!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def get_sections_lengths(self):
        sections = []
        for i in range(self.sections_listbox.size()):
            item_text = self.sections_listbox.get(i)
            list_item = item_text.split()
            try:
                name_section = list_item[0]
                length_m = list_item[2]
                sections.append([name_section, length_m])
            except ValueError:
                pass
        return sections

    def calc_lose(self):
        try:
            self.ax.clear()
            dn = float(self.dn.get())
            su = float(self.su.get())
            tp = float(self.temp_p.get())
            to = float(self.temp_o.get())
            tgr = float(self.temp_gr.get())
            lamizp = float(self.lamizp.get())
            lamizo = float(self.lamizo.get())
            lamgr = float(self.lam_gr.get())
            mu = float(self.mu.get())
            flow = float(self.flow_entry.get())
            sections_data = self.get_sections_lengths()
            sections_lengths = [float(i[1]) for i in sections_data]
            self.sections_name = [i[0] for i in sections_data]
            result_calc_lose = HeatLoses(dn = dn, su=su, tin=tp, tou=to, tgr=tgr, lamizp=lamizp, lamizo=lamizo, lamgr=lamgr)
            self.q_pr = result_calc_lose.calc_los()[1]
            self.flow = flow
            self.l_series = sections_lengths

            #Расчет прямой воды
            self.tp_data = [tp]
            self.tp_list = []
            self.l_list = [0]
            tp_in = tp
            for i in sections_lengths:
                Q_pr = self.q_pr * i * (1 + mu)
                delta_t = Q_pr * 0.001 / ((flow / 3.6) * 4.185)
                tp_out = tp_in - delta_t
                self.tp_data.append(tp_out)
                self.tp_list.append([tp_in, tp_out])
                tp_in = tp_out
                self.l_list.append(self.l_list[-1] + i)

            self.ax.clear()
            self.ax.plot(self.l_list, self.tp_data)
            self.ax.spines['bottom'].set_linewidth(1.5)
            self.ax.spines['left'].set_linewidth(1.5)
            self.ax.spines['right'].set_linewidth(1.5)
            self.ax.spines['top'].set_linewidth(1.5)
            self.ax.set_xlabel("Длина, м")
            self.ax.set_ylabel("Температура воды, °C")
            self.ax.grid(True, linestyle='--', color='k', linewidth=1)
            self.canvas.draw()

            self.excelbtn.config(state='normal')

        except Exception as e:
            messagebox.showerror(title="Ошибка", message=f'Ошибка в данных {e}!')


    def export_to_excel(self):
        data_to_excel = {
            'Название участка': [],
            'Длина участка': [],
            'Расход воды на участке, т/ч': [],
            'Диаметр трубы, мм': [],
            'Тип прокладки': [],
            'Температура прямой воды на входе в участок': [],
            'Температура прямой воды на выходе из участка': [],
            'Тепловые потери на участке в подающем трубопроводе, Вт': [],
            'Тепловые потери на участке в подающем трубопроводе, ккал/ч': [],
        }

        for i in range(len(self.l_series)):
            data_to_excel['Название участка'].append(self.sections_name[i])
            data_to_excel['Длина участка'].append(self.l_series[i])
            data_to_excel['Расход воды на участке, т/ч'].append(self.flow)
            data_to_excel['Диаметр трубы, мм'].append(float(self.dn.get()))
            data_to_excel['Тип прокладки'].append('Подземная бесканальная')
            data_to_excel['Температура прямой воды на входе в участок'].append(self.tp_list[i][0])
            data_to_excel['Температура прямой воды на выходе из участка'].append(self.tp_list[i][1])
            q_in = self.q_pr * self.l_series[i] * (1 + float(self.mu.get()))
            data_to_excel['Тепловые потери на участке в подающем трубопроводе, Вт'].append(q_in)
            data_to_excel['Тепловые потери на участке в подающем трубопроводе, ккал/ч'].append(q_in * 0.8598452278589853)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")],
                                                 title="Сохранение расчётов в Excel")

        if not file_path:
            return

        df = pd.DataFrame(data_to_excel)
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Успешно", f"Данные сохранены в файл:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении файла:\n{e}")


    def on_close(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = '12'
    plt.rcParams.update({'figure.max_open_warning': 0})
    root = tk.Tk()
    app = PipeSystemApp(root)
    root.mainloop()