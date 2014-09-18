def items_in_only_one_list(l):
    '''given a list of lists (or, really, an iterable of iterables),
    return every element that appears in exactly one list.
    As a list, of course :)'''
    return [x for sl in l for x in sl if not any(x in _sl for _sl in l if _sl != sl)]
