from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    index_dict = defaultdict()

    for doc_id in range(len(files)):
        doc_txt = get_text(files[doc_id])
        doc_words = words(doc_txt)

        for word in doc_words:
            if word not in index_dict:
                index_dict[word] = {doc_id}
            else:
                index_dict[word].add(doc_id)

    return index_dict


def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    matching_ids = set()

    if terms[0] in index.keys():
        matching_ids = index[terms[0]].copy()

    for term in terms[1:]:
        if term in index.keys():
            matching_ids.intersection_update(index[term])

    file_names = [files[doc_id] for doc_id in matching_ids]

    return file_names




