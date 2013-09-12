## Title Markdown: a very restrictive subset of Markdown, meant for titles and short messages

[![Travis build status](https://travis-ci.org/PeterScott/titlemarkdown.png)](https://travis-ci.org/PeterScott/titlemarkdown)

Wouldn't it be nice if you could put really basic Markdown formatting in one-line messages, like chat messages or titles of things? Full Markdown is too featureful, and plain text is plain. This is a middle ground.

Supported syntax:

```
[links](http://example.com)

*italic*

**boldface**
```

That's it. That's literally all the syntax. HTML is escaped, and unlike most Markdown dialects, the parser can handle links like

    [this thing](http://en.wikipedia.org/wiki/Tree_(data_structure))
