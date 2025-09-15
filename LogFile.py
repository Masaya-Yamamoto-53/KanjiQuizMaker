import os
import pandas as pd
from datetime import datetime
from ColumnNames import ColumnNames
from LoggerMixin import LoggerMixin

class LogFile(LoggerMixin):
    Answer = ColumnNames.ANSWER  # 答え
    Result = ColumnNames.RESULT  # 結果
    LastUpdate = ColumnNames.LAST_UPDATE  # 最終更新日

    def __init__(self):
        super().__init__(True)
        self.logfile = pd.DataFrame()
        self.path_of_logfile = ''

    def get_logfile_path(self):
        return self.path_of_logfile

    def set_logfile(self, logfile):
        self.logfile = logfile

    def create_logfile(self, path):
        # 最新の日付を取得
        now = datetime.today()
        self.logfile[self.LastUpdate] = now
        self.logfile.to_csv(path, encoding='shift-jis')

    def load_logfile(self, path):
        self.path_of_logfile = path
        try:
            self.logfile = self.read_csv_file(path)
        except Exception as e:
            self.print_error(f'ログファイルの読み込みに失敗しました: {e}')

    def record_logfile(self, path, result_list):
        err_msg = []
        # ファイルが存在する
        if os.path.exists(path):
            self.logfile = self.read_csv_file(path)
            self.print_info('ログファイル(' + path + ')を読み込みました')

            if len(self.logfile) == len(result_list):
                # 採点結果を反映する
                self.logfile[self.Result] = result_list
                # 更新した漢字プリントの出題記録を書き込む
                self.logfile.to_csv(path, encoding='shift-jis')
                self.print_info('ログファイル(' + path + ')を書き込みました')
            else:
                err_msg.append(self.print_error('ログファイルと採点結果の数が不一致です'))

        # ファイルが存在しない
        else:
            err_msg.append(self.print_info('ログファイル(' + path + ')は読み込みませんでした'))

        return len(err_msg), err_msg

    def delete_logfile(self, path):
        # ファイルが存在する
        if os.path.exists(path):
            # 漢字プリントの出題記録を削除する
            os.remove(path)
            self.print_info('ログファイル(' + path + ')を削除しました')

        # ファイルが存在しない
        else:
            self.print_error('存在しないログファイル(' + path + ')を削除しようとしました')

    def read_csv_file(self, path):
        try:
            return pd.read_csv(path, sep=',', index_col=0, encoding='shift-jis')
        except Exception as e:
            self.print_error(f'CSV読み込み失敗: {e}')
            return pd.DataFrame()  # 空のデータを返す

    def get_answer(self):
        if self.Answer in self.logfile.columns:
            return self.logfile[self.Answer].tolist()
        else:
            self.print_error('[Answer]列が存在しないため、空のリストを返しました')
            return []

    def get_result(self):
        if self.Result in self.logfile.columns:
            return self.logfile[self.Result].tolist()
        else:
            self.print_error('[Result]列が存在しないため、空のリストを返しました')
            return []
