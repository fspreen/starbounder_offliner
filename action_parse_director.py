#!/usr/bin/env python

from typing import Optional
import urllib.parse

# temporary arrangement
from api_director import MAXLAG

# as seen in mwoffliner/src/util/builders/url/action-parse.director.ts
class ActionParseUrlDirector:
    __slots__ = ('baseDomain', 'skin', 'variant')

    def __init__(self, baseDomain: str, skin: str) -> None:
        self.baseDomain: str = baseDomain
        self.skin: str = skin
        self.variant: Optional[str] = None

    def buildPageUrl(self, pageTitle: str, sectionId: str = "", langVar: Optional[str] = None, oldid: Optional[str] = None) -> str:
        base_url_parts = urllib.parse.urlsplit(self.baseDomain)

        params = [
                ('action', 'parse'),
                ('format', 'json'),
                ('prop', 'modules|jsconfigvars|headhtml|text|displaytitle|subtitle|categorieshtml'),
                ('usearticle', '1'),
                ('disabletoc', '1'),
                ('disableeditsection', '1'),
                ('disablelimitreport', '1'),
                ]

        if oldid is None:
            params.append(('page', pageTitle))

        if oldid:
            params.append(('oldid', oldid))

        params.append(('useskin', self.skin))

        if langVar:
            params.append(('variant', langVar))

        params += [
                ('redirects', '1'),
                ('formatversion', '2'),
                ('section', sectionId),
                ('maxlag', str(MAXLAG)),
                ]

        query: str = urllib.parse.urlencode(params)

        new_url: str = urllib.parse.urlunsplit((
            base_url_parts.scheme,
            base_url_parts.netloc,
            base_url_parts.path,
            query,
            base_url_parts.fragment))

        return new_url
