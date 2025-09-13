# WidgetSelectWorksheet.py
import os
import customtkinter as ctk
import tkinter.filedialog as filedialog
from Widget import Widget

class WidgetSelectWorksheet(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback
        self.path_of_worksheet = ctk.StringVar()

    # 問題集選択
    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_label(frame, 0, 0, u'問題集選択')
        self.create_entry(
              frame
            , 1, 0
            , 200
            , None
            , 'worksheet_entry'
            , self.path_of_worksheet
            , 'readonly'
        )
        self.create_button(
              frame
            , 1, 1
            , u'選択'
            , self.event_select_worksheet
            , 'select_worksheet_button'
        )

    # 問題集のファイルパスを取得
    def get_worksheet_path(self):
        return self.path_of_worksheet.get()

    # 問題集のファイルパスを設定
    def set_worksheet_path(self, path):
        self.path_of_worksheet.set(path)

    def update_worksheet_path(self):
        self.path_of_worksheet.set(self.setting_file.get_worksheet_path(self.select_student.get_student_name()))

    def button(self, state):
        getattr(self, 'select_worksheet_button').configure(state = state)

    # イベント発生条件：「選択」ボタンを押したとき
    # 処理概要：CSVファイルを選択する
    def event_select_worksheet(self):
        # CSVファイルを選択
        path = filedialog.askopenfilename(
              title = '問題集CSVを選択'
            , filetypes = [('CSVファイル', '*.csv')]
            , initialdir = os.path.abspath(os.path.dirname(__file__))
        )
        # キャンセル時は何もしない
        if not path:
            return

        # 設定ファイルに相対パスを登録する
        path = os.path.relpath(path)
        self.setting_file.set_worksheet_path(self.select_student.get_student_name(), path)
        # エントリーにパス名を表示
        self.set_worksheet_path(path)

        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_SelectWorksheet)