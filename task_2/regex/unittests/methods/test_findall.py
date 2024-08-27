import unittest
from typing import List
from ...classes import *
from ...methods import *


class TestFindall(unittest.TestCase):
    def test_simple(self):
        sample_string = "lllllaaaAaaaalaalalaa"
        reg = "a*"
        result: List[Re_Result] = re_findall(reg, sample_string)
        self.assertEqual(result[0].detection, "aaa")
        self.assertEqual(result[1].detection, "aaaa")
        self.assertEqual(result[2].detection, "aa")
        self.assertEqual(result[3].detection, "a")
        self.assertEqual(result[4].detection, "aa")

        reg = "a+l"
        result: List[Re_Result] = re_findall(reg, sample_string)
        self.assertEqual(result[0].detection, "aaaal")
        self.assertEqual(result[1].detection, "aal")
        self.assertEqual(result[2].detection, "al")

        reg = "(!a|A)+"
        result: List[Re_Result] = re_findall(reg, sample_string)
        self.assertEqual(result[0].detection, "aaaAaaaa")
        self.assertEqual(result[1].detection, "aa")
        self.assertEqual(result[2].detection, "a")
        self.assertEqual(result[3].detection, "aa")

    def test_harder(self):
        sample_string = "123CF)456ABBBBABASADSAD1234"
        reg = "(AB|CF+%))|((AB*){2,3})((SAD)+)"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "CF)")
        self.assertEqual(result[1].detection, "ABBBBABASADSAD")

        reg = "(!(!AS|S)AD(!SAD|$)*123)"
        result = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "ASADSAD123")

    def test_groupds(self):
        sample_string = "123CF)456ABBBBABASADSAD1234"
        reg = "(AB|CF+%))|((AB*){2,3})((SAD)+12)"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].groups[1], "CF)")
        self.assertEqual(result[1].groups[2], "ABBBBABA")
        self.assertEqual(result[1].groups[3], "ABBBB")
        self.assertEqual(result[1].groups[4], "SADSAD12")
        self.assertEqual(result[1].groups[5], "SADSAD")

        sample_string = "aaaaaare you crazy ****"
        reg = "(a{0,2})are (you|they) crazy (%*+|%+{1,3})"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "aaare you crazy ****")
        self.assertEqual(result[0].groups[1], "aa")
        self.assertEqual(result[0].groups[2], "you")
        self.assertEqual(result[0].groups[3], "****")

        sample_string = "aaaaaare they crazy ++"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "aaare they crazy ++")
        self.assertEqual(result[0].groups[1], "aa")
        self.assertEqual(result[0].groups[2], "they")
        self.assertEqual(result[0].groups[3], "++")

        reg = "([a-z]+|$)@(gmail|yahoo|hotmail).(com|org|ru|us)"
        sample_string = "myemailtest@gmail.com"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "myemailtest@gmail.com")
        self.assertEqual(result[0].groups[1], "myemailtest")
        self.assertEqual(result[0].groups[2], "gmail")
        self.assertEqual(result[0].groups[3], "com")
        sample_string = "@gmail.com"
        result: List[Re_Result] = re_findall(reg, sample_string)
        print(*result)
        self.assertEqual(result[0].detection, "@gmail.com")
        self.assertEqual(result[0].groups[1], "")
        self.assertEqual(result[0].groups[2], "gmail")
        self.assertEqual(result[0].groups[3], "com")



        # x = "(AD|B+%)){1, 3}"
