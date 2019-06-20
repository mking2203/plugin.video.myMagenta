#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime, timedelta
import uuid

import urllib
import urllib2
import urlparse
from random import randint

import re
import requests

import json

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import inputstreamhelper

PROTOCOL = 'ism'
DRM = 'com.widevine.alpha'

class anyItem:
    ID = ''
    title = ''
    orgTitle =''
    description = ''
    meta = ''
    thumb =''
    href = ''

class contentInformation(object):

    def __init__(self, data):
        self.jData = data

    def getID(self):
        if 'id' in self.jData:
            return self.jData['id']
        else:
            return ''

    def getTitle(self):
        if 'title' in self.jData:
            return self.jData['title']
        else:
            return 'no title'

    def getOrgignalTitle(self):
        if 'orgTitle' in self.jData:
            return self.jData['orgTitle']
        else:
            return ''

    def getDescription(self):
        if 'description' in self.jData:
            return self.jData['description']
        else:
            return 'no description'

    def getLongDescription(self):
        if 'longDescription' in self.jData:
            return self.jData['longDescription']
        else:
            return None

    def getMetaData(self):
        if 'metaData' in self.jData:
            return self.jData['metaData']
        else:
            return ''

    def getImages(self):
        if 'images' in self.jData:
            return self.jData['images']
        else:
            return []

    def getCast(self):
        if 'castAndCrew' in self.jData:
            return self.jData['castAndCrew']
        else:
            return []

    def getDetailPage(self):
        if 'detailPage' in self.jData:
            return self.jData['detailPage']['href']
        else:
            return ''

    def getAssetOrdinal(self):
        if 'assetOrdinal' in self.jData:
            return self.jData['assetOrdinal']
        else:
            return 0

    def getTrailer(self):
        if 'trailers' in self.jData:
            trs = self.jData['trailers']
            if len(trs)>0:
                return self.jData['trailers'][0]['href']
            else:
                return None
        else:
            return None

