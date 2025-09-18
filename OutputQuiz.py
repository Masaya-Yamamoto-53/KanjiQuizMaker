import math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape

# 文字が漢字であるか否かを評価する.
def is_kanji(char):
    return '\u4e00' <= char <= '\u9faf'

class OutputQuiz:
    def __init__(self):
        # フォント選択
        self.FontPath = 'C:\\Windows\\Fonts\\msmincho.ttc'
        self.Font = 'msmincho'
        pdfmetrics.registerFont(TTFont(self.Font, self.FontPath))  # フォント選択

        # PDF設定値
        self.ProbFontSize  = 17  # 問題文のフォントサイズ
        self.ProbFontSize  = 15  # 問題文のフォントサイズ
        self.ProbFrameSize = 10  # 問題枠のサイズ

        # 問題の枠のサイズ
        self.rect_size = 44

        # 問題文の記載位置を定義
        self.TopPos = 560  # 上の行の開始位置
        self.BtmPos = 270  # 下の行の開始位置

        # 上下の問題数を定義
        self.ProbTopNum = 0
        self.ProbBtmNum = 0

        # 列の問題数の下限
        self.ColNumMin = 10

        # 問題番号の下にオフセットする
        self.ProblemStartOffset = 20  # 問題文の開始位置

        self.problem_start_pos = 650  # 問題枠の開始位置
        self.problem_text_frame = []  # 問題枠

    def create(self, path, student_name, create_date, num, worksheet):
        num_t = num
        if num_t < self.ColNumMin:
            self.ProbTopNum = num_t
            self.ProbBtmNum = 0
        else:
            num_t = math.ceil(num / 2)
            num_t = max(num_t, self.ColNumMin)

            self.ProbTopNum = num_t
            self.ProbBtmNum = num - num_t
            if self.ProbBtmNum < 0:
                self.ProbBtmNum = 0

        # 列ごとの印字位置を演算する.
        # 問題ごとに印字する位置を決めたいため.
        for i in range(0, num):
            pos = self.problem_start_pos - self.problem_start_pos / max(self.ProbTopNum, self.ColNumMin) * i
            self.problem_text_frame.append(pos)

        # PDF設定
        self.page = canvas.Canvas(path, pagesize=landscape(A4))
        # 漢字プリントのタイトルを記述する
        self._draw_title(775, 525, 30)
        # 名前を記述する
        self._draw_name_frame(770, 300, 15, create_date)
        self._draw_student_name(777.5, 240, 25, student_name)
        # 作成日を記述する
        self._draw_date(770, 300, 15, create_date)
        # 問を記述する
        self._draw_problem(720, 550, 12)
        # 漢字プリントの出題番号を記述する
        self._draw_problem_number()
        # 漢字プリントの中央に線を記述する
        self._draw_center_line()
        # 問題を出力する
        # 漢字の問題を出力（上段）
        for i in range(0, self.ProbTopNum):
            self._draw_problem_statement(
                  # self.kTopPosには各問題の番号①～⑩が印字されているため、オフセットする.
                  self.TopPos - self.ProblemStartOffset
                , worksheet[i]
                , i
            )

        # 漢字の問題を出力（下段）
        for i in range(self.ProbTopNum, num):
            self._draw_problem_statement(
                  # self.kBtmPosには各問題の番号⑪～⑳が印字されているため、オフセットする.
                  self.BtmPos - self.ProblemStartOffset
                , worksheet[i]
                , i - self.ProbTopNum
            )
        # PDFを保存する
        self.page.save()

    def _draw_title(self, x_pos, y_pos, font_size):
        self._draw_string(x_pos, y_pos, font_size, u'かんじプリント')

    def _draw_name_frame(self, x_pos, y_pos, font_size, create_date):
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

    def _draw_student_name(self, x_pos, y_pos, font_size, student_name):
        self._draw_string(x_pos, y_pos, font_size, student_name)

    def _draw_date(self, x_pos, y_pos, font_size, create_date):
        self.page.setFont(self.Font, font_size)

        # 日付：月
        x_pos_tmp = x_pos + 4
        for month in str(create_date.month)[::-1]:
            self.page.drawString(x_pos_tmp, y_pos - 240, month)  # 月
            x_pos_tmp -= 7

        # 日付：日
        x_pos_tmp = x_pos + 29
        for day in str(create_date.day)[::-1]:
            self.page.drawString(x_pos_tmp, y_pos - 240, day)  # 日
            x_pos_tmp -= 7

        self.page.drawString(x_pos + 15, y_pos - 240, u'/')

    def _draw_problem(self, x_pos, y_pos, font_size):
        # 問をPDFに印字する。
        string = u'つぎの □に かんじ を かきましょう。'
        self._draw_string(x_pos, y_pos, font_size, string)

    def _draw_problem_number(self):
        num = u'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
        self.page.setFont(self.Font, self.ProbFontSize)

        # 上の行の番号を印字
        for i in range(0, self.ProbTopNum):
            self.page.drawString(self.problem_text_frame[i], self.TopPos, num[i])

        # 下の行の番号を印字
        for i in range(0, self.ProbBtmNum):
            self.page.drawString(self.problem_text_frame[i], self.BtmPos, num[i + self.ProbTopNum])

    def _draw_center_line(self):
        self.page.setStrokeColor('gray')
        self.page.setLineWidth(1)
        self.page.setDash([4])
        self.page.line(50, 300, 700, 300)

    def _draw_string(self, x_pos, y_pos, font_size, string):
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
                # 拗音のサイズを指定する.
                # self.page.setFont(self.kFont, font_size / 10 * 8)
                self.page.setFont(self.Font, font_size * 0.8)
                self.page.drawString(x_pos + (font_size / 3), y_pos + font_size / 3, word)
                # 文字のサイズを元に戻す.
                self.page.setFont(self.Font, font_size)
                # y_pos = y_pos - font_size / 10 * 8
                y_pos = y_pos - font_size * 0.8
            # スペースの場合
            elif word == u' ' or word == u'　':
                self.page.drawString(x_pos, y_pos, word)
                y_pos = y_pos - font_size / 3
            # 長音符の場合
            elif word == u'ー' or word == u'「' or word == u'」':
                # 用紙を-90度回転し、長音符を印字する.
                self.page.rotate(-90)
                self.page.drawString(-1 * y_pos - font_size + font_size / 8, x_pos + font_size / 8, word)
                # 用紙を90度回転し、基に戻す.
                self.page.rotate(90)
                y_pos = y_pos - font_size
            else:
                self.page.drawString(x_pos, y_pos, word)
                y_pos = y_pos - font_size

        return y_pos

    def _draw_ruby(self, x_pos, y_pos, kanji, string=u''):
        """漢字プリントの出題の漢字にルビを書く."""
        # 直前の漢字の右隣にルビを振るため, 1文字分だけ移動する.
        x_pos = x_pos + self.ProbFontSize

        # 直前の漢字にルビを振るため, 文字分だけ移動する.
        if len(kanji) == 1:
            y_pos = y_pos + self.ProbFontSize
        elif len(kanji) == 2:
            y_pos = y_pos + self.ProbFontSize * 1.5
        elif len(kanji) == 3:
            y_pos = y_pos + self.ProbFontSize * 2.0
        else:
            y_pos = y_pos + self.ProbFontSize * 2.5

        # ルビの文字サイズを問題文の 1/3 にする.
        font_size = self.ProbFontSize / 3
        self.page.setFont(self.Font, font_size)

        # ルビの文字数によって, 縦軸の描写位置を変更する.
        if len(string) == 1:
            y_start_offset = self.ProbFontSize / 4  # ルビ描写開始オフセット(文字数によって開始位置をずらす)
            y_pos_offset = self.ProbFontSize / 4  # ルビが 1文字 のとき
        elif len(string) == 2:
            y_start_offset = self.ProbFontSize / 2  # ルビ描写開始オフセット(文字数によって開始位置をずらす)
            y_pos_offset = self.ProbFontSize / 2  # ルビが 2文字 のとき
        elif len(string) == 3:
            y_start_offset = self.ProbFontSize / 6 * 3  # ルビ描写開始オフセット(文字数によって開始位置をずらす)
            y_pos_offset = self.ProbFontSize / 3  # ルビが 3文字 のとき
        else:
            y_start_offset = self.ProbFontSize / 4 * 3  # ルビ描写開始オフセット(文字数によって開始位置をずらす)
            y_pos_offset = self.ProbFontSize / 3  # ルビが 4文字 以外のとき

        if len(kanji) == 1:
            y_start_offset = y_start_offset
            y_pos_offset = y_pos_offset
        elif len(kanji) == 2:
            y_start_offset = y_start_offset * 1.3
            y_pos_offset = y_pos_offset * 1.3
        elif len(kanji) == 3:
            y_start_offset = y_start_offset * 1.6
            y_pos_offset = y_pos_offset * 1.6

        # ルビを記述する.
        for word in string:
            self._draw_string(x_pos, y_pos + y_start_offset, font_size, word)
            y_pos -= y_pos_offset

    # 漢字プリントの問題文の枠を書く.
    def _draw_frame(self, x_pos, y_pos, size, frame_num=0, string=u''):
        """漢字プリントの問題文の枠を書く."""
        rect_width = size
        rect_height = size

        y_pos -= (size + self.ProbFontSize) / 1.8

        # 枠内を点線で十字の線を記述する.
        self.page.setLineWidth(0.8)
        self.page.setStrokeColor('silver')
        self.page.setDash([2])
        self.page.line(x_pos + (rect_width / 2), y_pos, x_pos + (rect_width / 2), y_pos + rect_height)  # 縦
        self.page.line(x_pos, y_pos + (rect_height / 2), x_pos + rect_width, y_pos + (rect_height / 2))  # 横

        # 枠
        self.page.setStrokeColor('gray')
        #self.page.setStrokeColor('black')
        self.page.setLineWidth(1)
        self.page.setDash([])
        self.page.rect(x_pos, y_pos, rect_width, rect_height, fill=False)

        # フリガナの文字数によって、間隔を空ける.
        if len(string) == 1:  # 文字数が1の場合
            y_bias = 1 * (frame_num + 1)
            start_pos_bias = 2
        elif len(string) == 2:  # 文字数が2の場合
            y_bias = 2 * (frame_num + 1)
            start_pos_bias = 1
        elif len(string) == 3:  # 文字数が3の場合
            y_bias = 1.5 * (frame_num + 1)
            start_pos_bias = 0.5
        elif len(string) == 4:  # 文字数が4の場合
            y_bias = 1 * (frame_num + 1)
            start_pos_bias = 0.5
        else:
            y_bias = 1 * (frame_num + 1)
            start_pos_bias = 0.1

        if frame_num > 0:
            if len(string) == 1:  # 文字数が1の場合
                y_pos = y_pos + (rect_height * frame_num) * 0.5
            elif len(string) == 2:  # 文字数が2の場合
                y_pos = y_pos + (rect_height * frame_num) * 0.75
            elif len(string) == 3:  # 文字数が3の場合
                y_pos = y_pos + (rect_height * frame_num) * 0.75
            elif len(string) == 4:  # 文字数が4の場合
                y_pos = y_pos + (rect_height * frame_num) * 0.75
            elif len(string) == 5:  # 文字数が4の場合
                y_pos = y_pos + (rect_height * frame_num) * 0.90
            else:
                y_pos = y_pos + rect_height

        x_space = 2  # 枠にピッタリ付かないように少し間を空ける.
        next_print_pos = 0
        for word in string:
            if word == u'ゃ' or word == u'ゅ' or word == u'ょ' or word == u'っ':
                # 拗音(contracted sound)のオフセット
                cs_x_offset = self.ProbFrameSize / 10 * 3
                cs_y_offset = 5
                font_size = self.ProbFrameSize / 10 * 8
                self.page.setFont(self.Font, font_size)
            else:
                cs_x_offset = 0
                cs_y_offset = 0
                font_size = self.ProbFrameSize
                self.page.setFont(self.Font, font_size)

            # 問題枠の右端に位置を調整する.
            std_x_pos = x_pos + rect_width
            std_y_pos = y_pos + rect_height * (1 + 0.05) - self.ProbFrameSize

            y_start_offset = font_size * start_pos_bias

            self.page.drawString(
                std_x_pos + cs_x_offset + x_space
                , std_y_pos - next_print_pos - y_start_offset
                , word
            )
            next_print_pos += font_size * y_bias + cs_y_offset

    def _draw_problem_statement(self, y_pos_const, problem, idx, chk=False):
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
                            self._draw_frame(self.problem_text_frame[idx] - self.rect_size / 3, y_pos, self.rect_size, 0, arr)
                            frame_num += 1
                        else:
                            self._draw_frame(self.problem_text_frame[idx] - self.rect_size / 3, y_pos, self.rect_size, frame_num, arr)
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
                        self._draw_ruby(self.problem_text_frame[idx], y_pos, kanji, arr)
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
                    y_pos = self._draw_string(self.problem_text_frame[idx], y_pos, font_size, word)

                if is_kanji(word):
                    kanji = kanji + word
                else:
                    kanji = ""

            count += 1

        return y_pos_const - y_pos