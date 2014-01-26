from json_streaming import JsonStreamer
import unittest

class TestStreamer(unittest.TestCase):

  def test_only_objects(self):
    with self.assertRaises(Exception):
      JsonStreamer('[]').parse()
    with self.assertRaises(Exception):
      JsonStreamer('100').parse()
    with self.assertRaises(Exception):
      JsonStreamer('"asd"').parse()

class TestNumbers(unittest.TestCase):

  def test_int(self):
    JsonStreamer('123').pint()
    JsonStreamer('0').pint()
    JsonStreamer('123a').pint()
    JsonStreamer('0a').pint()
    JsonStreamer('-123').pint()
    JsonStreamer('-0').pint()
    JsonStreamer('-123a').pint()
    JsonStreamer('-0a').pint()
    with self.assertRaises(Exception):
      JsonStreamer('01').pint()
    with self.assertRaises(Exception):
      JsonStreamer('-01').pint()
    with self.assertRaises(Exception):
      JsonStreamer('-').pint()

  def test_frac(self):
    JsonStreamer('.123').pfrac()
    JsonStreamer('.0123123').pfrac()
    with self.assertRaises(Exception):
      JsonStreamer('.').pfrac()

  def test_exp(self):
    JsonStreamer('e1').pexp()
    JsonStreamer('E1').pexp()
    JsonStreamer('e+1').pexp()
    JsonStreamer('E1').pexp()
    JsonStreamer('e-1').pexp()
    JsonStreamer('E-1').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('e').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('E').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('e+').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('E+').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('e-').pexp()
    with self.assertRaises(Exception):
      JsonStreamer('E-').pexp()

  def test_num(self):
    JsonStreamer('1').pnumber()
    JsonStreamer('-1').pnumber()
    JsonStreamer('1.1').pnumber()
    JsonStreamer('-1.1').pnumber()
    JsonStreamer('1234567890').pnumber()
    JsonStreamer('-1234567890').pnumber()
    JsonStreamer('1234567890.1234567890').pnumber()
    JsonStreamer('-1234567890.1234567890').pnumber()
    JsonStreamer('1e1').pnumber()
    JsonStreamer('-1e1').pnumber()
    JsonStreamer('1.1e1').pnumber()
    JsonStreamer('-1.1e1').pnumber()
    JsonStreamer('1E1').pnumber()
    JsonStreamer('-1E1').pnumber()
    JsonStreamer('1.1E1').pnumber()
    JsonStreamer('-1.1E1').pnumber()
    JsonStreamer('1e+1').pnumber()
    JsonStreamer('-1e+1').pnumber()
    JsonStreamer('1.1e+1').pnumber()
    JsonStreamer('-1.1e+1').pnumber()
    JsonStreamer('1E+1').pnumber()
    JsonStreamer('-1E+1').pnumber()
    JsonStreamer('1.1E+1').pnumber()
    JsonStreamer('-1.1E+1').pnumber()
    JsonStreamer('1e-1').pnumber()
    JsonStreamer('-1e-1').pnumber()
    JsonStreamer('1.1e-1').pnumber()
    JsonStreamer('-1.1e-1').pnumber()
    JsonStreamer('1E-1').pnumber()
    JsonStreamer('-1E-1').pnumber()
    JsonStreamer('1.1E-1').pnumber()
    JsonStreamer('-1.1E-1').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1.').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1e').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('01').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('01e').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1e').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1e-').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1e+').pnumber()
    with self.assertRaises(Exception):
      JsonStreamer('1.E').pnumber()

class TestArray(unittest.TestCase):

  def test_empty(self):
    JsonStreamer('[]').parray()

  def test_one_element(self):
    JsonStreamer('[1]').parray()
    JsonStreamer('[""]').parray()

  def test_nested(self):
    JsonStreamer('[[]]').parray()
    JsonStreamer('[[1]]').parray()

  def test_requires_open_and_close(self):
    with self.assertRaises(Exception):
      JsonStreamer('[').parray()
    with self.assertRaises(Exception):
      JsonStreamer('[1').parray()
    with self.assertRaises(Exception):
      JsonStreamer(']').parray()

  def test_multiple_elements(self):
    JsonStreamer('[1,2]').parray()
    JsonStreamer('["a","b"]').parray()
    JsonStreamer('["a",2.123]').parray()
    JsonStreamer('[[], [] ,[]]').parray()

  def test_whitespace_okay(self):
    JsonStreamer('[ ]').parray()
    JsonStreamer('[\n]\n').parray()
    JsonStreamer('[ 1 , 2, 3 ,4,5 ]').parray()

class TestObject(unittest.TestCase):

  def test_empty_object(self):
    JsonStreamer('{}').pobject()

  def test_object_one_member(self):
    JsonStreamer('{"name": "value"}').pobject()

  def test_object_multiple_members(self):
    JsonStreamer('{"name": "value", "name":"value"}').pobject()

  def test_nested(self):
    JsonStreamer('{ "name": {} ,"name": {"value": 100} }').pobject()

class TestStrings(unittest.TestCase):

  def test_empty_string(self):
    JsonStreamer('""').pstring()

  def test_simple_strings(self):
    JsonStreamer('"asdf"').pstring()
    JsonStreamer('"foo"').pstring()
    JsonStreamer('"\n\t "').pstring()
    JsonStreamer('"123"').pstring()
    JsonStreamer('"[]{}[}[[][{"').pstring()

  def test_special_characters(self):
    JsonStreamer(r'"\n"').pstring()
    JsonStreamer(r'"\""').pstring()
    JsonStreamer(r'"\\"').pstring()
    JsonStreamer(r'"\/"').pstring()
    JsonStreamer(r'"\b"').pstring()
    JsonStreamer(r'"\f"').pstring()
    JsonStreamer(r'"\r"').pstring()
    JsonStreamer(r'"\t"').pstring()

  def test_no_invalid_escapes(self):
    with self.assertRaises(Exception):
      JsonStreamer(r'"\a"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\o"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\0"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\s"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\q"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\l"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\8"').pstring()

  def test_unicode_escapes(self):
    JsonStreamer(r'"\u1234"').pstring()
    JsonStreamer(r'"\uabcd"').pstring()
    with self.assertRaises(Exception):
      JsonStreamer(r'"\uadqqag"').pstring()

class TestConstants(unittest.TestCase):
  
  def test_true(self):
    JsonStreamer('true').pconstant()
    JsonStreamer('false').pconstant()
    JsonStreamer('null').pconstant()


if __name__ == '__main__':
  unittest.main()
