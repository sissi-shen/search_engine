# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs


from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    table = htable(4011)
    for doc_id in range(len(files)):
        doc_txt = get_text(files[doc_id])
        doc_words = words(doc_txt)

        for word in doc_words:
            index_values = htable_get(table, word)

            if index_values is None:
                index_values = set()
                htable_put(table, word, index_values)

            index_values.add(doc_id)

    return table


def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    matching_ids = set()
    # print(htable_get(index, "hawaii"))
    values = htable_get(index, terms[0])
    if values is not None:
        matching_ids.update(values)

    for term in terms[1:]:
        ids = htable_get(index, term)
        if ids is not None:
            matching_ids.intersection_update(ids)

    file_names = [files[doc_id] for doc_id in matching_ids]

    return file_names





