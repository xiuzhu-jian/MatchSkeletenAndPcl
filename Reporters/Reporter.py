import csv
from datetime import datetime


class Reporter:
    def __init__(self, type_name):
        self.type_name = type_name
        self.csv_file = None
        self.csv_writer = None

    def on_start(self, report_name: str, headers: list):
        self.csv_file = open(f'{self.type_name}_{report_name}.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(headers)

    def report(self, data: list):
        self.csv_writer.writerow(data)
        self.csv_file.flush()

    def on_finish(self):
        print('close csv file')
        self.csv_file.close()