class  myMagenta(object):

    def addHeading(self, title):

        li = xbmcgui.ListItem("[COLOR gold]" + title + "[/COLOR]")
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(handle=HANDLE, url='', listitem=li)

    def addHeading2(self, title):

        li = xbmcgui.ListItem("[COLOR silver]" + title + "[/COLOR]")
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(handle=HANDLE, url='', listitem=li)

    def addSelector(self, item):

        url = PATH + '?nav=' + item.href
        li = xbmcgui.ListItem(label=item.title, thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def addMovie(self, item):

        url = PATH + '?nav=' + item.href
        li = xbmcgui.ListItem(label=item.title, thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def addDetails(self, item):

        url = PATH + '?content=' + item.href
        li = xbmcgui.ListItem(label='Details', thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def addTrailer(self, item):

        url = PATH + '?trailer=' + item.href
        li = xbmcgui.ListItem(label='Trailer', thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def showMenu(self):

        xbmcplugin.setContent(HANDLE, 'files')

        url = PATH + '?search=_menu'
        li = xbmcgui.ListItem(label='Suchen')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        s = requests.Session()

        page = 'https://web.magentatv.de/EPG/JSON/Login?&T=Windows_firefox_67'
        data = { "userId": "Guest" ,
                 "mac" :"00:00:00:00:00:00" }

        payload = json.dumps(data)
        #response = s.post(page, params = payload)

        #if (response.status_code == 200):
        if (True):

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

            uid = uuid.uuid4().hex

            data = { "terminalid":"00:00:00:00:00:00",
                     "mac":"00:00:00:00:00:00",
                     "terminaltype":"WEBTV",
                     "utcEnable":1,
                     "timezone":"Africa/Ceuta",
                     "userType":3,
                     "terminalvendor":"Unknown",
                     "preSharedKeyID":"PC01P00002",
                     "cnonce": uid,
                     "areaid":"1",
                     "templatename":"NGTV",
                     "usergroup":"-1",
                     "subnetId":"4901" }

            #payload = json.dumps(data)
            #response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

            #if (response.status_code == 200):
            if (True):

                #data = json.loads(response.text)
                #token = data ['csrfToken']

                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

                data = {
                    '%24WhiteLabelId':'OTT',
                    '%24limitPrincipalCpl':'',
                    '%24theme':'hdr',
                    '%24resolution':'webClient1280',
                    '%24cid': uid,
                    '%24redirect':'false',
                    '%24hideAdult':'true' }

                page = 'https://wcss.t-online.de/cvss/IPTV2015@First/vodclient/v1/redirectdocumentgroup/TV_VOD_DG_SG_Mov' # homeurl from manifest
                response = s.get(page, headers = headers)# , params = data)

                if (response.status_code == 200):

                    jObj = json.loads(response.text)

                    if '$type' in jObj:
                        jType = jObj['$type']

                        if jType == 'structuredGrid':
                            if 'menu' in jObj:
                                for item in jObj['menu']:
                                    if 'title' in item :
                                        if 'screen' in item:

                                            locked = True
                                            if 'isLocked' in item:
                                                if item ['isLocked'] == 'false':
                                                    locked = False
                                            if xbmcplugin.getSetting(HANDLE, 'FSK18') == 'true':
                                                locked = False

                                            if not locked:
                                                title =  item ['title']
                                                href = item ['screen']['href']

                                                url = PATH + '?nav=' + href
                                                li = xbmcgui.ListItem(label=title)
                                                xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

    def navigate(self, href):

        xbmcplugin.setContent(HANDLE, 'episodes')

        s = requests.Session()

        page = 'https://web.magentatv.de/EPG/JSON/Login?&T=Windows_firefox_67'
        data = { "userId": "Guest" ,
                 "mac" :"00:00:00:00:00:00" }

        payload = json.dumps(data)
        response = s.post(page, params = payload)

        if (response.status_code == 200):

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

            uid = uuid.uuid4().hex

            data = { "terminalid":"00:00:00:00:00:00",
                     "mac":"00:00:00:00:00:00",
                     "terminaltype":"WEBTV",
                     "utcEnable":1,
                     "timezone":"Africa/Ceuta",
                     "userType":3,
                     "terminalvendor":"Unknown",
                     "preSharedKeyID":"PC01P00002",
                     "cnonce": uid,
                     "areaid":"1",
                     "templatename":"NGTV",
                     "usergroup":"-1",
                     "subnetId":"4901" }

            payload = json.dumps(data)
            response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

            if (response.status_code == 200):

                data = json.loads(response.text)
                token = data ['csrfToken']

                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

                data = {
                    '%24WhiteLabelId':'OTT',
                    '%24limitPrincipalCpl':'',
                    '%24theme':'hdr',
                    '%24resolution':'webClient1280',
                    '%24cid': uid,
                    '%24redirect':'false',
                    '%24hideAdult':'true' }

                response = s.get(href, headers = headers, params = data)

                if (response.status_code == 200):

                    jObj = json.loads(response.text)

                    if '$type' in jObj:
                        jType = jObj['$type']

                        if jType == 'structuredGrid':
                            if 'content' in jObj:

                                if 'header' in jObj ['content']:
                                    title = jObj ['content']['header']['title']
                                    self.addHeading(title)

                                for group in jObj['content']['groups']:
                                    groupType = group ['groupType']
                                    self.addHeading2('Gruppe')

                                    if 'showAll' in group:
                                        sItem = anyItem()
                                        sItem.title = 'alle anzeigen'
                                        sItem.href = group ['showAll']['href']
                                        self.addSelector(sItem)

                                    if groupType == 'assetList':
                                        for item in group ['items']:

                                            iType = item ['assetDetails']['type']
                                            if iType == 'Movie' or 'Season':
                                                c = contentInformation(item['assetDetails']['contentInformation'])

                                                mItem = anyItem()
                                                mItem.title = c.getTitle()
                                                mItem.orgTitle = c.getOrgignalTitle()
                                                mItem.description = c.getDescription()
                                                mItem.ID = c.getID()
                                                mItem.href = c.getDetailPage()

                                                images = c.getImages()
                                                for image in images:
                                                    iType = image ['imageType']
                                                    if(iType == '5x7 big' or mItem.thumb == ''):
                                                        mItem.thumb = image ['href']

                                                self.addMovie(mItem)

                                    if groupType == 'smallTeaser' or groupType == 'bigTeaser':
                                        for item in group ['items']:
                                            details = item ['teaser']

                                            if 'title' in details:
                                                tItem = anyItem()
                                                tItem.title = details ['title']
                                                tItem.meta = details ['metaData']
                                                if 'images' in details:
                                                    for image in details['images']:
                                                        name = image
                                                        if name == 'bigImage' or tItem.thumb =='':
                                                            tItem.thumb = details['images'][name]['href']

                                                tItem.href = details ['target']['href']
                                                self.addSelector(tItem)

                        if jType == 'labelpartnerList':
                            items = jObj['content']['items']

                            for item in items:

                                sItem = anyItem()
                                sItem.title = item['name']
                                sItem.description = sItem.title
                                sItem.thumb = item['image']['href']
                                sItem.href = item['target']['href']
                                self.addSelector(sItem)

                        if jType == 'topten':
                            items = jObj['content']['items']

                            for item in items:

                                c = contentInformation(item['assetDetails']['contentInformation'])

                                mItem = anyItem()
                                mItem.title = c.getTitle()
                                mItem.orgTitle = c.getOrgignalTitle()
                                mItem.description = c.getDescription()
                                mItem.ID = c.getID()
                                mItem.href = c.getDetailPage()

                                images = c.getImages()
                                for image in images:
                                    iType = image ['imageType']
                                    if(iType == '5x7 big' or mItem.thumb == ''):
                                        mItem.thumb = image ['href']

                                self.addMovie(mItem)

                        if jType == 'assetdetails':

                            if 'content' in jObj:

                                c = contentInformation(jObj['content']['contentInformation'])

                                title = c.getTitle()
                                desc = c.getDescription()

                                thumb = ''
                                images = c.getImages()

                                for image in images:
                                    iType = image ['imageType']
                                    if(iType == '5x7 big' or thumb == ''):
                                        thumb = image ['href']

                                assetType = jObj ['content']['type']

                                if  assetType == 'Episode' or assetType == 'Movie':

                                    mItem = anyItem()
                                    mItem.title = title
                                    mItem.description = desc
                                    mItem.thumb = thumb
                                    mItem.href = href
                                    self.addDetails(mItem)

                                    if c.getTrailer():

                                        mItem = anyItem()
                                        mItem.title = title
                                        mItem.description = desc
                                        mItem.thumb = thumb
                                        mItem.href = c.getTrailer()
                                        self.addTrailer(mItem)

                                # SUB CONTENT follows
                                if  assetType == 'Series' or assetType == 'Season':
                                    self.addHeading(title)

                                if 'multiAssetInformation' in jObj['content']:
                                    subs = jObj['content']['multiAssetInformation']['subAssetDetails']
                                    for sub in subs:

                                        c = contentInformation(sub['contentInformation'])
                                        sType = sub['type']

                                        if sType == 'Season':
                                            sItem = anyItem()
                                            sItem.title = c.getTitle()
                                            sItem.thumb = thumb
                                            sItem.href = c.getDetailPage()
                                            self.addSelector(sItem)

                                        if sType == 'Episode':

                                            episode = c.getAssetOrdinal()

                                            sItem = anyItem()
                                            sItem.title = title + ' Folge ' + str(episode) + ' - '+ c.getTitle()
                                            sItem.meta = c.getDescription()
                                            sItem.thumb = thumb
                                            sItem.href = c.getDetailPage()
                                            self.addSelector(sItem)

        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

    def showDetails(self, href):

        s = requests.Session()

        page = 'https://web.magentatv.de/EPG/JSON/Login?&T=Windows_firefox_67'
        data = { "userId": "Guest" ,
                 "mac" :"00:00:00:00:00:00" }

        payload = json.dumps(data)
        response = s.post(page, params = payload)

        if (response.status_code == 200):

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

            uid = uuid.uuid4().hex

            data = { "terminalid":"00:00:00:00:00:00",
                     "mac":"00:00:00:00:00:00",
                     "terminaltype":"WEBTV",
                     "utcEnable":1,
                     "timezone":"Africa/Ceuta",
                     "userType":3,
                     "terminalvendor":"Unknown",
                     "preSharedKeyID":"PC01P00002",
                     "cnonce": uid,
                     "areaid":"1",
                     "templatename":"NGTV",
                     "usergroup":"-1",
                     "subnetId":"4901" }

            payload = json.dumps(data)
            response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

            if (response.status_code == 200):

                data = json.loads(response.text)
                token = data ['csrfToken']

                response = s.get(href)
                details = json.loads(response.text)

                c = contentInformation(details['content']['contentInformation'])

                title = c.getTitle()
                desc = c.getDescription()
                if c.getLongDescription():
                    desc = c.getLongDescription()

                thumb = ''
                fanArt = ''
                images = c.getImages()

                for image in images:
                    iType = image ['imageType']
                    if(iType == '5x7 big' or thumb == ''):
                        thumb = image ['href']
                    if(iType == 'still'):
                        fanArt = image ['href']

                li = xbmcgui.ListItem(label=title, path='')
                li.setInfo('video', { 'plot': desc})
                li.setArt({'thumb': thumb,
                            'poster': thumb,
                            'fanart': fanArt})

                castList = []
                cast = c.getCast()

                for c in cast:
                    if c ['role'] == 'actor':
                        name = c ['person']['firstName']
                        if 'lastName' in  c ['person']:
                            name = c ['person']['firstName'] + ' ' + c ['person']['lastName']
                        nameFiction = c ['fictionalCharacter']['firstName']
                        castList.append(name)

                li.setInfo('video', {'cast': castList })
                xbmcgui.Dialog().info(li)

    def showTrailer(self, href):

        s = requests.Session()

        page = 'https://web.magentatv.de/EPG/JSON/Login?&T=Windows_firefox_67'
        data = { "userId": "Guest" ,
                 "mac" :"00:00:00:00:00:00" }

        payload = json.dumps(data)
        response = s.post(page, params = payload)

        if (response.status_code == 200):

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

            uid = uuid.uuid4().hex

            data = { "terminalid":"00:00:00:00:00:00",
                     "mac":"00:00:00:00:00:00",
                     "terminaltype":"WEBTV",
                     "utcEnable":1,
                     "timezone":"Africa/Ceuta",
                     "userType":3,
                     "terminalvendor":"Unknown",
                     "preSharedKeyID":"PC01P00002",
                     "cnonce": uid,
                     "areaid":"1",
                     "templatename":"NGTV",
                     "usergroup":"-1",
                     "subnetId":"4901" }

            payload = json.dumps(data)
            response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

            if (response.status_code == 200):

                data = json.loads(response.text)
                token = data ['csrfToken']

                response = s.get(href)
                trailerDetails = json.loads(response.text)

                list = []
                metaData = trailerDetails['content']['feature']['metadata']
                trailers = trailerDetails['content']['feature']['representations']

                cnt = 0
                sel = -1

                for one in trailers:

                    type = one['type']
                    quality = one['quality']
                    contentClass = one['contentPackages'][0]['contentClass']
                    contentWidth = one['contentPackages'][0]['resolution']['width']
                    contentHref = one['contentPackages'][0]['media']['href']

                    #if 'ISMV' in contentClass:
                    if 'SmoothStreaming' in type:

                        li = xbmcgui.ListItem(label = str(type) + ' ' + str(quality) + ' ' + str(contentWidth),
                                              path=contentHref)
                        list.append(li)
                        cnt = cnt + 1

                        if sel == -1:
                            if quality == 'HD':
                                sel = cnt-1

                dialog = xbmcgui.Dialog()
                ret = dialog.select('Wähle ein Trailer', list, preselect=sel)
                if ret >=0:
                    playlist =  list[ret].getPath()
                    response = s.get(playlist)

                    pattern = '<media.*?src="(.*?)"'
                    m = re.search(pattern,response.text)
                    if m is not None:
                        url = m.group(1)

                        is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)

                        if is_helper.check_inputstream():
                            playitem = xbmcgui.ListItem(label=metaData['title'], path=url, thumbnailImage=metaData['titleImage']['href'])
                            playitem.setInfo('video', { 'plot': metaData['fullDescription']})
                            playitem.setProperty('inputstreamaddon', is_helper.inputstream_addon)
                            playitem.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)

                            xbmc.Player().play(item=url, listitem=playitem)

    def search(self, query):

        s = requests.Session()

        page = 'https://web.magentatv.de/EPG/JSON/Login?&T=Windows_firefox_67'
        data = { "userId": "Guest" ,
                 "mac" :"00:00:00:00:00:00" }

        payload = json.dumps(data)
        response = s.post(page, params = payload)

        if (response.status_code == 200):

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Referer': 'https://web.magentatv.de/EPG/' }

            uid = uuid.uuid4().hex

            data = { "terminalid":"00:00:00:00:00:00",
                     "mac":"00:00:00:00:00:00",
                     "terminaltype":"WEBTV",
                     "utcEnable":1,
                     "timezone":"Africa/Ceuta",
                     "userType":3,
                     "terminalvendor":"Unknown",
                     "preSharedKeyID":"PC01P00002",
                     "cnonce": uid,
                     "areaid":"1",
                     "templatename":"NGTV",
                     "usergroup":"-1",
                     "subnetId":"4901" }

            payload = json.dumps(data)
            response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

            if (response.status_code == 200):

                data = json.loads(response.text)
                token = data ['csrfToken']

                if query == '_menu':
                    #shoe search menu
                    url = PATH + '?search=_new'
                    li = xbmcgui.ListItem(label= 'Neue Suche')
                    xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

                    searches = []
                    searches.append(str(xbmcplugin.getSetting(HANDLE, 'search1')))
                    searches.append(str(xbmcplugin.getSetting(HANDLE, 'search2')))
                    searches.append(str(xbmcplugin.getSetting(HANDLE, 'search3')))
                    searches.append(str(xbmcplugin.getSetting(HANDLE, 'search4')))
                    searches.append(str(xbmcplugin.getSetting(HANDLE, 'search5')))

                    for s in searches:
                        if(s <> ''):
                            url = PATH + '?search=' + s
                            li = xbmcgui.ListItem(label=s)
                            xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

                    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

                else:

                    if query == '_new':

                        query = ''

                        keyboard = xbmc.Keyboard('', 'Suchen')
                        keyboard.doModal()

                        if (keyboard.isConfirmed()):
                            keyword = keyboard.getText()

                            if len(keyword) > 0:
                                query = keyword

                                searches = []
                                searches.append(str(xbmcplugin.getSetting(HANDLE, 'search1')))
                                searches.append(str(xbmcplugin.getSetting(HANDLE, 'search2')))
                                searches.append(str(xbmcplugin.getSetting(HANDLE, 'search3')))
                                searches.append(str(xbmcplugin.getSetting(HANDLE, 'search4')))
                                searches.append(str(xbmcplugin.getSetting(HANDLE, 'search5')))

                                xbmcaddon.Addon().setSetting('search1', query)
                                xbmcaddon.Addon().setSetting('search2', value=searches[0])
                                xbmcaddon.Addon().setSetting('search3', value=searches[1])
                                xbmcaddon.Addon().setSetting('search4', value=searches[2])
                                xbmcaddon.Addon().setSetting('search5', value=searches[3])

                    if len(query) > 0:

                        # now search
                        url = 'https://web.magentatv.de/EPG/search/ngtv/select/all_ott/?query=%s&size=10&channelMapId=OTT&offset=0' % query

                        response = s.get(url)
                        jObj = json.loads(response.text)

                        items = jObj ['totalItems']

                        result = jObj['results']
                        for r in result:

                                detailID = r['id']
                                title = r['title']
                                year = ''
                                if 'year' in r:
                                    title = title + ' (%s)' % r['year']
                                thumb = ''
                                if 'poster' in r:
                                    thumb = r['poster']
                                genre = '?'
                                if 'mainGenre' in r:
                                    genre = r['mainGenre']
                                rating = 'Unbekannt'
                                if 'ageRatingId' in r:
                                    rating = r['ageRatingId']
                                description = genre + ' - ' + rating

                                # deep link aus dem manifest
                                url = 'https://wcss.t-online.de/cvss/IPTV2015@Mobile/vodclient/v1/assetDetails/44593/%s?$WhiteLabelId=OTT&checkUsageRights=false&$theme=hdr&$resolution=webClient1280&$cid=%s&$redirect=false&$hideAdult=false' % (detailID,str(uid))
                                url = PATH + '?nav=' + url

                                li = xbmcgui.ListItem(label= title, thumbnailImage=thumb)
                                li.setInfo('video', { 'plot': description })
                                xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

                        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


if __name__ == '__main__':

    ADDON = xbmcaddon.Addon()
    ADDON_NAME = ADDON.getAddonInfo('name')
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = urlparse.parse_qs(sys.argv[2][1:])

    magenta = myMagenta()

    if PARAMS.has_key('mode'):
        mode = PARAMS['mode'][0]
        magenta.showMenu()
    elif PARAMS.has_key('nav'):
            magenta.navigate(PARAMS['nav'][0])
    elif PARAMS.has_key('trailer'):
            magenta.showTrailer(PARAMS['trailer'][0])
    elif PARAMS.has_key('content'):
            magenta.showDetails(PARAMS['content'][0])
    elif PARAMS.has_key('search'):
            magenta.search(PARAMS['search'][0])
    else:
        magenta.showMenu()





