import math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.rl_settings import spaceShrinkage


# 文字が漢字であるか否かを評価する.
def is_kanji(char):
    return '\u4e00' <= char <= '\u9faf'

class OutputQuiz:
    def __init__(self):
        # フォント選択
        self.FontPath = 'C:\\Windows\\Fonts\\msmincho.ttc'
        self.Font = 'msmincho'
        pdfmetrics.registerFont(TTFont(self.Font, self.FontPath))  # フォント選択

        # PDF
        self.page = None
        # PDF設定値
        self.ProbFontSize  = 14  # 問題文のフォントサイズ
        self.ProbFrameSize = 10  # 問題枠のサイズ

        # 問題の枠のサイズ
        self.rect_size = 44

        # 問題文の記載位置を定義
        self.TopPos = 560  # 上の行の開始位置
        self.BtmPos = 270  # 下の行の開始位置

        # 1列に表示する問題数の最大値
        self.ColNumMax = 10

        # 上下の問題数を定義
        self.ProbTopNum = 0
        self.ProbBtmNum = 0

        # 問題番号の下にオフセットする
        self.ProblemYStartPos = 20    # 問題文の開始位置Y
        self.ProblemXStartPos = 650   # 問題文の開始位置X
        self.problem_text_frame = []  # 問題枠

    def output_quiz(self, path, student_name, create_date, num, worksheet):
        # 出題数が1列に収まる場合（最大表示数以下）、すべて上段に配置
        if num <= self.ColNumMax:
            self.ProbTopNum = num
            self.ProbBtmNum = 0
        # 出題数が1列の最大表示数を超える場合は、上下2段に分割して配置
        # 上段は「半分以上かつ最大値以上」、下段は残りを割り当てる
        else:
            top = max(math.ceil(num / 2), self.ColNumMax)
            self.ProbTopNum = top
            self.ProbBtmNum = max(num - top, 0)

        # 各列における問題文のX座標を計算する
        # 出題数に応じて、問題文の印字位置（左端基準）を等間隔で割り当てる
        step = self.ProblemXStartPos / self.ProbTopNum
        for i in range(0, self.ColNumMax):
            pos = self.ProblemXStartPos - step * i
            self.problem_text_frame.append(pos)

        # PDF設定
        self.page = canvas.Canvas(path, pagesize=landscape(A4))
        # 漢字プリントのタイトルを記述する
        self.draw_title(775, 525, 30)
        # 名前を記述する
        self.draw_name_frame(770, 300, 15)
        self.draw_student_name(777.5, 240, 25, student_name)
        # 作成日を記述する
        self.draw_date(770, 300, 15, create_date)
        # 問を記述する
        self.draw_problem(720, 550, 12)
        # 漢字プリントの出題番号を記述する
        self.draw_problem_number()
        # 漢字プリントの中央に線を記述する
        if num > self.ColNumMax:
            self.draw_center_line()

        # 漢字の問題を出力（上下段をまとめて処理）
        for i in range(num):
            # 上段か下段かで基準位置と表示インデックスを切り替える
            if i < self.ProbTopNum:
                base_y = self.TopPos
                display_index = i
            else:
                base_y = self.BtmPos
                display_index = i - self.ProbTopNum

            # 問題文の描画（基準位置からオフセット）
            self.draw_problem_statement(
                base_y - self.ProblemYStartPos,
                worksheet[i],
                display_index
            )

        # PDFを保存する
        self.page.save()

    def draw_title(self, x_pos, y_pos, font_size):
        self.draw_string(x_pos, y_pos, font_size, u'かんじプリント')

    def draw_name_frame(self, x_pos, y_pos, font_size):
        # 枠（名前）
        self.page.setStrokeColor('black')
        self.page.setLineWidth(1)
        self.page.setDash([])
        self.page.rect(x_pos - 10, y_pos - 5, 60, height=20, fill=True)

        self.page.setFont(self.Font, font_size)
        self.page.setFillColorRGB(255, 255, 255)
        self.page.drawString(x_pos - font_size / 3 / 2, y_pos, u'なまえ')
        self.page.setFillColorRGB(0, 0, 0)

        # 枠（欄）
        self.page.setStrokeColor('black')
        self.page.setLineWidth(1)
        self.page.setDash([])
        self.page.rect(x_pos - 10, y_pos - 205, 60, 200, fill=False)

        # 枠（日付）
        self.page.setStrokeColor('black')
        self.page.setLineWidth(1)
        self.page.setDash([])
        self.page.rect(x_pos - 10, y_pos - 245, 60, 40, fill=False)

    def draw_student_name(self, x_pos, y_pos, font_size, student_name):
        self.draw_string(x_pos, y_pos, font_size, student_name)

    def draw_reversed_digits(self, value, start_x, y):
        """指定された数値を逆順で描画する（1桁ずつ）"""
        x = start_x
        for digit in str(value)[::-1]:
            self.page.drawString(x, y, digit)
            x -= 7

    def draw_date(self, x_pos, y_pos, font_size, create_date):
        self.page.setFont(self.Font, font_size)

        # 日付：月
        self.draw_reversed_digits(create_date.month, x_pos + 4, y_pos - 240)
        # 日付：日
        self.draw_reversed_digits(create_date.day, x_pos + 29, y_pos - 240)
        # /
        self.page.drawString(x_pos + 15, y_pos - 240, '/')

    def draw_problem(self, x_pos, y_pos, font_size):
        # 問をPDFに印字する。
        string = u'つぎの □に かんじ を かきましょう。'
        self.draw_string(x_pos, y_pos, font_size, string)

    def draw_problem_number(self):
        num = u'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
        self.page.setFont(self.Font, self.ProbFontSize)

        # 上下の行の番号を印字
        for i in range(self.ProbTopNum + self.ProbBtmNum):
            y = self.TopPos if i < self.ProbTopNum else self.BtmPos
            self.page.drawString(self.problem_text_frame[i%self.ColNumMax], y, num[i])

    def draw_center_line(self):
        self.page.setStrokeColor('gray')
        self.page.setLineWidth(1)
        self.page.setDash([4])
        self.page.line(50, 300, 700, 300)

    def draw_string(self, x_pos, y_pos, font_size, string):
        # フォント設定
        self.page.setFont(self.Font, font_size)

        for word in string:
            # 句読点の場合
            if word == u'。' or word == u'、':
                self.page.drawString(x_pos + (font_size / 3) * 2, y_pos + font_size / 1.5, word)
                y_pos = y_pos - font_size
            # 拗音の場合
            elif word == u'ゃ' or word == u'ゅ' or word == u'ょ' or word == u'っ' \
                    or word == u'ャ' or word == u'ュ' or word == u'ョ' or word == u'ッ':
                # 拗音のサイズを指定する
                self.page.setFont(self.Font, font_size * 0.8)
                self.page.drawString(x_pos + (font_size / 3), y_pos + font_size / 3, word)
                # 文字のサイズを元に戻す
                self.page.setFont(self.Font, font_size)
                y_pos = y_pos - font_size * 0.8
            # スペースの場合
            elif word == u' ' or word == u'　':
                self.page.drawString(x_pos, y_pos, word)
                y_pos = y_pos - font_size / 3
            # 長音符の場合
            elif word == u'ー' or word == u'「' or word == u'」':
                # 用紙を-90度回転し、長音符を印字する
                self.page.rotate(-90)
                self.page.drawString(-1 * y_pos - font_size + font_size / 8, x_pos + font_size / 8, word)
                # 用紙を90度回転し、基に戻す
                self.page.rotate(90)
                y_pos = y_pos - font_size
            else:
                self.page.drawString(x_pos, y_pos, word)
                y_pos = y_pos - font_size

        return y_pos

    def draw_ruby(self, x_pos, y_pos, kanji, string=u''):
        # 直前の漢字の右隣にルビを振るため、1文字分だけ移動する
        x_pos = x_pos + self.ProbFontSize

        # ルビの文字サイズを問題文の 1/3 にする(小数点第一位で四捨五入)
        font_size = int(self.ProbFontSize / 3 + 0.5)
        self.page.setFont(self.Font, font_size)

        # 直前の漢字にルビを振るため、文字分だけ移動する
        if len(kanji) == 1:
            y_pos = y_pos + self.ProbFontSize * len(kanji) + self.ProbFontSize / 2 - font_size / 2 - font_size / 8
            if len(string) == 1:
                y_pos = y_pos
                y_pos_offset = font_size
            elif len(string) == 2:
                y_pos = y_pos + font_size
                y_pos_offset = font_size * 2
            elif len(string) == 3:
                y_pos = y_pos + font_size
                y_pos_offset = font_size
            elif len(string) == 4:
                y_pos = y_pos + font_size + font_size / 2
                y_pos_offset = font_size
            elif len(string) == 5:
                y_pos = y_pos + font_size * 2
                y_pos_offset = font_size
            else:
                y_pos = y_pos + font_size * 3 - font_size / 2
                y_pos_offset = font_size
        else:
            # 熟字訓 対応
            y_pos = y_pos + self.ProbFontSize * (1 + len(kanji) * 0.5) - font_size / 2
            y_pos_offset = self.ProbFontSize * len(kanji) / len(string)
            y_pos = y_pos + y_pos_offset * (len(string) - 1) / 2

        # ルビを記述する
        for word in string:
            self.draw_string(x_pos, y_pos, font_size, word)
            y_pos -= y_pos_offset

    # 漢字プリントの問題文の枠を書く
    def draw_frame(self, x_pos, y_pos, frame_num=0, string=u''):
        # 問題文の文字よりも漢字枠の方が大きいため、直前の文字との間隔をもう少し開ける
        y_pos -= (self.rect_size + self.ProbFontSize) / 1.8

        # 枠内を点線で十字の線を記述する
        self.page.setLineWidth(0.8)
        self.page.setStrokeColor('silver')
        self.page.setDash([2])
        # 縦
        self.page.line(
              x_pos + (self.rect_size / 2)
            , y_pos
            , x_pos + (self.rect_size / 2)
            , y_pos +  self.rect_size
        )
        # 横
        self.page.line(
              x_pos
            , y_pos + (self.rect_size / 2)
            , x_pos +  self.rect_size
            , y_pos + (self.rect_size / 2)
        )

        # 枠
        self.page.setStrokeColor('gray')
        self.page.setLineWidth(1)
        self.page.setDash([])
        self.page.rect(x_pos, y_pos, self.rect_size, self.rect_size, fill=False)

        if frame_num > 0:
            if len(string) == 1:  # 文字数が1の場合
                y_pos = y_pos + (self.rect_size * frame_num) * 0.5
            elif len(string) == 2:  # 文字数が2の場合
                y_pos = y_pos + (self.rect_size * frame_num) * 0.75
            elif len(string) == 3:  # 文字数が3の場合
                y_pos = y_pos + (self.rect_size * frame_num) * 0.85
            elif len(string) == 4:  # 文字数が4の場合
                y_pos = y_pos + (self.rect_size * frame_num) * 0.85
            elif len(string) == 5:  # 文字数が4の場合
                y_pos = y_pos + (self.rect_size * frame_num) * 0.95
            else:
                y_pos = y_pos + (self.rect_size * frame_num)

        next_print_pos = 0
        for word in string:
            if word == u'ゃ' or word == u'ゅ' or word == u'ょ' or word == u'っ':
                # 拗音のオフセット
                cs_x_offset = self.ProbFrameSize / 10 * 3
                cs_y_offset = 5
                font_size = self.ProbFrameSize / 10 * 8
                self.page.setFont(self.Font, font_size)
            else:
                cs_x_offset = 0
                cs_y_offset = 0
                font_size = self.ProbFrameSize
                self.page.setFont(self.Font, font_size)

            # 問題枠の右端に位置を調整する
            std_x_pos = x_pos + self.rect_size
            std_y_pos = y_pos + self.rect_size * (1 + 0.05) - self.ProbFrameSize

            # フリガナの文字数によって、間隔を空ける
            if len(string) == 1:
                start_pos = 0
                y_bias = 0
            elif len(string) == 2:
                start_pos = -(self.rect_size / 5)
                y_bias = (frame_num + 1) * 2
            elif len(string) == 3:
                start_pos = -(self.rect_size / 3)
                y_bias = (frame_num + 1) * 1.5
            elif len(string) == 4:
                start_pos = -(self.rect_size / 3)
                y_bias = (frame_num + 1)
            elif len(string) == 5:
                start_pos = -(self.rect_size / 2.2)
                y_bias = (frame_num + 1)
            else:
                start_pos = -(self.rect_size / 1.8)
                y_bias = (frame_num + 1)

            y_start_offset = self.rect_size / 2 - font_size / 2 + start_pos

            space = self.rect_size / 32 # 漢字枠より少し話した位置にする
            self.page.drawString(
                  std_x_pos + cs_x_offset + space
                , std_y_pos - next_print_pos - y_start_offset
                , word
            )
            next_print_pos += font_size * y_bias + cs_y_offset

    def draw_problem_statement(self, y_pos_const, problem, idx, chk=False):
        kFrameSttInit  = 0
        kFrameSttStart = 1  # 問題枠の開始
        kFrameSttEnd   = 2  # 問題枠の終了
        frame_stt = kFrameSttInit

        kRubySttEnd   = 0
        kRubySttStart = 1
        ruby_stt = kRubySttEnd

        fflg = 0
        arr = []
        kanji = ""
        y_pos = y_pos_const
        frame_num = 0

        count = 0
        for word in problem:
            # 問題枠を印字する。
            if frame_stt == kFrameSttStart:
                # []の内容を格納し終えた。
                if word == u']':
                    # 問題枠が初回の場合
                    if fflg == 0:
                        y_pos = y_pos - self.rect_size / 10 * 0.5
                        fflg = 1
                    if not chk:
                        if len(arr) <= 0:
                            self.draw_frame(self.problem_text_frame[idx] - self.rect_size / 3, y_pos, 0, arr)
                            frame_num += 1
                        else:
                            self.draw_frame(self.problem_text_frame[idx] - self.rect_size / 3, y_pos, frame_num, arr)
                            frame_num = 0
                    frame_stt = kFrameSttEnd
                    arr = []
                else:
                    arr.append(word)  # 問題の文字列をarrに格納する。
            # ルビを印字する。
            elif ruby_stt == kRubySttStart:
                # <>の内容を格納し終えた。
                if word == u'>':
                    if not chk:
                        self.draw_ruby(self.problem_text_frame[idx], y_pos, kanji, arr)
                    ruby_stt = kRubySttEnd
                    arr = []
                    kanji = ""
                else:
                    arr.append(word)  # ルビの文字列をarrに格納する。
            # 問題枠の開始
            elif word == u'[':
                # 問題枠を印字した直後の場合は位置を調整する。
                if frame_stt == kFrameSttEnd:
                    y_pos = y_pos - self.rect_size
                frame_stt = kFrameSttStart  # 問題枠の開始
            # ルビの開始
            elif word == u'<':
                ruby_stt = kRubySttStart  # ルビの開始
            # 問題文を印字する。
            else:
                # 問題枠、ルビの開始、終了でない場合
                font_size = self.ProbFontSize
                # 問題枠を印字した直後の場合は位置を調整する。
                if frame_stt == kFrameSttEnd:
                    y_pos = y_pos - font_size - self.rect_size / 10 * 8
                    frame_stt = kFrameSttInit
                if not chk:
                    y_pos = self.draw_string(self.problem_text_frame[idx], y_pos, font_size, word)

                if is_kanji(word):
                    kanji = kanji + word
                else:
                    kanji = ""

            count += 1

        return y_pos_const - y_pos