from functools import wraps
from collections import defaultdict


def return_enumerable(f):
    @wraps(f)
    def enum(*args, **kwargs):
        return IEnumerable(f(*args, **kwargs))
    return enum


class IEnumerable(object):
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        if not hasattr(iterable, '__iter__'):
            raise Exception('Must be initiated with an iterable')
        self.coll = iterable

    def __iter__(self):
        return self.coll.__iter__()

    @return_enumerable
    def where(self, filter):
        for el in self:
            if filter(el):
                yield el

    @return_enumerable
    def select(self, map):
        for el in self:
            yield map(el)

    def first(self):
        try:
            for el in self:
                return el
        except StopIteration:
            raise Exception('Empty enumerable')

    @return_enumerable
    def concat(self, *others):
        for el in self:
            yield el
        for other in others:
            for el in other:
                yield el

    @return_enumerable
    def distinct(self):
        seen = set()
        for el in self:
            if el not in seen:
                seen.add(el)
                yield el

    def element_at(self, idx):
        count = 0
        try:
            for el in self:
                count += 1
                if count == idx:
                    return count
        except StopIteration:
            raise Exception("Enumerable too short")

    @return_enumerable
    def without(self, other):
        for el in self:
            if el not in other:
                yield el

    @return_enumerable
    def group_by(self, func):
        groups = defaultdict(list)
        for el in self:
            group = func(el)
            groups[func(el)].append(el)
        for k, els in groups.items():
            yield IGrouping(k, els)

    @return_enumerable
    def intersect(self, other):
        seen = set()
        for el in self:
            if el in seen: continue
            if el in other:
                seen.add(el)
                yield el

    @return_enumerable
    def union(self, other):
        seen = set()
        for el in self:
            if el not in seen:
                yield el
                seen.add(el)
        for el in other:
            if el not in seen:
                yield el
                seen.add(el)

    @return_enumerable
    def join(outer, inner, outer_key, inner_key, result):
        inner_map = defaultdict(list)
        for el in inner:
           inner_map[inner_key(el)].append(el)
        for oel in outer:
            ok = outer_key(oel)
            if ok in inner_map:
                for iel in inner_map[ok]:
                    yield result(oel, iel)

    @return_enumerable
    def select_many(self, func):
        for el in self:
            for e2 in func(el):
                yield e2

    def single(self):
        found = False
        res = None
        for el in self:
            found = True
            if res is None:
                res = el
            else:
                raise Exception("Non-singular enumerable")
        if not found:
            raise Exception("Empty enumerable")
        return res

    @return_enumerable
    def skip(self, num):
        for el in self:
            if num > 0:
                num -= 1
            else:
                yield el

    @return_enumerable
    def skip_while(self, func):
        maybe_skip = True
        for el in self:
            if maybe_skip:
                if func(el):
                    continue
                else:
                    maybe_skip = False
                    yield el
            else:
                yield el

    @return_enumerable
    def take(self, num):
        for el in self:
            if num > 0:
                yield el
                num -= 1
            else:
                break

    @return_enumerable
    def take_while(self, func):
        for el in self:
            if func(el):
                yield el
            else:
                break

    def to_dict(self, key_func, val_func=lambda x: x):
        return { key_func(el): val_func(el) for el in self }


class IGrouping(IEnumerable):
    def __init__(self, key, elements):
        self.key = key
        super(IGrouping, self).__init__(elements)

def erange(min, max=None):
    if max is None:
        max = min
        min = 0
    return IEnumerable(range(min, max))

stuff = IEnumerable([
    (1, 'hello'),
    (2, 'world')])

print zip(erange(10), (range(5,25)))
