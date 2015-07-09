import unittest
from uncertainty.data_sources.sql import build_clas_value_query, build_source_query


class BuildSqlTest(unittest.TestCase):
    def test_basic_select(self):
        result = build_clas_value_query("3", "4", False)
        self.assertTrue(type(result), type(str))


class BuildSourceSql(unittest.TestCase):
    def test_type(self):
        result = build_source_query("SELECT * FROM NOTHING")
        self.assertEqual(type(result), str)

    def test_basic_select(self):
        result = build_source_query("SELECT * FROM NOTHING")
        self.assertEqual(result, "SELECT * FROM NOTHING")

    def test_with_year(self):
        result = build_source_query("SELECT * FROM NOTHING", year=2000)
        self.assertEqual(result, "SELECT * FROM NOTHING WHERE intYear = 2000")

    def test_with_region(self):
        result = build_source_query("SELECT * FROM NOTHING", region="here")
        self.assertEqual(result, "SELECT * FROM NOTHING WHERE strRegion = 'here'")

    def test_region_and_year(self):
        result = build_source_query("SELECT * FROM NOTHING", year=2000, region="here")
        self.assertEqual(result, "SELECT * FROM NOTHING WHERE strRegion = 'here' AND intYear = 2000")

    def test_region_bad_type(self):
        result = build_source_query("SELECT * FROM NOTHING", region=22)
        self.assertEqual(result, "SELECT * FROM NOTHING WHERE strRegion = '22'")
