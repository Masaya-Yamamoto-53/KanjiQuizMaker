# KanjiQuizMaker.py
import os
import customtkinter as ctk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedialog

from SettingFile import SettingFile

class KanjiQuizMaker:
    ERROR_EMPTY_NAME = u'名前を入力してください'
    ERROR_ALREADY_REGISTERED = u'既に登録済みです'
    WARNING_DELETE_STUDENT = u'本当に削除しますか'

    def __init__(self):
        # 設定ファイルを読み込む
        self.setting_file = SettingFile()

        self.setup_root()
        self.setup_widgets()

    def setup_root(self):
        self.root = ctk.CTk()
        self.root.title('漢字プリントメーカー')
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=0)

    def setup_widgets(self):
        top_frame = ctk.CTkFrame(self.root, corner_radius=10)
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nesw')
        top_frame.grid_columnconfigure(0, weight=0)

        btm_frame = ctk.CTkFrame(self.root, corner_radius=10)
        btm_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nesw')
        btm_frame.grid_columnconfigure(0, weight=0)

        lft_frame = ctk.CTkFrame(top_frame, corner_radius=10)
        lft_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nesw')
        lft_frame.grid_columnconfigure(0, weight=0)

        rgt_frame = ctk.CTkFrame(top_frame, corner_radius=10)
        rgt_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nesw')
        rgt_frame.grid_columnconfigure(0, weight=0)

        # 生徒登録
        self.create_registration_section(lft_frame, row=0, column=0)
        # 生徒選択
        self.create_student_selection_section(lft_frame, row=1, column=0)
        # 問題集選択
        self.create_worksheet_section(lft_frame, row=2, column=0)
        # 出題範囲選択＆出題数
        self.create_quiz_section(lft_frame, row=3, column=0)
        # プリント出力
        self.create_print_section(lft_frame, row=4, column=0)

        # レポート
        self.create_report_section(btm_frame, row=0, column=0)

    def create_registration_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        self._create_registration_label(frame, 0, 0)
        self._create_registration_entry_and_button(frame, 1, 0)

    def _create_registration_label(self, frame, row, column):
        label = ctk.CTkLabel(
              frame
            , text='生徒登録'
            , font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=row, column=column, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

    def _create_registration_entry_and_button(self, frame, row, column):
        self.student_name_entry = ctk.CTkEntry(
              frame
            , placeholder_text='生徒名を入力'
            , width=180
            , height=36
        )
        self.student_name_entry.grid(row=row, column=column, padx=(5, 10), pady=5, sticky='nw')

        self.student_name_register_button = ctk.CTkButton(
              frame
            , text='登録'
            , command=self.event_register_student
            , width=80
            , height=36
        )
        self.student_name_register_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='nw')

    def create_student_selection_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        self._create_selection_label(frame, 0, 0)
        self._create_selection_combbox_and_button(frame, 1, 0)
        self._create_selection_delete_button(frame, 1, 1)

    def _create_selection_label(self, frame, row, column):
        label = ctk.CTkLabel(
              frame
            , text='生徒選択'
            , font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=row, column=column, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

    def _create_selection_combbox_and_button(self, frame, row, column):
        if self.setting_file.is_empty():
            values = [u'']
        else:
            values = self.setting_file.get_student_list()

        self.student_select_combobox_value = ctk.StringVar(value=values[0])
        self.student_select_combobox = ctk.CTkOptionMenu(
              frame
            , values=values
            , variable=self.student_select_combobox_value
            , command=self.event_select_student
            , width=180
        )
        self.student_select_combobox.grid(row=row, column=column, padx=5, pady=5, sticky='nw')

    def _create_selection_delete_button(self, frame, row, column):
        self.selection_delete_button = ctk.CTkButton(
            frame,
            text='削除',
            command=self.event_delete_student,
            width=80,
            height=36
        )
        self.selection_delete_button.grid(row=row, column=column, padx=5, pady=5, sticky='nw')

    def create_worksheet_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        self._create_worksheet_label(frame, 0, 0)
        self._create_worksheet_entry_and_button(frame, 1, 0)

    def _create_worksheet_label(self, frame, row, column):
        label = ctk.CTkLabel(
              frame
            , text='問題集選択'
            , font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=row, column=column, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

    def _create_worksheet_entry_and_button(self, frame, row, column):
        self.worksheet_value = ctk.StringVar()
        self.worksheet_entry = ctk.CTkEntry(
              frame
            , textvariable=self.worksheet_value
            , width=180
            , height=36
            , state='readonly'
        )
        self.worksheet_entry.grid(row=row, column=column, padx=(5, 10), pady=5, sticky='nw')

        self.worksheet_button = ctk.CTkButton(
              frame
            , text='選択'
            , command=self.event_select_worksheet
            , width=80
            , height=36
            , state=ctk.DISABLED
        )
        self.worksheet_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='nw')

    def create_quiz_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        self._create_grade_section(frame, row=0, column=0)
        self._create_number_of_problem(frame, row=0, column=1)

    def _create_grade_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        lft_frame = ctk.CTkFrame(frame)
        lft_frame.grid(row=row+1, column=0, padx=5)

        rgt_frame = ctk.CTkFrame(frame)
        rgt_frame.grid(row=row+1, column=1, padx=5)

        self._create_grade_label(frame, 0, 0)
        self._create_grade_check_button(lft_frame, rgt_frame)

    def _create_grade_label(self, frame, row, column):
        label = ctk.CTkLabel(
            frame,
            text='出題範囲選択',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=row, column=column, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

    def _create_grade_check_button(self, lft_frame, rgt_frame):
        frame_list = (
            [lft_frame] * 3 +
            [rgt_frame] * 3
        )
        self.grade_frame_check_button_value = {}
        self.grade_frame_check_button = {}

        for i, (key, frame) in enumerate(zip(self.setting_file.GRADES, frame_list)):
            self.grade_frame_check_button_value[key] = ctk.BooleanVar(value=False)

            self.grade_frame_check_button[key] = ctk.CTkCheckBox(
                  frame
                , text=key
                , variable=self.grade_frame_check_button_value[key]
                , command=self.event_check_button
                , state=ctk.DISABLED
            )
            self.grade_frame_check_button[key].grid(row=i, column=0, sticky='nw', pady=2)

    def _create_number_of_problem(self, frame, row, column):
        pass
        self.number_of_problem_frame = ctk.CTkFrame(frame, corner_radius=10)
        self.number_of_problem_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nw')
        self.number_of_problem_frame.grid_columnconfigure(0, weight=0)

        label = ctk.CTkLabel(
            self.number_of_problem_frame,
            text='出題数',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

        self.number_of_problem_frame_value = ctk.StringVar()
        self.number_of_problem_frame_value.set('')
        self.number_of_problem_frame_value.trace_add('write', self.event_change_number_of_problem)
        self.number_of_problem_frame_value_entry = ctk.CTkEntry(
            self.number_of_problem_frame,
            width=50,
            textvariable=self.number_of_problem_frame_value,
            state=ctk.DISABLED
        )
        self.number_of_problem_frame_value_entry.grid(row=1, column=0, padx=(5, 10), pady=5, sticky='nw')

    def create_print_section(self, frame, row, column):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        frame.grid_columnconfigure(0, weight=0)

        self._create_generate_button(frame, 0, 0)
        self._create_print_button(frame, 0, 1)

    def _create_generate_button(self, frame, row, column):
        self.generate_button = ctk.CTkButton(
              frame
            , text='プリント作成'
            , command=self.event_generate
            , width=80
            , height=36
            , state=ctk.DISABLED
        )
        self.generate_button.grid(row=row, column=column, padx=(0, 5), pady=5, sticky='nw')

    def _create_print_button(self, frame, row, column):
        self.print_button = ctk.CTkButton(
              frame
            , text='印刷'
            , command=self.event_print
            , width=80
            , height=36
            , state=ctk.DISABLED
        )
        self.print_button.grid(row=row, column=column, padx=(0, 5), pady=5, sticky='nw')

    def create_report_section(self, frame, row, column):
        self._create_report_label(frame, 0, 0)
        # 出題数
        self._create_output_section(frame, 1, 0)
        # 正解
        self._create_correct_section(frame, 1, 1)
        # 不正解
        self._create_incorrect_section(frame, 1, 2)
        # 1日後
        self._create_day_section(frame, 1, 3)
        # 1週間後
        self._create_week_section(frame, 1, 4)
        # 1ヶ月後
        self._create_month_section(frame, 1, 5)

    def _create_report_label(self, frame, row, column):
        label = ctk.CTkLabel(
            frame,
            text='レポート',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=row, column=column, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

    def _create_output_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'出題状況', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='nw', padx=5, pady=(10, 5))

        self.outnum_frame_value = {}
        self.outnum_frame_value_entry = {}

        self.tolnum_frame_value = {}
        self.tolnum_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            # 学年
            grade_label = ctk.CTkLabel(section_frame, text=grade_text, font=ctk.CTkFont(size=14))
            grade_label.grid(row=i + 1, column=0, sticky='w', padx=5, pady=0)

            self.outnum_frame_value[i] = ctk.StringVar(value="")
            self.outnum_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.outnum_frame_value[i],
                state=ctk.DISABLED
            )
            self.outnum_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

            slash_label = ctk.CTkLabel(section_frame, text='/', font=ctk.CTkFont(size=14))
            slash_label.grid(row=i + 1, column=2, sticky='w', padx=5, pady=0)

            self.tolnum_frame_value[i] = ctk.StringVar(value="")
            self.tolnum_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.tolnum_frame_value[i],
                state=ctk.DISABLED
            )
            self.tolnum_frame_value_entry[i].grid(row=i + 1, column=3, sticky='w', padx=5, pady=0)

    def _create_correct_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'正解', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='n', padx=5, pady=(10, 5))

        self.correct_frame_value = {}
        self.correct_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.correct_frame_value[i] = ctk.StringVar(value="")
            self.correct_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.correct_frame_value[i],
                state=ctk.DISABLED
            )
            self.correct_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

    def _create_incorrect_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'不正解', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='n', padx=5, pady=(10, 5))

        self.incorrect_frame_value = {}
        self.incorrect_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.incorrect_frame_value[i] = ctk.StringVar(value="")
            self.incorrect_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.incorrect_frame_value[i],
                state=ctk.DISABLED
            )
            self.incorrect_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

    def _create_day_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'一日後', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='n', padx=5, pady=(10, 5))

        self.day_frame_value = {}
        self.day_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.day_frame_value[i] = ctk.StringVar(value="")
            self.day_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.day_frame_value[i],
                state=ctk.DISABLED
            )
            self.day_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

    def _create_week_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'一週間後', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='n', padx=5, pady=(10, 5))

        self.week_frame_value = {}
        self.week_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.week_frame_value[i] = ctk.StringVar(value="")
            self.week_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.week_frame_value[i],
                state=ctk.DISABLED
            )
            self.week_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

    def _create_month_section(self, frame, row, column):
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        label = ctk.CTkLabel(section_frame, text=u'一ヶ月後', font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, columnspan=2, sticky='n', padx=5, pady=(10, 5))

        self.month_frame_value = {}
        self.month_frame_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.month_frame_value[i] = ctk.StringVar(value="")
            self.month_frame_value_entry[i] = ctk.CTkEntry(
                section_frame,
                width=50,
                textvariable=self.month_frame_value[i],
                state=ctk.DISABLED
            )
            self.month_frame_value_entry[i].grid(row=i + 1, column=1, sticky='w', padx=5, pady=0)

    def get_student_name(self):
        return self.student_select_combobox_value.get()

    def set_student_name(self, student_name):
        self.student_select_combobox_value.set(student_name)

    def get_worksheet_path(self):
        return self.worksheet_value.get()

    def set_worksheet_path(self, path):
        return self.worksheet_value.set(path)

    def get_grade(self, key):
        return self.grade_frame_check_button_value[key].get()

    def get_number_of_problem(self):
        num = self.number_of_problem_frame_value.get()
        try:
            return int(num)
        except (ValueError, TypeError):
            return 0

    def set_number_of_problem(self, num):
        self.number_of_problem_frame_value.set(str(num))

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

        # 設定ファイルに生徒を登録する
        self.setting_file.set_register_student(student_name)

        # 設定ファイルに生徒を登録した後に登録できたことを伝えるため、「生徒登録」エントリーを空欄にする
        # 煩わしいため、メッセージボックスは使用しない
        self.student_name_entry.delete(0, ctk.END)

        # 状態を更新
        self.change_status()

    # イベント発生条件：「生徒選択」コンボボックスを押し、生徒を選択したとき
    # 処理概要：選択した生徒の設定に変更する
    def event_select_student(self, event):
        # 状態を更新
        self.change_status()

    # イベント発生条件：「選択」ボタンを押したとき
    # 処理概要：CSVファイルを選択する
    def event_select_worksheet(self):
        # CSVファイルを選択
        path = filedialog.askopenfilename(
            title='問題集CSVを選択',
            filetypes=[('CSVファイル', '*.csv')],
            initialdir=os.path.abspath(os.path.dirname(__file__))
        )
        # キャンセル時は何もしない
        if not path:
            return

        # 設定ファイルに相対パスを登録する
        self.setting_file.set_worksheet_path(self.get_student_name(), os.path.relpath(path))

        # 状態を更新
        self.change_status()

    # イベント発生条件：「削除」ボタンを押したとき
    # 処理概要：「生徒選択」コンボボックスに記入している生徒を削除する
    def event_delete_student(self):
        student_name = self.get_student_name()
        # 生徒名が有効なとき
        if len(student_name) > 0:
            msg = msgbox.askquestion('Warning', self.WARNING_DELETE_STUDENT, default='no')
            if msg == 'yes':
                self.setting_file.delete_student(student_name)
                self.set_student_name('')

        # 状態を更新
        self.change_status()

    # イベント発生条件：「出題反映選択」チェックボックスを選択したとき
    # 処理概要：チェックボックスの値が変化したとき、設定を反映する
    def event_check_button(self):
        for key in self.setting_file.GRADES:
            checked = self.get_grade(key)
            self.setting_file.set_grade(self.get_student_name(), key, checked)

    # イベント発生条件：「出題数」エントリーを変更したとき
    # 処理概要：出題数を更新する
    def event_change_number_of_problem(self, *args):
        self.setting_file.set_number_of_problem(
            self.get_student_name(),
            self.get_number_of_problem()
        )

    def event_generate(self):
        pass

    def event_print(self):
        pass

    def change_status(self):
        student_name = self.get_student_name()
        if len(student_name) > 0:
            # 「生徒選択」ボタンの有効化
            self.worksheet_button.configure(state=ctk.NORMAL)
        else:
            # 「生徒選択」エントリーを初期化
            self.set_worksheet_path('')
            # 「生徒選択」ボタンの無効化
            self.worksheet_button.configure(state=ctk.DISABLED)

        # 「生徒選択」エントリーを更新する
        self.student_select_combobox.configure(values=self.setting_file.get_student_list())

        if len(student_name) > 0:
            # 「問題集選択」エントリーにパスを表示する
            self.set_worksheet_path(self.setting_file.get_worksheet_path(student_name))
        else:
            # 「問題集選択」エントリーを書記か
            self.set_worksheet_path('')

        if len(student_name) > 0:
            # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
            grade_list = self.setting_file.get_grade_list(self.get_student_name())
            for key, checked in zip(self.setting_file.GRADES, grade_list):
                self.grade_frame_check_button[key].configure(state=ctk.NORMAL)
                self.grade_frame_check_button_value[key].set(checked)
        else:
            for key in self.setting_file.GRADES:
                self.grade_frame_check_button[key].configure(state=ctk.DISABLED)
                self.grade_frame_check_button_value[key].set(False)

        if len(student_name) > 0:
            # 「出題数」のエントリーを有効化
            self.number_of_problem_frame_value_entry.configure(state=ctk.NORMAL)
            self.number_of_problem_frame_value.set(self.setting_file.get_number_of_problem(student_name))
        else:
            # 「出題数」のエントリーを無効化
            self.number_of_problem_frame_value_entry.configure(state=ctk.DISABLED)
            # 「出題数」のエントリーを初期化
            self.number_of_problem_frame_value.set('')

    def run(self):
        # 状態を更新
        self.change_status()
        # GUIアプリケーションのメインループを開始する
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
