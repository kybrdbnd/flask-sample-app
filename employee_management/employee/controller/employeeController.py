def update_name_slug(data):
    name = data['name']
    nameObjs = name.split(' ')
    nameObjs = list(map(lambda x: x.lower(), nameObjs))
    data['nameSlug'] = '-'.join(nameObjs)
    return data
