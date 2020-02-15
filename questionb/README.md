# Question A: Version
A library to compare version strings.

It has two functions:

- ```compare(s1, s2, strict=False)```
    It compares two version strings (format X.Y.Z)
    -  if s1 < s2, returns -1
    -  if s1 == s2, returns 0
    -  if s1 > s2, returns 1
    -  if strict=False (default) 2.1 == 2
    -  if strict=True 2 < 2.1

- ```compare_strict(s1, s2)```
    Usefull to use as a cmp function in sort:
    ```
    from functools import cmp_to_key 
    sorted(["2.1.9", "1.9", "1"], key=cmp_to_key(version.compare_strict))
    ```

## How to run the program
In a shell prompt:
```
cd questionb/
python3 atila_romero_version/version.py 2.1.3 2.2.0
```
This should print the result ```-1``` because 2.1.3 is smaller than 2.2.0

## Using it as a library
In a shell prompt:
```
cd questionb/
python3 setup.py install --user
```

Then you can import the package in your programs like this:
```
#!/usr/bin/env python3
from atila_romero_version import version 
print(version.compare("2.1.9", "1.9"))

from functools import cmp_to_key 
print(sorted(["2.1.9", "1.9", "1"], key=cmp_to_key(version.compare_strict)))
```

## How it works
First each string is splitted in sections using '.' as separator.
Then each section is compared with the corresponding one in the other string.
When strict is turned off (default), the comparison stops when the string with fewer sections is fully processed. Otherwise, if they are equal up to that point, the one with fewer sections is considered smaller.

