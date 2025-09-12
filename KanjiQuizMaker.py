# KanjiQuizMaker.py
import os
import subprocess
import customtkinter as ctk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedialog

from SettingFile import SettingFile
from Worksheet import Worksheet
from GenerateQuiz import GenerateQuiz

class KanjiQuizMaker:
    ERROR_EMPTY_NAME = u'名前を入力してください'
    ERROR_ALREADY_REGISTERED = u'既に登録済みです'
    WARNING_DELETE_STUDENT = u'本当に削除しますか'
    INFO_QUIZ_CREATED = u'漢字プリントの作成が完了しました'
    ERROR_FILE_NOT_FOUND = u'ファイルが見つかりません'

    def __init__(self):
        self.root = ctk.CTk()
        self.path_of_worksheet = ctk.StringVar() # 問題集のパス
        self.number_of_problem = ctk.StringVar() # 出題数
        self.setting_file = SettingFile() # 設定ファイル
        self.worksheet = Worksheet(True)  # 問題集
        self.generate_quiz = GenerateQuiz()
        self.kanji_quiz_path = ''
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
        # 採点
        self.widget_score(rgt_frame, row=0, column=0)

        btm_frame = self._create_frame(self.root, 1, 0, 2)
        # レポート
        self.widget_report(btm_frame, row=0, column=0)

    def widget_register_student(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)
        self._create_section_label(frame, 0, 0, u'生徒登録')
        self._create_entry(
              frame
            , 1
            , 0
            , 200
            , u'生徒名を入力'
            , 'student_name_entry'
            , None
            , 'normal'
        )
        self._create_button(
              frame
            , 1
            , 1
            , u'登録'
            , self.event_register_student
            , 'register_student_button'
        )

    def widget_select_student(self, frame, row, column):
        frame = self._create_frame(frame, row, column, None)
        self._create_section_label(frame, 0, 0, u'生徒選択')
        self._create_combbox(frame, 1, 0)
        self._create_button(
              frame
            , 1
            , 1
            , u'削除'
            , self.event_delete_student
            , 'delete_student_button'
        )

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
            , width=200
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
            , 200
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
        getattr(self, 'number_of_problem_entry').bind('<FocusOut>', self.event_change_number_of_problem)
        #self.number_of_problem.trace_add('write', self.event_change_number_of_problem)

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

    def widget_score(self, frame, row, column):
        self._create_section_label(frame, 0, 0, u'採点')

        top_frame = self._create_frame(frame, 0, 0, None)
        btm_frame = self._create_frame(frame, 1, 0, None)
        menu_frame = self._create_frame(frame, 2, 0, None)

    def widget_report(self, frame, row, column):
        self._create_section_label(frame, 0, 0, u'レポート')
        # 学年
        self._create_grade_label_section(frame, 1, 0)
        # 出題数
        self._create_output_section(frame, 1, 1)

        self._create_schedule(frame, 1, 2, '正解', 'correct')
        self._create_schedule(frame, 1, 3, '不正解', 'incorrect')
        self._create_schedule(frame, 1, 4, '一日後', 'day')
        self._create_schedule(frame, 1, 5, '一週間後', 'week')
        self._create_schedule(frame, 1, 6, '一ヶ月後', 'month')

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
        self._create_text_label(frame, 0, 0, '出題状況', 3)
        self._create_grade_entries(frame, start_row=1, column_offset=0, value_prefixes=['outnum', 'tolnum'], show_slash=True)

    def _create_schedule(self, frame, row, column, title, value_attr_prefix):
        frame = self._create_frame(frame, row, column, None)
        label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, sticky='n', padx=5, pady=5)
        self._create_grade_entries(frame, start_row=1, column_offset=0, value_prefixes=[value_attr_prefix])

    def _create_grade_entries(self, frame, start_row, column_offset, value_prefixes, show_slash=False):
        for prefix in value_prefixes:
            setattr(self, f"{prefix}_value", {})
            setattr(self, f"{prefix}_value_entry", {})

        for i, grade_text in enumerate(self.setting_file.GRADES + ['合計']):
            for j, prefix in enumerate(value_prefixes):
                value_dict = getattr(self, f"{prefix}_value")
                entry_dict = getattr(self, f"{prefix}_value_entry")

                value_dict[i] = ctk.StringVar(value="")
                entry = ctk.CTkEntry(
                      frame
                    , width=50
                    , textvariable=value_dict[i]
                    , justify='right'
                    , state='readonly'
                )
                entry.grid(row=start_row + i, column=column_offset + j * 2, sticky='w', padx=5, pady=1)
                entry_dict[i] = entry

            if show_slash and len(value_prefixes) == 2:
                slash_label = ctk.CTkLabel(
                      frame
                    , text='/'
                    , font=ctk.CTkFont(size=14)
                )
                slash_label.grid(row=start_row + i, column=column_offset + 1, sticky='w', padx=5, pady=1)

    # 生徒名を取得
    def get_student_name(self):
        return self.select_student_combobox_value.get()

    # 生徒名を設定
    def set_student_name(self, student_name):
        self.select_student_combobox_value.set(student_name)

    # 問題集のファイルパスを取得
    def get_worksheet_path(self):
        return self.path_of_worksheet.get()

    # 問題集のファイルパスを設定
    def set_worksheet_path(self, path):
        return self.path_of_worksheet.set(path)

    # 指定された学年のチェック状態を取得
    def get_grade(self, key):
        return self.grade_check_button_value[key].get()

    # 指定された学年のチェック状態を設定
    def set_grade(self, key, checked):
        self.grade_check_button_value[key].set(checked)

    # 出題数を取得
    def get_number_of_problem(self):
        num = self.number_of_problem.get()
        try:
            return int(num)
        except (ValueError, TypeError):
            return 0

    # 出題数を設定
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

        # UIや状態の更新処理（ボタンの有効化など）
        self.change_status()

    # イベント発生条件：「生徒選択」コンボボックスを押し、生徒を選択したとき
    # 処理概要：選択した生徒の設定に変更する
    def event_select_student(self, event):
        # UIや状態の更新処理（ボタンの有効化など）
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

        # UIや状態の更新処理（ボタンの有効化など）
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

        # UIや状態の更新処理（ボタンの有効化など）
        self.change_status()

    # イベント発生条件：「出題反映選択」チェックボックスを選択したとき
    # 処理概要：チェックボックスの値が変化したとき、設定を反映する
    def event_check_button(self):
        # 設定ファイルに定義された学年ごとにチェック状態を取得・保存
        for key in self.setting_file.GRADES:
            # 該当学年のチェック状態を取得（True/False）
            checked = self.get_grade(key)
            # 生徒名と学年に対応する設定を保存
            self.setting_file.set_grade(self.get_student_name(), key, checked)

        # UIや状態の更新処理（ボタンの有効化など）
        self.change_status()

    # イベント発生条件：「出題数」エントリーのフォーカスが外れたとき
    # 処理概要：出題数を0〜20の範囲に制限し、設定ファイルに保存する
    def event_change_number_of_problem(self, *args):
        # 入力された出題数を取得し、最大値20に制限
        num = min(self.get_number_of_problem(), 20)
        # 最小値0に制限（負の値や空入力への対策）
        num = max(num, 0)

        # UI上の出題数を更新（制限後の値を反映）
        self.set_number_of_problem(num)

        # 設定ファイルに出題数を保存（生徒名と紐付け）
        self.setting_file.set_number_of_problem(
            self.get_student_name(),
            num
        )

    def event_generate(self):
        grade_list = []
        i = 1  # 学年のインデックス（1始まり）
        for key in self.setting_file.GRADES:
            checked = self.get_grade(key)  # 該当学年が選択されているかを取得
            if checked:
                grade_list.append(i)  # 選択されていればインデックスを追加

            i = i + 1  # 次の学年へインデックスを進める
        # 漢字プリントを作成する
        self.generate_quiz.create(
              self.kanji_quiz_path          # 保存先ファイルパス
            , self.worksheet                # ワークシート情報
            , self.get_number_of_problem()  # 出題数
            , grade_list                    # 対象学年のインデックスリスト
            , self.get_student_name()       # 生徒名
        )
        # 作成完了メッセージを表示
        msgbox.showinfo('Info', self.INFO_QUIZ_CREATED)
        # UIや状態の更新処理（ボタンの有効化など）
        self.change_status()

    def event_print(self):
        try:
            # 相対パスを絶対パスに変換
            full_path = os.path.abspath(self.kanji_quiz_path)
            # ファイルの存在を確認して開く
            if os.path.exists(full_path):
                os.startfile(full_path)
            else:
                # ファイルが存在しない場合は、エラーダイアログを表示
                msgbox.showerror('Error', self.ERROR_FILE_NOT_FOUND)
        except Exception as e:
            # ファイルの起動処理中に予期しない例外が発生した場合は、詳細を含めてエラーダイアログを表示
            msgbox.showerror('Error', f'ファイルの起動中にエラーが発生しました: {e}')

    def init_status(self):
        # 「登録」ボタンを有効化
        getattr(self, 'register_student_button').configure(state=ctk.NORMAL)

    def change_status(self):
        # 「生徒選択」エントリーを更新する
        self.select_student_combobox.configure(values=self.setting_file.get_student_list())

        student_name = self.get_student_name()
        if len(student_name) > 0:
            state = ctk.NORMAL
            path = self.setting_file.get_worksheet_path(student_name)
        else:
            state = ctk.DISABLED
            path = ''

        # 「削除」ボタンを有効/無効化
        getattr(self, 'delete_student_button').configure(state=state)
        # 「生徒選択」ボタンの有効/無効化
        getattr(self, 'select_worksheet_button').configure(state=state)

        # 「問題集選択」エントリーにパスを表示する
        self.set_worksheet_path(path)

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

        # 問題集の読み込み
        if not self.worksheet.is_worksheet_loaded(self.path_of_worksheet.get()):
            # 問題集の読み込みに成功
            (errnum, _) = self.worksheet.load_worksheet(self.path_of_worksheet.get())
            if errnum == 0:
                # レポートの更新
                self.update_report()

                # 「プリント作成」のエントリーを有効化
                getattr(self, 'generate_button').configure(state=ctk.NORMAL)
            else:
                getattr(self, 'generate_button').configure(state=ctk.DISABLED)

        # 生徒名を取得し、スペースをアンダーバーに置換
        safe_name = self.get_student_name().replace(' ', '_').replace('　', '_')
        # ファイルパスを生成（スペースがアンダーバーに置換された状態）
        self.kanji_quiz_path = './' + safe_name + '.pdf'

        if os.path.exists(self.kanji_quiz_path):
            getattr(self, 'print_button').configure(state=ctk.NORMAL)
        else:
            getattr(self, 'print_button').configure(state=ctk.DISABLED)

    def update_report(self):
        # マーク種別と対応する取得関数のマッピング
        mark_map = {
            'outnum': lambda grade: self.worksheet.get_count_by(grade) -
                                    self.worksheet.get_count_by(grade, self.worksheet.NotMk),
            'tolnum': lambda grade: self.worksheet.get_count_by(grade),
            'correct': lambda grade: self.worksheet.get_count_by(grade, self.worksheet.CrctMk),
            'incorrect': lambda grade: self.worksheet.get_count_by(grade, self.worksheet.IncrctMk),
            'day': lambda grade: self.worksheet.get_count_by(grade, self.worksheet.DayMk),
            'week': lambda grade: self.worksheet.get_count_by(grade, self.worksheet.WeekMk),
            'month': lambda grade: self.worksheet.get_count_by(grade, self.worksheet.MonthMk)
        }

        # 合計値の初期化
        total_counts = {key: 0 for key in mark_map}

        # 学年ごとの更新
        for i, grade in enumerate(range(self.worksheet.GradeRange[0], self.worksheet.GradeRange[-1] + 1)):
            for key, count_func in mark_map.items():
                count = count_func(grade)
                getattr(self, f"{key}_value")[i].set(count)
                total_counts[key] += count

        # 合計欄（末尾）にセット
        last_index = len(self.setting_file.GRADES)  # '合計' のインデックス
        for key in mark_map:
            getattr(self, f"{key}_value")[last_index].set(total_counts[key])

    def run(self):
        # UIの初期化
        self.init_status()
        # UIや状態の更新処理（ボタンの有効化など）
        self.change_status()
        # GUIアプリケーションのメインループを開始する
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
