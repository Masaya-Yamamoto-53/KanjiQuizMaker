# KanjiQuizMaker.py
import customtkinter as ctk
import tkinter.messagebox as msgbox

from SettingFile import SettingFile

class KanjiQuizMaker:
    ERROR_EMPTY_NAME = u'名前を入力してください'
    ERROR_ALREADY_REGISTERED = u'既に登録済みです'

    def __init__(self):
        # 設定ファイルを読み込む
        self.setting_file = SettingFile()

        self.setup_root()
        self.setup_widgets()

    def setup_root(self):
        self.root = ctk.CTk()
        self.root.title('漢字プリントメーカー')
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_widgets(self):
        self.create_registration_section()

    def create_registration_section(self):
        # メインフレーム（背景色と余白を調整）
        self.registration_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.registration_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self.registration_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        self._create_registration_label()
        self._create_registration_entry_and_button()

    def _create_registration_label(self):
        label = ctk.CTkLabel(
            self.registration_frame,
            text='生徒登録',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

    def _create_registration_entry_and_button(self):
        self.student_name_entry = ctk.CTkEntry(
            self.registration_frame,
            placeholder_text='生徒名を入力',
            height=36
        )
        self.student_name_entry.grid(row=1, column=0, padx=(5, 10), pady=5, sticky='ew')

        self.student_name_register_button = ctk.CTkButton(
            self.registration_frame,
            text='登録',
            command=self.event_register_student,
            width=80,
            height=36
        )
        self.student_name_register_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='w')

    ################################################################################
    # イベントメソッド
    ################################################################################
    # イベント発生条件：「登録」ボタンを押したとき
    # 処理概要：「生徒登録」エントリーに記入した名前を設定ファイルに登録する
    def event_register_student(self):
        # 「生徒登録」エントリーが空欄のとき、エラーを通知する
        student_name = self.student_name_entry.get()
        if not student_name:
            msgbox.showerror('Error', self.ERROR_EMPTY_NAME)
            return

        # 「生徒登録」エントリーに記入した名前がすでに登録済みのとき、エラーを通知する
        if self.setting_file.is_registered_student(student_name):
            msgbox.showerror('Error', self.ERROR_ALREADY_REGISTERED)
            return

        # 生徒を設定ファイルに登録する
        self.setting_file.set_register_student(student_name)

        # 生徒を設定ファイルに登録した後に登録できたことを伝えるため、「生徒登録」エントリーを空欄にする
        # 煩わしいため、メッセージボックスは使用しない
        self.student_name_entry.delete(0, ctk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
