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
        self.select_worksheet_button = None

    # 問題集選択
    def build_ui(self, frame, row, column):
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
        self.select_worksheet_button = self.create_button(
              frame
            , 1, 1
            , u'選択'
            , self.event_select_worksheet
        )

    # 問題集のファイルパスを取得
    def get_path_of_worksheet_from_ui(self):
        return self.path_of_worksheet.get()

    # 問題集のファイルパスを設定
    def set_path_of_worksheet_from_ui(self, path):
        self.path_of_worksheet.set(path)

    def set_select_worksheet_button_state(self, state):
        self.select_worksheet_button.configure(state = state)

    # イベント発生条件：「選択」ボタンを押したとき
    # 処理概要：CSVファイルを選択する
    def event_select_worksheet(self):
        # CSVファイルを選択
        path = filedialog.askopenfilename(
              title=u'問題集CSVを選択'
            , filetypes=[(u'CSVファイル', u'*.csv')]
            , initialdir=os.path.abspath(os.path.dirname(__file__))
        )
        # キャンセル時は何もしない
        if not path:
            return

        # 設定ファイルに相対パスを登録する
        path = os.path.relpath(path)
        self.setting_file.set_path_of_worksheet(
              self.select_student.get_student_name_from_ui()
            , path
        )
        # エントリーにパス名を表示
        self.set_path_of_worksheet_from_ui(path)
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_SelectWorksheet)