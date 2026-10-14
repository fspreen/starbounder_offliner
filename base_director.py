#!/usr/bin/env python

from typing import Optional
import urllib.parse

# xref mwoffliner/src/util/builders/url/base.director.ts

class BaseURLDirector:
    __slots__ = ('_baseDomain',)

    def __init__(self, baseDomain: str) -> None:
        bd: str = baseDomain

        if bd.endswith("/"):
            bd = bd[0:-1]

        self._baseDomain: str = bd

    # original returns WebAPI URL object
    def buildUrl(self, path: str) -> str:
        return urllib.parse.urljoin(self._baseDomain, path)

    # original returns a string ending in "?"
    def buildModuleUrl(self, path: Optional[str] = None) -> str:
        p = path if path is not None else "/w/load.php"

        return urllib.parse.urljoin(self._baseDomain, p)
