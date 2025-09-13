from Widget import Widget

class WidgetPrint(Widget):
    def __init__(self, setting_file, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.status_callback = status_callback
        self.generate_button = None
        self.print_button = None

    # 「印刷」ウィジェット作成
    def create(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.generate_button = self.create_button(
            frame, 0, 0, u'プリント作成', self.event_generate
        )
        self.print_button = self.create_button(
            frame, 0, 1, u'印刷', self.event_print
        )

    # プリント作成ボタンの状態を設定
    def set_generate_button_state(self, state):
        if self.generate_button:
            self.generate_button.configure(state = state)

    # 印刷ボタンの状態を設定
    def set_print_button_state(self, state):
        if self.print_button:
            self.print_button.configure(state = state)

    # イベント発生条件：「プリント作成」ボタンを押したとき
    # 処理概要：漢字プリントを作成する
    def event_generate(self):
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_Generate)

    # イベント発生条件：「印刷」ボタンを押したとき
    # 処理概要：ファイルを起動する
    def event_print(self):
        # UIや状態の更新処理（ボタンの有効化など）
        self.status_callback(self.Event_Print)
