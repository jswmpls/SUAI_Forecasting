import customtkinter as ctk
import tkinter as tk
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog


class LizaWindow(ctk.CTkToplevel):
    """Окно с анализом инфекционных заболеваний (выбор файла вручную)."""

    def __init__(self, master):
        super().__init__(master)
        self.data = None
        self.title("Анализ инфекционных заболеваний")
        self.geometry("800x650+350+10")
        self.main_app = master
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Верхняя панель
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=10, pady=5)

        # Кнопка "Открыть файл"
        self.file_button = ctk.CTkButton(top_frame, text="Открыть файл", command=self.load_data)
        self.file_button.pack(side='left', padx=5)

        # Ввод прогноза
        self.forecast_entry = ctk.CTkEntry(top_frame, placeholder_text="Введите N лет для прогноза", width=200)
        self.forecast_entry.pack(side='left', padx=5)

        # Прогноз и назад
        ctk.CTkButton(top_frame, text="Показать прогноз", command=self.plot_forecast).pack(side='left', padx=5)
        ctk.CTkButton(top_frame, text="Назад", command=self.go_back).pack(side='right', padx=5)

        # Отображение данных
        self.table = ctk.CTkTextbox(self, height=150)
        self.table.pack(fill='x', padx=10, pady=5)

        self.plot_output = ctk.CTkTextbox(self, height=150)
        self.plot_output.pack(fill='x', padx=10, pady=5)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def go_back(self):
        self.destroy()
        self.main_app.deiconify()

    def load_data(self, filepath=None):
        """Загрузка данных из JSON-файла через диалог, если путь не указан."""
        if not filepath:
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.show_table()
        except Exception as e:
            self.table.delete("1.0", tk.END)
            self.table.insert("1.0", f"Ошибка загрузки файла: {e}")

    def show_table(self):
        if not self.data:
            return

        years = self.data["years"]
        items = self.data["items"]
        table_text = "Год\t" + "\t".join(items.keys()) + "\n"
        for year in years:
            row = [str(items[item][years.index(year)]) for item in items]
            table_text += f"{year}\t" + "\t".join(row) + "\n"

        self.table.delete("1.0", tk.END)
        self.table.insert("1.0", table_text)

    def plot_forecast(self):
        self.plot_output.delete("1.0", tk.END)
        if not self.data:
            self.plot_output.insert("1.0", "Сначала загрузите файл с данными!\n")
            return

        try:
            N = int(self.forecast_entry.get())
            if N <= 0:
                raise ValueError
        except ValueError:
            self.plot_output.insert("1.0", "Ошибка: введите положительное число\n")
            return

        years = self.data["years"]
        infections = self.data["items"]
        df = pd.DataFrame(infections, index=years)

        changes = {inf: (df[inf].iloc[0] - df[inf].iloc[-1]) / df[inf].iloc[0] * 100 for inf in infections}
        max_item = max(changes.items(), key=lambda x: x[1])
        min_item = min(changes.items(), key=lambda x: x[1])

        forecast_years = [years[-1] + i + 1 for i in range(N)]
        forecast_df = df.copy()
        for year in forecast_years:
            forecast_df.loc[year] = df.iloc[-3:].mean() * (1 + np.random.normal(0, 0.08, len(df.columns)))

        result_text = (
            f"Наибольшее снижение: {max_item[0]} ({max_item[1]:.1f}%)\n"
            f"Наименьшее снижение: {min_item[0]} ({min_item[1]:.1f}%)\n\n"
            f"Прогноз на {N} лет:\n{forecast_df.tail(N).astype(int)}"
        )
        self.plot_output.insert("1.0", result_text)
        self.plot_graph(df, forecast_df)

    def plot_graph(self, history, forecast=None):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))
        for column in history.columns:
            ax.plot(history.index, history[column], label=column)
            if forecast is not None:
                ax.plot(forecast.index, forecast[column], '--', alpha=0.7)
                ax.fill_between(forecast.index, forecast[column] * 0.9, forecast[column] * 1.1, alpha=0.1)

        if forecast is not None:
            ax.axvline(x=history.index[-1], color='red', linestyle=':', alpha=0.5)

        ax.set_title(self.title())
        ax.set_xlabel("Год")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def on_close(self):
        """Метод для остановки программы после закрытия окна."""
        self.destroy()
        self.quit()
