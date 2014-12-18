from functools import wraps
from inspect import isfunction
def method_memoizer(f):
    cache = {}
    def to_key(*args, **kwargs):
        return tuple(args) + tuple((k, kwargs[k]) for k in sorted(kwargs.keys()))
    @wraps(f)
    def memoized(self, *args, **kwargs):
        key = to_key(*args, **kwargs)
        if key in cache:
            print 'hit'
            return cache[key]
        print 'miss'
        val = f(self, *args, **kwargs)
        cache[key] = val
        return val
    return memoized

class Memoized(type):
    def __new__(cls, name, bases, attrs):

        if name.startswith('None'):
            return None

        newattrs = {}
        for name, val in attrs.iteritems():
            if isfunction(val):
                newattrs[name] = method_memoizer(val)
            else:
                newattrs[name] = val

        return super(Memoized, cls).__new__(cls, name, bases, newattrs)

class C(object):
    __metaclass__ = Memoized

    def foo(self, a, b=-1):
        return (a, b)

    @classmethod
    def cfoo(cls, x):
        return (x,)

    @property
    def pfoo(self):
        return (1,)

    @staticmethod
    def sfoo(cls, x):
        return (-x, )

c = C()
c.foo(1,2)
c.foo(1,2)
c.foo(3,4)
