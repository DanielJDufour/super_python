# super_python
Take Python the Next Level!

Drastically trim down the number of lines of code.
You don't have to manually create variables that hold obvious things.
For example, if we have a list of cars, it's obvious what "number of cars" means, which is ```len(cars)```.

# Example
```
from super_python import evaluate as M
cars = ["Audi", "Benz", "Bentley", "Audi"]

# prints 4
print m('Number of Cars')

# prints 3
print m('Number of Unique Cars')

# print set
print m('Set of Cars')

# prints Audi
print m('Most Common Car')
