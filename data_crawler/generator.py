
import re

DELIMITERS = '!@#$%^&*()_+-=\"\'[]\{\}|\\/,.; '

def split_delimiter(tag):
    # http://code.activestate.com/recipes/577616-split-strings-w-multiple-separators/
    stack = [tag]
    for char in list(DELIMITERS):
        pieces = []
        for substr in stack:
            tmp = [x for x in substr.split(char) if x]
            pieces.extend(tmp)
        stack = pieces
    return stack


def tags_generator_from_text(str):
    return [x.lower() for x in re.sub("[^a-zA-Z0-9]", " ",  str).split()]

def tags_generator(tags):
    return [x.lower() for x in split_delimiter(" ".join(tags))]

def tags_finalize(tags):
    results = []
    for tag in tags:
        if len(tag) > 1:
            results.append(tag)
    return list(set(results))
