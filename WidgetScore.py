import customtkinter as ctk
import tkinter.messagebox as msgbox
from Widget import Widget
from ColumnNames import ColumnNames

class WidgetScore(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback
        self.button_all_correct = None
        self.button_all_incorrect = None
        self.button_done = None

        self.CrctMk = ColumnNames.CrctMk
        self.IncrctMk = ColumnNames.IncrctMk
        self.DayMk = ColumnNames.DayMk
        self.WeekMk = ColumnNames.WeekMk
        self.MonthMk = ColumnNames.MonthMk

        self.keys = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
                     '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']

        self.result_list = [] # 採点結果

    # 採点
    def create(self, frame, row, column):
        self.create_label(frame, 0, 0, u'採点')

        top_frame = self.create_frame(frame, 1, 0, None)
        btm_frame = self.create_frame(frame, 2, 0, None)
        menu_frame = self.create_frame(frame, 3, 0, None)

        self.scoring_answer_texts = {}
        self.scoring_answer_buttons = {}

        self.create_scoring_widgets(top_frame, self.keys[:10])
        self.create_scoring_widgets(btm_frame, self.keys[10:])

        menu_frame.grid_columnconfigure((0, 6), weight=1)

        self.button_all_correct = self.create_button(
              menu_frame, 0, 2, '全て○'
            , self.event_on_all_correct_clicked
        )
        self.button_all_incorrect = self.create_button(
              menu_frame, 0, 3, '全て×'
            , self.event_on_all_incorrect_clicked
        )
        self.button_done = self.create_button(
              menu_frame, 0, 4, '採点完了'
            , self.event_on_scoring_done
        )

    def create_scoring_widgets(self, parent_frame, keys):
        for i, key in enumerate(keys):
            col = 9 - i

            # ラベル
            label = ctk.CTkLabel(parent_frame, text = key, width = 30, font = ('Yu Gothic', 18))
            label.grid(row = 0, column = col, padx = 2, pady = 2)

            # 縦書き風ラベル群
            label_frame = ctk.CTkFrame(parent_frame, width=40)
            label_frame.grid(row=1, column=col, padx=2, pady=(0, 5))
            self.scoring_answer_texts[key] = []

            for row in range(5):  # 最大6文字まで表示
                char_label = ctk.CTkLabel(label_frame, text='', font=('Yu Gothic', 20), width=40)
                char_label.grid(row=row, column=0)
                self.scoring_answer_texts[key].append(char_label)

            # ボタン
            button = ctk.CTkButton(
                  parent_frame
                , text = '―'
                , width = 40
                , font = ('Yu Gothic', 14)
                , command = lambda k=key: self.event_on_scoring_button_click(k)
                , state = ctk.DISABLED
            )
            button.grid(row = 2, column = col, padx = 2, pady = (0, 5))
            self.scoring_answer_buttons[key] = button

    def set_all_correct_button_state(self, state):
        self.button_all_correct.configure(state = state)

    def set_all_incorrect_button_state(self, state):
        self.button_all_incorrect.configure(state = state)

    def set_done_button_state(self, state):
        self.button_done.configure(state = state)

    def set_answer(self, answer_list):
        for i, key in enumerate(self.keys):
            label_list = self.scoring_answer_texts.get(key)
            if label_list and isinstance(label_list, list):
                # 該当する答えがある場合
                if i < len(answer_list):
                    answer = str(answer_list[i])
                    for j in range(len(label_list)):
                        if j < len(answer):
                            label_list[j].configure(text = answer[j])
                        else:
                            label_list[j].configure(text = '')  # 空欄で初期化
                else:
                    # 答えがない場合はすべて空欄に初期化
                    for label in label_list:
                        label.configure(text = '')

    def set_result_buttons_state(self, result_list):
        for i, key in enumerate(self.keys):
            if i < len(result_list):
                self.scoring_answer_buttons[key].configure(state=ctk.NORMAL)
            else:
                self.scoring_answer_buttons[key].configure(state=ctk.DISABLED)

    def set_scoring_clear(self):
        for key in self.keys:
            self.scoring_answer_buttons[key].configure(text = '―')

    def set_scoring_result(self, result_list):
        for i, key in enumerate(self.keys):
            if i >= len(result_list):
                text = '―'
            else:
                if result_list[i] == self.MonthMk:
                    text = 'M'
                elif result_list[i] == self.WeekMk:
                    text = 'W'
                elif result_list[i] == self.DayMk:
                    text = 'D'
                elif result_list[i] == self.IncrctMk:
                    text = '×'
                elif result_list[i] == self.CrctMk:
                    text = '○'
                else:
                    text = '―'

            self.scoring_answer_buttons[key].configure(text = text)

    def event_on_scoring_button_click(self, key):
        if self.scoring_answer_buttons[key].cget('text') != '○':
            # 現在のボタン表示が「○」でない場合は「○」に変更（正解としてマーク）
            self.scoring_answer_buttons[key].configure(text = '○')
        else:
            # すでに「○」の場合は「×」に変更（不正解としてマーク）
            self.scoring_answer_buttons[key].configure(text = '×')

        self.status_callback(self.Event_OnScoringButtonClick)

    def event_on_all_correct_clicked(self):
        # 各キーに対応するボタンを「○」に設定（回答が存在する範囲のみ）
        for key in self.keys:
            # ボタンが無効のものは対象外にする
            button = self.scoring_answer_buttons[key]
            if button.cget('state') == 'disabled':
                continue
            self.scoring_answer_buttons[key].configure(text = '○')

        self.status_callback(self.Event_OnAllCorrectClicked)

    def event_on_all_incorrect_clicked(self):
        # 各キーに対応するボタンを「○」に設定（回答が存在する範囲のみ）
        for key in self.keys:
            # ボタンが無効のものは対象外にする
            button = self.scoring_answer_buttons[key]
            if button.cget('state') == 'disabled':
                continue
            self.scoring_answer_buttons[key].configure(text = '×')

        self.status_callback(self.Event_OnAllIncorrectClicked)

    def event_on_scoring_done(self):
        self.result_list = []
        for key in self.keys:
            # ボタンが無効のものは対象外にする
            button = self.scoring_answer_buttons[key]
            if button.cget('state') == 'disabled':
                continue

            # 採点結果がすべて入力済みであることを確認する
            text = self.scoring_answer_buttons[key].cget('text')
            if text == '○':
                self.result_list.append(self.CrctMk)
            elif text == '×':
                self.result_list.append(self.IncrctMk)
            else:
                msgbox.showerror('Error', '未回答の項目があります')
                return

        self.status_callback(self.Event_OnScoringDone)

    def get_result_list(self):
        return self.result_list
