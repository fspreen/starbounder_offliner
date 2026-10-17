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
import logging
import os

import offliner

_logger = logging.getLogger(__name__)

def main(args: argparse.Namespace) -> None:
    log_file_name: str = os.environ.get("PY_LOGFILE", "")

    if log_file_name:
        logging.basicConfig(
                filename = log_file_name,
                filemode = 'w',
                #DEFAULT: format = "%(levelname)s:%(name)s:%(message)s",
                format = "%(asctime)s %(name)s:%(levelname)s: %(message)s",
                level = os.environ.get("PY_LOG", "WARNING").upper()
                )
    else:
        logging.basicConfig(
                #DEFAULT: format = "%(levelname)s:%(name)s:%(message)s",
                format = "%(asctime)s %(name)s:%(levelname)s: %(message)s",
                level = os.environ.get("PY_LOG", "WARNING").upper()
                )

    offliner.main(args)


def instructions() -> None:
    print("ENVIRONMENT VARIABLES")
    print("  PY_LOGFILE - specify a file to write to (will be overwritten)")
    print("  PY_LOG     - log level to use (default 'WARNING')")
    print("               available levels are: debug, info, warning, error, critical")


def make_arg_parser() -> argparse.ArgumentParser:
    # taken from parameterList.ts
    arg_parser = argparse.ArgumentParser()

    # mwUrl would be required, except we already know Starbound's url
    #arg_parser.add_argument("--mwUrl", help='MediaWiki base URL (any URL paths appending)')
    arg_parser.add_argument("--adminEmail", required=True, help="Email of the StarbounderOffliner operator. Will be put in the HTTP user-agent string for information only")
    arg_parser.add_argument("--pageList", help="List of pages to include.  Comma separated list of titles or a local path or HTTP(S) URL to a file with one title (in UTF8) per line")
    #arg_parser.add_argument("--pageListToIgnore", help='List of pages to ignore. Comma separated list of titles or local path or HTTP(S) URL to a file with one title (in UTF8) per line')
    #arg_parser.add_argument("--customZimFavicon", help='Local path or HTTP(S) URL to a PNG favicon (will be resized to 48x48). Default to MediaWiki if not set')
    arg_parser.add_argument("--customZimTitle", help='ZIM custom title metadata (30 characters max)')
    arg_parser.add_argument("--customZimDescription", help="ZIM custom description (80 characters max)")
    #arg_parser.add_argument("--customZimLongDescription", help='ZIM custom long description (4000 characters max)')
    #arg_parser.add_argument("--customZimTags", help='ZIM tags metadata (semi-colon separated)')
    arg_parser.add_argument("--customZimLanguage", help='ZIM ISO 639-3 content language code')
    #arg_parser.add_argument("--customZimName", help='Custom ZIM Name template. Placeholders: {domain}, {lang}, {lang_or_variant}, {selection}.')
    #arg_parser.add_argument("--customZimFilename", help='Custom ZIM filename template, with the .zim extension. Placeholders: {zim_name}, {domain}, {lang}, {lang_or_variant}, {selection}, {flavour}, {period}.')
    arg_parser.add_argument("--customMainPage", help='Custom page to be used as welcome page.')
    #arg_parser.add_argument("--format", help='Flavour for the scraping. If missing, scrape all page contents. Each --format argument will cause a new ZIM file to be created but options can be combined. Supported options are:\n * novid: no video & audio content\n * nopic: no pictures (implies "novid")\n * nopdf: no PDF files\n * nodet: only the first/head paragraph (implies "novid")\nFlavour can be named (and corresponding ZIM metadata will be created) using a ":":\nExample: "--format=nopic,nodet:mini"')
    arg_parser.add_argument("--getCategories", action='store_true', help="Include the categories of all included pages.")
    arg_parser.add_argument("--categoriesPageSize", help="Number of items (subcategories, pages, files) to display per page on category pages (default: 200)")
    #arg_parser.add_argument("--keepEmptySections", help='Keep all sections, even empty ones typically used as placeholders in wikis to outline expected page structure.')
    #arg_parser.add_argument("--mwActionApiPath", help='MediaWiki API path (by default "/w/api.php")')
    arg_parser.add_argument("--mwModulePath", help="MediaWiki module load path ($wgLoadScript), automatically chosen based on script path otherwise.")
    #arg_parser.add_argument("--mwDomain", help='MediaWiki user domain (for private wikis)')
    #arg_parser.add_argument("--mwUsername", help='MediaWiki username (for private wikis)')
    #arg_parser.add_argument("--mwPassword", help='MediaWiki user password (for private wikis)')
    #arg_parser.add_argument("--minifyHtml", help='Try to reduce the size of the HTML')
    #arg_parser.add_argument("--outputDirectory", help='Directory to write the downloaded content')
    arg_parser.add_argument("--publisher", help="ZIM publisher meta data, by default 'Kiwix'")
    #arg_parser.add_argument("--redis", help='Redis path (redis:// URL or path to UNIX socket)')
    #arg_parser.add_argument("--requestTimeout", help='Request timeout in seconds (default is 120s)')
    #arg_parser.add_argument("--resume", help='Skip already existing/created ZIM files')
    #arg_parser.add_argument("--speed", help='Controls scraping speed. 1 is the default, 0.1 makes it ten times slower, 10 makes it ten times faster. Values above 1 must be integers (number of parallel workers).')
    #arg_parser.add_argument("--logLevel", help='Set the log level. One of: "debug", "info", "warn", "error", "silent" (default: "info"). All messages at the given level and above are printed.')
    #arg_parser.add_argument("--withoutZimFullTextIndex", help="Don't include a fulltext search index to the ZIM")
    #arg_parser.add_argument("--webp", help='Convert all jpeg, png and gif images to webp format')
    arg_parser.add_argument("--addNamespaces", help="Force additional namespace (comma separated numbers)")
    #arg_parser.add_argument("--addContentModels", help='Include additional content models besides wikitext (comma separated, e.g. "Scribunto,json"). By default, only wikitext pages are scraped.')
    arg_parser.add_argument("--onlyNamespaces", help="Include only pages of provided namespaces (comma separated numbers)")
    arg_parser.add_argument("--javaScript", help='Amount of JavaScript being allowed in pages, one of the following values can be given: "none", "trusted" or "all" (default being "trusted").')
    arg_parser.add_argument("--addModules", help="Add additional ResourceLoader modules for dynamic loading (comma separated list)")
    #arg_parser.add_argument("--osTmpDir", help='Override default operating system temporary directory path environment variable')
    #arg_parser.add_argument("--optimisationCacheUrl", help='Object Storage URL (including credentials and bucket name) to cache optimised media files')
    #arg_parser.add_argument("--forceRender", help='Force the usage of a specific API end-point/render, automatically chosen otherwise. Accepted values: [ ActionParse ]')
    arg_parser.add_argument("--forceSkin", help="Force the usage of a skin (must be available on wiki), default skin automatically chosen otherwise")
    #arg_parser.add_argument("--langVariant", help='Use a specific language variant, only for wikis supporting language conversion. Each --langVariant argument will cause a new ZIM file to be created.')
    #arg_parser.add_argument("--insecure", help='Skip HTTPS server authenticity verification step')
    #arg_parser.add_argument("--customCss", help='Comma-separated list of CSS URLs to inject into all rendered pages')
    #arg_parser.add_argument("--customJs", help='Comma-separated list of JS URLs to inject into all rendered pages')
    # TODO update help string with version info
    arg_parser.add_argument("--userAgent", help='Custom User-Agent header for all HTTP requests. Defaults to "StarbounderOffliner (<adminEmail>)"')
    #arg_parser.add_argument("--stableRevision", help='Prefer stable pages revisions when available, based on FlaggedRevs extension (which needs to be active on the wiki).')
    #arg_parser.add_argument("--customFlavour", help='A custom processor that can filter and process articles (see extensions/*.js)')
    #arg_parser.add_argument("--mathJaxSource", help='UNSTABLE: Local path or HTTP(S) URL to a MathJax ZIP archive to extract and push to the ZIM. Enables math rendering on wikis using MathJax. Pages are detected automatically by their JS module list.')
    #arg_parser.add_argument("--mathJaxConfig", help='UNSTABLE: Local path or HTTP(S) URL to a MathJax configuration HTML <script>. Its content is injected inline in pages that need MathJax, before the MathJax library.')
    #arg_parser.add_argument("--mathJaxEntryPoint", help='UNSTABLE: Relative path inside the extracted MathJax archive to the main entry-point script. Defaults to "MathJax.js" (MathJax 2). For MathJax 3 use e.g. "es5/tex-chtml.js".')
    #arg_parser.add_argument("--mathJaxAllPages", help='UNSTABLE: Inject MathJax config/entry-point scripts on all pages, instead of only on pages whose JS module list mentions MathJax. Useful for wikis which do not list MathJax in their page modules. Requires --mathJaxSource to also be set.')

    return arg_parser

if __name__ == "__main__":
    arg_parser = make_arg_parser()
    args = arg_parser.parse_args()

    main(args)
