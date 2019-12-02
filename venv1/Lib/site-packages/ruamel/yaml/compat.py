# coding: utf-8

from __future__ import print_function

# partially from package six by Benjamin Peterson

import sys
import os
import types

try:
    from ruamel.ordereddict import ordereddict  # type: ignore
except:
    try:
        from collections import OrderedDict
    except ImportError:
        from ordereddict import OrderedDict  # type: ignore
    # to get the right name import ... as ordereddict doesn't do that

    class ordereddict(OrderedDict):   # type: ignore
        if not hasattr(OrderedDict, 'insert'):
            def insert(self, pos, key, value):
                if pos >= len(self):
                    self[key] = value
                    return
                od = ordereddict()
                od.update(self)
                for k in od:
                    del self[k]
                for index, old_key in enumerate(od):
                    if pos == index:
                        self[key] = value
                    self[old_key] = od[old_key]


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY3:
    def utf8(s):
        return s

    def to_str(s):
        return s

    def to_unicode(s):
        return s

else:
    def utf8(s):
        return s.encode('utf-8')

    def to_str(s):
        return str(s)

    def to_unicode(s):
        return unicode(s)

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
    unichr = chr
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO

else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    # to allow importing
    unichr = unichr  # type: ignore
    from StringIO import StringIO as _StringIO
    StringIO = _StringIO
    import cStringIO
    BytesIO = cStringIO.StringIO

if PY3:
    builtins_module = 'builtins'
else:
    builtins_module = '__builtin__'


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})

DBG_TOKEN = 1
DBG_EVENT = 2
DBG_NODE = 4


_debug = None

if _debug:
    class ObjectCounter(object):
        def __init__(self):
            self.map = {}

        def __call__(self, k):
            self.map[k] = self.map.get(k, 0) + 1

        def dump(self):
            for k in sorted(self.map):
                print(k, '->', self.map[k])

    object_counter = ObjectCounter()


# used from yaml util when testing
def dbg(val=None):
    global _debug
    if _debug is None:
        # set to true or false
        _debug = os.environ.get('YAMLDEBUG')
        if _debug is None:
            _debug = 0
        else:
            _debug = int(_debug)
    if val is None:
        return _debug
    return _debug & val


def nprint(*args, **kw):
    if dbg:
        print(*args, **kw)

# char checkers following production rules


def check_namespace_char(ch):
    if u'\x21' <= ch <= u'\x7E':  # ! to ~
        return True
    if u'\xA0' <= ch <= u'\xD7FF':
        return True
    if (u'\xE000' <= ch <= u'\xFFFD') and ch != u'\xFEFF':  # excl. byte order mark
        return True
    if u'\x10000' <= ch <= u'\x10FFFF':
        return True
    return False


def check_anchorname_char(ch):
    if ch in u',[]{}':
        return False
    return check_namespace_char(ch)
