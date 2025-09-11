# GenerateQuiz.py
import datetime as datetime
import pandas as pd
import numpy as np
from OutputQuiz import OutputQuiz

class GenerateQuiz:
    def __init__(self):
        # PDF出力
        self.output_quiz = OutputQuiz()

        # 漢字プリント
        self.quiz = pd.DataFrame()  # 漢字プリントのデータを保持するデータフレーム

        self.list_x = []  # 間違えた問題のインデックス
        self.list_a_idx = []  # 出題してからしばらく再出題していない問題のインデックス
        self.list_d = []  # 昨日間違えた問題のインデックス
        self.list_w = []  # 一週間前に間違えた問題のインデックス
        self.list_m = []  # 一ヶ月前に間違えた問題のインデックス
        self.list_n = []  # 未出題のインデックス
        self.list_o = []  # 正解している問題のインデックス

    def create(self, path, worksheet, num, grade, student_name):
        # 作成日を取得する
        create_date = pd.to_datetime(datetime.datetime.today())

        # 問題数が20を超えている場合は20にする
        num = min(num, 20)
        num = max(num, 0)
        # 設定した問題数よりも問題集の問題数が少ないとき、
        # 問題集の問題数を出題数とする
        num_p = num
        if num_p > 0:
            num_i = len(worksheet.get_list())
            if num_i < num_p:
                num = num_i

        # 問題集を作成する
        self._create_train_mode(worksheet, num, grade)
        self.output_quiz.create(path, student_name, create_date, num, self.quiz[worksheet.Problem])

    def _create_train_mode(self, worksheet, num, grade):
        # テスト問題を選定する
        # 間違えた問題のインデックスを取得
        self.list_x = worksheet.get_quiz(worksheet.IncrctMk, grade)
        # 昨日間違えた問題のインデックスを取得する
        self.list_d = worksheet.get_quiz(worksheet.DayMk, grade)
        # 一週間前に間違えた問題のインデックスを取得する
        self.list_w = worksheet.get_quiz(worksheet.WeekMk, grade)
        # 一ヶ月前に間違えた問題のインデックスを取得する
        self.list_m = worksheet.get_quiz(worksheet.MonthMk, grade)

        # 問題を連結する
        # 優先順位：
        # 不正解 ＞ 次の日に出題 ＞ 一週間後に出題 ＞ 一ヶ月後に出題 ＞ 未出題 ＞ 正解
        self.quiz = pd.concat([
              self.list_x
            , self.list_d
            , self.list_w
            , self.list_m
        ], ignore_index=True)

        # 問題数が不足していないか計算する
        num_t = num - len(self.quiz)
        if num_t <= 0:
            # 間違えた問題で満足する場合
            # 0~numの問題のみ抽出する
            self.quiz = self.quiz[0:num]
        else:
            # 間違えた問題だけでは不足している場合
            # まだ出題していない問題を抽出する
            self.list_n = worksheet.get_quiz(worksheet.NotMk, grade)
            self.quiz = pd.concat([self.quiz, self.list_n], ignore_index=True)

            num_t = num_t - len(self.list_n[0:num])
            if num_t > 0:
                # 未出題の問題だけでは確保できなかった場合
                # 既に出題し、正解している問題を候補にする
                self.list_o = worksheet.get_quiz(worksheet.CrctMk, grade)
                self.quiz = pd.concat([self.quiz, self.list_o], ignore_index=True)

        # 出題をnum数にする
        self.quiz = self.quiz[0:num]
