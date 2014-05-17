class Var(object):
    id = 0
    def __init__(self, val=None):
        self._id = Var.id
        Var.id += 1
        if val:
            self._val = val

    def get_val(self):
        if hasattr(self._val, 'val'):
            return self._val.val
        else:
            return self._val

    def set_val(self, new_val):
        self._val = new_val

    val = property(get_val, set_val)

class Value(object):
    def __init__(self, val):
        self.val = val

locals().update({v: Var() for v in list('abcdefghijklmnopqrstuvwxyz')})

class Fun(Var):
    def __init__(self, func, args=()):
        self.func = func
        self.args = args

    def __call__(self, arg):
        if not isinstance(arg, Value) and not isinstance(arg, Var):
            arg = Value(arg)
        return Fun(self.func, self.args + (arg,))

    def _exec(self):
        return self.func(*[arg.val for arg in self.args])

def _sum(*args):
    tot = 0
    for arg in args:
        tot += arg
    return tot
plus = Fun(_sum)

class Lambda(Fun):
    def __init__(self, arg=None, args=None, fun=None, fargs=None, vals=None):
        # not calling super here. too different.
        self.args = args or []
        self.fun = fun
        self.fargs = fargs or []
        self.vals = vals or []
        if arg is None:
            return

        if not self.fun:
            new_args = self.args
        elif hasattr(arg, 'val'):
            new_args = self.vals
        else:
            new_args = self.fargs

        new_args.append(arg)

    def __call__(self, fun_or_var):
        if isinstance(fun_or_var, Fun):
            return Lambda(None, self.args, fun_or_var, self.fargs, self.vals)
        elif isinstance(fun_or_var, Var):
            if not self.fun:
                return Lambda(fun_or_var, self.args, self.fun, self.fargs, self.vals)
            else:
                return Lambda(None, self.args, fun_or_var, self.fargs, self.vals)
        elif hasattr(fun_or_var, 'val'):
            # this is either a value or a bound variable
            return Lambda(fun_or_var, self.args, self.fun, self.fargs, self.vals)
        else:
            var = Value(fun_or_var)
            return self(var)

    def __str__(self):
        return 'Lambda:\n%s\n%s\n%s\n%s' % (self.args, self.fun, self.fargs, self.vals)

    def _exec(self):
        for val, var in zip(self.vals, self.args):
            var.val = val
        return self.fun._exec()

assert (plus (1) (2))._exec() == 3

assert (
        (Lambda (x) (y)
            (plus (x) (y) (1)))
       )(1)(2)._exec() == 4
'''
X = (BEGIN
        (SET (F) (LAMBDA (X)
            (IF (EQ (X) (1))
                (1)
                (MUL (X) (F (SUB (X) (1)))))))
     
        (QUOTE (F (4)) (42)))
'''
