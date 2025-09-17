import customtkinter as ctk
from Widget import Widget
from WidgetAdvancedSettingPage import WidgetAdvancedSettingPage

class WidgetSelectGrade(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback

        self.grade_check_button_value = {}
        self.grade_check_button = {}
        self.advanced_button = None

        self.worksheet = None

    def set_worksheet(self, worksheet):
        self.worksheet = worksheet

    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_label(frame, 0, 0, u'出題範囲選択')

        lft_frame = self.create_frame(frame, 1, 0, None)
        rgt_frame = self.create_frame(frame, 1, 1, None)
        btm_frame = self.create_frame(frame, 2, 0, columnspan=2)

        row_num = len(self.setting_file.GRADES) // 2
        frame_list = ([lft_frame] * row_num + [rgt_frame] * row_num)

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

        self.advanced_button = self.create_button(
               btm_frame, 0, 0
            , u'詳細設定'
            , command = self.event_advanced_setting
            , attr_name = None
        )

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
            self.set_checkbox_state(key, ctk.NORMAL)
            self.set_grade(key, checked)
        self.set_advanced_button_state(ctk.NORMAL)

    def disable_grade(self):
        for key in self.setting_file.GRADES:
            self.set_checkbox_state(key, ctk.DISABLED)
            self.set_grade(key, False)
        self.set_advanced_button_state(ctk.DISABLED)

    def set_checkbox_state(self, key, state):
        self.grade_check_button[key].configure(state = state)

    def set_advanced_button_state(self, state):
        self.advanced_button.configure(state = state)

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

    # イベント発生条件：「詳細設定」ボタンを選択したとき
    # 処理概要：新しいページを表示する
    def event_advanced_setting(self):
        win = ctk.CTkToplevel()
        win.title("詳細設定")
        #win.geometry("500x400")  # 少し広めに調整

        # 最前面に表示するための処理
        win.attributes("-topmost", True)
        win.lift()
        win.focus_force()

        # タイトルラベル
        label = ctk.CTkLabel(win, text="詳細設定ページ", font=("Arial", 16))
        label.pack(pady=10)

        # 説明文ラベル（追加）
        description = (
            "この画面では、各学年の漢字を一文字ずつチェックボックスで選択できます。\n"
            "チェックされた漢字だけが出題対象になります。"
        )
        description_label = ctk.CTkLabel(win, text=description, font=("Arial", 12), justify="left")
        description_label.pack(pady=(0, 10))

        # タブビューの追加
        tabview = ctk.CTkTabview(win)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)

        self.kanji_check_vars = {}

        # 学年タブの追加
        grade_titles = [
            "一年生の漢字",
            "二年生の漢字",
            "三年生の漢字",
            "四年生の漢字",
            "五年生の漢字",
            "六年生の漢字"
        ]

        print(self.worksheet.kanji_by_grade_list)

        for i, grade_title in enumerate(grade_titles, start = 1):
            tabview.add(grade_title)
            tab_frame = tabview.tab(grade_title)

            kanji_list = self.worksheet.kanji_by_grade_list[i]

            for idx, kanji in enumerate(kanji_list):
                row = idx // 10  # 10文字ごとに改行
                col = idx % 10  # 横に並べる

                var = ctk.BooleanVar(value=False)
                self.kanji_check_vars[kanji] = var

                checkbox = ctk.CTkCheckBox(
                    tab_frame,
                    text=kanji,
                    variable=var
                )
                checkbox.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        close_button = ctk.CTkButton(win, text="閉じる", command=win.destroy)
        close_button.pack(pady=10)







