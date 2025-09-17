import os
import customtkinter as ctk
import tkinter.messagebox as msgbox

from SettingFile import SettingFile
from LogFile import LogFile
from Worksheet import Worksheet
from GenerateQuiz import GenerateQuiz

from Widget import Widget
from WidgetRegisterStudent import WidgetRegisterStudent
from WidgetSelectStudent import WidgetSelectStudent
from WidgetSelectWorksheet import WidgetSelectWorksheet
from WidgetSelectGrade import WidgetSelectGrade
from WidgetNumberOfProblem import WidgetNumberOfProblem
from WidgetPrint import WidgetPrint
from WidgetScore import WidgetScore
from WidgetReport import WidgetReport

class KanjiQuizMaker(Widget):
    def __init__(self):
        super().__init__()

        # アプリケーションのメインウィンドウを作成
        self.root = ctk.CTk()
        # ウィンドウのタイトルを設定
        self.root.title('漢字プリントメーカー')
        # ウィンドウサイズの変更を禁止
        self.root.resizable(False, False)

        self.setting_file = SettingFile()   # 設定ファイル
        self.logfile = LogFile()            # ログファイル
        self.worksheet = Worksheet(True)    # 問題集
        self.generate_quiz = GenerateQuiz() # PDF生成用

        # 問題集の各列の定義
        self.register_student = None  # 生徒登録
        self.select_student = None    # 生徒選択
        self.select_worksheet = None  # 問題集選択
        self.select_grade = None      # 出題範囲選択
        self.number_of_problem = None # 出題数
        self.print = None             # プリント作成 & 印刷
        self.score = None             # 採点
        self.report = None            # レポート

        self.kanji_file_path = '' # 漢字プリントのパスを作成
        self.log_file_path = ''   # ログファイルのパスを作成

        # ウィジェットを作成
        self.setup_widgets()

    def setup_widgets(self):
        top_frame = self.create_frame(self.root, 0, 0, None)
        lft_frame = self.create_frame(top_frame, 0, 0, None)
        rgt_frame = self.create_frame(top_frame, 0, 1, None)
        btm_frame = self.create_frame(self.root, 1, 0, 2)

        self.widget_register_student(lft_frame, row=0, column=0) # 生徒登録
        self.widget_select_student(lft_frame, row=1, column=0)   # 生徒選択
        self.widget_select_worksheet(lft_frame, row=2, column=0) # 問題集選択
        self.widget_select_quiz(lft_frame, row=3, column=0)      # 出題範囲選択＆出題数
        self.widget_print(lft_frame, row=4, column=0)            # プリント出力
        self.widget_score(rgt_frame, row=0, column=0)            # 採点
        self.widget_report(btm_frame, row=0, column=0)           # レポート

    ################################################################################
    # 生徒登録
    ################################################################################
    def widget_register_student(self, frame, row, column):
        self.register_student = WidgetRegisterStudent(self.setting_file, self.status_callback)
        self.register_student.create(frame, row, column)

    ################################################################################
    # 生徒選択
    ################################################################################
    def widget_select_student(self, frame, row, column):
        self.select_student = WidgetSelectStudent(self.setting_file, self.status_callback)
        self.select_student.create(frame, row, column)

    ################################################################################
    # 問題集選択
    ################################################################################
    def widget_select_worksheet(self, frame, row, column):
        self.select_worksheet = WidgetSelectWorksheet(self.setting_file, self.select_student, self.status_callback)
        self.select_worksheet.create(frame, row, column)

    ################################################################################
    # 出題範囲選択 & 出題数
    ################################################################################
    def widget_select_quiz(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.select_grade = WidgetSelectGrade(self.setting_file, self.select_student, self.status_callback)
        self.select_grade.create(frame, 0, 0)

        self.number_of_problem = WidgetNumberOfProblem(self.setting_file, self.select_student, self.status_callback)
        self.number_of_problem.create(frame, 0, 1)

    ################################################################################
    # プリント作成 & 印刷
    ################################################################################
    def widget_print(self, frame, row, column):
        self.print = WidgetPrint(self.setting_file, self.status_callback)
        self.print.create(frame, row, column)

    ################################################################################
    # 採点
    ################################################################################
    def widget_score(self, frame, row, column):
        self.score = WidgetScore(self.setting_file, self.select_student, self.status_callback)
        self.score.create(frame, row, column)

    ################################################################################
    # レポート
    ################################################################################
    def widget_report(self, frame, row, column):
        self.report = WidgetReport(self.setting_file, self.select_student, self.status_callback)
        self.report.create(frame, 0, 0)

    ################################################################################
    # 状態更新
    ################################################################################
    def status_callback(self, event_num):
        msg = ''
        if event_num == self.Event_RegisterStudent:
            msg = 'Event_RegisterStudent'
        if event_num == self.Event_DeleteStudent:
            msg = 'Event_DeleteStudent'
        if event_num == self.Event_SelectStudent:
            msg = 'Event_SelectStudent'
        if event_num == self.Event_SelectWorksheet:
            msg = 'Event_SelectWorksheet'
        if event_num == self.Event_CheckButton:
            msg = 'Event_CheckButton'
        if event_num == self.Event_ChangeNumberOfProblem:
            msg = 'Event_ChangeNumberOfProblem'
        if event_num == self.Event_Generate:
            msg = 'Event_Generate'
        if event_num == self.Event_Print:
            msg = 'Event_Print'
        if event_num == self.Event_OnScoringButtonClick:
            msg = 'Event_OnScoringButtonClick'
        if event_num == self.Event_OnAllCorrectClicked:
            msg = 'Event_OnAllCorrectClicked'
        if event_num == self.Event_OnAllIncorrectClicked:
            msg = 'Event_OnAllIncorrectClicked'
        if event_num == self.Event_OnScoringDone:
            msg = 'Event_OnScoringDone'

        self.print_info('called: status_callback: ' + msg)

        if event_num == Widget.Event_RegisterStudent \
        or event_num == Widget.Event_DeleteStudent:
            # 生徒を登録または、削除したとき、「生徒選択」コンボボックスを更新する
            self.select_student.set_combobox(self.setting_file.get_student_list())

        if event_num == Widget.Event_SelectStudent \
        or event_num == Widget.Event_DeleteStudent:
            # 生徒を変更したとき（生徒選択または、削除したとき）
            student_name = self.select_student.get_student_name()
            if len(student_name) > 0:
                state = ctk.NORMAL
            else:
                state = ctk.DISABLED

            # 「削除」ボタンを有効/無効化
            self.select_student.set_button_state(state)
            # 「問題集選択」ボタンの有効/無効化
            self.select_worksheet.set_button_state(state)

            if state == ctk.NORMAL:
                # 「問題集選択」エントリーにパスを表示する
                self.select_worksheet.update_worksheet_path()
                # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
                self.select_grade.enable_grade()
                # 「出題数」のエントリーを有効化
                self.number_of_problem.set_entry_state(ctk.NORMAL)
                self.number_of_problem.set_number_of_problem(
                    self.setting_file.get_number_of_problem(student_name)
                )
            else:
                # 「問題集選択」エントリーを空白にする
                self.select_worksheet.set_worksheet_path('')
                # 「出題範囲選択」のチェックボタンの無効化
                self.select_grade.disable_grade()
                # 「出題数」のエントリーを無効化
                self.number_of_problem.set_entry_state(ctk.DISABLED)
                self.number_of_problem.set_number_of_problem('')

            # 生徒名を取得し、スペースをアンダーバーに置換
            safe_name = self.select_student.get_student_name().replace(' ', '_').replace('　', '_')
            # 漢字プリントのパスを作成
            self.kanji_file_path = './' + safe_name + '.pdf'
            # ログファイルのパスを作成
            self.log_file_path = './.' + safe_name + '.log'

        if event_num == Widget.Event_SelectStudent \
        or event_num == Widget.Event_DeleteStudent \
        or event_num == Widget.Event_SelectWorksheet:
            # 問題集を変更したとき、問題集を読み込む
            self.worksheet.load_worksheet(self.select_worksheet.get_worksheet_path())
            self.select_grade.set_worksheet(self.worksheet)

        # 問題集を作成する設定がすべて完了している
        if self.worksheet.is_worksheet_loaded(self.select_worksheet.get_worksheet_path()) \
        and len(self.select_grade.get_grade_list()) > 0:
                # 「プリント作成」のエントリーを有効/無効化
            self.print.set_generate_button_state(ctk.NORMAL)
        else:
            self.print.set_generate_button_state(ctk.DISABLED)

        # 「作成」ボタンを押したとき
        if event_num == Widget.Event_Generate:
            # ログファイルが存在するとき
            msg = 'yes'
            if os.path.exists(self.log_file_path):
                msg = msgbox.askquestion('Warning', u'採点が終わっていません。このまま続けますか', default='no')

            if msg != 'no':
                # 漢字プリントを作成する
                quiz = self.generate_quiz.create(
                      self.kanji_file_path                            # 保存先ファイルパス
                    , self.worksheet                                  # ワークシート情報
                    , self.number_of_problem.get_number_of_problem()  # 出題数
                    , self.select_grade.get_grade_list()              # 対象学年のインデックスリスト
                    , self.select_student.get_student_name()          # 生徒名
                )
                # ログファイルを作成
                self.logfile.set_logfile(quiz)
                self.logfile.create_logfile(self.log_file_path)

                # 作成完了メッセージを表示
                msgbox.showinfo('Info', u'漢字プリントの作成が完了しました')

        # 問題集が存在する場合は「印刷」ボタンを有効にする
        if os.path.exists(self.kanji_file_path):
            self.print.set_print_button_state(ctk.NORMAL)
        else:
            self.print.set_print_button_state(ctk.DISABLED)

        # 「印刷」ボタンを押したとき
        if event_num == Widget.Event_Print:
            try:
                # 相対パスを絶対パスに変換
                full_path = os.path.abspath(self.kanji_file_path)
                # ファイルの存在を確認して開く
                if os.path.exists(full_path):
                    os.startfile(full_path)
                else:
                    # ファイルが存在しない場合は、エラーダイアログを表示
                    msgbox.showerror('Error', u'ファイルが見つかりません')
            except Exception as e:
                # ファイルの起動処理中に予期しない例外が発生した場合は、詳細を含めてエラーダイアログを表示
                msgbox.showerror('Error', f'ファイルの起動中にエラーが発生しました: {e}')

        # ログファイルが存在する場合は「採点」ボタンを有効にする
        if os.path.exists(self.log_file_path):
            state = ctk.NORMAL
        else:
            state = ctk.DISABLED

        self.score.set_all_correct_button_state(state)
        self.score.set_all_incorrect_button_state(state)
        self.score.set_done_button_state(state)

        if event_num == Widget.Event_SelectStudent \
        or event_num == Widget.Event_DeleteStudent \
        or event_num == Widget.Event_SelectWorksheet \
        or event_num == Widget.Event_ChangeNumberOfProblem \
        or event_num == Widget.Event_Generate:
            self.report.update_report(self.worksheet, diff = False)
            self.update_scoring()

        # 「採点完了」ボタンを押したとき
        if event_num == Widget.Event_OnScoringDone:
            result = self.worksheet.update_worksheet(self.logfile, self.score.get_result_list())
            # 採点の繁栄が正解した場合
            if result:
                # ログファイルを削除する
                self.logfile.delete_logfile(self.logfile.get_logfile_path())

                self.report.update_report(self.worksheet, diff = True)
                self.update_scoring()

    def update_scoring(self):
        # ログファイルが存在する場合、採点用のフィールドに答えと前回結果を入力する
        if os.path.exists(self.log_file_path):
            self.logfile.load_logfile(self.log_file_path)
            answer_list = self.logfile.get_answer() # 答えを取得
            result_list = self.logfile.get_result() # 前回の結果を取得

            # 漢字プリントの答えを印字する
            self.score.set_answer(answer_list)
            # 採点ボタンの状態を印字する
            self.score.set_result_buttons_state(result_list)
            # 採点ボタンを印字する
            self.score.set_scoring_result(result_list)
        else:
            self.score.set_scoring_clear()
            self.score.set_answer([])
            self.score.set_result_buttons_state([])
            self.score.set_scoring_result([])

    def init_status(self):
        # 「登録」ボタンを有効化
        self.register_student.set_button_state(ctk.NORMAL)
        # 既に生徒を選択している場合
        if len(self.select_student.get_student_name()) > 0:
            # UIや状態の更新処理（ボタンの有効化など）
            self.status_callback(Widget.Event_SelectStudent)

    def run(self):
        # UIの初期化
        self.init_status()
        # GUIアプリケーションのメインループを開始する
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
