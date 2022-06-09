from paths import data_path, target_path


def test_unzip():
    """
    ref: https://docs.python.org/3/library/zipfile.html

    You should first download labwork data:
      https://favour-link.feishu.cn/file/boxcnBrnmooS3OMCWjjiIjuZukb
    """

    import zipfile
    path_to_zip_file = data_path / 'Lab03-JUnit for Unit Test.zip'

    # lab_home = target_path / 'Lab03-JUnit for Unit Test'

    lab_name = path_to_zip_file.path.strip('.zip')
    lab_home = target_path / lab_name

    if not lab_home.exists():
        lab_home.mkdir(parents=True)

    with zipfile.ZipFile(path_to_zip_file, 'r') as my_zipfile:
        my_zipfile.extractall(lab_home)

    return


def test_traverse_files():
    path = target_path / 'Lab03-JUnit for Unit Test'
    for file in path.iterdir():
        print(file.path)
    pass


def test_rename_file():
    old_folder = 'L201926630134-HOMWEYETSUROMARTIN'
    new_folder = 'L201926630134-GoodGood'
    des_path = target_path / 'Lab03-JUnit for Unit Test'

    path = des_path / old_folder
    if not path.exists():
        path.mkdir(parents=True)

    path = path.rename(des_path / new_folder)
    assert path.path == new_folder

    path = path.rename(des_path / old_folder)
    assert path.path == old_folder


def test_read_csv():
    """
    ref: https://docs.python.org/3/library/csv.html

    You need first download student list:
      https://favour-link.feishu.cn/sheets/shtcnMo8kQ4kNnjxv2dlDWzpjqc
    """

    student_file = data_path / 'International Student List.csv'

    import csv
    with open(student_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            stu_id, full_name, short_name = row
            print(stu_id, full_name, short_name)
            pass
