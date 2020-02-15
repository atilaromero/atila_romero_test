import unittest
from .version import compare, compare_strict

class QuestionB(unittest.TestCase):
    def one_case(self, s1, s2, expected, strict):
        got = compare(s1, s2, strict)
        msg = 'input: %s %s expected: %d got: %d'%(s1,s2,expected,got)
        self.assertEqual(expected, got, msg)

    def test_batch_strict_on(self):
        # array of [s1, s2, expected]
        cases = [
            ["2", "2", 0],
            ["a", "a", 0],
            ["2.2", "2.2", 0],
            ["2.a", "2.a", 0],
            ["2.2.2", "2.2.2", 0],
            ["2.2.a", "2.2.a", 0],
            ["1", "2", -1],
            ["1.2", "2.2", -1],
            ["2.1", "2.2", -1],
            ["2.1", "2.a", -1],
            ["2", "2.2", -1],
            ["2", "2.0", -1],
            ["1.2.2", "2.2.2", -1],
            ["2.1.2", "2.2.2", -1],
            ["2.1.2", "2.a.2", -1],
            ["2.2.1", "2.2.2", -1],
            ["2.a.1", "2.a.2", -1],
            ["2.2", "2.2.0", -1],
            ["2", "2.0.0", -1],
            ["1.2.2", "2.2", -1],
            ["2.1.2", "2.2", -1],
            ["1.2.2", "2", -1],
            ["2.1.2", "3", -1],
        ]
        for case in cases:
            s1, s2, expected = case
            self.one_case(s1, s2, expected, strict=True)
            #test all cases in reverse order too
            self.one_case(s2, s1, -1 * expected, strict=True)

    def test_batch_strict_off(self):
        # array of [s1, s2, expected]
        cases = [
            ["2", "2", 0],
            ["a", "a", 0],
            ["2.2", "2.2", 0],
            ["2.a", "2.a", 0],
            ["2.2.2", "2.2.2", 0],
            ["2.2.a", "2.2.a", 0],
            ["1", "2", -1],
            ["1.2", "2.2", -1],
            ["2.1", "2.2", -1],
            ["2.1", "2.a", -1],
            ["2", "2.2", 0],
            ["2", "2.0", 0],
            ["1.2.2", "2.2.2", -1],
            ["2.1.2", "2.2.2", -1],
            ["2.1.2", "2.a.2", -1],
            ["2.2.1", "2.2.2", -1],
            ["2.a.1", "2.a.2", -1],
            ["2.2", "2.2.0", 0],
            ["2", "2.0.0", 0],
            ["1.2.2", "2.2", -1],
            ["2.1.2", "2.2", -1],
            ["1.2.2", "2", -1],
            ["2.1.2", "3", -1],
        ]
        for case in cases:
            s1, s2, expected = case
            self.one_case(s1, s2, expected, strict=False)
            #test all cases in reverse order too
            self.one_case(s2, s1, -1 * expected, strict=False)
