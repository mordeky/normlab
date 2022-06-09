from pathlib import Path
from typing import Sequence

from myarchive.archive_member import ArchiveMember
from myfilter.file_filter import FileFilter
from myfilter.tree_node import TreeNode


class StructureFilter:
    def __init__(self, reg_out_path: Path, vip_out_path: Path, out_path_generator):
        """
        reg_files: regular files
        vip_files: very important files
        """
        self.reg_out_path = reg_out_path.parent
        self.reg_out_folder = Path(reg_out_path.stem)

        self.vip_out_path = vip_out_path
        self.vip_filename = ''

        self.out_path_generator = out_path_generator
        self.tree_root = TreeNode()

        self.reg_files: Sequence[ArchiveMember] = []
        # self.vip_files: Sequence[ArchiveMember] = []

    def __call__(self, reg_files: Sequence[ArchiveMember], vip_files: Sequence[ArchiveMember]):
        self.reg_files: Sequence[ArchiveMember] = reg_files
        self._map_reg_files_to_tree()
        self.tree_root.prune_tree_from_top_to_down()
        self._map_tree_to_file_system()
        self._map_vip_files_to_file_system(vip_files)
        self._filter_subpaths()
        return reg_files, vip_files

    def reset_filter_setting(self, arch_file: ArchiveMember, out_path_generator=None):
        if not arch_file.is_archive:
            return
        if not out_path_generator:
            out_path_generator = self.out_path_generator(arch_file.to_file)

        self.tree_root = arch_file.del_from_tree()

        kwargs = next(out_path_generator)
        out_folder = kwargs['out_folder']
        self.reg_out_folder = Path(out_folder) if out_folder else Path(arch_file.to_file.stem)
        self.vip_filename = kwargs['vip_filename']

        return arch_file.to_file, out_path_generator

    def _map_reg_files_to_tree(self):
        for file in self.reg_files:
            file.tree_node = self.tree_root.add_child(self.reg_out_folder / file.file_decoded)

    def _map_tree_to_file_system(self):
        for file in self.reg_files:
            # print(file.tree_node.path[1:])
            file.set_to_file(self.reg_out_path, file.tree_node.path[1:])

    def _map_vip_files_to_file_system(self, vip_files):
        only_one_vip_file = len(vip_files) == 1
        for idx, file in enumerate(vip_files):
            suffix = f'{file.type}' if only_one_vip_file else f'-{idx + 1}{file.type}'
            file.to_file = self.vip_out_path / f'{self.vip_filename}{suffix}'

    def _filter_subpaths(self):
        self.reg_files = FileFilter.filter_reject_subpaths(self.reg_files)
