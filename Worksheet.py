import os
import pandas as pd
import numpy as np
import datetime as datetime

from ColumnNames import ColumnNames
from LoggerMixin import LoggerMixin

class Worksheet(LoggerMixin):
    def __init__(self, debug=False):
        super().__init__(True)

        # 問題集の列
        self.FileColumns = ColumnNames.FILE_COLUMNS
        self.Grade = ColumnNames.GRADE              # 学年
        self.GradeRange = ColumnNames.GRADE_RANGE   # 学年（有効範囲）
        self.Problem = ColumnNames.PROBLEM          # 問題文
        self.Answer = ColumnNames.ANSWER            # 答え
        self.Number = ColumnNames.NUMBER            # 番号
        self.AdminNumber = ColumnNames.ADMIN_NUMBER # 管理番号
        self.LastUpdate = ColumnNames.LAST_UPDATE   # 最終更新日
        self.Result = ColumnNames.RESULT            # 結果
        self.History = ColumnNames.HISTORY          # 履歴

        # 漢字テストの結果
        self.NotMk = ColumnNames.NotMk
        self.CrctMk = ColumnNames.CrctMk
        self.IncrctMk = ColumnNames.IncrctMk
        self.DayMk = ColumnNames.DayMk
        self.WeekMk = ColumnNames.WeekMk
        self.MonthMk = ColumnNames.MonthMk

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

    # 漢字プリントの問題集が空か否か
    def is_empty(self):
        return self.worksheet.empty

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

        # 学年ごとの出題漢字リストを作成する
        self.create_kanji_list()

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

    # 問題集から学年に対応する漢字をリスト化する
    def create_kanji_list(self):
        grade_pre = []  # 前の学年の漢字リスト
        for grade in range(self.GradeRange[0], self.GradeRange[-1] + 1):
            # 学年委該当するデータを抽出する
            worksheet = self.get_worksheet_by([grade])

            # 抽出したデータが存在する場合
            if len(worksheet) > 0:
                # 1語ずつ配列に格納する
                for ans in worksheet[self.Answer]:
                    self.kanji_by_grade_list[grade].extend([char for char in ans])

                # ソートして、ユニークにする
                self.kanji_by_grade_list[grade] = sorted(self.kanji_by_grade_list[grade])
                self.kanji_by_grade_list[grade] = list(set(self.kanji_by_grade_list[grade]))

                # 前の学年の漢字のみ取り除く
                self.kanji_by_grade_list[grade] = list(set(self.kanji_by_grade_list[grade]) - set(grade_pre))

                # 現在の学年の漢字だけを残すため、それ以降の漢字を記憶しておく
                grade_pre = grade_pre + self.kanji_by_grade_list[grade]

                # 学年毎に習う漢字数を表示する.
                self.print_info('小学' + str(grade) + '年生: 全 ' + str(len(self.kanji_by_grade_list[grade])) + ' 文字')

    # 指定した学年の問題を取得する
    def get_worksheet_by(self, grade):
        return self.worksheet[self.worksheet[self.Grade].isin(grade)]

    # 漢字を取得する
    def get_kanji_list(self, grades):
        kanji_list = []
        for grade in grades:
            kanji_list.extend(self.kanji_by_grade_list[grade])
        return kanji_list

    # 問題集を取得する
    def get_list(self):
        return self.worksheet

    def update_worksheet(self, logfile, result):
        matched_indices_list = []

        for i in range(len(logfile.logfile)):
            log_val = logfile.logfile.iloc[i][self.Problem]
            matches = self.worksheet[self.Problem] == log_val

            # 一致したインデックスを取得
            matched_indices = self.worksheet[matches].index.tolist()
            matched_indices_list.append(matched_indices)

            # History と LastUpdate の値を取得
            raw_history = logfile.logfile.iloc[i][self.History]
            new_update_time = logfile.logfile.iloc[i][self.LastUpdate]

            new = result[i]  # 今回の結果

            for idx in matched_indices:
                current_history = self.worksheet.at[idx, self.History]
                if pd.isna(current_history):
                    updated_history = str(result[i])
                else:
                    updated_history = str(raw_history) + str(result[i])

                self.worksheet.at[idx, self.History] = updated_history
                self.worksheet.at[idx, self.LastUpdate] = new_update_time

                # [結果]列を更新する.
                # 【凡例】
                # NaN: self.kNotMk   : 未実施
                #   o: self.kCrctMk  : 今回正解
                #   x: self.kIncrctMk: 今回不正解
                #   d: self.kDayMk   : 1日後に実施(前回xで今回oの時)
                #   w: self.kWeekMk  : 1週間後に実施(前回dで今回oの時)
                #   m: self.kMonthMk : 1ヶ月後に実施(前回wで今回oの時)

                # 今回, 正解した場合.
                old = self.worksheet.at[idx, self.Result]  # 以前の結果
                if new == self.CrctMk:
                    if old == self.IncrctMk:  # x -> d
                        key = self.DayMk
                    elif old == self.DayMk:  # d -> w
                        key = self.WeekMk
                    elif old == self.WeekMk:  # w -> m
                        key = self.MonthMk
                    else:  # m -> o or - -> o
                        key = self.CrctMk
                # 今回, 不正解の場合
                else:  # x
                    key = self.IncrctMk

                self.worksheet.at[idx, self.Result] = key

        self.save_worksheet()

    # 指定した学年と結果に一致する問題数を取得する
    def get_count_by(self, grade, result=None):
        df = self.worksheet
        if result is None:
            # 学年だけ指定された場合
            return int((df[self.Grade] == grade).sum())
        elif pd.isna(result):
            # 未マーク（欠損値）の場合：Result列がNaNの行をカウント
            return int(((df[self.Grade] == grade) & (df[self.Result].isna())).sum())
        else:
            # 学年と結果の両方が指定された場合
            return int(((df[self.Grade] == grade) & (df[self.Result] == result)).sum())

    # 条件に該当する問題集のインデックスを返す
    def get_quiz(self, result, grade, create_date, shuffle = False, days = -1):
        # 毎日同じ時間帯に学習する場合、前日に間違えた問題が抽出されない可能性があるため、
        # 判定時間に2時間のオフセットを加える。
        now_time = create_date + datetime.timedelta(hours = 6)

        # Grade条件でフィルタ
        grade_filtered = self.worksheet[self.worksheet[self.Grade].isin(grade)]

        # Result条件でフィルタ
        if result is np.nan:
            grade_filtered = grade_filtered[grade_filtered[self.Result].isna()]
        else:
            grade_filtered = grade_filtered[grade_filtered[self.Result] == result]
            if days != -1:
                delta = datetime.timedelta(days=days) < (now_time - pd.to_datetime(
                                                                         grade_filtered[self.LastUpdate]
                                                                       , format='mixed'
                                                                    ))
                grade_filtered = grade_filtered[delta]

        if shuffle:
            return grade_filtered.sample(frac=1).reset_index(drop=True)
        else:
            return grade_filtered