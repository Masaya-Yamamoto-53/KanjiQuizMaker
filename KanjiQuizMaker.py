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

        self.setting_file = SettingFile() # 設定ファイル
        self.logfile = LogFile()          # ログファイル

        self.worksheet = Worksheet(True)  # 問題集
        self.generate_quiz = GenerateQuiz()

        self.setup_widgets()

    def setup_widgets(self):
        top_frame = self.create_frame(self.root, 0, 0, None)

        lft_frame = self.create_frame(top_frame, 0, 0, None)
        # 生徒登録
        self.widget_register_student(lft_frame, row=0, column=0)
        # 生徒選択
        self.widget_select_student(lft_frame, row=1, column=0)
        # 問題集選択
        self.widget_select_worksheet(lft_frame, row=2, column=0)
        # 出題範囲選択＆出題数
        self.widget_select_quiz(lft_frame, row=3, column=0)
        # プリント出力
        self.widget_print_section(lft_frame, row=4, column=0)

        rgt_frame = self.create_frame(top_frame, 0, 1, None)
        # 採点
        self.widget_score(rgt_frame, row=0, column=0)

        btm_frame = self.create_frame(self.root, 1, 0, 2)
        # レポート
        self.widget_report(btm_frame, row=0, column=0)

    ################################################################################
    # 生徒登録
    ################################################################################
    def widget_register_student(self, frame, row, column):
        self.widget_register_student = WidgetRegisterStudent(self.setting_file, self.status_callback)
        self.widget_register_student.create(frame, row, column)

    ################################################################################
    # 生徒選択
    ################################################################################
    def widget_select_student(self, frame, row, column):
        self.widget_select_student = WidgetSelectStudent(self.setting_file, self.status_callback)
        self.widget_select_student.create(frame, row, column)

    ################################################################################
    # 問題集選択
    ################################################################################
    def widget_select_worksheet(self, frame, row, column):
        self.widget_select_worksheet = WidgetSelectWorksheet(
              self.setting_file
            , self.widget_select_student
            , self.status_callback
        )
        self.widget_select_worksheet.create(frame, row, column)

    ################################################################################
    # 出題範囲選択 & 出題数
    ################################################################################
    def widget_select_quiz(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.widget_select_grade = WidgetSelectGrade(
              self.setting_file
            , self.widget_select_student
            , self.status_callback
        )
        self.widget_select_grade.create(frame, 0, 0)

        self.widget_number_of_problem = WidgetNumberOfProblem(
              self.setting_file
            , self.widget_select_student
            , self.status_callback
        )
        self.widget_number_of_problem.create(frame, 0, 1)

    ################################################################################
    # プリント作成 & 印刷
    ################################################################################
    def widget_print_section(self, frame, row, column):
        self.widget_print = WidgetPrint(self.setting_file, self.status_callback)
        self.widget_print.create(frame, row, column)

    ################################################################################
    # 採点
    ################################################################################
    def widget_score(self, frame, row, column):
        self.widget_score = WidgetScore(self.setting_file, self.widget_select_student, self.status_callback)
        self.widget_score.create(frame, row, column)

    ################################################################################
    # レポート
    ################################################################################
    def widget_report(self, frame, row, column):
        self.widget_report = WidgetReport(self.setting_file, self.widget_select_student, self.status_callback)
        self.widget_report.create(frame, 0, 0)

    def init_status(self):
        # 「登録」ボタンを有効化
        self.widget_register_student.button(ctk.NORMAL)

    def status_callback(self, event_num):
        # 生徒を登録した
        if event_num == Widget.Event_RegisterStudent:
            # 新しい生徒を登録したため、「生徒選択」コンボボックスを更新する
            self.widget_select_student.set_combobox(self.setting_file.get_student_list())

        if event_num == Widget.Event_SelectStudent \
        or event_num == Widget.Event_DeleteStudent:
            # 変更または、削除したことにより、生徒が変更になった
            student_name = self.widget_select_student.get_student_name()
            if len(student_name) > 0:
                state = ctk.NORMAL
            else:
                state = ctk.DISABLED

            # 「削除」ボタンを有効/無効化
            self.widget_select_student.button(state)
            # 「問題集選択」ボタンの有効/無効化
            self.widget_select_worksheet.button(state)

            if state == ctk.NORMAL:
                # 「問題集選択」エントリーにパスを表示する
                self.widget_select_worksheet.update_worksheet_path()
                # 「出題範囲選択」のチェックボタンの有効化とチェックボタンの更新
                self.widget_select_grade.enable_grade()
                # 「出題数」のエントリーを有効化
                self.widget_number_of_problem.set_entry_state(ctk.NORMAL)
                self.widget_number_of_problem.set_number_of_problem(
                    self.setting_file.get_number_of_problem(student_name)
                )
            else:
                # 「問題集選択」エントリーを空白にする
                self.widget_select_worksheet.set_worksheet_path('')
                # 「出題範囲選択」のチェックボタンの無効化
                self.widget_select_grade.disable_grade()
                # 「出題数」のエントリーを無効化
                self.widget_number_of_problem.set_entry_state(ctk.DISABLED)
                self.widget_number_of_problem.set_number_of_problem('')

            # 生徒名を取得し、スペースをアンダーバーに置換
            safe_name = self.widget_select_student.get_student_name().replace(' ', '_').replace('　', '_')
            # 漢字プリントのパスを作成
            self.kanji_file_path = './' + safe_name + '.pdf'
            # ログファイルのパスを作成
            self.log_file_path = './.' + safe_name + '.log'

        if event_num == Widget.Event_SelectStudent \
        or event_num == Widget.Event_DeleteStudent \
        or event_num == Widget.Event_SelectWorksheet:
            if not self.worksheet.is_worksheet_loaded(self.widget_select_worksheet.get_worksheet_path()):
                # 問題集の読み込みに成功
                (errnum, _) = self.worksheet.load_worksheet(self.widget_select_worksheet.get_worksheet_path())
                if errnum == 0:
                    # レポートの更新
                    self.widget_report.update_report(self.worksheet)
                    # 「プリント作成」のエントリーを有効化
                    self.widget_print.set_generate_button_state(ctk.NORMAL)
                else:
                    self.widget_print.set_generate_button_state(ctk.DISABLED)

        # 「作成」ボタンを押したとき
        if event_num == Widget.Event_Generate:
            # ログファイルが存在するとき
            msg = 'yes'
            if os.path.exists(self.log_file_path):
                msg = msgbox.askquestion('Warning', u'採点が終わっていません。このまま続けますか', default='no')

            if msg != 'no':
                # 漢字プリントを作成する
                quiz = self.generate_quiz.create(
                      self.kanji_file_path # 保存先ファイルパス
                    , self.worksheet       # ワークシート情報
                    , self.widget_number_of_problem.get_number_of_problem()  # 出題数
                    , self.widget_select_grade.get_grade_list()              # 対象学年のインデックスリスト
                    , self.widget_select_student.get_student_name() # 生徒名
                )
                # ログファイルを作成
                self.logfile.set_logfile(quiz)
                self.logfile.create_logfile(self.log_file_path)

        if os.path.exists(self.kanji_file_path):
            self.widget_print.set_print_button_state(ctk.NORMAL)
        else:
            self.widget_print.set_print_button_state(ctk.DISABLED)

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

        if os.path.exists(self.log_file_path):
            self.widget_score.set_logfile(self.logfile)
            state = ctk.NORMAL
        else:
            state = ctk.DISABLED

        self.widget_score.all_correct_button(state)
        self.widget_score.all_incorrect_button(state)
        self.widget_score.done_button(state)

        # 「作成」ボタンを押したとき
        # 「採点完了」ボタンを押したとき
        if event_num == Widget.Event_Generate \
        or event_num == Widget.Event_OnScoringDone:
            self.widget_report.update_report(self.worksheet)
            self.update_scoring()

        if event_num == Widget.Event_Generate:
            # 作成完了メッセージを表示
            msgbox.showinfo('Info', u'漢字プリントの作成が完了しました')

    def update_scoring(self):
        # ログファイルが存在する場合、採点用のフィールドに答えと前回結果を入力する
        if os.path.exists(self.log_file_path):
            self.logfile.load_logfile(self.log_file_path)
            answer_list = self.logfile.get_answer()
            result_list = self.logfile.get_result()

            # 漢字プリントの答えを印字する
            self.widget_score.set_answer(answer_list)
            # 採点ボタンの状態を印字する
            self.widget_score.config_scoring_answer_buttons(result_list)
            self.widget_score.set_scoring_result(result_list)

    def run(self):
        # UIの初期化
        self.init_status()
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(Widget.Event_SelectStudent)
        # GUIアプリケーションのメインループを開始する
        self.root.mainloop()

if __name__ == "__main__":
    app = KanjiQuizMaker()
    app.run()
