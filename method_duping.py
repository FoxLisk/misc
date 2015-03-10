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
        delattr(cls, n)
    return cls

def dupe_all(*args):
    def _dupe_cls(cls):
        for n in dir(cls):
            if n.startswith('__'):
                continue
            f = getattr(cls, n)
            if not callable(f):
                continue
            dupe(*args)(f.im_func)
        return cls
    return _dupe_cls



@method_duper
@dupe_all('a', 'b')
class FooAll(object):

    def with_both(self, arg):
        return arg

    def another(self, arg):
        return arg

@method_duper
class Foo(object):
    @dupe('x', 'y')
    def duped_this_one(self, arg):
        print arg

    def unduped(self, arg):
        print arg

f = FooAll()
print f.with_both_0() # 'a'
print f.with_both_1() # 'b'
#print f.takes_two_0() # 3
#print f.takes_two_1() # 20
print f.another_0()
print f.another_1()

f = Foo()
f.duped_this_one_0()
f.duped_this_one_1()
f.unduped('z')
