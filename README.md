# super_python
Take Python the Next Level!

Drastically trim down the number of lines of code.
You don't have to manually create variables that hold obvious things.
For example, if we have a list of cars, it's obvious what "number of cars" means, which is ```len(cars)```.

# Example
```
from super_python import superfy

@superfy
def test():
    cars = ["Audi", "Benz", "Bentley", "Audi"]

    print number_of_cars
    # prints 4

    print set_of_cars
    # prints set(['Benz', 'Bentley', 'Audi'])

    print "number_of_unique_cars", number_of_unique_cars
    # prints 3

