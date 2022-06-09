def unzip(extractor, comp_file):
    extractor(comp_file)


def extractor_a(s):
    print(f'extractor_a does something on {s} ...')


def extractor_b(s):
    print(f'extractor_b does something on {s} ..')


def test_unzip_ex():
    print()
    file = 'xx.zip'
    if file.endswith('.zip'):
        unzip(extractor_a, file)
    elif file.endswith('.rar'):
        unzip(extractor_b, file)
