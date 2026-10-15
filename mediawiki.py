#/usr/bin/env python

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
import logging
import re
from typing import NamedTuple, Optional
from urllib.parse import urlsplit

from action_parse_director import ActionParseUrlDirector
from api_director import APIUrlDirector
# temporary arrangement
from api_director import MAXLAG
import constants
from base_director import BaseURLDirector
from downloader import Downloader
from site_info import SiteInfoResponse, SiteInfoQueryResponse, SiteInfoSkin
import util

_logger = logging.getLogger(__name__)

# xref mwoffliner/src/MediaWiki.ts

class MediaWiki:
    __slots__ = (
            'downloader',

            'metadata',
            'baseUrl',
            'getCategories',
            'categoriesPageSize',
            'namespaces',
            'namespacesToMirror',
            'apiCheckPageTitle',
            'queryOpts',
            'urlDirector',
            'skin',

            '_wikiPath',
            '_indexPhpPath',
            '_actionApiPath',
            '_modulePathOpt',
            '_username',
            '_password',
            '_domain',

            'actionParseUrlDirector',

            'actionApiUrl',
            'webUrl',

            'modulePath',

            '_apiUrlDirector',
            '_hasActionParseApi',
            '_hasCoordinates',
            '_hasModuleApi',
            '_hasFlaggedRevs',
            )

    def __init__(self, downloader: Downloader) -> None:
        self.downloader: Downloader = downloader

        self.metadata: Optional[MWMetaData]
        self.baseUrl: str = ""
        self.getCategories: bool
        self.categoriesPageSize: int = constants.CATEGORIES_PAGE_SIZE
        self.namespaces: dict[str, MWNamespaceData]
        self.namespacesToMirror: list[str]
        self.apiCheckPageTitle: str
        self.queryOpts: QueryOpts
        self.urlDirector: Optional[BaseURLDirector] = None
        self.skin: str = ""

        self._wikiPath: str
        self._indexPhpPath: str
        self._actionApiPath: str
        self._modulePathOpt: str
        self._username: str
        self._password: str
        self._domain: str

        self.actionParseUrlDirector: Optional[ActionParseUrlDirector] = None

        self.actionApiUrl: str = ""
        self.webUrl: str = ""

        self.modulePath: str = ""

        self._apiUrlDirector: Optional[APIUrlDirector] = None
        self._hasActionParseApi: Optional[bool]
        self._hasCoordinates: Optional[bool]
        self._hasModuleApi: Optional[bool]
        self._hasFlaggedRevs: Optional[bool]

        self._init_defaults()

    def _init_defaults(self) -> None:
        self._domain = ""
        self._username = ""
        self._password = ""
        self.getCategories = False

        self._actionApiPath = "/w/api.php"
        self._wikiPath = "/wiki/"
        self._indexPhpPath = "/w/index.php"
        self._modulePathOpt = "/w/load.php"

        self.namespaces = {}
        self.namespacesToMirror = []
        self.apiCheckPageTitle = "MediaWiki:Sidebar"    # "as PageTitle" which is just a readonly string?

        self.queryOpts = QueryOpts(
                action = "query",
                qformat = "json",
                prop = "info|redirects|revisions|categoryinfo|pageprops|categories",
                rdlimit = "max",
                rdprop = "pageid|title|fragment",
                ppprop = "nogallery",
                clprop = "hidden",
                cllimit = "max",
                redirects = False,
                formatversion = "2",
                maxlag = str(MAXLAG)
                )

        self._hasActionParseApi = None
        self._hasCoordinates = None
        self._hasModuleApi = None
        self._hasFlaggedRevs = None
        self.metadata = None

    def set_username(self, value: str) -> None:
        self._username = value

    def set_password(self, value: str) -> None:
        self._password = value

    def get_actionApiPath(self) -> str:
        return self._actionApiPath

    def set_actionApiPath(self, value: str) -> None:
        if value:
            self._actionApiPath = value

            if self.urlDirector:
                self.actionApiUrl = self.urlDirector.buildUrl(value)
            else:
                self.actionApiUrl = ""

            self._apiUrlDirector = APIUrlDirector(self.actionApiUrl)

    def set_domain(self, value: str) -> None:
        self._domain = value

    def set_wikiPath(self, value: str) -> None:
        if value:
            self._wikiPath = value

            if self.urlDirector:
                self.webUrl = self.urlDirector.buildUrl(value)
            else:
                self.webUrl = ""

            _logger.info("webUrl: %s", self.webUrl)

    def set_indexPhpPath(self, value: str) -> None:
        if value:
            self._indexPhpPath = value

    def set_base(self, value: str) -> None:
        if value:
            self.baseUrl = value
            self.urlDirector = BaseURLDirector(value)
            self.webUrl = self.urlDirector.buildUrl(self._wikiPath)
            self.actionApiUrl = self.urlDirector.buildUrl(self._actionApiPath)
            self._apiUrlDirector = APIUrlDirector(self.actionApiUrl)
            self.setModuleURL()

    def set_modulePathOpt(self, value: str) -> None:
        if value:
            self._modulePathOpt = value

        if self.urlDirector:
            self.setModuleURL()
        elif value:
            _logger.error("Base url detector should be specifiedd first")

    async def hasActionParseApi(self) -> bool:
        if self._hasActionParseApi is None:
            self.actionParseUrlDirector = ActionParseUrlDirector(self.actionApiUrl, self.skin)
            checkUrl = self.actionParseUrlDirector.buildPageUrl(self.apiCheckPageTitle)
            # TODO await checkApiAvailability() if it ever goes async
            self._hasActionParseApi = self.downloader.checkApiAvailability(checkUrl)
            _logger.info("Checked for ActionParseApi at %s -- result is: %s",
                         checkUrl,
                         self._hasActionParseApi)

        return self._hasActionParseApi

    # TODO hasCoordinates

    async def hasModuleApi(self) -> bool:
        if self._hasModuleApi is None:
            checkURL = f"{self.modulePath}lang=en&modules=startup&only=scripts"
            # TODO await checkApiAvailability() if it ever goes async
            self._hasModuleApi = self.downloader.checkApiAvailability(checkURL)
            _logger.info("Checked for Module API at %s -- result is: %s",
                         checkURL,
                         self._hasModuleApi)

        return self._hasModuleApi

    # TODO hasFlaggedRevs

    def setModuleURL(self) -> None:
        if self.urlDirector:
            self.modulePath = self.urlDirector.buildModuleUrl(self._modulePathOpt)

    # login not needed for Starbounder

    def setNamespaces(self, siqr: SiteInfoQueryResponse, addNamespaces: list[int], onlyNamespaces: list[int]) -> None:
        ### Work through namespaces in site info
        for entry in siqr.namespaces.values():
            name = entry.name
            num = entry.ident
            allowedSubpages = entry.subpages
            canonical = entry.canonical if entry.canonical else ""

            details = MWNamespaceData(num, allowedSubpages)

            self.namespaces[util.lc_first(name)] = details
            self.namespaces[util.uc_first(name)] = details

            if canonical:
                self.namespaces[util.lc_first(canonical)] = details
                self.namespaces[util.uc_first(canonical)] = details

            if onlyNamespaces:
                if num in onlyNamespaces:
                    self.namespacesToMirror.append(name)
            else:
                is_content = entry.content
                is_blocked_ns = name in constants.BLOCKED_NAMESPACES
                if (is_content or num in addNamespaces) and not is_blocked_ns:
                    self.namespacesToMirror.append(name)

        ### Same thing, but for namespace ALIASES
        for ns_alias in siqr.namespacealiases:
            name = ns_alias.alias
            num = ns_alias.ident
            allowedSubpages = ns_alias.subpages if ns_alias.subpages else False
            canonical = ns_alias.canonical if ns_alias.canonical else ""

            details = MWNamespaceData(num, allowedSubpages)

            self.namespaces[util.lc_first(name)] = details
            self.namespaces[util.uc_first(name)] = details

            if canonical:
                self.namespaces[util.lc_first(canonical)] = details
                self.namespaces[util.uc_first(canonical)] = details

            if onlyNamespaces:
                if num in onlyNamespaces:
                    self.namespacesToMirror.append(name)
            else:
                is_content = ns_alias.content if ns_alias.content else False
                is_blocked_ns = name in constants.BLOCKED_NAMESPACES
                if (is_content or num in addNamespaces) and not is_blocked_ns:
                    self.namespacesToMirror.append(name)

    # TODO extractPageTitleFromHref

    def getCreatorName(self) -> str:
        # NOTE:  mwoffliner has a whole heuristic for extracting this from the
        # base domain name, but we already know what the Starbounder wiki is
        # called
        return "Starbounder"

    def getDefaultSkin(self, skins: list[SiteInfoSkin]) -> str:
        default_skins = [skin.code for skin in skins if skin.default]

        if not default_skins:
            raise ValueError("This wiki has no default skin: " + str(skins))

        if len(default_skins) > 1:
            _logger.warn("Multiple default skins found, defaulting to the first one (%s)", default_skins[0])

        return default_skins[0]

    # TODO change to async when the time comes
    def getSiteInfo(self,
                    addNamespaces: Optional[list[int]] = None,
                    onlyNamespaces: Optional[list[int]] = None,
                    mwModulePath: Optional[str] = None,
                    forceSkin: Optional[str] = None,
                    langVariants: Optional[list[str]] = None
                    ) -> tuple[
                            str,
                            #bool,
                            str,
                            TextDirection,
                            str,
                            #str,
                            #str,
                            str,
                            str,
                            str,
                            str,
                            #str,
                            str
                            ]:
        _logger.info("Getting site info...")

        # Downloader.querySiteInfo()
        if not self._apiUrlDirector:
            raise ValueError("Need to set_base() or set_actionApiPath before getSiteInfo()")

        js_body = self.downloader.get_json(self._apiUrlDirector.buildSiteInfoURL())
        body = SiteInfoResponse.from_json(js_body)

        generalEntries = body.query.general

        mwVersion = generalEntries.generator.split()[-1]
        _logger.info("Mediawiki version reported: %s", mwVersion)

        addNamespaces = addNamespaces if addNamespaces else []
        onlyNamespaces = onlyNamespaces if onlyNamespaces else []
        self.setNamespaces(body.query, addNamespaces, onlyNamespaces)
        # TODO Gadgets.setGagdets(body.query.gadgets)

        licenseUrl = body.query.rightsinfo.url
        licenseName = body.query.rightsinfo.text
        subTitle = body.query.allmessages[0].content if body.query.allmessages else ""
        mainPage = generalEntries.mainpage
        #mainPageIsDomainRoot is missing from Starbounder
        siteName = generalEntries.sitename
        #categoryCollation is missing from Starbounder
        logo = generalEntries.logo
        langMw = generalEntries.lang
        textDir = TextDirection.RTL if generalEntries.rtl else TextDirection.LTR
        _logger.info("Text direction is %s", textDir)

        langs = [re.sub("-.*", "", s) for s in generalEntries.fallback]
        # TODO langIso2 and langIso3 (NOTE:  can't find any examples of this data)

        articlepath = generalEntries.articlepath
        if '?' in articlepath or not articlepath.endswith("$1"):
            raise NotImplementedError(f"Article path [{articlepath}] is not supported")

        self._wikiPath = articlepath.replace("$1", "")
        self._indexPhpPath = generalEntries.script
        self._modulePathOpt = mwModulePath if mwModulePath else generalEntries.scriptpath + "/load.php"

        skins = [sk for sk in body.query.skins if not sk.unusable]
        if forceSkin and forceSkin not in [sk.code for sk in skins]:
            raise ValueError(f"Skin [{forceSkin}] is not usable on the wiki")
        self.skin = forceSkin if forceSkin else self.getDefaultSkin(skins)

        if langVariants:
            validLangVars = generalEntries.variants if generalEntries.variants else []
            invalidLangVars = [v for v in langVariants if v not in validLangVars]
            if invalidLangVars:
                raise ValueError(f"Language variants {invalidLangVars} are not available on the wiki")

        return (
                mainPage,
                #mainPageIsDomainRoot,
                siteName,
                textDir,
                langMw,
                #langIso2,
                #langIso3,
                logo,
                licenseName,
                licenseUrl,
                subTitle,
                #categoryCollation,
                mwVersion
                )

    # TODO change to async when the time comes
    def getMwMetaData(self,
                    addNamespaces: Optional[list[int]] = None,
                    onlyNamespaces: Optional[list[int]] = None,
                    mwModulePath: Optional[str] = None,
                    forceSkin: Optional[str] = None,
                    langVariants: Optional[list[str]] = None
                    ) -> MWMetaData:
        if self.metadata:
            return self.metadata

        creator = self.getCreatorName() or "Kiwix"

        (
                mainPage,
                #mainPageIsDomainRoot,
                siteName,
                textDir,
                langMw,
                #langIso2,
                #langIso3,
                logo,
                licenseName,
                licenseUrl,
                subTitle,
                #categoryCollation,
                mwVersion
                ) = self.getSiteInfo(addNamespaces, onlyNamespaces, mwModulePath, forceSkin, langVariants)

        metadata = MWMetaData(
                #langIso2,
                #langIso3,
                siteName,
                subTitle,
                creator,
                mainPage,
                #mainPageIsDomainRoot: bool
                textDir,
                langMw,
                mwVersion,
                logo,
                licenseName,
                licenseUrl,
                #categoryCollation: str

                self.baseUrl,
                self._wikiPath,
                self._indexPhpPath,
                self._actionApiPath,
                self._domain,
                self.webUrl,
                self.actionApiUrl,
                urlsplit(self.webUrl).path,
                self.modulePath,
                self._modulePathOpt
                )

        self.metadata = metadata
        return metadata


class QueryOpts(NamedTuple):
    action: str
    qformat: str
    prop: str
    rdlimit: str
    rdprop: str
    ppprop: str
    clprop: str
    cllimit: str
    redirects: Optional[bool]
    formatversion: str
    maxlag: str


class MWNamespaceData(NamedTuple):
    num: int
    allowedSubpages: bool


class MWMetaData(NamedTuple):
    #langIso2: str                   # unused by Starbounder (can't find docs?)
    #langIso3: str
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


class TextDirection(enum.Enum):
    LTR = 1
    RTL = 2

    def as_str(self) -> str:
        if self == TextDirection.LTR:
            return "ltr"
        elif self == TextDirection.RTL:
            return "rtl"
        return self.name
