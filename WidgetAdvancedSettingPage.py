import customtkinter as ctk

class WidgetAdvancedSettingPage(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk):
        super().__init__(master)
        self.title("Advanced Settings")
        self.geometry("400x300")
        self.configure(fg_color="white")

        label = ctk.CTkLabel(self, text="詳細設定ページ", font=("Arial", 16))
        label.pack(pady=20)

        close_button = ctk.CTkButton(self, text="閉じる", command=self.destroy)
        close_button.pack(pady=10)

