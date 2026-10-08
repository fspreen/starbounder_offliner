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

import logging
import time
from typing import Any, Optional

import requests

from  requests import Response

from tmp_headers import HEADERS as HEADERS

_logger = logging.getLogger(__name__)

_TIMEOUT_SECONDS = 10

# TODO set config opt
# TODO incorporate version?
_USER_AGENT = "StarbounderOffliner"

# TODO turn this all into async or something

class Downloader:
    __slots__ = ("_headers", )

    # email address for user-agent string
    def __init__(self, email: str) -> None:
        self._headers: dict[str, str] = {
                'User-Agent': f"{_USER_AGENT} ({email})",
                }

    def _get(self, url: str) -> Response:
        _logger.debug("GET: %s", url)

        response = requests.get(
                url,
                headers = self._headers,
                timeout = _TIMEOUT_SECONDS,
                )

        return response

    def checkApiAvailability(self, url: str, allowedMimeTypes: Optional[list[str]] = None) -> bool:
        try:
            resp = self._get(url)
            isSuccess = resp.status_code == 200 and ('mediawiki-api-error' not in resp.headers or resp.headers['mediawiki-api-error'] == "rest-permission-error")

            validMimeType = False
            if not allowedMimeTypes:
                validMimeType = True
            else:
                for mimeType in allowedMimeTypes:
                    if mimeType in resp.headers.get('content-type', ""):
                        validMimeType = True
                        break

            return isSuccess and validMimeType

        except requests.RequestException as xc:
            # TODO better exception info?
            _logger.debug("checkApiAvailability failed: URL=%s :: %s", url, xc)
            return False

    # Performs several retries that back off in exponential time delays, up to a
    # maximum count.  Delay values in seconds.
    def get_json(self, url: str, max_tries: int=10, min_delay: int=1, max_delay: int=60) -> Any:
        tries = 0
        delay = min_delay

        while tries < max_tries:
            resp = None
            js = None
            exc = None

            try:
                resp = self._get(url)

                if resp.status_code < 400:
                    js = resp.json()
                    if 'error' not in js:
                        return js

            except requests.RequestException as xc:
                exc = xc

            if not _retry_json(url, resp, js, exc):
                _logger.debug("Failed to get %s", url)
                raise Exception(f"Failed to get {url}")

            tries += 1
            _logger.debug("Backoff-retry #%d after %d sec", tries, delay)

            # TODO async this?
            time.sleep(delay)
            delay = min(delay * 2, max_delay)

        # TODO more failure details?
        _logger.debug("Failed to get %s", url)
        raise Exception(f"Failed to get {url}")


# whether a GET of JSON should be retried
def _retry_json(url: str, resp: Optional[Response], js: Optional[Any], exc: Optional[requests.RequestException]) -> bool:
    # see https://requests.readthedocs.io/en/latest/api/#exceptions
    # Exceptions that are okay to retry:  timeouts, connection errors, JSON
    # decode, and certain HTTP codes (handled below)
    # Exceptions that are NOT okay to retry:  too-many-redirects, certain other
    # HTTP status codes
    if isinstance(exc, requests.JSONDecodeError):
        _logger.debug("Retrying %s due to malformed JSON", url)
        return True

    if isinstance(exc, requests.Timeout):
        _logger.debug("Retrying %s due to timeout", url)
        return True

    if isinstance(exc, requests.ConnectionError):
        _logger.debug("Retrying %s due to connection error", url)
        return True

    # taken from mwoffliner/src/Downloader.ts
    if resp and resp.status_code in (429, 500, 502, 503, 504, 524):
        _logger.info("Retrying %s due to HTTP %d error", url, resp.status_code)
        return True

    if js and 'error' in js:
        # retry certain mediawiki errors
        # see mwoffliner/src/Downloader.ts
        if js['error'].get('code', "") in (
                "missingtitle",
                "readapidenied",
                "permissiondenied",
                "internal_api_error_MediaWiki\\Revision\\BadRevisionException",
                "internal_api_error_Wikimedia\\Assert\\UnreachableException",
                "internal_api_error_Wikimedia\\Assert\\InvariantException",
                "internal_api_error_Wikimedia\\Parsoid\\Core\\ResourceLimitExceededException",
                ):
            _logger.debug("Retrying %s due to %s MediaWiki error", url, js['error'].get('code', ""))
            return True
        return False

    # no other errors should be retried
    return False
