from functools import wraps
import types

def logging_func(f):
    @wraps(f)
    def _logs(self, *args, **kwargs):
        alist = ', '.join(str(a) for a in args)
        kwlist = ', '.join('%s=%s' % (k, v) for k, v in kwargs.items())
        print '%s(%s)' % (f.__name__, ', '.join([alist, kwlist]))
        return f(self, *args, **kwargs)
    return _logs


class LoggingMeta(type):
    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if type(v) in (types.MethodType, types.FunctionType, types.LambdaType):
                attrs[k] = logging_func(v)
        return super(LoggingMeta, cls).__new__(cls, name, bases, attrs)

class SecretLogging(object):
    __metaclass__ = LoggingMeta

object = SecretLogging

class Foo(object):

    def something(self, g, a=None, b=None, *args, **k):
        return {'a': a, 'b': b}


f = Foo()
ret = f.something('g', a='asdf', x=123)
