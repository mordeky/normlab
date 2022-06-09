from pathlib import Path


def get_path_structure(path: Path, pre_path: Path = Path('.')) -> set:
    file_set = set()
    for p in path.iterdir():
        if p.name.endswith('.DS_Store'):
            continue

        if p.is_file():
            file_set.add((pre_path / p.name).as_posix())
            continue

        new_folder = pre_path / p.name
        file_set.add(new_folder.as_posix())
        sub_file_set = get_path_structure(p, new_folder)
        file_set = file_set.union(sub_file_set)
    return file_set


def print_path_structure(path_structure: set):
    for e in path_structure:
        print(e)
