#!/usr/bin/python

class Trampoline(object):
    def __init__(self, gens):
        '''
        gens is of the form: { 'name' : generator expression, ... }
        '''
        self.gens = gens
        self._started = False
        self._next = None

    def set_initial_gen(self, name):
        self.current = self.gens[name]

    def add_gen(self, name, gen):
        self.gens[name] = gen

    def start(self):
        if self._started:
            raise Exception('Already started')
        gen = self.current
        name = next(gen)
        self._next = self.gens[name]


    def __iter__(self):
        return self

    def next(self):
        gen = self._next
        name = next(gen)
        self._next = self.gens[name]


    def run(self):
        self.start()
        while True:
            next(self)

def make_gen(name, yields_to):
    def foo():
        while True:
            print 'in %s' % name
            yield yields_to
    return foo()

gens = {
    'a': make_gen('a', 'b'),
    'b': make_gen('b', 'c'),
    'c': make_gen('c', 'a')
}

tramp = Trampoline(gens)
tramp.set_initial_gen('a')
tramp.run()


