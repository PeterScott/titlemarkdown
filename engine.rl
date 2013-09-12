// Ragel file for the Title Markdown engine. Compiles to -*- C -*- code.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

%%{
  machine titleMarkdownEngine;
  write data;
}%%

static int putCharRaw(char **buf, size_t *bufPos, size_t *bufLen, char c) {
  if (*bufPos >= *bufLen) {
    *buf = realloc(*buf, *bufLen * 2);
    *bufLen *= 2;
    if (*buf == NULL) return 1;
  }
  (*buf)[*bufPos] = c;
  *bufPos = *bufPos + 1;
  return 0;
}

static int putStringRaw(char **buf, size_t *bufPos, size_t *bufLen, char *str) {
  char c;
  while ((c = *str++)) {
    if (putCharRaw(buf, bufPos, bufLen, c)) return 1;
  }
  return 0;
}

static int putCharEscaped(char **buf, size_t *bufPos, size_t *bufLen, char c) {
  if (c == '&') return putStringRaw(buf, bufPos, bufLen, "&amp;");
  else if (c == '<') return putStringRaw(buf, bufPos, bufLen, "&lt;");
  else if (c == '>') return putStringRaw(buf, bufPos, bufLen, "&gt;");
  else return putCharRaw(buf, bufPos, bufLen, c);
}

static int printBetween(char **buf, size_t *bufPos, size_t *bufLen, char *s, char *e) {
  while (s < e) {
    if (putCharEscaped(buf, bufPos, bufLen, *s++)) return 1;
  }
  return 0;
}


// Convert a Markdown string to HTML. Escapes any HTML that may be in it already. Takes
// pointer and length; does not treat NUL characters in any special way.
// NOTE: This allocates a new string. You must free it.
char *titleMarkdownToHtml(const char *markdown, int len, int copy) {
  char *p = (char *)markdown, *pe = p + len; char *eof = pe; int cs;
  char *ts, *te; int act;

  size_t bufLen = 1024, bufPos = 0;
  char *buf = malloc(bufLen * sizeof(char));
  if (buf == NULL) return NULL;

  char *linkStart, *linkEnd;
  char *urlStart, *urlEnd;

#define HOPEFULLY(x) if (x) goto err;
#define BUF &buf, &bufPos, &bufLen

  %%{
    nonparen = (any - ('(' | ')'));
    parenUrl = nonparen+ . '(' . nonparen+ . ')';
    simpleUrl = (any - ')')+;
    url = (parenUrl | simpleUrl) >{ urlStart = p; } %{ urlEnd = p; };
    linkText = (any - ']')+ >{ linkStart = p; } %{ linkEnd = p; };

    link = '[' . linkText . '](' . url . ')';
    boldface = '**' . (any+ -- '**') . '**';
    italic = '*' . (any - '*')+ . '*';
    
  main := |*
    link => {
      HOPEFULLY(putStringRaw(BUF, "<a href=\""));
      HOPEFULLY(printBetween(BUF, urlStart, urlEnd));
      HOPEFULLY(putStringRaw(BUF, "\">"));
      HOPEFULLY(printBetween(BUF, linkStart, linkEnd));
      HOPEFULLY(putStringRaw(BUF, "</a>"));
    };
    boldface => {
      HOPEFULLY(putStringRaw(BUF, "<b>"));
      HOPEFULLY(printBetween(BUF, ts + 2, te - 2));
      HOPEFULLY(putStringRaw(BUF, "</b>"));
    };
    italic => {
      HOPEFULLY(putStringRaw(BUF, "<i>"));
      HOPEFULLY(printBetween(BUF, ts + 1, te - 1));
      HOPEFULLY(putStringRaw(BUF, "</i>"));
    };
    any => {
      HOPEFULLY(putCharEscaped(BUF, *ts));
    };
    *|;

    write init;
    write exec;
  }%%

  HOPEFULLY(putCharRaw(BUF, '\0'));
  if (copy) {
    char *oldBuf = buf;
    buf = strdup(buf);
    free(oldBuf);
  }
  return buf;
 err:
  if (buf != NULL) free(buf);
  return NULL;
}


#if 0
int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s [text]\n", argv[0]);
    exit(1);
  }

  char *result = titleMarkdownToHtml(argv[1], strlen(argv[1]), 1);
  if (result != NULL) {
    puts(result);
    free(result);
    return 0;
  }

  fprintf(stderr, "%s: could not allocate memory\n", argv[0]);
  return 1;
}
#endif
