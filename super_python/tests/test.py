#-*- coding: utf-8 -*-
import unittest
import time
from super_python import evaluate as M

class TestMethods(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def test_print(self):
        print("\nstarting test_print")
        cars = ["Audi", "Benz", "Corola", "Audi", "Benz", "Audi"]
        print("set of cars = ", ("set of cars"))
        self.assertEqual(M("number of cars"), 6)
        self.assertEqual(M("number of unique cars"), 3)
        self.assertEqual(M("most common car"), "Audi")
        name = "Audi"
        self.assertEqual(M("cars matching name"), ["Audi","Audi","Audi"])

    def test_baseline(self):
        print("\nstarting test_baseline")
        from collections import Counter
        cars = ["Audi", "Benz", "Corola", "Audi", "Benz", "Audi"]
        self.assertEqual(len(cars), 6)
        self.assertEqual(len(set(cars)), 3)
        self.assertEqual(Counter(cars).most_common(1)[0][0], "Audi")
        name = "Audi"
        self.assertEqual([car for car in cars if car == name], ["Audi","Audi","Audi"])
