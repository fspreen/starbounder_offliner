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

import enum
from typing import NamedTuple, Optional

# I think mwoffliner defines these types to make them readonly.
ZimPath = str
PageTitle = str
PageID = str


class TextDirection(enum.Enum):
    LTR = 1
    RTL = 2

    def as_str(self) -> str:
        if self == TextDirection.LTR:
            return "ltr"
        if self == TextDirection.RTL:
            return "rtl"
        return self.name


class DownloadKind(enum.Enum):
    IMAGE = 0
    JSON = 1
    MEDIA = 2
    VIDEO = 3
    SUBTITLE = 4
    MODULE = 5
    CSS = 6
    JS = 7
    DATA = 8


class PageInfo(NamedTuple):
    ns: Optional[int]
    title: PageTitle


class PageThumbnail(NamedTuple):
    source: str
    height: int
    width: int


class CategoryInfo(NamedTuple):
    size: int
    pages: int
    files: int
    subcats: int
    hidden: bool
    nogallery: bool


class PageDetail(NamedTuple):
    pages: list[PageInfo]
    thumbnail: Optional[PageThumbnail]
    categoryinfo: Optional[CategoryInfo]
    categories: list[str]
    coordinates: Optional[str]          # mwoffliner: "coordinates.0.lat;coordinatese.0.lon"
    timestamp: Optional[str]            # mwoffliner: "revisions.0.timestamp"
    revisionID: Optional[int]           # mwoffliner: "revisions.0.revid"
    stableRevisionID: Optional[int]     # mwoffliner: "flagged.stable_revid (FlaggedRevs)
    internalThumbnailURL: Optional[str] # mwoffliner: "internalThumbnailUrl"
    missing: Optional[str]
    pagelang: Optional[str]
    pagedir: Optional[TextDirection]
    contentmodel: Optional[str]


class FileToDownload(NamedTuple):
    path: str
    download_attempts: int


class FileDetail(NamedTuple):
    url: str
    mult: Optional[int]
    width: Optional[int]
    kind: DownloadKind


class MWNamespaceData(NamedTuple):
    num: int
    allowedSubpages: bool


class MWMetaData(NamedTuple):
    langIso2: str
    langIso3: str
    title: str
    subTitle: str
    creator: str
    mainPage: str
    #mainPageIsDomainRoot: bool      # missing from Starbounder
    textDir: TextDirection
    langMw: str
    versionMw: str
    logo: str
    licenseName: str
    licenseUrl: str
    #categoryCollation: str          # missing from Starbounder

    baseUrl: str
    wikiPath: str
    indexPhpPath: str
    actionApiPath: str
    domain: str
    webUrl: str
    actionApiUrl: str
    webUrlPath: str
    modulePath: str
    modulePathOpt: str
