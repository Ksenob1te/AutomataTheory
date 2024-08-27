import unittest
from typing import List
from ...classes import *
from ...methods import *


class TestDifference(unittest.TestCase):
    def test_check_difference(self):
        # Test the method check_product
        a = re_compile("(a|b|c)")
        b = re_compile("(b|c)")
        res = difference_dfa(a, b)
        result = re_findall(res, "b")
        self.assertEqual(len(result), 0)
        result = re_findall(res, "c")
        self.assertEqual(len(result), 0)
        result = re_findall(res, "a")
        self.assertEqual(len(result), 1)

        a = "k|abc"
        b = "abc*"
        res = difference_dfa(a, b)
        result = re_findall(res, "kabc")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].detection, "k")
