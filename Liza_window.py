import customtkinter as ctk

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