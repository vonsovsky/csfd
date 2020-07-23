import unidecode


def beautify(name):
    name = unidecode.unidecode(name)
    name = name.lower()
    name = name.replace('"', '').replace(',', '').replace(':', '').replace('-', '')
    name = ' '.join(name.split())
    return name