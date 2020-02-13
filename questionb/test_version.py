import unittest
import version

class QuestionB(unittest.TestCase):
    def one_case(self, s1, s2, expected):
        got = version.compare(s1, s2)
        msg = 'input: %s %s expected: %d got: %d'%(s1,s2,expected,got)
        self.assertEqual(expected, got, msg)

    def test_batch(self):
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
            self.one_case(s1, s2, expected)
            #test all cases in reverse order too
            self.one_case(s2, s1, -1 * expected)
