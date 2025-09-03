# SettingFile.py
import pandas as pd

class SettingFile:
    PATH = './.setting'
    ENCODING = 'shift-jis'
    SEP = ','

    STUDENT_NAME = 'Name'
    WORKSHEET_PATH = 'Path'
    NUMBER = 'Number'
    GRADES = [
        u'小学一年生', u'小学二年生', u'小学三年生',
        u'小学四年生', u'小学五年生', u'小学六年生'
    ]
    MODE = u'出題形式'

    DEFAULT_NUMBER = '20'
    DEFAULT_MODE = 2

    def __init__(self):
        # 設定ファイルを初期化
        self.setting_file = pd.DataFrame()
        # 設定ファイルの読み込み
        self.load_setting_file()

    def get_columns(self):
        return [self.STUDENT_NAME, self.WORKSHEET_PATH, self.NUMBER] + self.GRADES + [self.MODE]

    def load_setting_file(self):
        # 設定ファイルを読み込む
        try:
            # 設定ファイルをファイルを開く
            self.setting_file = pd.read_csv(
                  self.PATH
                , sep=self.SEP
                , encoding=self.ENCODING
            )
        except FileNotFoundError:
            # 空の設定ファイルを作成する
            self.setting_file = pd.DataFrame(columns=self.get_columns())
            # 設定ファイルを保存する
            self.save_setting_file()

    def save_setting_file(self):
        # 設定ファイルを保存する
        self.setting_file.to_csv(
              self.PATH
            , sep=self.SEP
            , index=False
            , encoding=self.ENCODING
        )

    def set_register_student(self, student_name):
        # 生徒を登録する
        student_data = pd.DataFrame({
              self.STUDENT_NAME: [student_name]
            , self.WORKSHEET_PATH: ['']
            , self.NUMBER: self.DEFAULT_NUMBER
            , **dict.fromkeys(self.GRADES, False)
            , self.MODE: self.DEFAULT_MODE
        })
        # 設定ファイルにデータを結合し、インデックスを更新する
        self.setting_file = pd.concat([self.setting_file, student_data], ignore_index=True)

        # 設定ファイルを保存する
        self.save_setting_file()

    def is_registered_student(self, student_name):
        return student_name in self.setting_file[self.STUDENT_NAME].values

    def get_student_list(self):
        return self.setting_file[self.STUDENT_NAME].values.tolist()

    def is_empty(self):
        return len(self.setting_file[self.STUDENT_NAME]) == 0