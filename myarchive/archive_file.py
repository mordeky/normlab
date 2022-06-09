import shutil
import warnings
from pathlib import Path
from typing import Sequence
from zipfile import ZipFile, BadZipFile
from rarfile import RarFile, BadRarFile

from myarchive.archive_member import ArchiveMember
from myfilter.filter import Filter


class MyArchiveFile:
    def __init__(self, arch_file: Path, gbk_first=True):
        self.file = arch_file
        self.members: Sequence[ArchiveMember] = [ArchiveMember(member, gbk_first) for member in self.namelist()]

    def extractall(self, filter_out=None, filter_extract=None):
        members = filter_out(self.members) if filter_out else self.members
        for file in members:
            file.extract(self.open)

            if file.is_archive:
                filter_extract(file)

    def unlink(self):
        self.file.unlink()


class MyZipFile(MyArchiveFile, ZipFile):
    # Note that the inheritance order does matter!!
    def __init__(self, zip_file: Path, *args):
        ZipFile.__init__(self, zip_file, 'r')
        MyArchiveFile.__init__(self, zip_file, *args)


class MyRarFile(MyArchiveFile, RarFile):
    def __init__(self, rar_file: Path, *args):
        # super().__init__(rar_file, 'r')
        RarFile.__init__(self, rar_file, 'r')
        MyArchiveFile.__init__(self, rar_file, *args)


class FilteringExtractor:
    def __init__(self, arch_file: Path, out_path_generator, gbk_first=True,
                 out_path: Path = None, vip_path: Path = None):
        self.target_arch_file = arch_file
        self.gbk_first = gbk_first
        self.bad_arch_files = []
        self.final_out_path = self.get_out_path(out_path, arch_file)
        self.filter = Filter(self.final_out_path, vip_path, out_path_generator)

    @staticmethod
    def get_out_path(out_path: Path, arch_file):
        out_path = out_path if out_path else arch_file.parent
        out_path = out_path / arch_file.stem
        if out_path.exists():
            # out_path.rmdir()  # cannot remove empty directory
            shutil.rmtree(out_path, ignore_errors=True)
        out_path.mkdir(parents=True)
        return out_path

    @staticmethod
    def get_archive_class(archive: Path):
        if archive.suffix == '.zip':
            return MyZipFile
        if archive.suffix == '.rar':
            return MyRarFile

    def __call__(self, arch_file=None, out_path_generator=None):
        if isinstance(arch_file, ArchiveMember):
            arch_file, out_path_generator = self.filter.reset_filter_setting(arch_file, out_path_generator)
        arch_file = arch_file if arch_file else self.target_arch_file
        archive_class = self.get_archive_class(arch_file)
        try:
            with archive_class(arch_file, self.gbk_first) as arch_file:
                arch_file.extractall(self.filter, lambda x: self(x, out_path_generator))
            if arch_file.file != self.target_arch_file:
                arch_file.unlink()
        except (BadZipFile, BadRarFile):
            arch_file = arch_file.file
            warnings.warn(f'{arch_file} is not a {arch_file.suffix} file!')
            self.bad_arch_files.append(arch_file)
            return self.final_out_path

        return self.final_out_path
