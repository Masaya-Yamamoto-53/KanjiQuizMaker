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

        # 生徒情報
        self.student_name = self.get_student_name()

    def setup_root(self):
        self.root = ctk.CTk()
        self.root.title('漢字プリントメーカー')
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_widgets(self):
        self.create_registration_section(row=0, column=0)
        self.create_student_selection_section(row=1, column=0)
        self.create_worksheet_section(row=2, column=0)
        self.create_grade_section(row=3, column=0)
        self.create_number_of_problem()

    def create_registration_section(self, row, column):
        # メインフレーム（背景色と余白を調整）
        self.registration_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.registration_frame.grid(row=row, column=column, padx=20, pady=20, sticky='ew')
        self.registration_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        self._create_registration_label()
        self._create_registration_entry_and_button()

    def _create_registration_label(self):
        label = ctk.CTkLabel(
            self.registration_frame,
            text='生徒登録',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

    def _create_registration_entry_and_button(self):
        self.student_name_entry = ctk.CTkEntry(
            self.registration_frame,
            placeholder_text='生徒名を入力',
            height=36
        )
        self.student_name_entry.grid(row=1, column=0, padx=(5, 10), pady=5, sticky='ew')

        self.student_name_register_button = ctk.CTkButton(
            self.registration_frame,
            text='登録',
            command=self.event_register_student,
            width=80,
            height=36
        )
        self.student_name_register_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='w')

    def create_student_selection_section(self, row, column):
        self.selection_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.selection_frame.grid(row=row, column=column, padx=20, pady=20, sticky='ew')
        self.selection_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        self._create_selection_label()
        self._create_selection_combbox_and_button()
        self._create_selection_delete_button()

    def _create_selection_label(self):
        label = ctk.CTkLabel(
            self.selection_frame,
            text='生徒選択',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

    def _create_selection_combbox_and_button(self):
        if self.setting_file.is_empty():
            values = [u'']
        else:
            values = self.setting_file.get_student_list()

        self.student_select_combobox_value = ctk.StringVar(value=values[0])
        self.student_select_combobox = ctk.CTkOptionMenu(
            self.selection_frame
            , values=values
            , variable=self.student_select_combobox_value
            , command=self.event_select_student
        )
        self.student_select_combobox.grid(row=1, column=0, padx=20, pady=5, sticky='ew')

    def _create_selection_delete_button(self):
        self.selection_delete_button = ctk.CTkButton(
            self.selection_frame,
            text='削除',
            command=self.event_delete_student,
            width=80,
            height=36
        )
        self.selection_delete_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='w')

    def create_worksheet_section(self, row, column):
        self.selection_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.selection_frame.grid(row=row, column=column, padx=20, pady=20, sticky='ew')
        self.selection_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        self._create_worksheet_label()
        self._create_worksheet_entry_and_button()

    def _create_worksheet_label(self):
        label = ctk.CTkLabel(
            self.selection_frame,
            text='問題集選択',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

    def _create_worksheet_entry_and_button(self):
        self.worksheet_value = ctk.StringVar()
        self.worksheet_entry = ctk.CTkEntry(
            self.selection_frame,
            textvariable=self.worksheet_value,
            height=36,
            state='readonly'
        )
        self.worksheet_entry.grid(row=1, column=0, padx=(5, 10), pady=5, sticky='ew')

        self.worksheet_button = ctk.CTkButton(
            self.selection_frame,
            text='選択',
            command=self.event_select_worksheet,
            width=80,
            height=36,
            state=ctk.DISABLED
        )
        self.worksheet_button.grid(row=1, column=1, padx=(0, 5), pady=5, sticky='w')

    def create_grade_section(self, row, column):
        self.grade_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.grade_frame.grid(row=row, column=column, padx=20, pady=20, sticky='ew')
        self.grade_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        self.grade_lft_frame = ctk.CTkFrame(self.grade_frame)
        self.grade_lft_frame.grid(row=1, column=0, padx=5)

        self.grade_rgt_frame = ctk.CTkFrame(self.grade_frame)
        self.grade_rgt_frame.grid(row=1, column=1, padx=5)

        self._create_grade_label()
        self._create_grade_check_button()

    def _create_grade_label(self):
        label = ctk.CTkLabel(
            self.grade_frame,
            text='出題範囲選択',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

    def _create_grade_check_button(self):
        frame_list = (
            [self.grade_lft_frame] * 3 +
            [self.grade_rgt_frame] * 3
        )
        self.grade_frame_check_button_value = {}
        self.grade_frame_check_button = {}

        for i, (key, frame) in enumerate(zip(self.setting_file.GRADES, frame_list)):
            self.grade_frame_check_button_value[key] = ctk.BooleanVar(value=False)

            self.grade_frame_check_button[key] = ctk.CTkCheckBox(
                frame,
                text=key,
                variable=self.grade_frame_check_button_value[key],
                command=self.event_check_button,
                state=ctk.DISABLED
            )
            self.grade_frame_check_button[key].grid(row=i, column=0, sticky='w', pady=2)

    def create_number_of_problem(self):
        self.number_of_problem_frame = ctk.CTkFrame(self.grade_frame, corner_radius=10)
        self.number_of_problem_frame.grid(row=1, column=2, padx=20, pady=20, sticky='ew')
        self.number_of_problem_frame.grid_columnconfigure(0, weight=1)  # ← エントリーの列を広げる

        label = ctk.CTkLabel(
            self.number_of_problem_frame,
            text='出題数',
            font=ctk.CTkFont(size=18, weight='bold')
        )
        label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))

        self.number_of_problem_frame_value = ctk.StringVar()
        self.number_of_problem_frame_value.set('')
        self.number_of_problem_frame_value.trace_add('write', self.event_change_number_of_problem)
        self.number_of_problem_frame_value_entry = ctk.CTkEntry(
            self.number_of_problem_frame,
            width=10,
            textvariable=self.number_of_problem_frame_value,
            state=ctk.DISABLED
        )
        self.number_of_problem_frame_value_entry.grid(row=1, column=0, padx=(5, 10), pady=5, sticky='ew')

    def get_student_name(self):
        return self.student_select_combobox_value.get()

    def clear_student_name(self):
        self.student_select_combobox_value.set('')

    def get_worksheet_path(self):
        return self.worksheet_value.get()

    def set_worksheet_path(self, path):
        return self.worksheet_value.set(path)

    def get_grade(self, key):
        return self.grade_frame_check_button_value[key].get()

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

        # 生徒を設定ファイルに登録する
        self.setting_file.set_register_student(student_name)

        # 生徒を設定ファイルに登録した後に登録できたことを伝えるため、「生徒登録」エントリーを空欄にする
        # 煩わしいため、メッセージボックスは使用しない
        self.student_name_entry.delete(0, ctk.END)

        # 生徒を登録したタイミングでコンボボックスに表示できるようにする
        self.student_select_combobox.configure(values=self.setting_file.get_student_list())

    # イベント発生条件：「生徒選択」コンボボックスを押し、生徒を選択したとき
    # 処理概要：選択した生徒の設定に変更する
    def event_select_student(self, event):
        self.student_name = self.get_student_name()

    # イベント発生条件：「選択」ボタンを押したとき
    # 処理概要：CSVファイルを選択する
    def event_select_worksheet(self):
        # CSVファイルを選択
        path = filedialog.askopenfilename(
            title='問題集CSVを選択',
            filetypes=[('CSVファイル', '*.csv')],
            initialdir=os.path.abspath(os.path.dirname(__file__))
        )

        if not path:
            return # キャンセル時は何もしない

        # エントリーにパスを表示
        self.set_worksheet_path(os.path.relpath(path))

    def event_delete_student(self):
        student_name = self.get_student_name()
        # 生徒名が有効なとき
        if len(student_name) > 0:
            msg = msgbox.askquestion('Warning', self.WARNING_DELETE_STUDENT, default='no')
            if msg == 'yes':
                self.setting_file.delete_student(student_name)
                self.clear_student_name()

    def event_check_button(self):
        for key in self.setting_file.GRADES:
            checked = self.get_grade(key)
            self.setting_file.set_grade(self.get_student_name(), key, checked)

    def event_change_number_of_problem(self, *args):
        pass

    def monitor(self):
        # 「選択」ボタンの有効化
        student_name = self.get_student_name()
        if len(student_name) > 0:
            self.worksheet_button.configure(state=ctk.NORMAL)
        else:
            self.set_worksheet_path('')
            self.worksheet_button.configure(state=ctk.DISABLED)

        # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
        if len(student_name) > 0:
            grade_list = self.setting_file.get_grade_list(self.get_student_name())
            for key, checked in zip(self.setting_file.GRADES, grade_list):
                if len(student_name) > 0:
                    self.grade_frame_check_button[key].configure(state=ctk.NORMAL)
                else:
                    self.grade_frame_check_button[key].configure(state=ctk.DISABLED)

                self.grade_frame_check_button_value[key].set(checked)
        else:
            for key in self.setting_file.GRADES:
                self.grade_frame_check_button[key].configure(state=ctk.DISABLED)
                self.grade_frame_check_button_value[key].set(False)

        # 「出題数」のエントリーを有効化
        if len(student_name) > 0:
            self.number_of_problem_frame_value_entry.configure(state=ctk.NORMAL)
        else:
            self.number_of_problem_frame_value_entry.configure(state=ctk.DISABLED)
            self.number_of_problem_frame_value.set('')

        self.root.after(300, self.monitor)

    def run(self):
        self.monitor()
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
