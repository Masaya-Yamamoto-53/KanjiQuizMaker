# WidgetSelectStudent.py
import customtkinter as ctk
import tkinter.messagebox as msgbox
from Widget import Widget

class WidgetSelectStudent(Widget):
    def __init__(self, setting_file, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.status_callback = status_callback

    # 生徒選択
    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_label(frame, 0, 0, u'生徒選択')
        self.create_combbox(frame, 1, 0)
        self.create_button(
              frame
            , 1, 1
            , u'削除'
            , self.event_delete_student
            , 'delete_student_button'
        )

    def create_combbox(self, frame, row, column):
        if self.setting_file.is_empty():
            values = [u'']
        else:
            values = self.setting_file.get_student_list()

        self.select_student_combobox_value = ctk.StringVar(value=values[0])
        self.select_student_combobox = ctk.CTkOptionMenu(
              frame
            , values = values
            , variable = self.select_student_combobox_value
            , command = self.event_select_student
            , width = 200
            , height = 36
        )
        self.select_student_combobox.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'nesw')

    # 「生徒選択」コンボボックスを取得する
    def get_student_name(self):
        return self.select_student_combobox_value.get()

    # 「生徒選択」コンボボックスを設定する
    def set_student_name(self, student_name):
        self.select_student_combobox_value.set(student_name)

    def set_combobox(self, list):
        self.select_student_combobox.configure(values = list)

    def button(self, state):
        getattr(self, 'delete_student_button').configure(state = state)

    # イベント発生条件：「削除」ボタンを押したとき
    # 処理概要：「生徒選択」コンボボックスに記入している生徒を削除する
    def event_delete_student(self):
        student_name = self.get_student_name()
        # 生徒名が有効なとき
        if len(student_name) > 0:
            msg = msgbox.askquestion('Warning', u'本当に削除しますか', default='no')
            if msg == 'yes':
                self.setting_file.delete_student(student_name)
                self.set_student_name('')

        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_DeleteStudent)

    # イベント発生条件：「生徒選択」コンボボックスを押し、生徒を選択したとき
    # 処理概要：選択した生徒の設定に変更する
    def event_select_student(self, event):
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_SelectStudent)
