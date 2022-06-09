from pathlib import Path
from typing import Sequence

from myarchive.archive_member import ArchiveMember
from myfilter.file_filter import FileFilter
from myfilter.structure_filter import StructureFilter


class Filter:
    def __init__(self, out_path: Path, vip_path: Path, out_path_generator):
        self.file_filter = FileFilter(vip_path)
        self.structure_filter = StructureFilter(out_path, vip_path, out_path_generator)

    def __call__(self, all_files: Sequence[ArchiveMember]):
        reg_files, vip_files = self.file_filter(all_files)
        reg_files, vip_files = self.structure_filter(reg_files, vip_files)
        return reg_files + vip_files

    def reset_filter_setting(self, arch_file: ArchiveMember, out_path_generator=None):
        assert isinstance(arch_file, ArchiveMember)
        arch_file, out_path_generator = self.structure_filter.reset_filter_setting(arch_file, out_path_generator)
        return arch_file, out_path_generator
