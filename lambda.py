class Var(object):
    id = 0
    def __init__(self, val=None, name=None):
        self._id = Var.id
        Var.id += 1
        if val:
            self._val = val
        self.name = name or self._id

    def get_val(self):
        if hasattr(self._val, 'val'):
            return self._val.val
        else:
            return self._val

    def set_val(self, new_val):
        self._val = new_val

    @property
    def has_val(self):
        return hasattr(self, '_val')

    val = property(get_val, set_val)

    def __str__(self):
        return '%s %s' % (self.name, self.val if hasattr(self, '_val') else '')

class Value(object):
    def __init__(self, val):
        self.val = val

    def __str__(self):
      return 'Value(%s)' % self.val

    @property
    def has_val(self):
      return True

_locals = locals()
_locals.update({v: Var(name=v) for v in list('abcdefghijklmnopqrstuvwxyz')})

class Fun(Var):
    def __init__(self, func, args=(), name=None):
        self.func = func
        self.args = args
        self.name = name

    def __call__(self, arg):
        if not isinstance(arg, Value) and not isinstance(arg, Var):
            arg = Value(arg)
        return Fun(self.func, self.args + (arg,), self.name)

    def _exec(self):
        funcargs = []
        for arg in self.args:
          if not arg.has_val:
            raise Exception("Tried to execute %s with unbound variable %s" % (self, arg))
          else:
            funcargs.append(arg.val)
        return self.func(*funcargs)
    
    def __str__(self):
      return '%s(%s)' % (self.name, ' '.join(map(str, self.args)))

plus = Fun(lambda *ints: sum(ints), name='plus')

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
        s = 'Lambda(%s)' % ' '.join(map(str, self.args)).rstrip()
        s += '\n  %s(%s)' % (self.fun, self.fargs)
        s += '\n  executing with vals: %s' % ' '.join(map(str, self.vals))
        return s

    def _exec(self):
        for val, var in zip(self.vals, self.args):
            var.val = val
        for arg in self.vals[len(self.args):]:
          self.fun = self.fun(arg)
        return self.fun._exec()

def _define(name, val):
  global _locals
  if not isinstance(val, Value):
    val = Value(val)
  val = Var(val=val, name=name)
  _locals[name] = val

define = Fun(_define)

(define ('something') (3))._exec()

assert (plus (something) (5))._exec() == 8


assert (plus (1) (2))._exec() == 3

assert (
        (Lambda (x) (y) (plus (x) (y) (1))))(1)(2)._exec() == 4
assert (
((Lambda (x)
   (plus (x) (1)))
   (5)))._exec() == 6

myl = (Lambda (z) (plus (z) (10)))(5)

myl = (Lambda (a)
      (Lambda (b)
        (plus (b) (a))
  ))
assert myl(5)(10)._exec() == 15
