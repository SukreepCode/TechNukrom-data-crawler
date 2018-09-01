from data_crawler.generator import *

def compare_list(a, b):
    if len(a) != len(b):
        return False
    for i, value in enumerate(a):
        if a[i] != b[i]:
            return False
    return True

def test_split_delimiter():
    assert compare_list(split_delimiter('cat dog'), ['cat','dog'])
    assert compare_list(split_delimiter(' cat dog '), ['cat','dog'])
    assert compare_list(split_delimiter('cat*dog'), ['cat','dog'])
    assert compare_list(split_delimiter('+cat dog+'), ['cat','dog'])
    assert compare_list(split_delimiter('&cat^dog\\'), ['cat','dog'])
    assert compare_list(split_delimiter('*&(#* &%@ !& @$(cat *(#dog'), ['cat','dog'])

def test_tags_generator():
    actual = tags_generator(['cat DoG','MO'])
    expect = ['cat','dog','mo']
    assert compare_list(actual, expect)

def test_tags_generator_from_text():
    assert compare_list(tags_generator_from_text('test ทดสอบ Wer, ewioj'),
        ['test','wer','ewioj'])
