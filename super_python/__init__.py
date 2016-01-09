import inspect
from re import compile as re_compile
from re import sub as re_sub
from re import UNICODE

# special print method for some objects
def super_print(*args):
    try:
        for arg in args:
            print arg,
        print "\n"
    except Exception as e:
        print e
p = super_print

# adds new things into memory ready for users to call
def expand():
    stack = inspect.stack()
    locals_ = stack[1][0].f_locals
    for key, value in list(locals_.iteritems()):
        if isinstance(value, list):
            locals_['number_of_' + key] = len(value)
            value_as_set = set(value)
            locals_[key + "_as_set"] = value_as_set
            locals_["number_of_unique_" + key] = len(value_as_set)
            locals_[key + "_lower"] = [e.lower() if isinstance(e, str) or isinstance(e, unicode) else e for e in value]
            del value_as_set
        elif isinstance(value, str) or isinstance(value, unicode):
            locals_[key + "_lower"] = value.lower()

def unpack(d):
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
