from json_streaming import make_parser
from make_big_json import make_json
from tests import gen_from_str
import unittest

class TestLongString(unittest.TestCase):

  def test_long(self):
    big_json = make_json()
    make_parser(big_json).parse()


class TestLongStream(unittest.TestCase):

  def test_long(self):
    big_json = make_json()
    make_parser(gen_from_str(big_json)).parse()


if __name__ == '__main__':
  unittest.main()
