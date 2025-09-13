import customtkinter as ctk
import tkinter.messagebox as msgbox
from Widget import Widget

class WidgetRegisterStudent(Widget):
    def __init__(self, setting_file, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.status_callback = status_callback
        self.student_name_entry = None
        self.register_student_button = None

    # 「生徒登録」ウィジェット作成
    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_label(frame, 0, 0, u'生徒登録')
        self.student_name_entry = self.create_entry(
              frame
            , 1, 0
            , 200
            , u'生徒名を入力'
            , None
            , None
            , 'normal'
        )
        self.register_student_button = self.create_button(
              frame
            , 1, 1
            , u'登録'
            , self.event_register_student
        )

    # 「生徒登録」エントリーの値を取得
    def get_student_name_entry(self):
        return self.student_name_entry.get()

    # 「生徒登録」エントリーの値を削除
    def clear_student_name_entry(self):
        self.student_name_entry.delete(0, ctk.END)

    # 登録ボタンの状態を変更
    def button(self, state):
        if self.register_student_button:
            self.register_student_button.configure(state = state)

    # イベント発生条件：「登録」ボタンを押したとき
    # 処理概要：「生徒登録」エントリーに記入した名前を設定ファイルに登録する
    def event_register_student(self):
        # 「生徒登録」エントリーが空欄のとき、エラーを通知する
        student_name = self.get_student_name_entry()
        if not student_name:
            msgbox.showerror('Error', u'名前を入力してください')
            return

        # 「生徒登録」エントリーに記入した名前がすでに登録済みのとき、エラーを通知する
        if self.setting_file.is_registered_student(student_name):
            msgbox.showerror('Error', u'既に登録済みです')
            return

        # 設定ファイルに生徒を登録する
        self.setting_file.set_register_student(student_name)

        # 設定ファイルに生徒を登録した後に登録できたことを伝えるため、「生徒登録」エントリーを空欄にする
        # 煩わしいため、メッセージボックスは使用しない
        self.clear_student_name_entry()

        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_RegisterStudent)