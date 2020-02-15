import unittest
from .overlap import overlap

class QuestionA(unittest.TestCase):
    def multiple_cases(self,cases):
        """ Auxiliary test function
            receives an array of test cases in the format:
            [ [x1,x2,x3,x4,expected], ]
            Also test points in inverted orders
        """
        for case in cases:
            x1, x2, x3, x4, expected = case
            self.one_case(x1,x2,x3,x4,expected)
            self.one_case(x1,x2,x4,x3,expected)
            self.one_case(x2,x1,x3,x4,expected)
            self.one_case(x2,x1,x4,x3,expected)
            self.one_case(x3,x4,x1,x2,expected)
            self.one_case(x4,x3,x1,x2,expected)
            self.one_case(x3,x4,x2,x1,expected)
            self.one_case(x4,x3,x2,x1,expected)

    def one_case(self, x1,x2,x3,x4,expected):
        """ Auxiliary test function
            applies the 'overlap' function in the input and checks if the result matches
        """
        got = overlap(x1,x2,x3,x4)
        msg = 'input: %d %d %d %d expected: %s got: %s'%(x1,x2,x3,x4,expected,got)
        self.assertEqual(expected, got, msg)

    def test_left(self):
        cases = [
            [1,2,3,4,False],
            [-2,-1,3,4,False],
            [-2.5,-1,3,4,False],
            [-1,2,3,4,False],
            [0,0,4,3,False],
            [0,0,3,3,False],
            [-3,-4,-2,-1,False],
        ]
        self.multiple_cases(cases)

    def test_right(self):
        cases = [
            [5,6,3,4,False],
            [6,5,-3,-4,False],
            [6.5,5,-3,-4,False],
            [5,6,-3,4,False],
            [5,6,0,0,False],
            [5,5,0,0,False],
            [-3,-4,-6,-5,False],
        ]
        self.multiple_cases(cases)

    def test_overlap(self):
        cases = [
            [1,3,2,4,True],
            [1,4,2,3,True],
            [1,2.5,2.5,3,True],
            [-1,3,2,4,True],
            [-1,-3,-2,-4,True],
            [-1,-4,-2,-3,True],
            [-1,3,-2,4,True],
        ]
        self.multiple_cases(cases)

if __name__ == '__main__':
    unittest.main()