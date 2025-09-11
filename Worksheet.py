# Worksheet.py
import os
import pandas as pd
import numpy as np

class Worksheet:
    def __init__(self, debug=False):
        # デバッグ情報を表示する場合はTrue
        self.Debug = debug

        # 問題集の列
        self.FileColumns = [
              '学年'
            , '問題文'
            , '答え'
            , '番号'
            , '管理番号'
            , '最終更新日'
            , '結果'
            , '履歴'
        ]

        self.Grade = self.FileColumns[0]
        self.GradeRange = [1, 6]
        self.Problem = self.FileColumns[1]
        self.Answer = self.FileColumns[2]
        self.Number = self.FileColumns[3]
        self.AdminNumber = self.FileColumns[4]
        self.LastUpdate = self.FileColumns[5]
        self.Result = self.FileColumns[6]
        self.History = self.FileColumns[7]

        # 漢字テストの結果
        self.NotMk = np.nan
        self.CrctMk = 'o'
        self.IncrctMk = 'x'
        self.DayMk = 'd'
        self.WeekMk = 'w'
        self.MonthMk = 'm'

        # レポートの辞書キー
        self.report_key_list = [
              self.NotMk     # 未提出
            , self.CrctMk    # 正解
            , self.IncrctMk  # 不正解
            , self.DayMk     # 一日後
            , self.WeekMk    # 一週間後
            , self.MonthMk   # 一ヶ月後
        ]

        # 問題集
        self.path_of_worksheet = ''      # 問題集のパス
        self.worksheet = pd.DataFrame()  # 問題集のデータを保持するデータフレーム

        # 学年毎の漢字リスト
        self.kanji_by_grade_list = [[] for _ in range(self.GradeRange[1] + 1)]

    # 漢字プリントの読み込み確認
    def is_worksheet_loaded(self, path):
        return not self.worksheet.empty and self.path_of_worksheet == path

    # 漢字プリントの問題集を読み込む
    def load_worksheet(self, path):
        self.path_of_worksheet = path
        error_message = []

        if os.path.exists(self.path_of_worksheet):
            # ファイルが存在する
            try:
                # 問題集を読み込む
                self.worksheet = pd.read_csv(self.path_of_worksheet, sep=',', encoding='shift-jis')
                self.print_info('問題集(' + path + ')を読み込みました')
            except pd.errors.EmptyDataError:
                error_message.append(self.print_error(u'問題集が空です'))

        else:
            # ファイルが存在しない
            self.worksheet = pd.DataFrame()
            error_message.append(self.print_info('問題集(' + path + ')の読み込みに失敗しました'))

        return len(error_message), error_message

    # 漢字プリントの問題集を書き込む
    def save_worksheet(self):
        error_message = []

        # ファイルが存在する
        if os.path.exists(self.path_of_worksheet):
            try:
                self.worksheet.to_csv(self.path_of_worksheet, index=False, encoding='shift-jis')
            # 問題集を開くなどして書き込みができない
            except PermissionError:
                error_message.append(self.print_error(u'問題集(' + self.path_of_worksheet + u')を閉じてください'))
        # ファイルが存在しない
        else:
            error_message.append(self.print_error(u'問題集が存在しません'))

        return error_message

    # 指定した学年と結果に一致する問題数を取得する
    def get_count_by(self, grade, result=None):
        df = self.worksheet
        if result is None:
            # 学年だけ指定された場合
            return int((df[self.Grade] == grade).sum())
        else:
            # 学年と結果の両方が指定された場合
            return int(((df[self.Grade] == grade) & (df[self.Result] == result)).sum())

    # デバッグ情報を標準出力する
    def print_info(self, msg):
        if self.Debug:
            print('Info: ' + msg)

    # エラーメッセージを標準出力する
    def print_error(self, msg):
        if self.Debug:
            print('\033[31m' + 'Error: ' + msg + '\033[0m')
        return msg

    # 問題集を取得する
    def get_list(self):
        return self.worksheet

    # 条件に該当する問題集のインデックスを返す
    def get_quiz(self, result, grade):
        # Grade条件でフィルタ
        grade_filtered = self.worksheet[self.worksheet[self.Grade].isin(grade)]

        # Result条件でフィルタ
        if result is np.nan:
            return grade_filtered[grade_filtered[self.Result].isna()]
        else:
            return grade_filtered[grade_filtered[self.Result] == result]