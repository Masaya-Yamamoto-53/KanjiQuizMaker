import customtkinter as ctk
from Widget import Widget

class WidgetSelectGrade(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback

    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_label(frame, 0, 0, u'出題範囲選択')

        lft_frame = self.create_frame(frame, 1, 0, None)
        rgt_frame = self.create_frame(frame, 1, 1, None)

        row_num = len(self.setting_file.GRADES) // 2
        frame_list = ([lft_frame] * row_num + [rgt_frame] * row_num)

        self.grade_check_button_value = {}
        self.grade_check_button = {}

        for i, (key, frame) in enumerate(zip(self.setting_file.GRADES, frame_list)):
            self.grade_check_button_value[key] = ctk.BooleanVar(value = False)
            self.grade_check_button[key] = ctk.CTkCheckBox(
                  frame
                , text = key
                , variable = self.grade_check_button_value[key]
                , command = self.event_check_button
                , state = ctk.DISABLED
            )
            self.grade_check_button[key].grid(row = i, column = 0, sticky = 'nesw', pady = 5)

    # 指定された学年のチェック状態を取得
    def get_grade_list(self):
        grade_list = []
        i = 1  # 学年のインデックス（1始まり）
        for key in self.setting_file.GRADES:
            checked = self.get_grade(key)  # 該当学年が選択されているかを取得
            if checked:
                grade_list.append(i)  # 選択されていればインデックスを追加

            i = i + 1  # 次の学年へインデックスを進める

        return grade_list

    def get_grade(self, key):
        return self.grade_check_button_value[key].get()

    # 指定された学年のチェック状態を設定
    def set_grade(self, key, checked):
        self.grade_check_button_value[key].set(checked)

    def enable_grade(self):
        # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
        grade_list = self.setting_file.get_grade_list(self.select_student.get_student_name())
        for key, checked in zip(self.setting_file.GRADES, grade_list):
            self.button(key, ctk.NORMAL)
            self.set_grade(key, checked)

    def disable_grade(self):
        for key in self.setting_file.GRADES:
            self.button(key, ctk.DISABLED)
            self.set_grade(key, False)

    def button(self, key, state):
        self.grade_check_button[key].configure(state = state)

    # イベント発生条件：「出題反映選択」チェックボックスを選択したとき
    # 処理概要：チェックボックスの値が変化したとき、設定を反映する
    def event_check_button(self):
        # 設定ファイルに定義された学年ごとにチェック状態を取得・保存
        for key in self.setting_file.GRADES:
            # 該当学年のチェック状態を取得（True/False）
            checked = self.get_grade(key)
            # 生徒名と学年に対応する設定を保存
            self.setting_file.set_grade(self.select_student.get_student_name(), key, checked)

        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_CheckButton)