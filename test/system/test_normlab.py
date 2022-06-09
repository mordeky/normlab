import pytest
from normlab import NormLab, NormFile
from paths import mid_exam_path
from utils.path_structure import get_path_structure
from utils.path_structure import print_path_structure


@pytest.mark.parametrize('NormClass, arch_file, expected_dir', [
    (NormFile,
     mid_exam_path / 'test-case-01/ZipOuter/Lab01-中文.zip',
     mid_exam_path / 'test-case-01/ExpectedOutput/Lab01-中文'),

    (NormFile,
     mid_exam_path / 'test-case-01/ZipInner/Lab01-中文.zip',
     mid_exam_path / 'test-case-01/ExpectedOutput/Lab01-中文'),

    (NormLab,
     mid_exam_path / 'test-case-02/Lab03-JUnit for Unit Test.zip',
     mid_exam_path / 'test-case-02/Output-Expected/Lab03-JUnit for Unit Test'),

    (NormLab,
     mid_exam_path / 'test-case-03/Lab03-JUnit for Unit Test.zip',
     mid_exam_path / 'test-case-03/Output-Expected/Lab03-JUnit for Unit Test'),

    # (NormFile,
    #  mid_exam_path / 'test-case-04/mavenproject1.zip',
    #  None)
])
def test_normlab(NormClass, arch_file, expected_dir):
    # argv = '--use-shortname --utf-first'
    argv = '--use-shortname --gbk-first'
    main = NormClass(arch_file, user_args=argv)
    main()

    output_structure = get_path_structure(main.out_path / arch_file.stem)
    print_path_structure(output_structure)

    expected_structure = get_path_structure(expected_dir)
    print_path_structure(expected_structure)

    assert output_structure == expected_structure


@pytest.mark.parametrize('arch_file', [
    mid_exam_path / 'test-case-01/ZipOuter/Lab01-中文.zip',
    mid_exam_path / 'test-case-01/ZipInner/Lab01-中文.zip',
    mid_exam_path / 'test-case-02/Lab03-JUnit for Unit Test.zip',
    mid_exam_path / 'test-case-03/Lab03-JUnit for Unit Test.zip',
    mid_exam_path / 'test-case-04/mavenproject1.zip',
])
def test_clear_normlab_output(arch_file):
    import shutil
    out_dir = arch_file.parent / 'Output' / arch_file.stem
    if out_dir.exists():
        print(f'Removing {out_dir} ...')
        # out_dir.rmdir()
        # out_dir.unlink()
        shutil.rmtree(out_dir, ignore_errors=True)
        pass
