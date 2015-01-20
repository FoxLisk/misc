def items_in_only_one_list(l):
    '''given a list of lists (or, really, an iterable of iterables),
    return every element that appears in exactly one list.
    As a list, of course :)'''
    return [x for sl in l for x in sl if not any(x in _sl for _sl in l if _sl != sl)]

class Summer(object):
    def __init__(self):
        self.sum = 0

    def evilmap(self, other_arg):
        import pudb; pu.db
        self.sum += other_arg

def columnar(d, *columns):
    return (d[c] for c in columns)

a, c = columnar({'a': 1, 'b':2, 'c':3}, 'a', 'c')
print a, c
