import csv

from paths import student_csv_file


def load_student_data(student_file):
    with open(student_file, newline='') as csvfile:
        # reader = csv.DictReader(csvfile, delimiter=',')
        # all_students = list(reader)

        reader = csv.reader(csvfile, delimiter=',')
        return list(reader)[1:]


class StudentCsvFile:
    def __init__(self):
        self.all_rows = load_student_data(student_csv_file)
        pass

    def get_short_name(self, stu_id):
        for row in self.all_rows:
            if row[0] == stu_id:
                return row[-1]
