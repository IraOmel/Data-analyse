import sys
from collections import Counter
from PyQt5 import QtWidgets
from windrose import WindroseAxes
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QComboBox
import numpy as np
from matplotlib import pyplot as plt
import design
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from grafic import Month_statistic

dict_month_num = {"Січень": 1, "Лютий": 2, "Березень": 3, "Квітень": 4, "Травень": 5, "Червень": 6, "Липень": 7,
                  "Серпень": 8, "Вересень": 9, "Жовтень": 10, "Листопад": 11, "Грудень": 12}


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.creat_table_show)

        self.do_2.clicked.connect(self.histogram_wind)
        self.do_1.clicked.connect(self.grafic_temperature)
        self.addToolBar(NavigationToolbar(self.widget.canvas, self))

    def num_month(self):
        dict_month = {"Січень": f"data/{self.regions.currentText()}/2012-1.xlsx",
                      "Лютий": f"data/{self.regions.currentText()}/2012-2.xlsx",
                      "Березень": f"data/{self.regions.currentText()}/2012-3.xlsx",
                      "Квітень": f"data/{self.regions.currentText()}/2012-4.xlsx",
                      "Травень": f"data/{self.regions.currentText()}/2012-5.xlsx",
                      "Червень": f"data/{self.regions.currentText()}/2012-6.xlsx",
                      "Липень": f"data/{self.regions.currentText()}/2012-7.xlsx",
                      "Серпень": f"data/{self.regions.currentText()}/2012-8.xlsx",
                      "Вересень": f"data/{self.regions.currentText()}/2012-9.xlsx",
                      "Жовтень": f"data/{self.regions.currentText()}/2012-10.xlsx",
                      "Листопад": f"data/{self.regions.currentText()}/2012-11.xlsx",
                      "Грудень": f"data/{self.regions.currentText()}/2012-12.xlsx"}
        return dict_month[self.listmonth.currentText()]

    def creat_table_show(self):
        edit_data = Month_statistic(self.num_month())
        edit_data.edit_weather()
        edit_data.input_table.to_excel(self.num_month(), index=False)
        input_table_header = edit_data.input_table.columns.values.tolist()
        self.table.setColumnCount(edit_data.input_table_colunms)
        self.table.setRowCount(edit_data.input_table_rows)
        self.table.setHorizontalHeaderLabels(input_table_header)
        for i in range(edit_data.input_table_rows):
            input_table_rows_values = edit_data.input_table.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            for j in range(edit_data.input_table_colunms):
                input_table_items_list = input_table_rows_values_list[j]
                input_table_items = str(input_table_items_list)
                newItem = QTableWidgetItem(input_table_items)
                self.table.setItem(i, j, newItem)

    def grafic_temperature(self):
        if self.listmonth_3.currentText() == "Температурні умови регіону":
            self.statistic_for_day()
        if self.listmonth_3.currentText() == "Тривалість температурних режимів":
            self.histogram()

    def statistic_for_day(self):
        choosen_from_date = self.fromdata.date()
        choosen_to_date = self.todata.date()
        choosen_day = self.spinBox.value()
        month = self.listmonth.currentText()
        region = self.num_month()
        edit_data = Month_statistic(region, month, choosen_day)
        edit_data.edit_weather()
        self.widget.canvas.axes.clear()
        if self.listmonth_2.currentText() == "Статистика від-до":
            edit_data.statistic_from_to(choosen_from_date.toPyDate(), choosen_to_date.toPyDate())
            X = edit_data.days
            Y = edit_data.temperature
            self.widget.canvas.axes.plot(X, Y)
        if self.listmonth_2.currentText() == "Статистика за день":
            edit_data.statistic_day()
            new_table_header = edit_data.new_table.columns.values.tolist()
            self.table_2.setColumnCount(edit_data.new_table.shape[1])
            self.table_2.setRowCount(edit_data.new_table.shape[0])
            self.table_2.setHorizontalHeaderLabels(new_table_header)
            for i in range(edit_data.new_table.shape[0]):
                input_table_rows_values = edit_data.new_table.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(edit_data.new_table.shape[1]):
                    input_table_items_list = input_table_rows_values_list[j]
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    self.table_2.setItem(i, j, newItem)
            edit_data.statistic_day()
            X = edit_data.days
            Y = edit_data.temperature
            self.widget.canvas.axes.plot(X, Y)
        if self.listmonth_2.currentText() == "Статистика за місяць":
            edit_data.statistic_month()
            X = edit_data.days
            Y = edit_data.temperature
            self.widget.canvas.axes.plot(X, Y)
        self.widget.canvas.axes.tick_params(axis='x',
                                            labelsize=7,
                                            labelbottom=True,
                                            labelleft=True,
                                            labelrotation=90)
        self.widget.canvas.axes.set_xlabel('Days')
        self.widget.canvas.axes.set_ylabel('Temperature in Celsium')
        self.widget.canvas.axes.set_title('Графік температур')
        self.widget.canvas.draw()

    def histogram(self):
        choosen_day = self.spinBox.value()
        month = self.listmonth.currentText()
        region = self.num_month()
        edit_data = Month_statistic(region, month, choosen_day)
        self.widget.canvas.axes.clear()
        temperature = []
        y_hour = []
        for i in range(edit_data.input_table_rows):
            temperature.append(edit_data.input_table["T"][i])
        c = Counter(sorted(temperature))
        for value in dict(c).values():
            y_hour.append(value * 0.5 - 0.5)
        self.widget.canvas.axes.bar(c.keys(), y_hour)
        self.widget.canvas.axes.set_ylabel('Час')
        self.widget.canvas.axes.set_xlabel('Температура в Цельсіях')
        self.widget.canvas.draw()

    def histogram_wind(self):
        choosen_day = self.spinBox.value()
        month = self.listmonth.currentText()
        region = self.num_month()
        edit_data = Month_statistic(region, month, choosen_day)
        speed = []
        direction = []
        y_hour = []
        if self.listmonth_4.currentText() == "Троянда вітрів":
            for i in range(edit_data.input_table_rows):
                speed.append(edit_data.input_table["FF"][i])
            for i in range(edit_data.input_table_rows):
                if edit_data.input_table['dd'][i] == "Північний":
                    edit_data.input_table['dd'][i] = 90
                if edit_data.input_table['dd'][i] == "Західний":
                    edit_data.input_table['dd'][i] = 180
                if edit_data.input_table['dd'][i] == "Південний":
                    edit_data.input_table['dd'][i] = 270
                if edit_data.input_table['dd'][i] == "Змінний":
                    edit_data.input_table['dd'][i] = np.nan
                if edit_data.input_table['dd'][i] == "Східний":
                    edit_data.input_table['dd'][i] = 0
                if edit_data.input_table['dd'][i] == "Пн-Зх":
                    edit_data.input_table['dd'][i] = 135
                if edit_data.input_table['dd'][i] == "Пд-Зх":
                    edit_data.input_table['dd'][i] = 225
                if edit_data.input_table['dd'][i] == "Пд-Сх":
                    edit_data.input_table['dd'][i] = 315
                if edit_data.input_table['dd'][i] == "Пн-Сх":
                    edit_data.input_table['dd'][i] = 45
                direction.append(edit_data.input_table["dd"][i])
            ax = WindroseAxes.from_ax()
            ax.bar(direction, speed, normed=True, opening=0.8, edgecolor='white')
            ax.set_legend()
            plt.show()
        if self.listmonth_4.currentText() == "Тривалість режимів вітрової активності":
            for i in range(edit_data.input_table_rows):
                speed.append(edit_data.input_table["FF"][i])
            c = Counter(sorted(speed))
            for value in dict(c).values():
                y_hour.append(value * 0.5 - 0.5)
            self.widget_2.canvas.axes.bar(c.keys(), y_hour)
            self.widget_2.canvas.axes.set_ylabel('Час')
            self.widget_2.canvas.axes.set_xlabel('Швидкість вітру')
            self.widget_2.canvas.axes.plot(c.keys(), y_hour, label='Тривалість вітру')
            self.widget_2.canvas.axes.legend()
            self.widget_2.canvas.draw()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()  # Вивід вікна
    app.exec_()  # Запуск застосунку


if __name__ == '__main__':
    main()
