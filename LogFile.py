# LogFile.py
import os
import pandas as pd
from Worksheet import Worksheet

class LogFile(Worksheet):
    def __init__(self):
        super().__init__(True)
        self.log = pd.DataFrame()

    def create_logfile(self, path, worksheet):
        worksheet.to_csv(path, encoding='shift-jis')

    def load_logfile(self, path):
        self.log = pd.read_csv(path, sep=',', index_col=0, encoding='shift-jis')

    def record_logfile(self, path, result_list):
        err_msg = []
        # ファイルが存在する
        if os.path.exists(path):
            self.log = pd.read_csv(path, sep=',', index_col=0, encoding='shift-jis')
            self.print_info('ログファイル(' + path + ')を読み込みました')

            if len(self.log) == len(result_list):
                # 採点結果を反映する
                self.log[self.Result] = result_list
                # 更新した漢字プリントの出題記録を書き込む
                self.log.to_csv(path, encoding='shift-jis')
                self.print_info('ログファイル(' + path + ')を書き込みました')
            else:
                err_msg.append(self.print_error('ログファイルと採点結果の数が不一致です'))

        # ファイルが存在しない
        else:
            err_msg.append(self.print_info('ログファイル(' + path + ')あ読み込みませんでした'))

        return len(err_msg), err_msg

    def delete_logfile(self, path):
        # ファイルが存在する
        if os.path.exists(path):
            # 漢字プリントの出題気力を削除する
            os.remove(path)
            self.print_info('ログファイル(' + path + ')を削除しました')

        # ファイルが存在しない
        else:
            self.print_error('存在しないログファイル(' + path + ')を削除しようとしました')

    def get_answer(self):
        return self.log[self.Answer].tolist()

    def get_result(self):
        return self.log[self.Result].tolist()
