from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json


class DimaWindow(ctk.CTkToplevel):
    """Окно с анализом снижения численности населения по регионам России за последние 15 лет."""

    def __init__(self, master):
        super().__init__(master)
        self.data = None
        self.title("Анализ численности населения")
        self.geometry("800x650+350+10")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Сохраняем ссылку на главное окно
        self.main_app = master

        # Верхняя панель с кнопками
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=10, pady=5)

        self.forecast_entry = ctk.CTkEntry(top_frame, placeholder_text="Введите N лет для прогноза", width=200)
        self.forecast_entry.pack(side='left', padx=5)

        self.table = ctk.CTkTextbox(self, height=150)
        self.table.pack(fill='x', padx=10, pady=5)

        self.plot_output = ctk.CTkTextbox(self, height=150)
        self.plot_output.pack(fill='x', padx=10, pady=5)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def go_back(self):
        """Закрывает текущее окно и возвращает пользователя в главное окно приложения."""
        self.destroy()
        self.main_app.deiconify()

    def load_data(self):
        """Загружает данные из JSON-файла, выбранного пользователем через диалоговое окно."""
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self.show_table()
            except Exception as e:
                self.table.delete("1.0", tk.END)
                self.table.insert("1.0", f"Ошибка загрузки файла: {e}")

    def show_table(self):
        """Форматирует и отображает загруженные данные в виде текстовой таблицы."""
        if self.data:
            years = self.data["years"]
            items = self.data["items"]
            table_str = "Год\t" + "\t".join(items.keys()) + "\n"
            for year in years:
                table_str += str(year) + "\t" + "\t".join(
                    [str(items[item][years.index(year)]) for item in items]) + "\n"
            self.table.delete("1.0", tk.END)
            self.table.insert("1.0", table_str)

    def plot_forecast(self):
        """Метод с анализом снижения численности населения по регионам России за последние 15 лет."""
        self.plot_output.delete("1.0", tk.END)
        if self.data is None:
            self.plot_output.insert("1.0", "Сначала загрузите файл с данными!\n")
            return

        try:
            N = int(self.forecast_entry.get())
            if N <= 0:
                self.plot_output.insert("1.0", "Ошибка: число должно быть положительным.\n")
                return
        except ValueError:
            self.plot_output.insert("1.0", "Ошибка: введите корректное целое число лет для прогноза.\n")
            return

        try:
            years = self.data["years"]
            items_data = self.data["items"]
            df = pd.DataFrame(items_data, index=years)

            decreases = {}
            # Анализ снижения численности населения
            for item in items_data:
                start = df[item].iloc[0]
                end = df[item].iloc[-1]
                if end < start:
                    decreases[item] = start - end

            if not decreases:
                self.plot_output.insert("1.0", "Нет регионов с уменьшением численности.\n")
                return

            max_decrease = max(decreases.items(), key=lambda x: x[1])
            min_decrease = min(decreases.items(), key=lambda x: x[1])

            # Прогнозирование методом скользящей средней
            window = 3
            forecast_years = [years[-1] + i + 1 for i in range(N)]
            forecast_df = df.copy()

            for year in forecast_years:
                last_values = forecast_df.iloc[-window:].mean()
                # Добавляем случайные колебания
                noise = np.random.normal(0, last_values.std() * 0.1, len(last_values))
                forecast_df.loc[year] = last_values + noise

            # Вывод результатов
            result_text = (
                f"Максимальное снижение: {max_decrease[0]} ({max_decrease[1]:.0f} чел.)\n"
                f"Минимальное снижение: {min_decrease[0]} ({min_decrease[1]:.0f} чел.)\n\n"
                f"Прогноз численности населения на {N} лет:\n"
                f"{forecast_df.tail(N).astype(int).to_string()}"
            )
            self.plot_output.insert("1.0", result_text)

            # Построение графика
            self.plot_graph(df, forecast_df)

        except Exception as e:
            self.plot_output.insert("1.0", f"Ошибка: {e}\n")

    def plot_graph(self, history, forecast=None):
        """Метод для построения графиков."""
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))

        # Общая логика построения графиков
        for column in history.columns:
            ax.plot(history.index, history[column], label=column, linewidth=2)

            if forecast is not None:
                ax.plot(forecast.index, forecast[column], '--', alpha=0.7)
                ax.fill_between(
                    forecast.index,
                    forecast[column] * 0.9,
                    forecast[column] * 1.1,
                    alpha=0.1
                )

        if forecast is not None:
            ax.axvline(x=history.index[-1], color='red', linestyle=':', alpha=0.5)

        ax.set_title("Динамика численности населения по регионам")
        ax.set_xlabel("Год")
        ax.set_ylabel("Численность населения")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def on_close(self):
        """Метод для остановки программы после закрытия окна."""
        self.destroy()
        self.quit()
