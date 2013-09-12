"""Tests for title markdown."""

from titlemarkdown import toHtml as m
import unittest



class TestTitleMarkdown(unittest.TestCase):
    """Tests for title markdown conversion."""

    def testBasicConversion(self):
        self.assertEqual(m('Hello, world!'), 'Hello, world!')
        self.assertEqual(m('Hello, *world!*'), 'Hello, <i>world!</i>')
        self.assertEqual(m('**Hello**, *world!*'), '<b>Hello</b>, <i>world!</i>')
        self.assertEqual(m('A [link](http://foo.com/bar) is here!'),
                         'A <a href="http://foo.com/bar">link</a> is here!')


    def testNewlinesNotConvertedIntoParagraphs(self):
        self.assertEquals(m('\n\n\nfoo\n\nbar\n\n\nbaz'), '\n\n\nfoo\n\nbar\n\n\nbaz')


    def testUnicodeConversion(self):
        self.assertEquals(m(u'Hello, *world!*'), 'Hello, <i>world!</i>')
        self.assertEquals(m(u'Hello,\xa0*world!*'), 'Hello,\xc2\xa0<i>world!</i>')


    def testHtmlEscaping(self):
        self.assertEquals(m('<script>alert("OMG!");</script>'), '&lt;script&gt;alert("OMG!");&lt;/script&gt;')
        self.assertEquals(m('*hey <3 man*'), '<i>hey &lt;3 man</i>')


    def testLinksWithParentheses(self):
        self.assertEquals(m('(it is a [link](http://en.wikipedia.org/wiki/Tree_(data_structure)))'),
                          '(it is a <a href="http://en.wikipedia.org/wiki/Tree_(data_structure)">link</a>)')
