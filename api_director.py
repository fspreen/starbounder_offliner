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

import urllib.parse

# TODO what is this?
# TODO move to config option, with this default value
MAXLAG = 5

# expects apiUrl to be something like "https://en.wikipedia.org/w/api.php"
# see mwoffliner/src/util/builders/url/api.director.ts
class APIUrlDirector:
    __slots__ = ('_apiUrl',)

    def __init__(self, apiUrl: str) -> None:
        self._apiUrl: str = apiUrl

    def buildQueryURL(self, params: list[tuple[str, str]]) -> str:
        base_url_parts = urllib.parse.urlsplit(self._apiUrl)

        query: str = urllib.parse.urlencode(params)

        new_url: str = urllib.parse.urlunsplit((
            base_url_parts.scheme,
            base_url_parts.netloc,
            base_url_parts.path,
            query,
            base_url_parts.fragment))

        return new_url

    def buildCategoryMembersURL(self, pageTitle: str, continueStr: str = "") -> str:
        params = [
                ('action', 'query'),
                ('list', 'categorymembers'),
                ('cmtype', 'subcat|page|file'),
                ('cmprop', 'title|sortkeyprefix|type'),
                ('cmsort', 'sortkey'),
                ('cmlimit', 'max'),
                ('format', 'json'),
                ('formatversion', '2'),
                ('cmtitle', pageTitle),
                ('cmcontinue', continueStr),
                ('maxlag', str(MAXLAG)),
                ]

        return self.buildQueryURL(params)


    def buildSiteInfoURL(self) -> str:
        params: list[tuple[str, str]] = [
                ('action', 'query'),
                ('meta', 'siteinfo|allmessages'),
                ('siprop', 'general|skins|rightsinfo|namespaces|namespacealiases'),
                ('ammessages', 'tagline'),
                ('amenableparser', '1'),
                ('list', 'gadgets'),
                ('gaprop', 'id|metadata'),
                ('gaallowedonly', '1'),
                ('gaenabledonly', '1'),
                ('format', 'json'),
                ('formatversion', '2'),
                ('maxlag', str(MAXLAG)),
                ]

        return self.buildQueryURL(params)

    def buildLogEventsQuery(self, letype: str, pageTitle: str) -> str:
        params = [
                ('action', 'query'),
                ('list', 'logevents'),
                ('letype', letype),
                ('letitle', pageTitle),
                ('format', 'json'),
                ('maxlag', str(MAXLAG)),
                ]

        return self.buildQueryURL(params)

# -------------------------------------------------------------------------------------------- #

def test_build_site_info_url() -> None:
    api_dir = APIUrlDirector("https://en.wikipedia.org/w/api.php")
    siu = api_dir.buildSiteInfoURL()
    expected = "https://en.wikipedia.org/w/api.php?action=query&meta=siteinfo%7Callmessages&siprop=general%7Cskins%7Crightsinfo%7Cnamespaces%7Cnamespacealiases&ammessages=tagline&amenableparser=1&list=gadgets&gaprop=id%7Cmetadata&gaallowedonly=1&gaenabledonly=1&format=json&formatversion=2&maxlag=5"

    assert siu == expected

def test_build_query_url() -> None:
    api_dir = APIUrlDirector("https://en.wikipedia.org/w/api.php")
    url = api_dir.buildQueryURL([('param1', 'param1'), ('param2', 'param2')])

    assert url == "https://en.wikipedia.org/w/api.php?param1=param1&param2=param2"
