# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

# install_requires of ruamel.base is not really required but the old
# ruamel.base installed __init__.py, and thus a new version should
# be installed at some point

_package_data = dict(
    full_package_name='ruamel.yaml',
    version_info=(0, 13, 14),
    __version__='0.13.14',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order',  # NOQA
    entry_points=None,
    install_requires=dict(
        any=[],
        py33=['typing'],
        py34=['typing'],
        py27=['ruamel.ordereddict', 'typing'],
        pypy=['typing'],
    ),
    ext_modules=[dict(
            name='_ruamel_yaml',
            src=['ext/_ruamel_yaml.c', 'ext/api.c', 'ext/writer.c', 'ext/dumper.c',
                'ext/loader.c',
                'ext/reader.c',
                'ext/scanner.c',
                'ext/parser.c',
                'ext/emitter.c',
            ],
            lib=[],
            test='#include "ext/yaml.h"\n\nint main(int argc, char* argv[])\n{\nyaml_parser_t parser;\nparser = parser;  /* prevent warning */\nreturn 0;\n}\n',  # NOQA
        )],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
    ],
    windows_wheels=True,
    read_the_docs='yaml',
    many_linux='libyaml-devel',
    supported=[(2, 7), (3, 3)],  # minimum
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

try:
    from .cyaml import *  # NOQA
    __with_libyaml__ = True
except (ImportError, ValueError):  # for Jython
    __with_libyaml__ = False

from ruamel.yaml.main import *  # NOQA
