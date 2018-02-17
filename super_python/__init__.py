import inspect
from collections import Counter
from re import compile as re_compile
from re import sub as re_sub
from re import UNICODE
from re import match
import sys
import ctypes
from os.path import dirname, realpath
from os import getcwd


def get_hash(arg):
    if isinstance(arg, list) or isinstance(arg, set) or isinstance(arg, dict):
        return str(arg)
    else:
        return str(arg.__hash__())

def memoize(f):
    memo = {}
    def helper(*args):
        ##print "args are", args, type(args)
     #try
        arg_hash = ""
        for i in range(len(args)):
            arg_hash += get_hash(args[i])

        if arg_hash not in memo:
            memo[arg_hash] = f(*args)

        ##print "\tmemo is", memo

        return memo[arg_hash]
     #except Exception as e:
     #     ##print e,"when", arg

    return helper

def evaluate(name):

    ##print "starting super_python.evaluate with", name

    name = name.lower()

    f_locals = inspect.stack()[1][0].f_locals
    ##print "f_locals are", f_locals

    mg = match("set of ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        if base in f_locals:
            return set_of_(f_locals[base])

    mg = match("(?:number|count) of unique ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        if base in f_locals:
            return number_of_unique_(f_locals[base])

    mg = match("(?:number|count) of ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        ##print "base is", base
        if base in f_locals:
            return number_of_(f_locals[base])

    mg = match("most common ([a-z]*)", name)
    if mg:
        base = mg.group(1) + "s"
        if base in f_locals:
            return most_common_of_(f_locals[base])

    if "matching" in name:
        mg = match("([a-z]+) matching ([a-z]+)", name)
        if mg:
            iterable = mg.group(1)
            term = mg.group(2)
            if iterable and term:
                if iterable in f_locals and term in f_locals:
                    ##print "term is", term
                    iterable = f_locals[iterable]
                    ##print "iterable = ", iterable
                    value = f_locals[term]
                    ##print "value = ", value
                    return list_matching_term_and_value(iterable, term, value)

    mg = match("([a-z]+) of ([a-z]+)", name)
    if mg:
        name_of_property, name_of_obj = mg.groups()
        obj = f_locals[name_of_obj]
        return property_of_object(name_of_property, obj)
        
        
@memoize
def property_of_object(prop, obj):
    if isinstance(obj, dict):
        if prop in obj:
            return obj[prop]

    if hasattr(obj, prop):
        return getattr(obj, prop)


@memoize
def list_matching_term_and_value(lst, term, value):
    ##print "starting list_ma"
    return_list = []
    for element in lst:
        if isinstance(element, str) or isinstance(element, str):
            if element == value:
                return_list.append(element)
        elif isinstance(element, dict):
            if element[term] == value:
                return_list.append(element)
        else:
            if getattr(element, term) == value:
                return_list.append(element)
    return return_list



@memoize
def list_of_names_of_(things):
    return [thing['name'] for thing in things]

@memoize
def set_of_(list_of_things):
    return set(list_of_things)

@memoize
def number_of_(inpt):
    ##print "starting number_of_ with", inpt
    type_of_inpt = str(type(inpt))
    if type_of_inpt == "<type 'list'>":
        return len(inpt)
    elif type_of_inpt == "<type 'set'>":
        return len(inpt)
    elif type_of_inpt == "<class 'django.db.models.query.QuerySet'>":
        return inpt.count()

@memoize
def number_of_unique_(list_of_things):
    return number_of_(set_of_(list_of_things))

@memoize
def counter_of_(list_of_things):
    return Counter(list_of_things)

@memoize
def most_common_of_(list_of_things):
    return counter_of_(list_of_things).most_common(1)[0][0] or counter_of_(list_of_things).most_common(2)[1][0]

@memoize
def most_common_count_of_(list_of_things):
    return counter_of_(list_of_things).most_common(1)[0][1] or counter_of_(list_of_things).most_common(2)[1][1]

@memoize
def second_most_common_of_(list_of_things):
    tuples = counter_of_(list_of_things)
    if number_of_(tuples) == 0:
        return None
    elif number_of_(tuples) == 1:
        return tuples[0][0]
    elif number_of_(tuples) == 2:
        return tuples[0][0] or tuples[1][0]
    elif number_of_(tuples) >= 3:
        return tuples[0][0] or tuples[1][0] or tuples[2][0]

@memoize
def second_most_common_count_of_(list_of_things):
    tuples = counter_of_(list_of_things)
    if number_of_(tuples) == 0:
        return None
    elif number_of_(tuples) == 1:
        return tuples[0][1]
    elif number_of_(tuples) == 2:
        return tuples[0][1] or tuples[1][1]
    elif number_of_(tuples) >= 3:
        return tuples[0][1] or tuples[1][1] or tuples[2][1]


class dependent_set_counter():

    def __init__(self, name_of_independent):
        self.hash_value = {}
        self.name_of_independent = name_of_independent

        for name_of_method in dir(0):
            try:
              exec(("""
def {0}(*args):
    return getattr(self.calculate(), "{0}")(*args)
self.{0} = {0}
""".format(name_of_method)), locals())
            except Exception as e:
              print(e)

    def calculate(self, frame=None):
        #print "starting calculate with frame = ", frame
        if not frame:
            frame = inspect.stack()[2][0]

        if self.name_of_independent in frame.f_locals:
            value_of_independent = frame.f_locals[self.name_of_independent]
        elif self.name_of_independent in frame.f_globals:
            value_of_independent = frame.f_globals[self.name_of_independent].calculate(frame)
        else:
            raise Exception("can't find " + self.name_of_independent + " anywhere")
 
        hash_of_independent = value_of_independent.__str__()
        #print "hash_of_independent = ", hash_of_independent
        if hash_of_independent not in self.hash_value:
            if hasattr(value_of_independent, "__len__"):
                self.hash_value[hash_of_independent] = len(value_of_independent)
        return self.hash_value[hash_of_independent]
        


class dependent_int():

    def __init__(self, name_of_independent):
        #print "starting dpeenden_int"
        self.hash_value = {}
        self.name_of_independent = name_of_independent

        for name_of_method in dir(0):
            try:
              exec(("""
def {0}(*args):
    return getattr(self.calculate(), "{0}")(*args)
self.{0} = {0}
""".format(name_of_method)), locals())
            except Exception as e:
              print(e)

    def calculate(self, frame=None):
        #print "starting calculate"
        if not frame:
            frame = inspect.stack()[2][0]
        #print "frame is", dir(frame)
        #print "frame is", frame.f_code
        flocals = frame.f_locals
        if self.name_of_independent in flocals:
            #print self.name_of_independent, "in flocals"
            value_of_independent = flocals[self.name_of_independent]
            hash_of_independent = value_of_independent.__str__()
            #print "hash_of_independent = ", hash_of_independent
            if hash_of_independent not in self.hash_value:
                if hasattr(value_of_independent, "__len__"):
                    self.hash_value[hash_of_independent] = len(value_of_independent)
                elif hasattr(value_of_independent, "count"):
                    self.hash_value[hash_of_independent] = value_of_independent.count()
            return self.hash_value[hash_of_independent]
        
        else:
            raise NameError(self.name_of_independent + " not found in frame")
        #print "finishing calculate"





class dependent_set():

    def __init__(self, name_of_independent):
        #print "starting dpeenden_int"
        self.hash_value = {}
        self.name_of_independent = name_of_independent

        for name_of_method in dir(set):
            try:
              exec(("""
def {0}(*args):
    return getattr(self.calculate(), "{0}")(*args)
self.{0} = {0}
""".format(name_of_method)), locals())
            except Exception as e:
              print(e)

    def calculate(self, frame=None):
        #print "starting calculate with frame = ", frame
        if not frame:
            frame = inspect.stack()[2][0]
        #print "frame is", dir(frame)
        #print "frame is", frame.f_code
        flocals = frame.f_locals
        if self.name_of_independent in flocals:
            #print self.name_of_independent, "in flocals"
            value_of_independent = flocals[self.name_of_independent]
            hash_of_independent = value_of_independent.__str__()
            #print "hash_of_independent = ", hash_of_independent
            if hash_of_independent not in self.hash_value:
                if hasattr(value_of_independent, "__iter__"):
                    self.hash_value[hash_of_independent] = set(value_of_independent)
            return self.hash_value[hash_of_independent]
        
        else:
            #return #eval(self.name_of_independent + ".calculate(frame)") in frame.f_globals
            #f_globals = frame.f_globals

            raise NameError(self.name_of_independent + " not found in frame")
        #print "finishing calculate"



def superfy(f):

    #print "f is", f

    stack = inspect.stack()
    frame = stack[1][0]
    f_locals = frame.f_locals

    #print "co_varnames = ", dir(f)
    names_of_variables = sorted(f.__code__.co_varnames)
    for name_of_variable in names_of_variables:
        #print "for name_of_variable", name_of_variable
        if name_of_variable.count("_") <= 1 and match("^[a-z_]{2,}s$", name_of_variable):
            #print "\tmatch!"
            f.__globals__["number_of_" + name_of_variable] = f.__globals__["count_of_" + name_of_variable] = dependent_int(name_of_variable)
            f.__globals__["set_of_" + name_of_variable] = dependent_set(name_of_variable)
            f.__globals__["number_of_unique_" + name_of_variable] = f.__globals__["number_of_distinct_" + name_of_variable] = dependent_set_counter("set_of_" + name_of_variable)

    return f



"""
    path_to_directory_of_this_file = dirname(realpath(__file__))
    ##print "pdf is", pdf
    current_working_directory = getcwd()
    result = f(*args)
    del path_to_directory_of_this_file
    del current_working_directory
    return result
"""

# special ##print method for some objects
def p(*args):
    try:
        for arg in args:
            print(arg, end=' ')
        print("\n")
    except Exception as e:
        print(e)

# help from http://faster-cpython.readthedocs.org/mutable.html
def unpack(d):
    stack = inspect.stack()
    frame = stack[1][0]
    for key in d:
        frame.f_locals[key] = d[key]
    ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))
    del stack

def unpack_old(d):
    stack = inspect.stack()
    locals_ = stack[1][0].f_locals
    for key in d:
        locals_[key] = d[key]
    del stack

class super_str(str):
    def remove(self, i):
        if isinstance(i, str):
            self.replace(i,'')
        elif isinstance(i, list):
            for e in i:
                self = self.replace(e,'')
        return self

    def lremove(self, i):
        if isinstance(i, str):
            return re_sub(re_compile('^' + i), '', self)
        elif isinstance(i, list):
            return re_sub(re_compile('^' + '(' + '|'.join(i) + ')'), '', self)

    def rremove(self, i):
        if isinstance(i, str):
            return re_sub(re_compile(i + '$'), '', self)
        elif isinstance(i, list):
            return re_sub(re_compile('(' + '|'.join(i) + ')' + '$'), '', self)

class super_unicode(str):
    def remove(self, i):
        if isinstance(i, str):
            self.replace(i,'')
        elif isinstance(i, list):
            for e in i:
                self = self.replace(e,'')
        return self

    def lremove(self, i):
        if isinstance(i, str):
            return re_sub(re_compile('^' + i, UNICODE), '', self)
        elif isinstance(i, list):
            return re_sub(re_compile('^' + '(' + '|'.join(i) + ')', UNICODE), '', self)

    def rremove(self, i):
        if isinstance(i, str):
            return re_sub(re_compile(i + '$', UNICODE), '', self)
        elif isinstance(i, list):
            return re_sub(re_compile('(' + '|'.join(i) + ')' + '$', UNICODE), '', self)
