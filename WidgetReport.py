# WidgetReport.py
import customtkinter as ctk
import tkinter.messagebox as msgbox
from Widget import Widget

class WidgetReport(Widget):
    def __init__(self, setting_file, select_student, status_callback):
        super().__init__()
        self.setting_file = setting_file
        self.select_student = select_student
        self.status_callback = status_callback

    def create(self, frame, row, column):
        self.create_label(frame, 0, 0, u'レポート')
        # 学年
        self.create_grade_label_section(frame, 1, 0)
        # 出題数
        self.create_output_section(frame, 1, 1)

        self.create_schedule(frame, 1, 2, '正解', 'correct')
        self.create_schedule(frame, 1, 3, '不正解', 'incorrect')
        self.create_schedule(frame, 1, 4, '一日後', 'day')
        self.create_schedule(frame, 1, 5, '一週間後', 'week')
        self.create_schedule(frame, 1, 6, '一ヶ月後', 'month')

    def create_grade_label_section(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)

        self.create_text_label(frame, 0, 0, u'学年')

        for i, grade_text in enumerate(self.setting_file.GRADES + [u'合計']):
            grade_label = ctk.CTkLabel(
                  frame
                , text=grade_text
                , font=ctk.CTkFont(size=14)
            )
            grade_label.grid(row=i + 1, column=0, sticky='n', padx=5, pady=1)

    def create_output_section(self, frame, row, column):
        frame = self.create_frame(frame, row, column, None)
        self.create_text_label(frame, 0, 0, '出題状況', 3)
        self.create_grade_entries(frame, start_row=1, column_offset=0, value_prefixes=['outnum', 'tolnum'], show_slash=True)

    def create_schedule(self, frame, row, column, title, value_attr_prefix):
        frame = self.create_frame(frame, row, column, None)
        label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        label.grid(row=0, column=0, sticky='n', padx=5, pady=5)
        self.create_grade_entries(frame, start_row=1, column_offset=0, value_prefixes=[value_attr_prefix])

    def create_grade_entries(self, frame, start_row, column_offset, value_prefixes, show_slash=False):
        for prefix in value_prefixes:
            setattr(self, f"{prefix}_value", {})
            setattr(self, f"{prefix}_value_entry", {})

        for i, grade_text in enumerate(self.setting_file.GRADES + ['合計']):
            for j, prefix in enumerate(value_prefixes):
                value_dict = getattr(self, f"{prefix}_value")
                entry_dict = getattr(self, f"{prefix}_value_entry")

                value_dict[i] = ctk.StringVar(value="")
                entry = ctk.CTkEntry(
                      frame
                    , width=50
                    , textvariable=value_dict[i]
                    , justify='right'
                    , state='readonly'
                )
                entry.grid(row=start_row + i, column=column_offset + j * 2, sticky='w', padx=5, pady=1)
                entry_dict[i] = entry

            if show_slash and len(value_prefixes) == 2:
                slash_label = ctk.CTkLabel(
                      frame
                    , text='/'
                    , font=ctk.CTkFont(size=14)
                )
                slash_label.grid(row=start_row + i, column=column_offset + 1, sticky='w', padx=5, pady=1)

    def update_report(self, worksheet):
        # 出題数を求める
        def calc_outnum(grade):
            return worksheet.get_count_by(grade) - worksheet.get_count_by(grade, worksheet.NotMk)

        # マーク種別と対応する取得関数のマッピング
        mark_map = {
              'outnum': lambda grade: calc_outnum(grade)
            , 'tolnum': lambda grade: worksheet.get_count_by(grade)
            , 'correct': lambda grade: worksheet.get_count_by(grade, worksheet.CrctMk)
            , 'incorrect': lambda grade: worksheet.get_count_by(grade, worksheet.IncrctMk)
            , 'day': lambda grade: worksheet.get_count_by(grade, worksheet.DayMk)
            , 'week': lambda grade: worksheet.get_count_by(grade, worksheet.WeekMk)
            , 'month': lambda grade: worksheet.get_count_by(grade, worksheet.MonthMk)
        }

        # 合計値の初期化
        total_counts = {key: 0 for key in mark_map}

        # 学年ごとの更新
        for i, grade in enumerate(range(worksheet.GradeRange[0], worksheet.GradeRange[-1] + 1)):
            for key, count_func in mark_map.items():
                count = count_func(grade)
                getattr(self, f"{key}_value")[i].set(count)
                total_counts[key] += count

        # 合計欄（末尾）にセット
        last_index = len(self.setting_file.GRADES)  # '合計' のインデックス
        for key in mark_map:
            getattr(self, f"{key}_value")[last_index].set(total_counts[key])