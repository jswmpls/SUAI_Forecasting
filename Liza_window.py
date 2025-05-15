import customtkinter as ctk
import tkinter as tk
import json

class LizaWindow(ctk.CTkToplevel):

    # Базовый каркас приложения
    def __init__(self, master):
        super().__init__(master)
        self.data = None
        self.title("Анализ инфекционных заболеваний")
        self.geometry("800x650+350+10")
        self.main_app = master

        # Верхняя панель с кнопками
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=10, pady=5)

        # Кнопки управления
        self.forecast_entry = ctk.CTkEntry(top_frame, placeholder_text="Введите N лет для прогноза", width=200)
        self.forecast_entry.pack(side='left', padx=5)
        ctk.CTkButton(top_frame, text="Показать прогноз").pack(side='left', padx=5)
        ctk.CTkButton(top_frame, text="Назад", command=self.go_back).pack(side='right', padx=5)

        # Области для отображения
        self.table = ctk.CTkTextbox(self, height=150)
        self.table.pack(fill='x', padx=10, pady=5)
        self.plot_output = ctk.CTkTextbox(self, height=150)
        self.plot_output.pack(fill='x', padx=10, pady=5)
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Автоматическая загрузка данных при открытии окна
        self.load_data()

    def go_back(self):
        self.destroy()
        self.main_app.deiconify()

    # Функционал загрузки и отображения данных
    def load_data(self, filepath="infection_data.json"):
        """Автоматическая загрузка данных из JSON файла"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.show_table()

    def show_table(self):
        """Отображение данных в табличном виде"""
        if not self.data:
            return

        years = self.data["years"]
        items = self.data["items"]

        # Формируем строку с таблицей
        table_text = "Год\t" + "\t".join(items.keys()) + "\n"
        for year in years:
            row = [str(items[item][years.index(year)]) for item in items]
            table_text += f"{year}\t" + "\t".join(row) + "\n"

        self.table.delete("1.0", tk.END)
        self.table.insert("1.0", table_text)