# -*- coding: utf8 -*-
from json_streaming import make_parser
import unittest

def gen_from_str(s):
  def gen():
    for c in s:
      yield c
  return gen()

class TestStreamer(unittest.TestCase):

  def test_only_objects(self):
    with self.assertRaises(Exception):
      make_parser('[]').parse()
    with self.assertRaises(Exception):
      make_parser('100').parse()
    with self.assertRaises(Exception):
      make_parser('"asd"').parse()

  def test_fails_incomplete_strings(self):
    with self.assertRaises(Exception):
      make_parser('{"name').parse()

  def test_empty_string(self):
    with self.assertRaises(Exception):
      make_parser('').parse()

class TestNumbers(unittest.TestCase):

  def test_int(self):
    make_parser('123').pint()
    make_parser('0').pint()
    make_parser('123a').pint()
    make_parser('0a').pint()
    make_parser('-123').pint()
    make_parser('-0').pint()
    make_parser('-123a').pint()
    make_parser('-0a').pint()
    with self.assertRaises(Exception):
      make_parser('01').pint()
    with self.assertRaises(Exception):
      make_parser('-01').pint()
    with self.assertRaises(Exception):
      make_parser('-').pint()

  def test_frac(self):
    make_parser('.123').pfrac()
    make_parser('.0123123').pfrac()
    with self.assertRaises(Exception):
      make_parser('.').pfrac()

  def test_exp(self):
    make_parser('e1').pexp()
    make_parser('E1').pexp()
    make_parser('e+1').pexp()
    make_parser('E1').pexp()
    make_parser('e-1').pexp()
    make_parser('E-1').pexp()
    with self.assertRaises(Exception):
      make_parser('e').pexp()
    with self.assertRaises(Exception):
      make_parser('E').pexp()
    with self.assertRaises(Exception):
      make_parser('e+').pexp()
    with self.assertRaises(Exception):
      make_parser('E+').pexp()
    with self.assertRaises(Exception):
      make_parser('e-').pexp()
    with self.assertRaises(Exception):
      make_parser('E-').pexp()

  def test_num(self):
    make_parser('1').pnumber()
    make_parser('-1').pnumber()
    make_parser('1.1').pnumber()
    make_parser('-1.1').pnumber()
    make_parser('1234567890').pnumber()
    make_parser('-1234567890').pnumber()
    make_parser('1234567890.1234567890').pnumber()
    make_parser('-1234567890.1234567890').pnumber()
    make_parser('1e1').pnumber()
    make_parser('-1e1').pnumber()
    make_parser('1.1e1').pnumber()
    make_parser('-1.1e1').pnumber()
    make_parser('1E1').pnumber()
    make_parser('-1E1').pnumber()
    make_parser('1.1E1').pnumber()
    make_parser('-1.1E1').pnumber()
    make_parser('1e+1').pnumber()
    make_parser('-1e+1').pnumber()
    make_parser('1.1e+1').pnumber()
    make_parser('-1.1e+1').pnumber()
    make_parser('1E+1').pnumber()
    make_parser('-1E+1').pnumber()
    make_parser('1.1E+1').pnumber()
    make_parser('-1.1E+1').pnumber()
    make_parser('1e-1').pnumber()
    make_parser('-1e-1').pnumber()
    make_parser('1.1e-1').pnumber()
    make_parser('-1.1e-1').pnumber()
    make_parser('1E-1').pnumber()
    make_parser('-1E-1').pnumber()
    make_parser('1.1E-1').pnumber()
    make_parser('-1.1E-1').pnumber()
    with self.assertRaises(Exception):
      make_parser('1.').pnumber()
    with self.assertRaises(Exception):
      make_parser('1e').pnumber()
    with self.assertRaises(Exception):
      make_parser('01').pnumber()
    with self.assertRaises(Exception):
      make_parser('01e').pnumber()
    with self.assertRaises(Exception):
      make_parser('1e').pnumber()
    with self.assertRaises(Exception):
      make_parser('1e-').pnumber()
    with self.assertRaises(Exception):
      make_parser('1e+').pnumber()
    with self.assertRaises(Exception):
      make_parser('1.E').pnumber()

class TestArray(unittest.TestCase):

  def test_empty(self):
    make_parser('[]').parray()

  def test_one_element(self):
    make_parser('[1]').parray()
    make_parser('[""]').parray()

  def test_nested(self):
    make_parser('[[]]').parray()
    make_parser('[[1]]').parray()

  def test_requires_open_and_close(self):
    with self.assertRaises(Exception):
      make_parser('[').parray()
    with self.assertRaises(Exception):
      make_parser('[1').parray()
    with self.assertRaises(Exception):
      make_parser(']').parray()

  def test_multiple_elements(self):
    make_parser('[1,2]').parray()
    make_parser('["a","b"]').parray()
    make_parser('["a",2.123]').parray()
    make_parser('[[], [] ,[]]').parray()

  def test_whitespace_okay(self):
    make_parser('[ ]').parray()
    make_parser('[\n]\n').parray()
    make_parser('[ 1 , 2, 3 ,4,5 ]').parray()
    make_parser('[1, -2]').parray()

