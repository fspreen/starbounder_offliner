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

import argparse
import datetime as dt
import logging
from typing import NamedTuple

import downloader
from mediawiki import MediaWiki
from site_info import SiteInfoResponse

_logger = logging.getLogger(__name__)

# TODO set config opt?
# TODO incorporate version?
_USER_AGENT = "StarbounderOffliner"
_PUBLISHER = "openZIM"

def main(args: argparse.Namespace) -> None:
    # In mwoffliner, these are CLI parameters.
    mwUrl = "https://starbounder.org"
    mwActionApiPath = "/mediawiki/api.php"

    publisher = args.publisher or _PUBLISHER

    # TODO add version info
    _logger.info("Starting Starbound offliner...")

    # TODO change to config option?
    # TODO incorporate version?
    ua = args.userAgent if args.userAgent else _USER_AGENT
    full_ua = f"{ua} ({args.adminEmail})"

    # TODO Redis setup
    # TODO pass Redis and S3 to downloader
    down = downloader.Downloader(full_ua)

    mediawiki = MediaWiki(down)
    mediawiki.set_base(mwUrl)
    mediawiki.set_actionApiPath(mwActionApiPath)
    mediawiki.getCategories = args.getCategories
    if args.categoriesPageSize:
        mediawiki.categoriesPageSize = args.categoriesPageSize
    # not used for SB: domain (field is used for private wikis)
    # not used for SB: username or password

    # TODO log unrecognize value? (values should be "none", "trusted", or "all")
    javascript = args.javaScript if args.javaScript else "trusted"
    addModules = (args.addModules if args.addModules else "").split(',')
    # TODO trustedJS

    # user-agent string and downloader were initialized earlier

    # not used for SB: login

    # Redis setup should finish before downloader (see above)

    addNamespaces = []
    onlyNamespaces = []
    if args.addNamespaces:
        addNamespaces = [int(x) for x in args.addNamespaces.split(',')]
    if args.onlyNamespaces:
        onlyNamespaces = [int(x) for x in args.onlyNamespaces.split(',')]
    # TODO determine how langVariants is calculated

    try:
        mwMetaData = mediawiki.getMwMetaData(
                addNamespaces,
                onlyNamespaces,
                args.mwModulePath,
                args.forceSkin)
    except Exception as xc:
        _logger.error("FATAL - failed to get MediaWiki metadata")
        raise xc

    metaDataRequiredKeys = RequiredMetadata(
            creator = mwMetaData.creator,
            description = args.customZimDescription or mwMetaData.subTitle,
            language = args.customZimLanguage or mwMetaData.langIso3,
            publisher = publisher,
            title = args.customZimTitle or mwMetaData.title,
            date = dt.date.today().isoformat()
            # TODO illustration
            )

    # TODO validateMetadata() (mwoffliner/src/util/metaData.ts)

    mainPage = "" if args.pageList else mwMetaData.mainPage
    if args.customMainPage:
        main_page = args.customMainPage.replace('_', ' ')

    mediawiki.apiCheckPageTitle = mwMetaData.mainPage
    # TODO await these three calls if they ever go async
    # TODO await mediawiki.hasCoordinates()
    mediawiki.hasActionParseApi()
    mediawiki.hasModuleApi()

    _logger.error("APPLICATION IS NOT COMPLETE")


class RequiredMetadata(NamedTuple):
    creator: str
    description: str
    language: str
    publisher: str
    title: str
    date: str
    #illustration: str
