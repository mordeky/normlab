import difflib


def string_similar(s1: str, s2: str):
    return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).quick_ratio()
