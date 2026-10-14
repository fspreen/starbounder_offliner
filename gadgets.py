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

# probably not used by Starbounder at all, based on the warnings issued by the
# site-info query

from typing import NamedTuple, Optional, Any

# classes patterned after mwoffliner/src/Gadgets.ts (but some fields are
# missing even from up-to-date Wikipedia query?)

class Gadget(NamedTuple):
    ident: str
    metadata: Metadata

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Gadget:
        ident = d['id']
        metadata = Metadata.from_json(d['metadata'])

        return cls(ident, metadata)


class Metadata(NamedTuple):
    settings: Settings
    module: Module

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Metadata:
        settings = Settings.from_json(d['settings'])
        module = Module.from_json(d['module'])

        return cls(settings, module)


class Settings(NamedTuple):
    rights: list[str]
    skins: list[str]
    actions: list[str]
    categories: list[str]
    namespaces: list[int]
    contentModels: list[str]
    default: bool
    hidden: bool
    package: bool
    shared: bool
    #category: str
    #legacyscripts: bool
    requiresES6: bool
    supportsUrlLoad: bool

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Settings:
        rights = d['rights']
        skins = d['skins']
        actions = d['actions']
        categories = d['categories']
        namespaces = d['namespaces']
        contentModels = d['contentModels']
        default = d['default']
        hidden = d['hidden']
        package = d['package']
        shared = d['shared']
        #category = d['category']
        #legacyscripts = d['legacyscripts']
        requiresES6 = d['requiresES6']
        supportsUrlLoad = d['supportsUrlLoad']

        return cls(
                rights,
                skins,
                actions,
                categories,
                namespaces,
                contentModels,
                default,
                hidden,
                package,
                shared,
                #category,
                #legacyscripts,
                requiresES6,
                supportsUrlLoad
                )


class Module(NamedTuple):
    scripts: list[str]
    styles: list[str]
    datas: list[str]
    dependencies: list[str]
    peers: list[str]
    messages: list[str]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> Module:
        scripts = d['scripts']
        styles = d['styles']
        datas = d['datas']
        dependencies = d['dependencies']
        peers = d['peers']
        messages = d['messages']

        return cls(scripts, styles, datas, dependencies, peers, messages)
