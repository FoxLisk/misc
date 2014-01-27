class JsonStreamer(object):
  WHITESPACE = set(' \t\n')
  DIGITS = set('0123456789')

  def __init__(self):
    self.pos = 0
    self._skip_whitespace()

  def _expect(self, char):
    if self.current != char:
      raise Exception("Invalid JSON: found `%s`, expected %s at position %d"
          % (self.current, char, self.pos))
    self.next()

  def _expect_string(self, string):
    for c in string:
      self._expect(c)

  def _skip_whitespace(self):
    while self.current in self.WHITESPACE:
      self.next()

  def pchars(self):
    S_REG = 1
    S_ESCAPE = 2
    S_UNICODE = 3

    state = S_REG
    unicode_chars = ''

    while not self.done:
      c = self.current
      if state == S_REG:
        if c == '\\':
          state = S_ESCAPE
        elif c == '"':
          return
        self.next()
      elif state == S_ESCAPE:
        if c == 'u':
          state = S_UNICODE
        elif c in set('"\\/bfnrt'):
          state = S_REG
        else:
          raise Exception('Invalid escape sequence: `\\%s' % c)
        self.next()
      elif state == S_UNICODE:
        if c in set('0123456789abcdeABCDE'):
          unicode_chars += c
          if len(unicode_chars) == 4:
            state = S_REG
        else:
          raise Exception('Invalid unicode escape sequence: `\\u%s`' % unicode_chars)
        self.next()

  def pstring(self):
    #TODO correct this
    self._expect('"')
    if self.current != '"':
      self.pchars()
    self._expect('"')

  def pint(self):
    '''digit
    digit1-9 digits
    - digit
    - digit1-9 digits'''

    starts_with_zero = False
    if self.current == '-':
      self._expect('-')

    if self.current == '0':
      starts_with_zero = True
      self.next()

    if self.current not in self.DIGITS and not starts_with_zero:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))

    while self.current in self.DIGITS:
      if starts_with_zero:
        raise Exception('Invalid JSON: Non-fractional numbers must not begin with leading zeros (position %d)' % self.pos)
      self.next()

  def pfrac(self):
    self._expect('.')
    if self.current not in self.DIGITS:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))
    while self.current in self.DIGITS:
      self.next()
    
  def pexp(self):
    self.next()
    if self.current in '-+':
      self.next()
    if self.current not in self.DIGITS:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))
    while self.current in self.DIGITS:
      self.next()

  def pnumber(self):
    self.pint()
    if self.current == '.':
      self.pfrac()
    if self.current in set('eE'):
      self.pexp()

  def pelements(self):
    self.pvalue()
    self._skip_whitespace()
    while self.current == ',':
      self._expect(',')
      self._skip_whitespace()
      self.pvalue()
      self._skip_whitespace()
    self._skip_whitespace()

  def parray(self):
    self._expect('[')
    self._skip_whitespace()
    if self.current != ']':
      self.pelements()
    self._skip_whitespace()
    self._expect(']')

  def pconstant(self):
    if self.current == 't':
      self._expect_string('true')
    elif self.current == 'f':
      self._expect_string('false')
    else:
      self._expect_string('null')

  def pvalue(self):
    if self.current == '"':
      self.pstring()
    elif self.current in self.DIGITS:
      self.pnumber()
    elif self.current == '{':
      self.pobject()
    elif self.current == '[':
      self.parray()
    else:
      self.pconstant()
      

  def ppair(self):
    self._skip_whitespace()
    self.pstring()
    self._skip_whitespace()
    self._expect(':')
    self._skip_whitespace()
    self.pvalue()

  def pmembers(self):
    '''expects { to be eaten; doesnot eat }'''
    self.ppair()
    self._skip_whitespace()
    while self.current == ',':
      self._expect(',')
      self.ppair()
      self._skip_whitespace()

  def pobject(self):
    self._expect('{')
    if self.current != '}':
      self.pmembers()
    self._expect('}')

  def parse(self):
    self.pobject()


class StringJsonStreamer(JsonStreamer):
  def __init__(self, content):
    self.content = content
    self.pos = 0
    self.max = len(content)
    self._skip_whitespace()
    super(StringJsonStreamer, self).__init__()

  @property
  def done(self):
    return self.pos >= self.max

  @property
  def current(self):
    if self.done:
      return ''
    return self.content[self.pos]

  def next(self):
    self.pos += 1


class IterableJsonStreamer(JsonStreamer):
  def __init__(self, content):
    self.done = False
    self.content = content
    self._skip_whitespace()
    super(StringJsonStreamer, self).__init__()

  @property
  def current(self):
    if self.done:
      return ''
    return self.content[self.pos]

  def next(self):
    try:
      next(self.content)
      self.pos += 1
    except StopIteration:
      self.done = True


def make_parser(content):
  if isinstance(content, basestring):
    return StringJsonStreamer(content)
  elif hasattr(content, '__iter__'):
    return IterableJsonStreamer(content)
  else:
    raise Exception("I can only make a parser out of a string or an iterable")
