# Question A: Overlap
A program to check if two 1D lines intercept each other

Given two 1D line segments, say (10,20) and (50,60)

## How to run the program
In a shell prompt:
```
cd questiona/
python3 atila_romero_overlap/overlap.py 10 20 50 60
```
This should print the result ```False```

## Using as a library
In a shell prompt:
```
cd questiona/
python3 setup.py install
```

Then you can import the package in your programs like this:
```
#!/usr/bin/env python3
from atila_romero_overlap import overlap 
print(overlap(10,20,50,60)) 
```


