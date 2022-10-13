import datetime
import pandas as pd
import numpy as np
from pandas import isnull
from datetime import datetime
from datetime import date

pd.options.mode.chained_assignment = None

dict_month_num = {"Січень": 1, "Лютий": 2, "Березень": 3, "Квітень": 4, "Травень": 5, "Червень": 6, "Липень": 7,
               "Серпень": 8, "Вересень": 9, "Жовтень": 10, "Листопад": 11, "Грудень": 12}


class Data():
    def __init__(self, excel_file, month=None, choosen_day=None):
        self.kyiv_table = None
        self.excel_file = excel_file
        self.month = month
        self.choosen_day = choosen_day
        self.input_table = pd.read_excel(self.excel_file)
        self.input_table.rename(columns={'Число месяца': 'Число місяця'}, inplace=True)
        self.input_table_rows = self.input_table.shape[0]
        self.input_table_colunms = self.input_table.shape[1]
        self.new_table = 0

    def edit_weather(self):
        self.input_table['U'].fillna(0, inplace=True)
        for i in range(self.input_table_rows):
            self.input_table['U'][i] = np.random.randint(30, 100)
        self.input_table['ww'].fillna("CL", inplace=True)
        self.input_table['dd'].fillna("Штиль", inplace=True)
        for i in range(self.input_table_rows):
            if self.input_table['dd'][i] == "Северный":
                self.input_table['dd'][i] = "Північний"
            if self.input_table['dd'][i] == "Западный":
                self.input_table['dd'][i] = "Західний"
            if self.input_table['dd'][i] == "Южный":
                self.input_table['dd'][i] = "Південний"
            if self.input_table['dd'][i] == "Переменный":
                self.input_table['dd'][i] = "Змінний"
            if self.input_table['dd'][i] == "Восточный":
                self.input_table['dd'][i] = "Східний"
            if self.input_table['dd'][i] == "С-З":
                self.input_table['dd'][i] = "Пн-Зх"
            if self.input_table['dd'][i] == "Ю-З":
                self.input_table['dd'][i] = "Пд-Зх"
            if self.input_table['dd'][i] == "Ю-В":
                self.input_table['dd'][i] = "Пд-Сх"
            if self.input_table['dd'][i] == "С-В":
                self.input_table['dd'][i] = "Пн-Сх"
        for i in range(self.input_table_rows):
            try:
                float(self.input_table['vv'][i])
            except:
                self.input_table['vv'][i] = np.nan
        if isnull(self.input_table['vv'][0]):
            self.input_table['vv'][0] = round(self.input_table['vv'].median())
        self.input_table['vv'].fillna(method="pad", inplace=True)
        if isnull(self.input_table['hhh'][0]):
            self.input_table['hhh'][0] = round(self.input_table['hhh'].median())
        self.input_table['hhh'] = round(self.input_table['hhh'].interpolate(method="linear"))
        if isnull(self.input_table['N'][0]):
            self.input_table['N'][0] = round(self.input_table['N'].median())
        self.input_table['N'] = round(self.input_table['N'].interpolate(method="linear"))
        self.input_table['T'] = round(self.input_table['T'].interpolate(method="linear"))
        for i in range(self.input_table_rows):
            self.input_table['T'][i] = int(self.input_table['T'][i])

    def day_statistic(self):
        day = date(2012, dict_month_num[self.month], self.choosen_day)
        filter_large = self.input_table['Число місяця'] == str(day)
        self.new_table = self.input_table.loc[filter_large]

    def data_statistic(self, choosen_from_date, choosen_to_date):
        self.kyiv_table = pd.read_excel("data/Київ/Київ-2012.xlsx")
        filter_large = self.kyiv_table['Число місяця'] >= datetime.strptime(str(choosen_from_date), '%Y-%m-%d')
        filter_first_class = self.kyiv_table['Число місяця'] <= datetime.strptime(str(choosen_to_date), '%Y-%m-%d')
        self.new_table = self.kyiv_table.loc[filter_large & filter_first_class]
        # print(self.new_table)





