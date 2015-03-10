def dupe(*dupe_args):
    def wrapper(f):
        f._dupe = True
        f._dupe_args = dupe_args
        return f
    return wrapper


def method_duper(cls):
    def maker(f, *args):
        def new_f(self):
            return f(self, *args)
        return new_f

    for n in dir(cls):
        f = getattr(cls, n)
        if not callable(f) or not getattr(f, '_dupe', False):
            continue


        for i, new_args in enumerate(f._dupe_args):
            mod = maker(f, *new_args)
            name = '%s_%d' % (n, i)
            mod.func_name = name
            setattr(cls, name, mod)
    return cls


@method_duper
class Foo(object):

    @dupe('a', 'b')
    def with_both(self, arg):
        return arg

    @dupe((1, 3), (4, 5))
    def takes_two(self, a, b):
        return a * b

    def another(self, arg):
        return arg

f = Foo()
print f.with_both_0() # 'a'
print f.with_both_1() # 'b'
print f.takes_two_0() # 3
print f.takes_two_1() # 20
print f.another('foo')
