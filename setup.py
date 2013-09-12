"""Title markdown: a very limited markdown subset for titles."""

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
import os

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'engine.c')):
    os.system('ragel -C engine.rl -o engine.c -G2')

setup(
    name = 'titlemarkdown',
    version = '0.1',
    description = 'A very limited Markdown subset for titles',
    author = 'Peter Scott',
    author_email = 'peter@cueup.com',
    license = 'Apache',
    url = 'https://github.com/PeterScott/titlemarkdown',
    test_suite = 'tests',
    zip_safe = False,
    ext_modules = [Extension("titlemarkdown", ["titlemarkdown.c", "engine.c"])],
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
