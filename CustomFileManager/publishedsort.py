import os
import re
import urllib.request as url
from enum import IntEnum
import json

read_sub = ''  # 'noflag/'
website = 'https://atlas.dustforce.com/%s/%s'

_default_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/"

config_file = './_config.json'
try:
    with open(config_file, 'r') as f:
        config_dict = json.load(f)
except FileNotFoundError:
    config_dict = {}
BASE = config_dict.get('level_dir', _default_dir)


class Published(IntEnum):
    UNKNOWN = 0
    UNPUBLISHED = 1
    HIDDEN = 2
    VISIBLE = 3


def get_published_status(map_name):
    name_split = list(map_name.rsplit('-', 1))
    name = name_split[0]
    num = name_split[1]
    try:
        data = url.urlopen(website % (num, name))
        data = str(data.read())
        # There's no definite way to tell if a map is published,
        # but if the name is not visible, that probably means the map is not visible
        if r'<meta property="og:title" content=" - a Dustforce map" >' in data:
            # print(map_name, ',HIDDEN')
            return Published.HIDDEN
        else:
            # AUTHOR NAME
            # print(map_name, ','+re.search(r'by </span><strong><a href="http://atlas.dustforce.com/user/([^"]+)"', data).group(1))
            return Published.VISIBLE
    except Exception:
        # print(map_name, ',UNPUBLISHED')
        return Published.UNPUBLISHED


if __name__ == '__main__':
    for map_name in os.listdir(BASE + read_sub):  # ('w-%d' % d for d in range(11060, 11830)):
        try:
            status = get_published_status(map_name)
            print(map_name, Published(status).name)
        except Exception:
            print(map_name, '---------------------------------------------------------------')
            continue
        if status == Published.HIDDEN:
            os.rename(BASE + read_sub + map_name, BASE + 'hidden/' + map_name)
        elif status == Published.UNPUBLISHED:
            os.rename(BASE + read_sub + map_name, BASE + 'nonpublished/' + map_name)
