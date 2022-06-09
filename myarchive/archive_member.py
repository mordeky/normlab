import shutil
import warnings
from pathlib import Path

from myarchive.decoder import StringDecoder


class ArchiveMember:
    def __init__(self, filename: str, gbk_first=True):
        self.from_file = filename
        self.file_decoded = StringDecoder(filename, gbk_first)()
        # self.real_name = Path(self.file_decoded).name
        self.to_file = None
        self.tree_node = None

        p = filename.rfind('.')
        # self.type = os.path.splitext(self.path)[-1]
        self.type = filename[p:]

    def del_from_tree(self):
        parent = self.tree_node.parent
        parent.del_child(self.tree_node.name)
        return parent

    def set_to_file(self, root_path: Path, pruned_file_path: str):
        # pruned_file_path = pruned_file_path.lstrip(root_path.name).lstrip('/')
        self.to_file = root_path / self.format_out_path(pruned_file_path)

    @staticmethod
    def format_out_path(path: str):
        return path.replace(':', '_')

    @property
    def is_archive(self):
        return self.type in ['.zip', '.rar']

    def extract(self, arc_open):
        print('Extracting: ', self.to_file, ' ...')
        if not self.to_file.parent.exists():
            self.to_file.parent.mkdir(parents=True)
        try:
            with arc_open(self.from_file, 'r') as from_file:  # 打开原文件
                with open(self.to_file, 'wb') as to_file:  # 创建并打开新文件
                    shutil.copyfileobj(from_file, to_file)  # 将原文件内容复制到新文件
        except FileNotFoundError:
            warnings.warn(f'\n{self.to_file} cannot be created!')
            print('')
