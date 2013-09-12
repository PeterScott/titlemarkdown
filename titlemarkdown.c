#include <Python.h>

char *titleMarkdownToHtml(const char *markdown, int len, int copy);

static PyObject *toHtml(PyObject *self, PyObject *args) {
  const char *str = NULL; unsigned int len;
  if (!PyArg_ParseTuple(args, "et#", "utf8", &str, &len)) return NULL;
  char *result = titleMarkdownToHtml(str, len, 0);
  PyMem_Free((void*)str);
  if (result == NULL) return NULL;

#if PY_MAJOR_VERSION >= 3
  PyObject *resultStr = PyBytes_FromString(result);
#else
  PyObject *resultStr = PyString_FromString(result);
#endif

  free(result);
  return resultStr;
}

static PyMethodDef titlemarkdown_methods[] = {
  {"toHtml", (PyCFunction)toHtml, METH_VARARGS,
   "Convert title markdown to HTML. Takes UTF-8 str or unicode, returns UTF-8 str."},
  {NULL, NULL}
};


// The rest of this is rather ugly boilerplate to allow this module to compile on both
// Python 2 and 3. For more details, see http://docs.python.org/3/howto/cporting.html

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT, "titlemarkdown", NULL, 0, titlemarkdown_methods, NULL, NULL, NULL, NULL
};
#define INITERROR return NULL
PyObject *PyInit_titlemarkdown(void)
#else
#define INITERROR return
void inittitlemarkdown(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("titlemarkdown", titlemarkdown_methods);
#endif
  if (module == NULL) INITERROR;
#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}
