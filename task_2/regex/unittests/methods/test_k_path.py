import unittest
from typing import List
from ...classes import *
from ...methods import *


class TestKPath(unittest.TestCase):
    def check_equal(self, result_1: List[Re_Result], result_2: List[Re_Result]):
        for i in range(len(result_1)):
            self.assertEqual(result_1[i].detection, result_2[i].detection)

    def test_simple(self):
        sample_string = "lllllaaaAaaaalaalalaa"
        reg = "a*"
        atm: Automat = re_compile(reg)
        atm_k = re_k_path(atm)
        result_1 = re_findall(atm, sample_string)
        result_2 = re_findall(atm_k, sample_string)
        self.check_equal(result_1, result_2)

    def test_harder(self):
        sample_string = "123CF)456ABBBBABASADSAD1234"
        reg = "(AB*){2,3}((SAD)+)"
        atm: Automat = re_compile(reg)
        atm_k = re_k_path(atm)
        result_1 = re_findall(atm, sample_string)
        result_2 = re_findall(atm_k, sample_string)
        for i in range(len(result_1)):
            self.assertEqual(result_1[i].detection, result_2[i].detection)

