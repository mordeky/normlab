import re
from pathlib import Path
from typing import Sequence
from myarchive.archive_member import ArchiveMember

from data.file_configs import reject_file_types, reject_files
from data.file_configs import reject_subpaths, reject_folders, reject_structured_folders, vip_file_types


class File:
    def __init__(self, full_path, vip_path=None, reject_paths=None):
        self.path = full_path
        self.folder_seq = full_path.split('/')
        full_path = Path(full_path)
        self.name = full_path.name
        self.suffix = full_path.suffix
        self.vip_path = vip_path
        self.reject_paths = reject_paths

    def is_reject_file(self):
        for reject_file in reject_files:
            if re.match(reject_file, self.name):
                return True

    def has_reject_folder(self):
        for folder in reject_folders:
            if folder in self.folder_seq:
                return True

    def has_reject_subpath(self):
        for subpath in reject_subpaths:
            if subpath in self.path:
                return True

    def has_reject_path(self):
        for reject_path in self.reject_paths:
            if self.path.startswith(reject_path):
                return True

    @property
    def should_be_rejected(self):
        if self.path.endswith('/'):  # a folder
            return True
        if self.suffix in reject_file_types:
            return True
        if self.is_reject_file():
            return True
        if self.has_reject_subpath():
            return True
        if self.has_reject_folder():
            return True
        if self.has_reject_path():
            return True
        return False

    @property
    def is_vip(self):
        return self.vip_path is not None and self.suffix in vip_file_types

    def in_conditional_neglect_list(self, all_file_list):
        for reject_folder, ref_folder in reject_structured_folders:
            if reject_folder in self.folder_seq:
                idx = self.folder_seq.index(reject_folder)
                ref_path = '/'.join(self.folder_seq[:idx] + [ref_folder])
                for file in all_file_list:
                    if file.file_decoded.startswith(ref_path):
                        # It's used to improve efficiency.
                        #   Next time, when the same structured rejected folder appears again,
                        #   we can directly reject it by using the self.reject_paths, see self.has_reject_path().
                        self.reject_paths.add('/'.join(self.folder_seq[:idx + 1]))
                        return True
        return False


class FileFilter:
    def __init__(self, vip_path: Path = None):
        self.vip_path = vip_path
        self.reject_paths = set()

    def __call__(self, all_files: Sequence[ArchiveMember]):
        reg_files, vip_files = [], []
        for file in all_files:
            cur_file = File(file.file_decoded, self.vip_path, self.reject_paths)
            if cur_file.should_be_rejected:
                continue
            if cur_file.in_conditional_neglect_list(all_files):
                continue
            if cur_file.is_vip:
                vip_files.append(file)
                continue
            reg_files.append(file)
        return reg_files, vip_files

    @staticmethod
    def filter_reject_subpaths(all_files: Sequence[ArchiveMember]):
        reg_files = []
        for file in all_files:
            to_file = File(file.to_file.as_posix())
            if to_file.has_reject_subpath():
                continue
            reg_files.append(file)
        return reg_files
