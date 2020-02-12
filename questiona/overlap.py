import sys

def overlap(x1,x2,x3,x4):
    """overlap take 4 numbers, x1,x2,x3,x4, that are positions 
        for 2 lines: (x1,x2) and (x3, x4).
        It returns a boolean indicating whether the lines overlap
    """
    #There are only 2 situations where the two lines do not overlap:
    #  one of them must have both points smaller than the other two or 
    #  they both must be bigger.
    if x1 < x3 and x1 < x4: 
        if x2 < x3 and x2 < x4:
            return False # both points smaller
    if x1 > x3 and x1 >  x4:
        if x2 > x3 and x2 > x4:
            return False # both points bigger
    return True

if __name__ == "__main__":
    try:
        x1, x2, x3, x4 = [float(x) for x in sys.argv[1:]]
    except ValueError:
        print("This program requires 4 numbers as arguments")
        print(overlap.__doc__)
        sys.exit(1)
    result = overlap(x1, x2, x3, x4)
    print(result)
