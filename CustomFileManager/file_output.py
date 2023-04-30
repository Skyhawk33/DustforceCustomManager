import json
from dustmaker import LevelType
from CustomFileManager.publishedsort import Published

config_file = './_config.json'
_default_level_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels"
_default_index = './_level_index.json'


def csv_string(index, fields):
    csv = ''
    csv += ','.join(fields) + '\n'

    for id, level in index.items():
        row = ''
        for field in fields:
            field = field.lower().replace(' ', '_')
            if field == 'id':
                row += id
            elif field == 'name':
                row += '"' + level['filename'].rsplit('-', 1)[0].replace('-', ' ').replace('   ', ' - ') + '"'
            elif field == 'url':
                row += 'https://dustkid.com/level/%s/all/0 ' % level['filename'].replace(' ', '%20')
            elif field == 'level_type' and 'level_type' in level:
                row += 'boss' if level['level_type'] == 5 else LevelType(level['level_type']).name.lower()
            elif field == 'published' and 'published' in level:
                row += Published(level['published']).name.lower()
            elif field in index[id]:
                row += '"' + index[id][field].replace(',', ';') + '"'
            row += ','
        csv += row[:-1] + '\n'
    return csv


def filter_index(base_index, mask_index, mask_condition):
    mask_set = set()
    for key in mask_index:
        if mask_condition(mask_index[key]):
            mask_set.add(key)
    filter_dict = {}
    for key in mask_set:
        if key in base_index:
            filter_dict[key] = base_index[key]
    return filter_dict


def main():
    try:
        with open(config_file, 'r') as f:
            config_dict = json.load(f)
    except FileNotFoundError:
        config_dict = {}

    index_file = config_dict.get('index_file', _default_index)

    with open(index_file, 'r') as f:
        level_dict = json.load(f)
    # with open(index_file.replace('index', 'index_bck_20221019'), 'r') as f2:
    #     level_dict2 = json.load(f2)
    #
    # print(index_file.replace('index', 'index_bck_20221019'))
    # l = sorted(list(set(level_dict).difference(level_dict2)))
    # for k in l:
    #     print(level_dict[k])
    # return

    filenames = []
    # filenames = ['_level_index_a.json', '_level_index_b.json', '_level_index_c.json',
    #              '_level_index_d.json', '_level_index_e.json']

    filter_dict = level_dict
    for name in filenames:
        with open(name, 'r') as f:
            mask = json.load(f)
        filter_dict = filter_index(filter_dict, mask, (lambda level: 'rank' not in level or level['rank'] != 'SS'))

    # filter_dict = filter_index(filter_dict, filter_dict,
    #                            (lambda level: level['readable'] and
    #                                           level['level_type'] in (0, 6,) and
    #                                           level['has_end'] and 'ss_impossible' not in level and
    #                                           # level['published'] == 3 and
    #                                           ('rank' not in level or level['rank'] != 'SS')))

    # output = csv_string(filter_dict, ('ID', 'Name', 'URL', 'Level Type', 'Published', 'SS Difficult'))
    # output = csv_string(filter_dict, ('ID', 'filename'))
    output = csv_string(filter_dict, ('URL', 'filename', 'Name', 'Level Type', 'Published'))
    # l = output.splitlines()
    # l.sort()
    # output = '\n'.join(l)
    print(output)
    print(output.count('\n'))

    # with open(output_path, 'w') as f:
    #     f.write(csv)


if __name__ == '__main__':
    main()
