import chardet

from myarchive.decoder import StringDecoder


def decode_filename(file_name):
    filename_encoded = file_name.encode('cp437')
    encode_info = chardet.detect(filename_encoded)
    encoding = encode_info['encoding'] if encode_info['confidence'] > .8 else 'GBK'
    return filename_encoded.decode(encoding)


def test_decode():
    import zipfile
    from paths import mid_exam_path
    # archive = mid_exam_path / 'test-case-04/RAR/RAR文档.zip'
    archive = 'E:/Work/Job/Teaching/SoftwareDesign/Exam/2022-期中考试/软件设计-2022-2021-2022 第二学期 期中考试(pdf)/202003340220-徐瑕.zip'
    # archive = 'E:/Work/Job/Teaching/SoftwareDesign/Exam/2022-期中考试/软件设计-2022-2021-2022 第二学期 期中考试(pdf)/202003340309-黄温和.zip'
    print()
    with zipfile.ZipFile(archive) as zip_file:
        file_names = zip_file.namelist()
        for name in file_names:
            name_decoded = StringDecoder(name)()
            print(name, '-->', name_decoded)
