class JsonStreamer(object):
  WHITESPACE = set(' \t\n')
  DIGITS = set('0123456789')
  def __init__(self, content):
    self.content = content
    self.pos = 0
    self.max = len(content)
    self._skip_whitespace()

  @property
  def done(self):
    return self.pos >= self.max

  @property
  def current(self):
    if self.done:
      return ''
    return self.content[self.pos]

  def _expect(self, char):
    if self.current != char:
      raise Exception("Invalid JSON: found `%s`, expected %s at position %d"
          % (self.current, char, self.pos))
    self.pos += 1

  def _skip_whitespace(self):
    while self.content[self.pos] in self.WHITESPACE:
      self.pos += 1

  def pstring(self):
    #TODO correct this
    self._expect('"')
    while self.current != '"':
      self.pos += 1
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
      self.pos += 1

    if self.current not in self.DIGITS and not starts_with_zero:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))

    while self.current in self.DIGITS:
      if starts_with_zero:
        raise Exception('Invalid JSON: Non-fractional numbers must not begin with leading zeros (position %d)' % self.pos)
      self.pos += 1

  def pfrac(self):
    self._expect('.')
    if self.current not in self.DIGITS:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))
    while self.current in self.DIGITS:
      self.pos += 1
    
  def pexp(self):
    self.pos += 1 # assuming pnumber only called us if we've got e or E
    if self.current in '-+':
      self.pos += 1
    if self.current not in self.DIGITS:
      raise Exception('Invalid JSON: Found `%s`, expected digit at position %d' % (self.current, self.pos))
    while self.current in self.DIGITS:
      self.pos += 1

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
