#!/usr/bin/env python2

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import codecs

from lib.core.settings import IS_WIN
from thirdparty.six.moves import http_client as _http_client

def dirtyPatches():
    """
    Place for "dirty" Python related patches
    """

    # accept overly long result lines (e.g. SQLi results in HTTP header responses)
    _http_client._MAXLINE = 1 * 1024 * 1024

    # add support for inet_pton() on Windows OS
    if IS_WIN:
        from thirdparty.wininetpton import win_inet_pton

    # Reference: https://github.com/nodejs/node/issues/12786#issuecomment-298652440
    codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)

    # Reference: http://bugs.python.org/issue17849
    if hasattr(_http_client, "LineAndFileWrapper"):
        def _(self, *args):
            return self._readline()

        _http_client.LineAndFileWrapper._readline = _http_client.LineAndFileWrapper.readline
        _http_client.LineAndFileWrapper.readline = _
