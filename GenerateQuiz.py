import datetime as datetime
import pandas as pd
from OutputQuiz import OutputQuiz
from LoggerMixin import LoggerMixin

# 文字が漢字であるか否かを評価する.
def is_kanji(char):
    return '\u4e00' <= char <= '\u9faf'

class GenerateQuiz(LoggerMixin):
    def __init__(self):
        super().__init__(True)
        # PDF出力
        self.output_quiz = OutputQuiz()

        # 漢字プリント
        self.quiz = pd.DataFrame()  # 漢字プリントのデータを保持するデータフレーム

        self.list_x = []  # 間違えた問題のインデックス
        self.list_a = []  # 出題してからしばらく再出題していない問題のインデックス
        self.list_d = []  # 昨日間違えた問題のインデックス
        self.list_w = []  # 一週間前に間違えた問題のインデックス
        self.list_m = []  # 一ヶ月前に間違えた問題のインデックス
        self.list_n = []  # 未出題のインデックス
        self.list_o = []  # 正解している問題のインデックス

        self.create_date = None  # 作成日

    def create(self, path, worksheet, num, grades, student_name):
        # 作成日を取得する
        self.create_date = pd.to_datetime(datetime.datetime.today())

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
        self.create_train_mode(worksheet, num, grades)
        # 問題の答えに含まれている関数を取得する
        answer_list = self.get_answer_kanji_keyword(worksheet)
        # 問題文に答えが記載されている場合は、その漢字をルビに置き換える
        self.replace_kanji_with_ruby(worksheet, answer_list)
        # 選択中の学年未満のルビを削除する
        self.remove_unnecessary_ruby(worksheet, grades)
        # PDFを作成する
        self.output_quiz.create(path, student_name, self.create_date, num, self.quiz[worksheet.Problem])

        return self.quiz

    def get_answer_kanji_keyword(self, worksheet):
        answer_list = []
        for answer in self.quiz[worksheet.Answer]:
            answer_list.extend([char for char in answer])

        return answer_list

    def replace_kanji_with_ruby(self, worksheet, answer_list):
        self.print_info('問題文中に答えが存在するため、ひらがなに置き換えました.')

        for i, statement in enumerate(self.quiz[worksheet.Problem]):
            temp = []
            contains_answer_kanji = False
            kanji_in_ruby_tag_count = 0

            for word in statement:
                if is_kanji(word):
                    if word in answer_list:
                        contains_answer_kanji = True
                    temp.append(word)
                    kanji_in_ruby_tag_count += 1
                elif word == '<':
                    if contains_answer_kanji:
                        temp = temp[:-kanji_in_ruby_tag_count]
                    else:
                        temp.append(word)
                    kanji_in_ruby_tag_count = 0

                elif word == '>':
                    if contains_answer_kanji:
                        contains_answer_kanji = False
                    else:
                        temp.append(word)
                else:
                    temp.append(word)

            new_statement = ''.join(temp)

            if statement != new_statement:
                self.print_info('Before: ' + statement)
                self.print_info('After : ' + new_statement)
                self.quiz.loc[i, worksheet.Problem] = new_statement

    def remove_unnecessary_ruby(self, worksheet, grades):
        self.print_info('問題文中に不要なルビがあるため、削除しました.')

        kanji_list = worksheet.get_kanji_list(grades[:-1])

        for i, statement in enumerate(self.quiz[worksheet.Problem]):
            temp = []
            inside_ruby = False
            should_delete_ruby = False

            for word in statement:
                if is_kanji(word):
                    inside_ruby = False
                    if word in kanji_list:
                        inside_ruby = True
                    temp.append(word)
                else:
                    if word == '<':
                        should_delete_ruby = True
                        temp.append(word)
                    elif word == '>':
                        should_delete_ruby = False
                        inside_ruby = False
                        temp.append(word)
                    elif should_delete_ruby:
                        if not inside_ruby:
                            temp.append(word)
                        else:
                            temp.append(' ')
                    else:
                        temp.append(word)

            new_statement = ''.join(temp)

            if statement != new_statement:
                self.print_info('Before: ' + statement)
                self.print_info('After : ' + new_statement)
                self.quiz.loc[i, worksheet.Problem] = new_statement

    def create_train_mode(self, worksheet, num, grade):
        # テスト問題を選定する
        # 間違えた問題のインデックスを取得
        self.list_x = worksheet.get_quiz(worksheet.IncrctMk, grade, self.create_date, shuffle = True, days = 0)
        # 昨日間違えた問題のインデックスを取得する
        self.list_d = worksheet.get_quiz(worksheet.DayMk, grade, self.create_date, shuffle = True, days = 1)
        # 一週間前に間違えた問題のインデックスを取得する
        self.list_w = worksheet.get_quiz(worksheet.WeekMk, grade, self.create_date, shuffle = True, days = 7 - 1)
        # 一ヶ月前に間違えた問題のインデックスを取得する
        self.list_m = worksheet.get_quiz(worksheet.MonthMk, grade, self.create_date, shuffle = True, days = 7 * 3)

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
            self.list_n = worksheet.get_quiz(worksheet.NotMk, grade, self.create_date, shuffle = True)
            self.quiz = pd.concat([self.quiz, self.list_n], ignore_index=True)

            num_t = num_t - len(self.list_n[0:num])
            if num_t > 0:
                # 未出題の問題だけでは確保できなかった場合
                # 既に出題し、正解している問題を候補にする
                self.list_o = worksheet.get_quiz(worksheet.CrctMk, grade, self.create_date, shuffle = True)
                self.quiz = pd.concat([self.quiz, self.list_o], ignore_index=True)

        # 出題をnum数にする
        self.quiz = self.quiz[0:num]