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

def mainSelector():

    xbmcplugin.setContent(HANDLE, 'files')

    li = xbmcgui.ListItem(label='Startseite', thumbnailImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(HANDLE, PATH + '?mode=start', li, True)

    li = xbmcgui.ListItem(label='TV', thumbnailImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(HANDLE, PATH + '?mode=tv', li, True)

    li = xbmcgui.ListItem(label='Trailer Saphirblau', thumbnailImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(HANDLE, PATH + '?mode=trailer', li, True)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

def showChannels():

    xbmcplugin.setContent(HANDLE, 'episodes')

    # login to page
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

        # token has been received
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

def showTV():

    xbmcplugin.setContent(HANDLE, 'episodes')

    # login to page
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

        # token has been received
        token = s.cookies['CSRFSESSION']
        tm = int(time.time())

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

            channels = json.loads(response.text)

            # we want +/- 5 h
            tStart = datetime.now() - timedelta(hours=5)
            tStop = datetime.now() + timedelta(hours=5)

            # get programm
            page = 'https://web.magentatv.de/EPG/JSON/PlayBillList?userContentFilter=1992763264&sessionArea=1&SID=ottall&T=Windows_firefox_67'

            data = {"type":2,"isFiltrate":0,"orderType":4,"isFillProgram":1,"channelNamespace":"3","offset":0,"count":-1,"properties":[{"name":"playbill","include":"subName,id,name,starttime,endtime,channelid,ratingid,seriesID,genres,relatedVodIds,tipType,externalIds"}],"endtime": tStop.strftime('%Y%m%d%H%M00'),"begintime": tStart.strftime('%Y%m%d%H%M00')}
            payload = json.dumps(data)

            response = s.post(page, data=payload, headers = headers)

            if (response.status_code == 200):

                playlist = json.loads(response.text)
                actTime = datetime.now()

                for item in playlist['playbilllist']:

                    startPlay = item ['starttime']
                    startPlay = startPlay [:19]
                    startDT = datetime.strptime(startPlay, '%Y-%m-%d %H:%M:%S')

                    stopPlay = item ['endtime']
                    stopPlay = stopPlay [:19]
                    stopDT = datetime.strptime(stopPlay, '%Y-%m-%d %H:%M:%S')

                    # show actual programm
                    if(startDT<=actTime) & (stopDT>actTime):

                        title = item ['name']
                        channelName = ''

                        channel = item ['channelid']
                        for item in channels ['channellist']:
                            if(item ['contentId'] == channel):
                                channelName = item ['name']

                        desc =  startPlay + ' - ' +  title
                        url = ''

                        li = xbmcgui.ListItem(label=channelName, thumbnailImage='') # no thumb yet
                        li.setInfo('video', { 'plot': desc })

                        xbmcplugin.addDirectoryItem(HANDLE, url, li, False)

        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

def showTrailer():

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

        # get details of playlist
        url = 'https://wcss.t-online.de/cvss/IPTV2015%40Mobile/vodclient/v1/assetdetails/44593/GN_MV007404670000?$whiteLabelId=megathek&%24theme=hdr&%24resolution=webClient1280&%24cid=8TBRGG8HcdgKubRt5Jxoq5iEoi5DY1oR&%24redirect=false&%24hideAdult=true'
        response = s.get(url)

        details = json.loads(response.text)

        trailerInfo = details['content']['contentInformation']['trailers'][0]['href']

        # get trailer info
        response = s.get(trailerInfo)
        tailerDetails = json.loads(response.text)

        # get playlist
        playlist =  tailerDetails['content']['feature']['representations'][0]['contentPackages'][0]['media']['href']
        response = s.get(playlist)

        pattern = '<media.*?src="(.*?)"'
        m = re.search(pattern,response.text)
        if m is not None:
            # play
            url = m.group(1)

            is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)

            if is_helper.check_inputstream():
                playitem = xbmcgui.ListItem(path=url)
                playitem.setProperty('inputstreamaddon', is_helper.inputstream_addon)
                playitem.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)

                xbmc.Player().play(item=url, listitem=playitem)

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
        elif mode == 'tv':
            showTV()
        elif mode == 'trailer':
            showTrailer()
        else:
            mainSelector()
    else:
        mainSelector()





