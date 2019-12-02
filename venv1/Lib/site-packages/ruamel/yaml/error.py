# coding: utf-8

from __future__ import absolute_import

import warnings

from ruamel.yaml.compat import utf8

__all__ = ['FileMark', 'StringMark', 'CommentMark',
           'YAMLError', 'MarkedYAMLError', 'ReusedAnchorWarning',
           'UnsafeLoaderWarning']


class StreamMark(object):
    __slots__ = 'name', 'index', 'line', 'column',

    def __init__(self, name, index, line, column):
        self.name = name
        self.index = index
        self.line = line
        self.column = column

    def __str__(self):
        where = "  in \"%s\", line %d, column %d"   \
                % (self.name, self.line+1, self.column+1)
        return where


class FileMark(StreamMark):
    __slots__ = ()


class StringMark(StreamMark):
    __slots__ = 'name', 'index', 'line', 'column', 'buffer', 'pointer',

    def __init__(self, name, index, line, column, buffer, pointer):
        StreamMark.__init__(self, name, index, line, column)
        self.buffer = buffer
        self.pointer = pointer

    def get_snippet(self, indent=4, max_length=75):
        if self.buffer is None:  # always False
            return None
        head = ''
        start = self.pointer
        while (start > 0 and
               self.buffer[start-1] not in u'\0\r\n\x85\u2028\u2029'):
            start -= 1
            if self.pointer-start > max_length/2-1:
                head = ' ... '
                start += 5
                break
        tail = ''
        end = self.pointer
        while (end < len(self.buffer) and
               self.buffer[end] not in u'\0\r\n\x85\u2028\u2029'):
            end += 1
            if end-self.pointer > max_length/2-1:
                tail = ' ... '
                end -= 5
                break
        snippet = utf8(self.buffer[start:end])
        caret = '^'
        caret = '^ (line: {})'.format(self.line+1)
        return ' '*indent + head + snippet + tail + '\n' \
               + ' '*(indent+self.pointer-start+len(head)) + caret

    def __str__(self):
        snippet = self.get_snippet()
        where = "  in \"%s\", line %d, column %d"   \
                % (self.name, self.line+1, self.column+1)
        if snippet is not None:
            where += ":\n"+snippet
        return where


class CommentMark(object):
    __slots__ = 'column',

    def __init__(self, column):
        self.column = column


class YAMLError(Exception):
    pass


class MarkedYAMLError(YAMLError):
    def __init__(self, context=None, context_mark=None,
                 problem=None, problem_mark=None, note=None):
        self.context = context
        self.context_mark = context_mark
        self.problem = problem
        self.problem_mark = problem_mark
        self.note = note

    def __str__(self):
        lines = []
        if self.context is not None:
            lines.append(self.context)
        if self.context_mark is not None  \
           and (self.problem is None or self.problem_mark is None or
                self.context_mark.name != self.problem_mark.name or
                self.context_mark.line != self.problem_mark.line or
                self.context_mark.column != self.problem_mark.column):
            lines.append(str(self.context_mark))
        if self.problem is not None:
            lines.append(self.problem)
        if self.problem_mark is not None:
            lines.append(str(self.problem_mark))
        if self.note is not None:
            lines.append(self.note)
        return '\n'.join(lines)


class ReusedAnchorWarning(Warning):
    pass


class UnsafeLoaderWarning(Warning):
    text = """
The default 'Loader' for 'load(stream)' without further arguments can be unsafe.
Use 'load(stream, Loader=ruamel.yaml.Loader)' explicitly if that is OK.
Alternatively include the following in your code:

  import warnings
  warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

In most other cases you should consider using 'safe_load(stream)'"""
    pass

warnings.simplefilter('once', UnsafeLoaderWarning)
