# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
import logging
import xbmcaddon
import xbmcgui
import xbmc
import requests
import json
import random
import string

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

def get_uuid():
    uuid = kodiutils.get_setting('uuid')
    if not uuid:
        stringLength = 10
        letters = string.ascii_lowercase
        uuid = ''.join(random.choice(letters) for i in range(stringLength))
        logger.info('Setting Shiri X-UUID to: ' + uuid)
        kodiutils.set_setting('uuid', uuid)
    return uuid

def next_song(headers):
    next_url = 'https://api.shiriapp.org.il/api/session/next-song'
    song = requests.post(next_url, headers=headers, verify=False).json()
    file = song['file_url']
    title = song['title'].encode('utf8')
    try:
        artist = song['artist']['pretty_name'].encode('utf8')
    except TypeError:
        artist = ''
    try:
        album = song['album']['pretty_name'].encode('utf8')
    except TypeError:
        album = ''
    duration = song['file_duration']

    listitem = xbmcgui.ListItem(title)
    listitem.setInfo('music', {
        'title': title,
        'artist': artist,
        'album': album,
        'mediatype': 'song',
        'duration': duration
    })
    listitem.setPath(file)
    return listitem

def run():
    uuid = get_uuid()
    headers = {'Content-Type': 'application/json', 'X-UUID': uuid}

    # Set artists
    payload = {'ids': [10, 11, 12, 13,  14]}
    artists_url = 'https://api.shiriapp.org.il/api/session/current-artist/set-all'
    requests.post(artists_url, headers=headers, data=json.dumps(payload), verify=False)

    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()

    for i in range(10):
        listitem = next_song(headers)
        playlist.add(listitem.getPath(), listitem, i+1)

    xbmc.Player().play(playlist)
