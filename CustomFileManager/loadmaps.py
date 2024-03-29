import urllib, urllib.request as urllib2, time, re
import json

url_raw = "http://atlas.dustforce.com/gi/downloader.php?id=%d"

_default_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels/"

config_file = './_config.json'
try:
    with open(config_file, 'r') as f:
        config_dict = json.load(f)
except FileNotFoundError:
    config_dict = {}
dest_dir = config_dict.get('level_dir', _default_dir) + '/%s'


def download_map(id, dir=dest_dir, debug=False, save_file=True):
    url = url_raw % id
    url_data = urllib2.urlopen(url)
    headers = url_data.info()
    if debug: print(headers)
    content = url_data.read()
    if debug: print(content)
    if content:
        name = re.search("filename=\"(.*?)\"", headers["content-disposition"])
        if name:
            name = name.group(1)
            name = name.replace('\\', '%5C')
            if save_file:
                try:
                    map = urllib2.URLopener()
                    map.retrieve(url, dir % name)
                except FileNotFoundError:
                    print("error: Could not save file")
                    return None
                if debug: print(id, name)
            return name
        else:
            if debug: print("error:\n", content.read())
    return None


def download_all(start, end=1000000, debug=False):
    blank_count = 0
    MAX_BLANKS = 5
    for i in range(start, end):
        success = download_map(i, debug=debug)
        if not success:
            # apparently, there are some IDs that do not have maps
            # the only thing I can do to know that I've reached the end
            # is to find enough empty IDs in a row
            blank_count += 1
            if blank_count > MAX_BLANKS:
                break
        else:
            blank_count = 0


if __name__ == '__main__':
    download_all(8315, debug=True)
