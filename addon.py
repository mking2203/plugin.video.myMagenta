#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
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

def mainSelector():

    xbmcplugin.setContent(HANDLE, 'files')

    li = xbmcgui.ListItem(label='Startseite', thumbnailImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(HANDLE, PATH + '?mode=start', li, True)

    li = xbmcgui.ListItem(label='TV', thumbnailImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(HANDLE, PATH + '?mode=tv', li, True)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

def showChannels():

    xbmcplugin.setContent(HANDLE, 'episodes')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://web.magentatv.de/EPG/' }

    uid = uuid.uuid4().hex

    data = {
        "terminalid":"00:00:00:00:00:00",
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

    s = requests.Session()
    response = s.post('https://web.magentatv.de/EPG/JSON/Authenticate?SID=firstup&T=Windows_firefox_67', headers = headers, data=payload)

    if (response.status_code == 200):

        token = s.cookies['CSRFSESSION']
        tm = int(time.time())

        # startseite
        page = 'https://web.magentatv.de/EPG/rest/hub/79983?tm=' + str(tm)


        response = s.get(page, headers = headers)
        if (response.status_code == 200):

            j = json.loads(response.text)

            for item in j ['groups']:

                section = item['title']
                li = xbmcgui.ListItem("[COLOR gold]" + section + "[/COLOR]")
                li.setProperty("IsPlayable", "false")
                xbmcplugin.addDirectoryItem(handle=HANDLE, url="", listitem=li)

                for t in item ['tiles']:

                    title= t['formattedContent']['title']
                    shortName = ''
                    thumb = ''

                    url = ''

                    if 'shortName' in t['formattedContent']:
                        shortName = t['formattedContent']['shortName']
                    if 'backgroundUrl' in t['formattedContent']:
                        thumb = t['formattedContent']['backgroundUrl']

                    desc = title + '\n' + shortName

                    li = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
                    li.setInfo('video', { 'plot': desc })

                    xbmcplugin.addDirectoryItem(HANDLE, url, li, False)


        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

if __name__ == '__main__':

    ADDON = xbmcaddon.Addon()
    ADDON_NAME = ADDON.getAddonInfo('name')
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = urlparse.parse_qs(sys.argv[2][1:])

    if PARAMS.has_key('mode'):
        mode = PARAMS['mode'][0]
        if mode == 'start':
            showChannels()
        else:
            mainSelector()
    else:
        mainSelector()





