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

    # logfileを読み込む
    def load_logfile(self, path):
        self.path_of_logfile = path
        try:
            self.logfile =pd.read_csv(path, sep=',', index_col=0, encoding='shift-jis')
        except Exception as e:
            self.print_error(f'CSV読み込み失敗: {e}')
            return pd.DataFrame()  # 空のデータを返す

    # logfileを書き込む
    def save_logfile(self, path, logfile):
        self.logfile = logfile
        self.logfile[self.LastUpdate] = datetime.today() # 最新の日付を取得
        self.logfile.to_csv(path, encoding='shift-jis')

    # logfileを削除する
    def delete_logfile(self, path):
        # ファイルが存在する
        if os.path.exists(path):
            # 漢字プリントの出題記録を削除する
            os.remove(path)
            self.print_info(u'ログファイル(' + path + u')を削除しました')
        else:
            self.print_error(u'存在しないログファイル(' + path + u')を削除しようとしました')

    # logfileのパスを取得する
    def get_logfile_path(self):
        return self.path_of_logfile

    # logfileのAnswer列を取得する
    def get_answer(self):
        if self.Answer in self.logfile.columns:
            return self.logfile[self.Answer].tolist()
        else:
            self.print_error(u'Answer列が存在しないため、空のリストを返しました')
            return []

    # logfileのResult列を取得する
    def get_result(self):
        if self.Result in self.logfile.columns:
            return self.logfile[self.Result].tolist()
        else:
            self.print_error(u'Result列が存在しないため、空のリストを返しました')
            return []
