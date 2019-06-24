#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime
from datetime import timedelta
import uuid

import urllib
import urllib2
import cookielib
import urlparse
from random import randint

import re
import requests

import json

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import xbmcvfs
import inputstreamhelper

from resources.lib.contentInformation import contentInformation
from resources.lib.channels import channels
from resources.lib.channels import channel

PROTOCOL = 'ism'
DRM = 'com.widevine.alpha'
#DRM = 'com.microsoft.playready'

class anyItem:
    ID = ''
    title = ''
    orgTitle =''
    description = ''
    thumb =''
    href = ''

class  myMagenta(object):

    def addHeading(self, title):

        li = xbmcgui.ListItem("[COLOR gold]" + title + "[/COLOR]")
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(handle=HANDLE, url='', listitem=li)

    def addHeading2(self, title, thumb):

        li = xbmcgui.ListItem("[COLOR orange]" + title + "[/COLOR]", thumbnailImage=thumb)
        li.setProperty("IsPlayable", 'false')
        xbmcplugin.addDirectoryItem(handle=HANDLE, url='', listitem=li)

    def addSelector(self, item):

        url = PATH + '?nav=' + item.href
        li = xbmcgui.ListItem(label=item.title, thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        li.setProperty("IsPlayable", 'false')
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
        li.setProperty("IsPlayable", 'false')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def addTrailer(self, item):

        url = PATH + '?trailer=' + item.href
        li = xbmcgui.ListItem(label='Trailer', thumbnailImage=item.thumb)
        li.setInfo('video', { 'plot': item.description })
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

    def showMenu(self):

        xbmcplugin.setContent(HANDLE, 'files')

        url = PATH + '?search=_menu'
        li = xbmcgui.ListItem(label='Suche', thumbnailImage = 'defaultaddonssearch.png')
        li.setProperty("IsPlayable", 'false')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        url = PATH + '?TV=_menu'
        li = xbmcgui.ListItem(label='TV', thumbnailImage = 'defaulttvshows.png')
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        page = 'https://wcss.t-online.de/cvss/IPTV2015@First/vodclient/v1/redirectdocumentgroup/TV_VOD_DG_SG_Mov' # homeurl from manifest

        s = requests.Session()
        response = s.get(page)

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

                                        sItem = anyItem()
                                        sItem.title = item['title']
                                        sItem.href = item['screen']['href']
                                        self.addSelector(sItem)


            url = PATH + '?settings=SET'
            li = xbmcgui.ListItem(label='Einstellungen', thumbnailImage = '')
            li.setProperty("IsPlayable", "false")
            xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

    def navigate(self, href):

        xbmc.log('MYMAGENTA (Navigate): ' + href)

        xbmcplugin.setContent(HANDLE, 'episodes')


        s = requests.Session()
        s.cookies = cookielib.LWPCookieJar('cookiejar')

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

                    s.cookies.save(COOKIE, ignore_discard=True, ignore_expires=True)

                    jObj = json.loads(response.text)

                    if '$type' in jObj:
                        jType = jObj['$type']

                        if jType == 'structuredGrid':
                            if 'content' in jObj:

                                hasHeader = False

                                if 'header' in jObj ['content']:
                                    title = jObj ['content']['header']['title']
                                    hasHeader = True
                                    self.addHeading(title)

                                for group in jObj['content']['groups']:
                                    groupType = group ['groupType']

                                    background = ''
                                    if 'backgroundImage' in group:
                                        background = group ['backgroundImage']['href']

                                    if 'title' in group:
                                        self.addHeading2(group ['title'], background)
                                    else:
                                        if not hasHeader:
                                            self.addHeading2('---------------------------', background)

                                    hasHeader = False

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
                                                mItem.title = c.title
                                                mItem.orgTitle = c.originalTitle
                                                mItem.description = c.description
                                                mItem.ID = c.ID
                                                mItem.href = c.detailPage

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
                                mItem.title = c.title
                                mItem.orgTitle = c.originalTitle
                                mItem.description = c.description
                                mItem.ID = c.ID
                                mItem.href = c.detailPage

                                images = c.getImages()
                                for image in images:
                                    iType = image ['imageType']
                                    if(iType == '5x7 big' or mItem.thumb == ''):
                                        mItem.thumb = image ['href']

                                self.addMovie(mItem)

                        if jType == 'assetdetails':

                            if 'content' in jObj:

                                c = contentInformation(jObj['content']['contentInformation'])

                                title = c.title
                                desc = c.description

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
                                            sItem.title = c.title
                                            sItem.thumb = thumb
                                            sItem.href = c.detailPage
                                            self.addSelector(sItem)

                                        if sType == 'Episode':

                                            episode = c.assetOrdinal

                                            sItem = anyItem()
                                            sItem.title = title + ' Folge ' + str(episode) + ' - '+ c.title
                                            sItem.description = c.description
                                            sItem.thumb = thumb
                                            sItem.href = c.detailPage
                                            self.addSelector(sItem)

        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

    def showDetails(self, href):

        xbmc.log('MYMAGENTA (Details): ' + href)

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

                title = c.title
                desc = c.description
                if c.longDescription: desc = c.longDescription

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

                for ca in cast:
                    if ca['role'] == 'actor':

                        name = ''
                        first = ''
                        last = ''

                        if 'firstName' in  ca['person']:
                            first = ca['person']['firstName']
                        if 'lastName' in  ca['person']:
                            last = ca['person']['lastName']

                        name = first
                        if first != '':
                            name = name + ' ' + last
                        else:
                            name = last

                        if 'fictionalCharacter' in ca:
                            nameFiction = ca['fictionalCharacter']['firstName']
                        castList.append(name)

                li.setInfo('video', {'mpaa': c.childProtection })
                li.setInfo('video', {'genre': c.genre })
                li.setInfo('video', {'country': c.country })
                if c.year:
                    li.setInfo('video', {'year': c.year })
                if c.runtime:
                    li.setInfo('video', {'duration': c.runtime })
                if c.communityRating:
                    li.setInfo('video', {'rating':c.communityRating * 2 })

                # crahes KODI
                #if c.getTrailer():
                #    li.setInfo('video', {'trailer': PATH + '?trailer=' + c.getTrailer() })

                li.setInfo('video', {'cast': castList })
                xbmcgui.Dialog().info(li)

    def showTrailer(self, href):

        xbmc.log('MYMAGENTA (Trailer): ' + href)

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

                            thumb = ''
                            if 'titleImage' in metaData: thumb = metaData['titleImage']['href']
                            if 'smallCoverImage' in metaData: thumb = metaData['smallCoverImage']['href']

                            playitem = xbmcgui.ListItem(label=metaData['title'], path=url, thumbnailImage=thumb)
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

    def showTV(self):

        xbmcplugin.setContent(HANDLE, 'files')

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
                    'Referer': 'https://web.magentatv.de/EPG/',
                    'X_CSRFToken': token }

                # get all channels
                page = 'https://web.magentatv.de/EPG/JSON/AllChannel?SID=first&T=Windows_firefox_67'

                data = {"properties":[{"name":"logicalChannel","include":"/channellist/logicalChannel/contentId,/channellist/logicalChannel/type,/channellist/logicalChannel/name,/channellist/logicalChannel/chanNo,/channellist/logicalChannel/pictures/picture/imageType,/channellist/logicalChannel/pictures/picture/href,/channellist/logicalChannel/foreignsn,/channellist/logicalChannel/externalCode,/channellist/logicalChannel/sysChanNo,/channellist/logicalChannel/physicalChannels/physicalChannel/mediaId,/channellist/logicalChannel/physicalChannels/physicalChannel/fileFormat,/channellist/logicalChannel/physicalChannels/physicalChannel/definition"}],"metaDataVer":"Channel/1.1","channelNamespace":"2","filterlist":[{"key":"IsHide","value":"-1"}],"returnSatChannel":0}
                payload = json.dumps(data)

                response = s.post(page, data=payload, headers = headers)
                if (response.status_code == 200):

                    allChannels  = channels(json.loads(response.text))

                    # get actual program +/- 4 h
                    actTime = datetime.now()
                    tStart = actTime - timedelta(hours=4)
                    tStop = actTime + timedelta(hours=4)

                    page = 'https://web.magentatv.de/EPG/JSON/PlayBillList?userContentFilter=1992763264&sessionArea=1&SID=ottall&T=Windows_firefox_67'

                    data = {"type":2,"isFiltrate":0,"orderType":4,"isFillProgram":1,"channelNamespace":"3","offset":0,"count":-1,"properties":[{"name":"playbill","include":"subName,id,name,starttime,endtime,channelid,ratingid,seriesID,genres,relatedVodIds,tipType,externalIds"}],"endtime": tStop.strftime('%Y%m%d%H%M00'),"begintime": tStart.strftime('%Y%m%d%H%M00')}
                    payload = json.dumps(data)

                    response = s.post(page, data=payload, headers = headers)
                    if (response.status_code == 200):

                        playlist = json.loads(response.text)

                        for item in playlist['playbilllist']:

                            if 'starttime' in item:

                                startPlay = item ['starttime']
                                startPlay = startPlay [:19]

                                # strptime bug
                                #startDT = datetime.strptime(startPlay, '%Y-%m-%d %H:%M:%S')
                                startDT = datetime(*(time.strptime(startPlay, '%Y-%m-%d %H:%M:%S')[0:6]))
                                start = ('%02i' % startDT.hour) + ':' + ('%02i' % startDT.minute)

                                stopPlay = item ['endtime']
                                stopPlay = stopPlay [:19]

                                # strptime bug
                                #stopDT = datetime.strptime(stopPlay, '%Y-%m-%d %H:%M:%S')
                                stopDT = datetime(*(time.strptime(stopPlay, '%Y-%m-%d %H:%M:%S')[0:6]))
                                stop = ('%02i' % stopDT.hour) + ':' + '%02i' % (stopDT.minute)

                                if(startDT<=actTime) & (stopDT>actTime):

                                    title = item ['name']
                                    chID = item ['channelid']
                                    url = ''

                                    channel = allChannels.getChannel(chID)

                                    thumb = channel.picture
                                    channelName = channel.name
                                    channelNo = int(channel.number)

                                    fulltitle = ('%03i ' % channelNo) + channelName
                                    title = title + '\n' + start + ' - ' + stop

                                    li = xbmcgui.ListItem(label= fulltitle, thumbnailImage=thumb)
                                    li.setInfo('video', { 'plot': title })
                                    xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


if __name__ == '__main__':

    ADDON = xbmcaddon.Addon()
    ADDON_NAME = ADDON.getAddonInfo('name')
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = urlparse.parse_qs(sys.argv[2][1:])

    PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode("utf-8")
    if not xbmcvfs.exists(PROFILE): xbmcvfs.mkdirs(PROFILE)
    COOKIE = os.path.join(PROFILE, "cookie.db")


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
    elif PARAMS.has_key('TV'):
            magenta.showTV()
    elif PARAMS.has_key('settings'):
            ADDON.openSettings()
    else:
        magenta.showMenu()





