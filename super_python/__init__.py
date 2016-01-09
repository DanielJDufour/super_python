import inspect
from re import compile as re_compile
from re import sub as re_sub
from re import UNICODE

def unpack(d):
    stack = inspect.stack()
    try:
        locals_ = stack[1][0].f_locals
    finally:
        del stack
    for key in d:
        locals_[key] = d[key]

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
