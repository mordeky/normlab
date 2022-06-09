from dataclasses import dataclass
from pathlib import Path


@dataclass
class Student:
    id: str
    name: str

    path_pre: str
    lab_path: Path
    # code_folder: str = id + '-' + name
    # lab_report_name: str = code_folder

    @property
    def code_folder(self):
        path_pre = self.path_pre + '-' if self.path_pre else ''
        return path_pre + self.id + '-' + self.name

    @property
    def lab_report_name(self):
        return self.code_folder

    @property
    def code_path(self):
        return self.lab_path / self.code_folder
