import tkinter as tk
from tkinter import messagebox,ttk
import numpy as np
from statistical_test_realization import generate_sample, criterion_test


class Application:
    
    def __init__(self, root):
        
        self.root = root
        self.root.geometry("800x400")
        self.root.title("Статистический тест χ² для отрицательного биномиального распределения")

        # Основной контейнер для центрирования
        frame = tk.Frame(root)
        frame.pack(expand=True)  # Центрирует все элементы

        # Метки и поля ввода
        tk.Label(frame, text="Число экспериментов:").pack(pady=5)
        self.entry_exp = tk.Entry(frame)
        self.entry_exp.pack(pady=5)

        tk.Label(frame, text="Число интервалов:").pack(pady=5)
        self.entry_int = tk.Entry(frame)
        self.entry_int.pack(pady=5)

        tk.Label(frame, text="Уровень значимости α:").pack(pady=5)
        self.entry_alpha = tk.Entry(frame)
        self.entry_alpha.pack(pady=5)

        # Кнопка запуска теста
        self.btn_run = tk.Button(frame, text="Выполнить тест", command=self.run_test)
        self.btn_run.pack(pady=10)

        # Метка для вывода результата
        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side="top", pady=5, fill="y")

        self.result_label = tk.Label(self.frame_right, text="Результат теста:", font=("Arial", 12, "bold"), fg="black")
        self.result_label.pack()

        self.result_text = tk.Label(self.frame_right, text="", font=("Arial", 12), fg="blue", justify="left")
        self.result_text.pack(pady=10)
        
        # Таблица
        self.tree = ttk.Treeview(frame, columns=("1", "2"), show="headings")
        self.tree.heading('1', text="Интервал")
        self.tree.heading('2', text="Теоретическая вероятность")
        self.tree.column("1", anchor="center", width=150)
        self.tree.column("2", anchor="center", width=200)
        self.tree.pack(pady=10)

    def run_test(self):
     
        try:
            p = 0.5
            n = 3  # успехи
            experiments = int(self.entry_exp.get())
            k = int(self.entry_int.get())
            alpha = float(self.entry_alpha.get())
            
            if k < 2 or not (0 < alpha < 1):
                raise ValueError

            # Генерация выборки
            generated_sample = generate_sample(n, p, experiments) #список
            sample = np.array(generated_sample)
            
            # Выполняем хи-квадрат тест
            int_prob, intervals, F, accept_h0 = criterion_test (sample, k, alpha, p, n)

            # Формируем текст результата
            result_text = f"Значение обратной функции распределения хи квадрат(p-value): {F}\n"
            result_text += "Гипотеза H₀ отвергается" if accept_h0 else "Гипотеза H₀ принимается"
            self.result_label.config(text=result_text, fg="green" if not accept_h0 else "red")
        
            # Очищаем старые данные в таблице
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Заполняем таблицу теоретическими вероятностями
            for i in range(len(intervals) - 1):
                interval = f"[{intervals[i]:.1f}, {intervals[i+1]:.1f})"
                self.tree.insert("", "end", values=(interval, f"{int_prob[i]:.4f}"))    
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения параметров!")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

