"""Tests for title markdown."""

from titlemarkdown import toHtml as m
import unittest
import sys

PYTHON3 = sys.version_info[0] == 3


def b(s):
    """Bytes from a string."""
    if PYTHON3:
        return bytes(s, 'utf8')
    if isinstance(s, unicode):
        return s.encode('utf8')
    return str(s)


def u(s):
    """Unicode string from a string."""
    if PYTHON3:
        return s
    if isinstance(s, str):
        return s.decode('utf8')
    return unicode(s)



class TestTitleMarkdown(unittest.TestCase):
    """Tests for title markdown conversion."""

    def testBasicConversion(self):
        self.assertEqual(m(b('Hello, world!')), b('Hello, world!'))
        self.assertEqual(m(b('Hello, *world!*')), b('Hello, <i>world!</i>'))
        self.assertEqual(m(b('**Hello**, *world!*')), b('<b>Hello</b>, <i>world!</i>'))
        self.assertEqual(m(b('A [link](http://foo.com/bar) is here!')),
                         b('A <a href="http://foo.com/bar">link</a> is here!'))


    def testNewlinesNotConvertedIntoParagraphs(self):
        self.assertEquals(m(b('\n\n\nfoo\n\nbar\n\n\nbaz')), b('\n\n\nfoo\n\nbar\n\n\nbaz'))


    def testUnicodeConversion(self):
        self.assertEquals(m(u(u'Hello, *world!*')), b('Hello, <i>world!</i>'))
        self.assertEquals(m(u(u'Hello,\xa0*world!*')), b(u'Hello,\xa0<i>world!</i>'))


    def testHtmlEscaping(self):
        self.assertEquals(m(b('<script>alert("OMG!");</script>')),
                          b('&lt;script&gt;alert("OMG!");&lt;/script&gt;'))
        self.assertEquals(m(b('*hey <3 man*')), b('<i>hey &lt;3 man</i>'))


    def testLinksWithParentheses(self):
        self.assertEquals(
            m(b('(it is a [link](http://en.wikipedia.org/wiki/Tree_(data_structure)))')),
            b('(it is a <a href="http://en.wikipedia.org/wiki/Tree_(data_structure)">link</a>)'))
