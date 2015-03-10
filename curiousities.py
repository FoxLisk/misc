def items_in_only_one_list(l):
    '''given a list of lists (or, really, an iterable of iterables),
    return every element that appears in exactly one list.
    As a list, of course :)'''
    return [x for sl in l for x in sl if not any(x in _sl for _sl in l if _sl != sl)]

class Summer(object):
    def __init__(self):
        self.sum = 0

    def evilmap(self, other_arg):
        self.sum += other_arg

def columnar(d, *columns):
    '''
    extracts each column in columns from d.

    useful for like:

    [columnar(my_dict, 'foo', 'bar') for my_dict in list_of_dicts]
    '''
    return (d[c] for c in columns)

class Increment(object):
    '''
    i = Increment()
    print i.val # 0
    ++i
    print i.val # 1
    '''
    def __init__(self, val=0):
        self.val = val
        self._inc = False

    def __pos__(self):
        if self._inc:
            self.val += 1
        self._inc = not self._inc
        return self

    def __getattr__(self, name):
        return getattr(self.val, name)
