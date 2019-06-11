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

def run():
    uuid = get_uuid()
    headers = {'Content-Type': 'application/json', 'X-UUID': uuid}

    # Set artists
    payload = {'ids': [66, 52, 43]}
    artists_url = 'https://api.shiriapp.org.il/api/session/current-artist/set-all'
    requests.post(artists_url, headers=headers, data=json.dumps(payload), verify=False)

    # Get song
    next_url = 'https://api.shiriapp.org.il/api/session/next-song'
    song = requests.post(next_url, headers=headers, verify=False).json()
    file = song['file_url']
    title = song['title'].encode('utf8')
    listitem = xbmcgui.ListItem(title)
    listitem.setInfo('video', {'Title': title})
    xbmc.Player().play(file, listitem)
