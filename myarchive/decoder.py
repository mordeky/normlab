import chardet


class StringDecoder:
    def __init__(self, filename, gbk_first):
        self.filename = filename
        self.gbk_first = gbk_first
        self.filename_encoded, self.encoding_set = self.get_possible_encoding()

    def get_possible_encoding(self):
        try:
            filename_encoded = self.filename.encode('cp437')
        except UnicodeEncodeError:
            return self.filename, []

        encode_info = chardet.detect(filename_encoded)
        # encode_info_2 = chardet.detect_all(filename_encoded)
        # encoding_set = [] if encode_info['language'] == 'Russian' else [encode_info['encoding']]
        gbk_conf, utf_conf = (.8, .79) if self.gbk_first else (.79, .8)
        encoding_set = {
            'gbk': gbk_conf, 'utf-8': utf_conf,
            encode_info['encoding']: encode_info['confidence']
        }

        scores = list(encoding_set.values())
        idx_set = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        encoding_set = list(encoding_set.keys())
        encoding_set = [encoding_set[i] for i in idx_set]

        return filename_encoded, encoding_set

    def __call__(self):
        for encoding in self.encoding_set:
            try:
                return self.filename_encoded.decode(encoding)
            except UnicodeDecodeError:
                continue
        return self.filename