class TestObject(unittest.TestCase):

  def test_empty_object(self):
    make_parser('{}').pobject()

  def test_object_one_member(self):
    make_parser('{"name": "value"}').pobject()

  def test_object_multiple_members(self):
    make_parser('{"name": "value", "name":"value"}').pobject()

  def test_nested(self):
    make_parser('{ "name": {} ,"name": {"value": 100} }').pobject()

class TestStrings(unittest.TestCase):

  def test_empty_string(self):
    make_parser('""').pstring()

  def test_simple_strings(self):
    make_parser('"asdf"').pstring()
    make_parser('"foo"').pstring()
    make_parser('"\n\t "').pstring()
    make_parser('"123"').pstring()
    make_parser('"[]{}[}[[][{"').pstring()

  def test_some_unicode(self):
    make_parser(u'"ķ"').pstring()
    make_parser(u'ķ').pchars()

  def test_special_characters(self):
    make_parser(r'"\n"').pstring()
    make_parser(r'"\""').pstring()
    make_parser(r'"\\"').pstring()
    make_parser(r'"\/"').pstring()
    make_parser(r'"\b"').pstring()
    make_parser(r'"\f"').pstring()
    make_parser(r'"\r"').pstring()
    make_parser(r'"\t"').pstring()

  def test_no_invalid_escapes(self):
    with self.assertRaises(Exception):
      make_parser(r'"\a"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\o"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\0"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\s"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\q"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\l"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\8"').pstring()

  def test_unicode_escapes(self):
    make_parser(r'"\u1234"').pstring()
    make_parser(r'"\uabcd"').pstring()
    with self.assertRaises(Exception):
      make_parser(r'"\uadqqag"').pstring()

class TestConstants(unittest.TestCase):
  
  def test_true(self):
    make_parser('true').pconstant()
    make_parser('false').pconstant()
    make_parser('null').pconstant()

class TestStreamerGenerator(unittest.TestCase):

  def test_only_objects(self):
    with self.assertRaises(Exception):
      make_parser(gen_from_str('[]')).parse()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('100')).parse()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('"asd"')).parse()

  def test_fails_incomplete_strings(self):
    with self.assertRaises(Exception):
      make_parser(gen_from_str('{"name')).parse()

  def test_empty_string(self):
    with self.assertRaises(Exception):
      make_parser(gen_from_str('')).parse()

class TestNumbersGenerator(unittest.TestCase):

  def test_int(self):
    make_parser(gen_from_str('123')).pint()
    make_parser(gen_from_str('0')).pint()
    make_parser(gen_from_str('123a')).pint()
    make_parser(gen_from_str('0a')).pint()
    make_parser(gen_from_str('-123')).pint()
    make_parser(gen_from_str('-0')).pint()
    make_parser(gen_from_str('-123a')).pint()
    make_parser(gen_from_str('-0a')).pint()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('01')).pint()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('-01')).pint()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('-')).pint()

  def test_frac(self):
    make_parser(gen_from_str('.123')).pfrac()
    make_parser(gen_from_str('.0123123')).pfrac()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('.')).pfrac()

  def test_exp(self):
    make_parser(gen_from_str('e1')).pexp()
    make_parser(gen_from_str('E1')).pexp()
    make_parser(gen_from_str('e+1')).pexp()
    make_parser(gen_from_str('E1')).pexp()
    make_parser(gen_from_str('e-1')).pexp()
    make_parser(gen_from_str('E-1')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('e')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('E')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('e+')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('E+')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('e-')).pexp()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('E-')).pexp()

  def test_num(self):
    make_parser(gen_from_str('1')).pnumber()
    make_parser(gen_from_str('-1')).pnumber()
    make_parser(gen_from_str('1.1')).pnumber()
    make_parser(gen_from_str('-1.1')).pnumber()
    make_parser(gen_from_str('1234567890')).pnumber()
    make_parser(gen_from_str('-1234567890')).pnumber()
    make_parser(gen_from_str('1234567890.1234567890')).pnumber()
    make_parser(gen_from_str('-1234567890.1234567890')).pnumber()
    make_parser(gen_from_str('1e1')).pnumber()
    make_parser(gen_from_str('-1e1')).pnumber()
    make_parser(gen_from_str('1.1e1')).pnumber()
    make_parser(gen_from_str('-1.1e1')).pnumber()
    make_parser(gen_from_str('1E1')).pnumber()
    make_parser(gen_from_str('-1E1')).pnumber()
    make_parser(gen_from_str('1.1E1')).pnumber()
    make_parser(gen_from_str('-1.1E1')).pnumber()
    make_parser(gen_from_str('1e+1')).pnumber()
    make_parser(gen_from_str('-1e+1')).pnumber()
    make_parser(gen_from_str('1.1e+1')).pnumber()
    make_parser(gen_from_str('-1.1e+1')).pnumber()
    make_parser(gen_from_str('1E+1')).pnumber()
    make_parser(gen_from_str('-1E+1')).pnumber()
    make_parser(gen_from_str('1.1E+1')).pnumber()
    make_parser(gen_from_str('-1.1E+1')).pnumber()
    make_parser(gen_from_str('1e-1')).pnumber()
    make_parser(gen_from_str('-1e-1')).pnumber()
    make_parser(gen_from_str('1.1e-1')).pnumber()
    make_parser(gen_from_str('-1.1e-1')).pnumber()
    make_parser(gen_from_str('1E-1')).pnumber()
    make_parser(gen_from_str('-1E-1')).pnumber()
    make_parser(gen_from_str('1.1E-1')).pnumber()
    make_parser(gen_from_str('-1.1E-1')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1.')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1e')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('01')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('01e')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1e')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1e-')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1e+')).pnumber()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('1.E')).pnumber()

