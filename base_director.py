#!/usr/bin/env python

#####
# Copyright (C) 2026  Fred Spreen
# Distributed under the terms of the GNU General Public License
#
# This file is part of StarbounderOffliner, a program to copy the Starbounder
# wiki into an OpenZIM file for offline perusal.
#
# StarbounderOffliner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# StarbounderOffliner is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# StarbounderOffliner. If not, see <https://www.gnu.org/licenses/>.
#####

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
