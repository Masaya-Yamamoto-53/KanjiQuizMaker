# LogFile.py
import os
import pandas as pd
from Worksheet import Worksheet

class LogFile(Worksheet):
    def __init__(self):
        super.__init__(self, True)
        pass

    def create_logfile(self, path, worksheet):
        pass

    def record_logfile(self, path, result_list):
        err_msg = []
        # ファイルが存在する
        if os.path.exists(path):
            log = pd.read_csv(path, sep=',', index_col=0, encoding='shift-jis')
            self.print_info('ログファイル(' + path + ')を読み込みました')

            if len(log) == len(result_list):
                # 採点結果を反映する
                logs[self.Result] = result_list
                # 更新した漢字プリントの出題記録を書き込む
                logs.to_csv(path, encoding='shift-jis')
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
