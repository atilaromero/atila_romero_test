#!/usr/bin/env python3
import sys

def compare(s1, s2, strict=False):
    """version.compare compares two version strings (format X.Y.Z)
    if s1 < s2, returns -1
    if s1 == s2, returns 0
    if s1 > s2, returns 1
    if strict=False (default) 2.1 == 2
    if strict=True 2 < 2.1
    """
    s1v = s1.split('.')
    s2v = s2.split('.')
    #process both string version in parts
    for (v1, v2) in zip(s1v, s2v):
        if v1 == v2:
            continue
        try:
            iv1 = int(v1)
            iv2 = int(v2)
        except:
            # this part of the string version is not a number
            # it is not clear what to do, let's compare the strings
            if v1<v2:
                return -1
            else:
                return 1
        if iv1<iv2:
            return -1
        else:
            return 1
    # if we did not return, all compared parts were equal
    if not strict:
        return 0
    # but they may have different sizes: 
    # the shortest is considered smaller when strict=True
    if len(s1v) < len(s2v):
        return -1
    elif len(s2v) < len(s1v):
        return 1
    else:
        return 0

if __name__ == "__main__":
    try:
        s1, s2 = sys.argv[1:]
    except ValueError:
        print("This program requires 2 strings as arguments")
        print(compare.__doc__)
        sys.exit(1)
    result = compare(s1, s2)
    print(result)