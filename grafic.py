import numpy as np
from new_data import Data


class Month_statistic(Data):
    def __init__(self, excel_file, month=None, choosen_day=None):
        super().__init__(excel_file, month, choosen_day)
        self.days = []
        self.temperature = []

    def statistic_day(self):
        self.day_statistic()
        self.new_table.index = np.arange(len(self.new_table))
        self.days.clear()
        self.temperature.clear()
        for i in range(self.new_table.shape[0]):
            self.days.append(self.new_table['UTC'][i])
        for i in range(self.new_table.shape[0]):
            self.temperature.append(self.new_table["T"][i])

    def statistic_month(self):
        self.days.clear()
        self.temperature.clear()
        for i in range(self.input_table_rows):
            self.days.append(self.input_table['Число місяця'][i])
        for i in range(self.input_table_rows):
            self.temperature.append(self.input_table["T"][i])

    def statistic_from_to(self,choosen_from_date, choosen_to_date):
        self.data_statistic(choosen_from_date, choosen_to_date)
        self.new_table.index = np.arange(len(self.new_table))
        # print(self.new_table)
        self.days.clear()
        self.temperature.clear()
        for i in range(self.new_table.shape[0]):
            self.days.append(self.new_table['Число місяця'][i].strftime('%Y-%m-%d') +" "+ self.new_table['UTC'][i])
        for i in range(self.new_table.shape[0]):
            self.temperature.append(self.new_table["T"][i])


