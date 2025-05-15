import customtkinter as ctk


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

    def on_close(self):
        """Метод для остановки программы после закрытия окна."""
        self.destroy()
        self.quit()
