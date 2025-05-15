from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
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

    def on_close(self):
        """Метод для остановки программы после закрытия окна."""
        self.destroy()
        self.quit()
