import customtkinter as ctk
from Widget import Widget

class WidgetNumberOfProblem(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback
        self.number_of_problem = ctk.StringVar()
        self.number_of_problem_entry = None

    # 「出題数」ウィジェット作成
    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.create_label(frame, 0, 0, u'出題数')
        self.number_of_problem_entry = self.create_entry(
              frame
            , 1
            , 0
            , 50
            , None
            , None
            , self.number_of_problem
            , ctk.DISABLED
        )
        self.number_of_problem_entry.bind('<FocusOut>', self.event_change_number_of_problem)

    # 出題数を取得（文字列を整数に変換、失敗時は0を返す）
    def get_number_of_problem(self):
        num = self.number_of_problem.get()
        try:
            return int(num)
        except (ValueError, TypeError):
            return 0

    # 出題数を設定（整数を文字列に変換して反映）
    def set_number_of_problem(self, num):
        self.number_of_problem.set(str(num))

    # エントリーの状態（有効／無効）を設定
    def set_entry_state(self, state):
        if self.number_of_problem_entry:
            self.number_of_problem_entry.configure(state = state)

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
              self.select_student.get_student_name()
            , num
        )

        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_ChangeNumberOfProblem)