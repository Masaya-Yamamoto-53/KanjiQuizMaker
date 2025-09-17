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
        self.create_advanced_setting_page()

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

    def create_advanced_setting_page(self):
        self.advanced_window = ctk.CTkToplevel()
        self.advanced_window.withdraw()
        self.advanced_window.title("詳細設定")

        # タイトル・説明
        label = ctk.CTkLabel(self.advanced_window, text="詳細設定ページ", font=("Arial", 16))
        label.pack(pady=10)

        description = (
            "各学年の漢字を一文字ずつチェックボックスで選択できます。\n"
            "チェックされた漢字だけが出題対象になります。"
        )
        description_label = ctk.CTkLabel(self.advanced_window, text=description, font=("Arial", 12), justify="left")
        description_label.pack(pady=(0, 10))

        # タブビュー
        self.advanced_tabview = ctk.CTkTabview(self.advanced_window)
        self.advanced_tabview.pack(expand=True, fill="both", padx=20, pady=10)

        self.kanji_check_vars = {}

        grade_titles = [
            "一年生の漢字",
            "二年生の漢字",
            "三年生の漢字",
            "四年生の漢字",
            "五年生の漢字",
            "六年生の漢字"
        ]

        for i, grade_title in enumerate(grade_titles, start=1):
            self.advanced_tabview.add(grade_title)
            tab_frame = self.advanced_tabview.tab(grade_title)

            kanji_list = self.worksheet.kanji_by_grade_list[i]

            # 列数を計算（10行構成なので列数 = ceil(len / 10)）
            max_col = len(kanji_list) // 10 + 1
            for col_index in range(max_col):
                tab_frame.grid_columnconfigure(col_index, weight=1)  # ← 各列を均等に広げる

            row = 0
            col = 0
            for idx, kanji in enumerate(kanji_list):
                row = idx % 10
                col = idx // 10

                var = ctk.BooleanVar(value=False)
                self.kanji_check_vars[kanji] = var

                checkbox = ctk.CTkCheckBox(tab_frame, text=kanji, variable=var, width=60) #, width=40, font=("Arial", 14))
                checkbox.grid(row=row, column=col, padx=2, pady=2, sticky="")

            # 一括操作ボタン（gridで配置）
            button_frame = ctk.CTkFrame(tab_frame)
            button_frame.grid(row=row+1, column=0, columnspan=col+1, pady=(0, 10))

            def check_all(kanji_list=kanji_list):
                for kanji in kanji_list:
                    self.kanji_check_vars[kanji].set(True)

            def uncheck_all(kanji_list=kanji_list):
                for kanji in kanji_list:
                    self.kanji_check_vars[kanji].set(False)

            check_button = ctk.CTkButton(button_frame, text="全てチェックを入れる", command=check_all)
            uncheck_button = ctk.CTkButton(button_frame, text="すべてチェックを外す", command=uncheck_all)

            check_button.grid(row=0, column=0, padx=10)
            uncheck_button.grid(row=0, column=1, padx=10)

        # 閉じるボタン
        close_button = ctk.CTkButton(self.advanced_window, text="閉じる", command=self.advanced_window.withdraw)
        close_button.pack(pady=10)

        # 描画キューを消化してちらつき防止
        self.advanced_window.update_idletasks()

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
    def event_advanced_setting(self, grade_index=1):
        self.advanced_window.deiconify()  # ← 表示
        self.advanced_window.focus_force()  # ← フォーカスを当てる
        self.advanced_window.lift()  # ← 最前面に持ち上げる（ここで使う）

        self.advanced_window.protocol("WM_DELETE_WINDOW", self.advanced_window.withdraw)

        # 指定タブに切り替え（例：1年生なら index=1）
        grade_titles = [
            "一年生の漢字",
            "二年生の漢字",
            "三年生の漢字",
            "四年生の漢字",
            "五年生の漢字",
            "六年生の漢字"
        ]
        selected_tab = grade_titles[grade_index - 1]
        self.advanced_tabview.set(selected_tab)