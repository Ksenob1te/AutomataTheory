import unittest
from typing import List
from ...classes import *
from ...methods import *

class TestInverse(unittest.TestCase):
    def test_inverse(self):
        sample_string = "aaaaaare you crazy ****"
        reg = "(a{0,2})are (you|they) crazy (%*+|%+{1,3})"
        reg_inv = inverse_re(reg)
        result: List[Re_Result] = re_findall(reg, sample_string)
        result_inv = re_findall(reg_inv, sample_string[::-1])
        self.assertEqual(result_inv[0].detection[::-1], result[0].detection)
        # self.check_equal(result, result_inv_inv)

        sample_string = "123CF)456ABBBBABASADSAD1234"
        reg = "(!(!AS|S)AD(!SAD|$)*123)"
        reg_inv = inverse_re(reg)
        result = re_findall(reg, sample_string)
        result_inv = re_findall(reg_inv, sample_string[::-1])
        self.assertEqual(result_inv[0].detection[::-1], result[0].detection)