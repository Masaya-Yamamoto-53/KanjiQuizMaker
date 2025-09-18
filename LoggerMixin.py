class LoggerMixin:
    def __init__(self, debug=False):
        # デバッグ情報を表示する場合はTrue
        self.Debug = debug

    # デバッグ情報を標準出力する
    def print_info(self, msg):
        if self.Debug:
            print('Info: ' + msg)
        return msg

    # エラーメッセージを標準出力する
    def print_error(self, msg):
        if self.Debug:
            print('\033[31m' + 'Error: ' + msg + '\033[0m')
        return msg