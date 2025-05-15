import customtkinter as ctk
from Liza_window import LizaWindow

# Основное окно приложения
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Анализ данных")
        self.geometry("400x300")
        self.configure_appearance()
        self.create_widgets()

    def configure_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def create_widgets(self):
        # Создаем элементы интерфейса
        ctk.CTkLabel(self, text="Выберите вариант:", font=("Arial", 18)).pack(pady=20)

        # Кнопки для выбора варианта анализа
        ctk.CTkButton(self, text="Вариант Димы").pack(pady=10)
        ctk.CTkButton(self, text="Вариант Лизы", command=self.open_liza_window).pack(pady=10)

    def open_liza_window(self):
        self.withdraw()  # Скрываем главное окно
        LizaWindow(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()