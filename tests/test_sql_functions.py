import unittest
from uncertainty.data_sources.sql import _build_query

class BuildSqlTest(unittest.TestCase):
    def test_basic_select(self):
        result = _build_query("3", "4", False)
        self.assertTrue(type(result), type(str))