class TestArrayGenerator(unittest.TestCase):

  def test_empty(self):
    make_parser(gen_from_str('[]')).parray()

  def test_one_element(self):
    make_parser(gen_from_str('[1]')).parray()
    make_parser(gen_from_str('[""]')).parray()

  def test_nested(self):
    make_parser(gen_from_str('[[]]')).parray()
    make_parser(gen_from_str('[[1]]')).parray()

  def test_requires_open_and_close(self):
    with self.assertRaises(Exception):
      make_parser(gen_from_str('[')).parray()
    with self.assertRaises(Exception):
      make_parser(gen_from_str('[1')).parray()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(']')).parray()

  def test_multiple_elements(self):
    make_parser(gen_from_str('[1,2]')).parray()
    make_parser(gen_from_str('["a","b"]')).parray()
    make_parser(gen_from_str('["a",2.123]')).parray()
    make_parser(gen_from_str('[[], [] ,[]]')).parray()

  def test_whitespace_okay(self):
    make_parser(gen_from_str('[ ]')).parray()
    make_parser(gen_from_str('[\n]\n')).parray()
    make_parser(gen_from_str('[ 1 , 2, 3 ,4,5 ]')).parray()

class TestObjectGenerator(unittest.TestCase):

  def test_empty_object(self):
    make_parser(gen_from_str('{}')).pobject()

  def test_object_one_member(self):
    make_parser(gen_from_str('{"name": "value"}')).pobject()

  def test_object_multiple_members(self):
    make_parser(gen_from_str('{"name": "value", "name":"value"}')).pobject()

  def test_nested(self):
    make_parser(gen_from_str('{ "name": {} ,"name": {"value": 100} }')).pobject()

class TestStringsGenerator(unittest.TestCase):

  def test_empty_string(self):
    make_parser(gen_from_str('""')).pstring()

  def test_simple_strings(self):
    make_parser(gen_from_str('"asdf"')).pstring()
    make_parser(gen_from_str('"foo"')).pstring()
    make_parser(gen_from_str('"\n\t "')).pstring()
    make_parser(gen_from_str('"123"')).pstring()
    make_parser(gen_from_str('"[]{}[}[[][{"')).pstring()

  def test_some_unicode(self):
    make_parser(gen_from_str(u'"ķ"')).pstring()
    make_parser(gen_from_str(u'ķ')).pchars()

  def test_special_characters(self):
    make_parser(gen_from_str(r'"\n"')).pstring()
    make_parser(gen_from_str(r'"\""')).pstring()
    make_parser(gen_from_str(r'"\\"')).pstring()
    make_parser(gen_from_str(r'"\/"')).pstring()
    make_parser(gen_from_str(r'"\b"')).pstring()
    make_parser(gen_from_str(r'"\f"')).pstring()
    make_parser(gen_from_str(r'"\r"')).pstring()
    make_parser(gen_from_str(r'"\t"')).pstring()

  def test_no_invalid_escapes(self):
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\a"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\o"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\0"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\s"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\q"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\l"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\8"')).pstring()

  def test_unicode_escapes(self):
    make_parser(gen_from_str(r'"\u1234"')).pstring()
    make_parser(gen_from_str(r'"\uabcd"')).pstring()
    with self.assertRaises(Exception):
      make_parser(gen_from_str(r'"\uadqqag"')).pstring()

class TestConstantsGenerator(unittest.TestCase):
  
  def test_true(self):
    make_parser(gen_from_str('true')).pconstant()
    make_parser(gen_from_str('false')).pconstant()
    make_parser(gen_from_str('null')).pconstant()

if __name__ == '__main__':
  unittest.main()
