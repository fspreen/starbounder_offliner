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

import json
from typing import NamedTuple, Optional, Any

from gadgets import Gadget

# xref mwoffliner/src/MediaWiki.ts :: SiteInfoResponse
class SiteInfoResponse(NamedTuple):
    batchcomplete: bool
    query: SiteInfoQueryResponse
    warnings: Optional[dict[str, dict[str, str]]]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> SiteInfoResponse:
        batchcomplete: bool = d['batchcomplete']
        query = SiteInfoQueryResponse.from_json(d['query'])
        warnings = d.get('warnings', None)
        return cls(batchcomplete, query, warnings)

# xref mwoffliner/src/MediaWiki.ts :: SiteInfoQueryResponse
class SiteInfoQueryResponse(NamedTuple):
    general: SiteInfoGeneral
    skins: list[SiteInfoSkin]
    rightsinfo: RightsInfo
    namespaces: dict[str, Namespace]
    namespacealiases: list[NamespaceAlias]
    allmessages: list[Message]
    gadgets: Optional[list[Gadget]]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> SiteInfoQueryResponse:
        general = SiteInfoGeneral.from_json(d['general'])
        skins = [SiteInfoSkin.from_json(j) for j in d['skins']]
        rightsinfo = RightsInfo.from_json(d['rightsinfo'])
        namespaces = {k:Namespace.from_json(v) for (k,v) in d['namespaces'].items()}
        namespacealiases = [NamespaceAlias.from_json(j) for j in d['namespacealiases']]
        allmessages = [Message.from_json(j) for j in d['allmessages']]

        gadgets = None
        if 'gadgets' in d:
            gadgets = [Gadget.from_json(j) for j in d['gadgets']]

        return cls(general, skins, rightsinfo, namespaces, namespacealiases, allmessages, gadgets)


class SiteInfoGeneral(NamedTuple):
    generator: str
    mainpage: str
    #mainpageisdomainroot: bool
    sitename: str
    logo: str
    lang: str
    rtl: bool
    articlepath: str
    script: str
    scriptpath: str
    fallback: list[Any]                 # TODO
    variants: Optional[list[Any]]       # TODO
    #categorycollation: str              # TODO remove?

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> SiteInfoGeneral:
        generator = d['generator']
        mainpage = d['mainpage']
        #mainpageisdomainroot = d['mainpageisdomainroot']       # missing from Starbounder
        sitename = d['sitename']
        logo = d['logo']
        lang = d['lang']
        rtl = d['rtl']
        articlepath = d['articlepath']
        script = d['script']
        scriptpath = d['scriptpath']
        fallback = d['fallback']
        variants = d.get('variants', None)
        #categorycollation = d['categorycollation']             # missing from Starbounder

        return cls(
                generator,
                mainpage,
                #mainpageisdomainroot,
                sitename,
                logo,
                lang,
                rtl,
                articlepath,
                script,
                scriptpath,
                fallback,
                variants,
                #categorycollation
                )


class Namespace(NamedTuple):
    ident: int
    name: str
    canonical: Optional[str]
    content: bool
    subpages: bool
    nonincludable: bool

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Namespace:
        ident = d['id']
        name = d['name']
        canonical = d.get('canonical', None)
        content = d['content']
        subpages = d['subpages']
        nonincludable = d['nonincludable']

        return cls(ident, name, canonical, content, subpages, nonincludable)


class NamespaceAlias(NamedTuple):
    ident: int
    alias: str
    canonical: Optional[str]
    content: Optional[bool]
    subpages: Optional[bool]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> NamespaceAlias:
        ident = d['id']
        alias = d['alias']
        canonical = d.get('canonical', None)
        content = d.get('content', None)
        subpages = d.get('subpages', None)

        return cls(ident, alias, canonical, content, subpages)


class RightsInfo(NamedTuple):
    url: str
    text: str

    @classmethod
    def from_json(cls, d: dict[str, str]) -> RightsInfo:
        url = d['url']
        text = d['text']
        return cls(url, text)


class SiteInfoSkin(NamedTuple):
    code: str
    name: str
    default: Optional[bool]
    unusable: Optional[bool]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> SiteInfoSkin:
        code = d['code']
        name = d['name']
        default = d['default'] if 'default' in d else None
        unusable = d['unusable'] if 'unusable' in d else None

        return cls(code, name, default, unusable)


class Message(NamedTuple):
    name: str
    normalizedname: str
    content: str

    @classmethod
    def from_json(cls, d: dict[str, str]) -> Message:
        name = d['name']
        normalizedname = d['normalizedname']
        content = d['content']

        return cls(name, normalizedname, content)
