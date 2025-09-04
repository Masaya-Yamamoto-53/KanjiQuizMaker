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
        self.root = ctk.CTk()
        self.path_of_worksheet = ctk.StringVar() # 問題集のパス
        self.number_of_problem = ctk.StringVar() # 出題数
        self.number_of_problem.trace_add('write', self.event_change_number_of_problem)

        self.setting_file = SettingFile() # 設定ファイルを読み込む
        self.setup_root()
        self.setup_widgets()

    def setup_root(self):
        self.root.title('漢字プリントメーカー')
        self.root.resizable(False, False)

    def setup_widgets(self):
        top_frame = self._create_frame(self.root, 0, 0, None)
        lft_frame = self._create_frame(top_frame, 0, 0, None)

        # 生徒登録
        self.widget_register_student(lft_frame, row=0, column=0)
        # 生徒選択
        self.widget_select_student(lft_frame, row=1, column=0)
        # 問題集選択
        self.widget_select_worksheet(lft_frame, row=2, column=0)
        # 出題範囲選択＆出題数
        self.widget_select_quiz(lft_frame, row=3, column=0)
        # プリント出力
        self.create_print_section(lft_frame, row=4, column=0)

        rgt_frame = self._create_frame(top_frame, 0, 1, None)
        btm_frame = self._create_frame(self.root, 1, 0, 2)

        # レポート
        self.widget_report(btm_frame, row=0, column=0)

    def widget_register_student(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_section_label(frame, 0, 0, u'生徒登録')
        self._create_entry(frame, 1, 0, 180, u'生徒名を入力', 'student_name_entry', None, 'normal')
        self._create_button(frame, 1, 1, u'登録', self.event_register_student, 'register_student_button')

    def widget_select_student(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_section_label(frame, 0, 0, u'生徒選択')
        self._create_combbox(frame, 1, 0)
        self._create_button(frame, 1, 1, u'削除', self.event_delete_student, 'delete_student_button')

    def _create_combbox(self, frame, row, column):
        if self.setting_file.is_empty():
            values = [u'']
        else:
            values = self.setting_file.get_student_list()

        self.select_student_combobox_value = ctk.StringVar(value=values[0])
        self.select_student_combobox = ctk.CTkOptionMenu(
              frame
            , values=values
            , variable=self.select_student_combobox_value
            , command=self.event_select_student
            , width=180
            , height=36
        )
        self.select_student_combobox.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')

    def widget_select_worksheet(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_section_label(frame, 0, 0, u'問題集選択')
        self._create_entry(
              frame
            , 1
            , 0
            , 180
            , None
            , 'worksheet_entry'
            , self.path_of_worksheet
            , 'readonly'
        )
        self._create_button(
              frame
            , 1
            , 1
            , u'選択'
            , self.event_select_worksheet
            , 'select_worksheet_button'
        )

    def widget_select_quiz(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._widget_select_grade(frame, row=0, column=0)
        self._create_number_of_problem(frame, row=0, column=1)

    def _widget_select_grade(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_section_label(frame, 0, 0, u'出題範囲選択')

        lft_frame = self._create_frame(frame, 1, 0, None)
        rgt_frame = self._create_frame(frame, 1, 1, None)

        self._widget_select_grade_check_button(lft_frame, rgt_frame)

    def _widget_select_grade_check_button(self, lft_frame, rgt_frame):
        row_num = len(self.setting_file.GRADES) // 2
        frame_list = ([lft_frame] * row_num + [rgt_frame] * row_num)

        self.grade_check_button_value = {}
        self.grade_check_button = {}

        for i, (key, frame) in enumerate(zip(self.setting_file.GRADES, frame_list)):
            self.grade_check_button_value[key] = ctk.BooleanVar(value=False)
            self.grade_check_button[key] = ctk.CTkCheckBox(
                  frame
                , text=key
                , variable=self.grade_check_button_value[key]
                , command=self.event_check_button
                , state=ctk.DISABLED
            )
            self.grade_check_button[key].grid(row=i, column=0, sticky='nesw', pady=5)

    def _create_number_of_problem(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_section_label(frame, 0, 0, u'出題数')
        self._create_entry(
              frame
            , 1
            , 0
            , 50
            , None
            , 'number_of_problem_entry'
            , self.number_of_problem
            , ctk.DISABLED
        )

    def create_print_section(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_button(frame, 0, 0, u'プリント作成', self.event_generate, 'generate_button')
        self._create_button(frame, 0, 1, u'印刷', self.event_print, 'print_button')


    def _create_frame(self, frame, row, column, columnspan):
        frame = ctk.CTkFrame(frame, corner_radius=10)
        frame.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky='nesw')
        return frame


    def _create_section_label(self, frame, row, column, text):
        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(family='Yu Gothic UI', size=18, weight='bold'))
        label.grid(row=row, column=column, sticky='nw', padx=5, pady=5)

    def _create_text_label(self, frame, row, column, text, columnspan=None):
        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(family='Yu Gothic UI', size=14))
        label.grid(row=row, column=column, columnspan=columnspan, sticky='n', padx=5, pady=5)

    def _create_entry(
              self
            , frame
            , row
            , column
            , width
            , placeholder_text=None
            , attr_name=None
            , textvariable=None
            , state='normal'):

        entry = ctk.CTkEntry(
              frame
            , placeholder_text=placeholder_text
            , textvariable=textvariable
            , width=width
            , height=36
            , state=state
        )
        entry.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        if attr_name:
            setattr(self, attr_name, entry)

    def _create_button(self, frame, row, column, text, command, attr_name):
        button = ctk.CTkButton(
              frame
            , text=text
            , command=command
            , width=80
            , height=36
            , state=ctk.DISABLED
        )
        button.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
        setattr(self, attr_name, button)

    def widget_report(self, frame, row, column):
        self._create_section_label(frame, 0, 0, u'レポート')
        # 学年
        self._create_grade_label_section(frame, 1, 0)
        # 出題数
        self._create_output_section(frame, 1, 1)

        self._create_grade_value_section(frame, 1, 2, '正解', 'correct')
        self._create_grade_value_section(frame, 1, 3, '不正解', 'incorrect')
        self._create_grade_value_section(frame, 1, 4, '一日後', 'day')
        self._create_grade_value_section(frame, 1, 5, '一週間後', 'week')
        self._create_grade_value_section(frame, 1, 6, '一ヶ月後', 'month')
#
    def _create_grade_label_section(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_text_label(frame, 0, 0, u'学年')

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            grade_label = ctk.CTkLabel(
                  frame
                , text=grade_text
                , font=ctk.CTkFont(size=14)
            )
            grade_label.grid(row=i + 1, column=0, sticky='n', padx=5, pady=1)

    def _create_output_section(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)

        self._create_text_label(frame, 0, 0, u'出題状況', 3)

        # 出題数
        self.outnum_value = {}
        self.outnum_value_entry = {}

        # 問題数
        self.tolnum_value = {}
        self.tolnum_value_entry = {}

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            self.outnum_value[i] = ctk.StringVar(value="")
            self.outnum_value_entry[i] = ctk.CTkEntry(
                  frame
                , width=50
                , textvariable=self.outnum_value[i]
                , state=ctk.DISABLED
            )
            self.outnum_value_entry[i].grid(row=i + 1, column=0, sticky='w', padx=5, pady=1)

            slash_label = ctk.CTkLabel(
                  frame
                , text='/'
                , font=ctk.CTkFont(size=14)
            )
            slash_label.grid(row=i + 1, column=1, sticky='w', padx=5, pady=1)

            self.tolnum_value[i] = ctk.StringVar(value="")
            self.tolnum_value_entry[i] = ctk.CTkEntry(
                  frame
                , width=50
                , textvariable=self.tolnum_value[i]
                , state=ctk.DISABLED
            )
            self.tolnum_value_entry[i].grid(row=i + 1, column=2, sticky='w', padx=5, pady=1)

    def _create_grade_value_section(self, frame, row, column, title, value_attr_prefix):
        frame = self._create_frame(frame, row, column, None)

        label = ctk.CTkLabel(
              frame
            , text=title
            , font=ctk.CTkFont(size=14)
        )
        label.grid(row=0, column=0, sticky='n', padx=5, pady=5)

        # 動的に属性を作成
        setattr(self, f"{value_attr_prefix}_value", {})
        setattr(self, f"{value_attr_prefix}_value_entry", {})

        value_dict = getattr(self, f"{value_attr_prefix}_value")
        entry_dict = getattr(self, f"{value_attr_prefix}_value_entry")

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            value_dict[i] = ctk.StringVar(value="")
            entry_dict[i] = ctk.CTkEntry(
                  frame
                , width=50
                , textvariable=value_dict[i]
                , state=ctk.DISABLED
            )
            entry_dict[i].grid(row=i + 1, column=0, sticky='w', padx=5, pady=1)

    def get_student_name(self):
        return self.select_student_combobox_value.get()

    def set_student_name(self, student_name):
        self.select_student_combobox_value.set(student_name)

    def get_worksheet_path(self):
        return self.path_of_worksheet.get()

    def set_worksheet_path(self, path):
        return self.path_of_worksheet.set(path)

    def get_grade(self, key):
        return self.grade_check_button_value[key].get()

    def set_grade(self, key, checked):
        self.grade_check_button_value[key].set(checked)

    def get_number_of_problem(self):
        num = self.number_of_problem.get()
        try:
            return int(num)
        except (ValueError, TypeError):
            return 0

    def set_number_of_problem(self, num):
        self.number_of_problem.set(str(num))

    ################################################################################
    # イベントメソッド
    ################################################################################
    # イベント発生条件：「登録」ボタンを押したとき
    # 処理概要：「生徒登録」エントリーに記入した名前を設定ファイルに登録する
    def event_register_student(self):
        # 「生徒登録」エントリーが空欄のとき、エラーを通知する
        student_name = getattr(self, 'student_name_entry').get()
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
        getattr(self, 'student_name_entry').delete(0, ctk.END)

        # 状態を更新
        self.change_status()

    # イベント発生条件：「生徒選択」コンボボックスを押し、生徒を選択したとき
    # 処理概要：選択した生徒の設定に変更する
    def event_select_student(self, event):
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

    # イベント発生条件：「選択」ボタンを押したとき
    # 処理概要：CSVファイルを選択する
    def event_select_worksheet(self):
        # CSVファイルを選択
        path = filedialog.askopenfilename(
              title='問題集CSVを選択'
            , filetypes=[('CSVファイル', '*.csv')]
            , initialdir=os.path.abspath(os.path.dirname(__file__))
        )
        # キャンセル時は何もしない
        if not path:
            return

        # 設定ファイルに相対パスを登録する
        self.setting_file.set_worksheet_path(self.get_student_name(), os.path.relpath(path))

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
        # 「登録」ボタンを有効化
        getattr(self, 'register_student_button').configure(state=ctk.NORMAL)

        # 「生徒選択」エントリーを更新する
        self.select_student_combobox.configure(values=self.setting_file.get_student_list())

        student_name = self.get_student_name()
        if len(student_name) > 0:
            # 「削除」ボタンを有効化
            getattr(self, 'delete_student_button').configure(state=ctk.NORMAL)
        else:
            # 「削除」ボタンを無効化
            getattr(self, 'delete_student_button').configure(state=ctk.DISABLED)

        if len(student_name) > 0:
            # 「生徒選択」ボタンの有効化
            getattr(self, 'select_worksheet_button').configure(state=ctk.NORMAL)
            # 「問題集選択」エントリーにパスを表示する
            self.set_worksheet_path(self.setting_file.get_worksheet_path(student_name))
        else:
            # 「生徒選択」ボタンの無効化
            getattr(self, 'select_worksheet_button').configure(state=ctk.DISABLED)
            # 「問題集選択」エントリーを初期化
            self.set_worksheet_path('')#

        if len(student_name) > 0:
            # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
            grade_list = self.setting_file.get_grade_list(self.get_student_name())
            for key, checked in zip(self.setting_file.GRADES, grade_list):
                self.grade_check_button[key].configure(state=ctk.NORMAL)
                self.set_grade(key, checked)
        else:
            for key in self.setting_file.GRADES:
                self.grade_check_button[key].configure(state=ctk.DISABLED)
                self.set_grade(key, False)

        if len(student_name) > 0:
            # 「出題数」のエントリーを有効化
            getattr(self, 'number_of_problem_entry').configure(state=ctk.NORMAL)
            self.number_of_problem.set(self.setting_file.get_number_of_problem(student_name))
        else:
            # 「出題数」のエントリーを無効化
            getattr(self, 'number_of_problem_entry').configure(state=ctk.DISABLED)
            # 「出題数」のエントリーを初期化
            self.number_of_problem.set('')

    def run(self):
        # 状態を更新
        self.change_status()
        # GUIアプリケーションのメインループを開始する
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
