# coding: utf-8

from __future__ import absolute_import

from ruamel.yaml.reader import Reader
from ruamel.yaml.scanner import Scanner, RoundTripScanner
from ruamel.yaml.parser import Parser, RoundTripParser
from ruamel.yaml.composer import Composer
from ruamel.yaml.constructor import BaseConstructor, SafeConstructor, Constructor, \
    RoundTripConstructor
from ruamel.yaml.resolver import VersionedResolver

__all__ = ['BaseLoader', 'SafeLoader', 'Loader', 'RoundTripLoader']


class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        BaseConstructor.__init__(self)
        VersionedResolver.__init__(self)


class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        VersionedResolver.__init__(self)


class Loader(Reader, Scanner, Parser, Composer, Constructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        VersionedResolver.__init__(self)


class RoundTripLoader(Reader, RoundTripScanner, RoundTripParser, Composer,
                      RoundTripConstructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        RoundTripScanner.__init__(self)
        RoundTripParser.__init__(self)
        Composer.__init__(self)
        RoundTripConstructor.__init__(self, preserve_quotes=preserve_quotes)
        VersionedResolver.__init__(self, version)
