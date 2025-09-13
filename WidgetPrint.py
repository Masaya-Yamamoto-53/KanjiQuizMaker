# WidgetPrint.py
import os
import customtkinter as ctk
import tkinter.messagebox as msgbox
from Widget import Widget

class WidgetPrint(Widget):
    def __init__(self, setting_file, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.status_callback = status_callback

    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.create_button(frame, 0, 0, u'プリント作成', self.event_generate, 'generate_button')
        self.create_button(frame, 0, 1, u'印刷', self.event_print, 'print_button')

    def generate_button_config(self, state):
        getattr(self, 'generate_button').configure(state = state)

    def print_button_config(self, state):
        getattr(self, 'print_button').configure(state = state)

    # イベント発生条件：「プリント作成」ボタンを押したとき
    # 処理概要：漢字プリントを作成する
    def event_generate(self):
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_Generate)

    # イベント発生条件：「印刷」ボタンを押したとき
    # 処理概要：ファイルを起動する
    def event_print(self):
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_Print)
