import warnings
from pathlib import Path

from data.student_csv_file import StudentCsvFile
from data.student import Student
from myarchive.archive_file import FilteringExtractor
from utils.args import UserArgsParser

args_specs = {
    # '-l': dict(default='', type=str, help='Image Preprocessing Operators'),
    '--use-shortname': dict(action='store_true', help='A flag used to indicate if using the students'' shortname.'),
    '--gbk-first': dict(action='store_true', help='A flag used to indicate if `gbk` encoding is used in priority.'),
    '--utf-first': dict(action='store_true', help='A flag used to indicate if `utf-8` encoding is used in priority.'),
}


class NormFile:
    def __init__(self, whole_arch_file: Path, path_pre: str = '', user_args=None):
        assert whole_arch_file.suffix in ['.zip', '.rar']

        if isinstance(whole_arch_file, str):
            whole_arch_file = Path(whole_arch_file)

        user_args = UserArgsParser(args_specs).parse_args(user_args)

        self.target_arch_file = whole_arch_file
        self.out_path = whole_arch_file.parent / 'Output'
        self.vip_path = None
        self.path_pre = path_pre
        self.gbk_first = True if user_args.gbk_first else False
        self.use_shortname = user_args.use_shortname

    def __call__(self):
        extractor = FilteringExtractor(
            self.target_arch_file,
            gbk_first=self.gbk_first,
            out_path=self.out_path,
            vip_path=self.vip_path,
            out_path_generator=self.out_locations_generator)

        extractor()
        for bad_zip_file in extractor.bad_arch_files:
            warnings.warn(f'\n{bad_zip_file} is not a zip file!')

    def out_locations_generator(self, zip_file: Path):
        while True:
            yield dict(out_folder='', vip_filename='')


class NormLab(NormFile):
    def __init__(self, whole_arch_file: Path, path_pre: str = '', user_args=None):
        super().__init__(whole_arch_file, path_pre, user_args)

        self.vip_path = self.out_path / self.target_arch_file.stem
        self.path_pre = path_pre if path_pre else self.target_arch_file.stem.split('-')[0]

        if self.use_shortname:
            self.student_data = StudentCsvFile()

    def out_locations_generator(self, arch_file: Path):
        student_id, student_name = str(arch_file.stem).split('-')
        shortname = student_name if not self.use_shortname else self.student_data.get_short_name(student_id)
        student = Student(student_id, shortname, self.path_pre, self.vip_path)
        vip_filename = student.lab_report_name

        yield dict(out_folder=student.code_folder, vip_filename=vip_filename)
        while True:
            yield dict(out_folder='', vip_filename=vip_filename)


if __name__ == '__main__':
    import sys

    zip_file, args = sys.argv[-1], sys.argv[1:-1]

    from paths import project_path

    # zip_file = project_path / 'test/MidtermExam/test-case-data/Lab03-JUnit for Unit Test.zip'
    # zip_file = 'E:/Work/Job/Teaching/SoftwareTest(Inter)/Exam/2022-Midterm/Midterm-SQAT-2022.zip'
    # zip_file = 'E:/Work/Job/Teaching/SoftwareDesign/Exam/2022-期中考试/软件设计-2022-2021-2022 第二学期 期中考试(pdf).zip'
    # zip_file = 'E:/Work/Job/Teaching/SoftwareDesign/Exam/2022-期中考试/Output/软件设计-2022-2021-2022 第二学期 期中考试(pdf)/软件设计-202003340104-陈煜杭/uml.zip'

    NormLab(zip_file, user_args=args)()
    # NormFile(zip_file)()
