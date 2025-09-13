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

    def delete_student(self, student_name):
        mask = self.setting_file[self.STUDENT_NAME] == student_name

        self.setting_file = self.setting_file.loc[~mask].reset_index(drop=True)

        # 設定ファイルを保存する
        self.save_setting_file()

    # 生徒が登録済みかどうかを判定
    def is_registered_student(self, student_name):
        return student_name in self.setting_file[self.STUDENT_NAME].values

    # 登録されている生徒名の一覧を取得
    def get_student_list(self):
        return self.setting_file[self.STUDENT_NAME].values.tolist()

    # 生徒に紐づくワークシートのパスを取得
    def get_worksheet_path(self, student_name):
        mask = self.setting_file[self.STUDENT_NAME] == student_name
        return self.setting_file.loc[mask, self.WORKSHEET_PATH].iloc[0]

    # 生徒に紐づくワークシートのパスを更新
    def set_worksheet_path(self, student_name, path):
        mask = self.setting_file[self.STUDENT_NAME] == student_name
        self.setting_file[self.WORKSHEET_PATH] = self.setting_file[self.WORKSHEET_PATH].astype(str)
        self.setting_file.loc[mask, self.WORKSHEET_PATH] = path

        self.save_setting_file()

    # 生徒が選択している学年のフラグ一覧を取得
    def get_grade_list(self, student_name):
        return self.setting_file.loc[
            self.setting_file[self.STUDENT_NAME] == student_name,
            self.GRADES
        ].values.flatten().tolist()

    # 生徒の指定学年の出題フラグを更新
    def set_grade(self, student_name, key, checked):
        mask = self.setting_file[self.STUDENT_NAME] == student_name
        self.setting_file.loc[mask, key] = checked
        self.save_setting_file()

    # 生徒ごとの出題数を取得
    def get_number_of_problem(self, student_name):
        mask = self.setting_file[self.STUDENT_NAME] == student_name
        return self.setting_file.loc[mask, self.NUMBER].iloc[0]

    # 生徒ごとの出題数を更新
    def set_number_of_problem(self, student_name, value):
        mask = self.setting_file[self.STUDENT_NAME] == student_name
        self.setting_file.loc[mask, self.NUMBER] = value
        self.save_setting_file()

    # 設定ファイルに生徒が1人も登録されていないかを判定
    def is_empty(self):
        return len(self.setting_file[self.STUDENT_NAME]) == 0