import inspect
from collections import Counter
from re import compile as re_compile
from re import sub as re_sub
from re import UNICODE
from re import match
import sys
import ctypes
from os.path import dirname, realpath


def get_hash(arg):
    if isinstance(arg, list) or isinstance(arg, set):
        return str(arg)
    else:
        return str(arg.__hash__())

def memoize(f):
    memo = {}
    def helper(*args):
        print "args are", args, type(args)
     #try
        arg_hash = ""
        for i in range(len(args)):
            arg_hash += get_hash(args[i])

        if arg_hash not in memo:
            memo[arg_hash] = f(*args)

        print "\tmemo is", memo

        return memo[arg_hash]
     #except Exception as e:
     #     print e,"when", arg

    return helper

def evaluate(name):

    print "starting super_python.evaluate with", name

    name = name.lower()

    f_locals = inspect.stack()[1][0].f_locals
    print "f_locals are", f_locals

    mg = match("set of ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        if base in f_locals:
            return set_of_(f_locals[base])

    mg = match("number of unique ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        if base in f_locals:
            return number_of_unique_(f_locals[base])

    mg = match("number of ([a-z]*s)", name)
    if mg:
        base = mg.group(1)
        print "base is", base
        if base in f_locals:
            return number_of_(f_locals[base])

    mg = match("most common ([a-z]*)", name)
    if mg:
        base = mg.group(1) + "s"
        if base in f_locals:
            return most_common_of_(f_locals[base])

    mg = match("([a-z]+) matching ([a-z]+)", name)
    iterable = mg.group(1)
    term = mg.group(2)
    if iterable and term:
        if iterable in f_locals and term in f_locals:
            print "term is", term
            iterable = f_locals[iterable]
            print "iterable = ", iterable
            value = f_locals[term]
            print "value = ", value
            return list_matching_term_and_value(iterable, term, value)


@memoize
def list_matching_term_and_value(lst, term, value):
    print "starting list_ma"
    return_list = []
    for element in lst:
        if isinstance(element, str) or isinstance(element, unicode):
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
    print "starting number_of_ with", inpt
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

def superfy():
    pdf = path_to_directory_of_this_file = dirname(realpath(__file__))
    print "pdf is", pdf
    current_working_directory = getcwd()


# special print method for some objects
def super_print(*args):
    try:
        for arg in args:
            print arg,
        print "\n"
    except Exception as e:
        print e
p = super_print

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

class super_unicode(unicode):
    def remove(self, i):
        if isinstance(i, unicode):
            self.replace(i,u'')
        elif isinstance(i, list):
            for e in i:
                self = self.replace(e,'')
        return self

    def lremove(self, i):
        if isinstance(i, unicode):
            return re_sub(re_compile('^' + i, UNICODE), u'', self)
        elif isinstance(i, list):
            return re_sub(re_compile('^' + '(' + '|'.join(i) + ')', UNICODE), '', self)

    def rremove(self, i):
        if isinstance(i, unicode):
            return re_sub(re_compile(i + '$', UNICODE), '', self)
        elif isinstance(i, list):
            return re_sub(re_compile('(' + '|'.join(i) + ')' + '$', UNICODE), '', self)
