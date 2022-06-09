from pathlib import Path
from paths import mid_exam_path
# import patoolib
import rarfile
# from unrar import rarfile
import zipfile

archives = [
    # mid_exam_path / 'test-case-01/ZipInner/Lab01-中文.zip',
    # mid_exam_path / 'test-case-02/Lab03-JUnit for Unit Test.zip',
    # mid_exam_path / 'test-case-02/new/L201926630101-KIPESHAMLONDWAKAPERA.zip',
    # mid_exam_path / 'test-case-02/new/L201926630102-DENNISERTANDY/Lab3_L201926630102.zip',
    # '/Users/xxli/work/Teaching/SoftwareTest(Inter)/Exam/Midterm-SQAT-2022/Midterm-L201926630105-Precious/midterm.rar',
    # mid_exam_path / 'test-case-04/RAR/RAR文档-Inner.rar',
    # mid_exam_path / 'test-case-04/RAR/RAR文档-Nestted.rar',
    # mid_exam_path / 'test-case-04/RAR/RAR文档-Outter.rar',
    # mid_exam_path / 'test-case-04/RAR/RAR文档.zip',
    'E:/Work/Job/Teaching/SoftwareDesign/Exam/2022-期中考试/软件设计-2022-2021-2022 第二学期 期中考试(pdf)/202003340220-徐瑕.zip'
]


def get_output_path(archive, path: Path = None):
    p = Path(archive)
    p = p.parent / p.stem
    if path is not None:
        p = path / p

    if not p.exists():
        p.mkdir(parents=True)
    return p


def archives_generator():
    print('/n')
    for archive in archives:
        yield archive, get_output_path(archive)


def test_yield():
    for archive, out_dir in archives_generator():
        print(archive)


def test_unrar():
    for archive, out_dir in archives_generator():
        with rarfile.RarFile(archive) as rar_file:
            rar_file.extractall(path=out_dir)
            # files = rar_file.namelist()
            # rar_file.extract(files[0], path=out_dir)
            continue


# def test_patoolib():
#     for archive, out_dir in archives_generator():
#         # out_dir = str(out_dir.as_posix())
#         # TypeError: stat: path should be string, bytes, os.PathLike or integer, not module
#         patoolib.extract_archive(archive, outdir=out_dir, verbosity=1)


# patool的正常运行依赖于其他解压软件，
# 例如，我平时用patool来解压文件时它主要调用了我电脑的7z、Rtools两个程序，
# 如果电脑上没有能够处理相应压缩文件的软件，则会报错：
# patoolib.util.PatoolError: could not find an executable program to extract format rar;
#   candidates are (rar,unrar,7z)

def test_unzip():
    print('\n')
    for archive, out_dir in archives_generator():
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extractall(path=out_dir)
            continue
            # member = 'L201926630101-KIPESHAMLONDWAKAPERA.zip'
            # Note: 如果 zipfile.extract() 所解压的 member 是 .zip 文件，解压出来的结果将仍是 .zip 文件
            # zip_file.extract(member, path=get_output_path(member, out_dir))


def test_unzip():
    print('\n')
    for archive, out_dir in archives_generator():
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extractall(path=out_dir)


class Archive:
    def __init__(self, *args):
        print('ok')
        pass

    def extract_all(self, path):
        self.extractall(path)
        # raise NotImplementedError

    def extract_one(self, member, out_file):
        import shutil
        with self.open(member, 'r') as from_file:  # 打开原文件
            with open(out_file, 'wb') as to_file:  # 创建并打开新文件
                shutil.copyfileobj(from_file, to_file)
        # raise NotImplementedError


class MyZipFile(Archive, zipfile.ZipFile):
    def __init__(self, zip_file: Path):
        Archive.__init__(self)
        zipfile.ZipFile.__init__(self, zip_file, 'r')


class MyRarFile(rarfile.RarFile, Archive):
    def __init__(self, rar_file: Path):
        super().__init__(rar_file, 'r')
        # Archive.__init__(self)
        # rarfile.RarFile.__init__(self, rar_file, 'r')


def get_archive_class(archive):
    if archive.endswith('.zip'):
        return MyZipFile
    if archive.endswith('.rar'):
        return MyRarFile


def test_extract():
    for archive, out_dir in archives_generator():
        archive_class = get_archive_class(archive)
        with archive_class(archive) as arc:
            files = arc.namelist()
            arc.extract_one(files[0], out_dir / files[0])
