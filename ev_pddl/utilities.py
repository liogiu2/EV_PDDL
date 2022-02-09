import json
import importlib.resources as pkg_resources
import json_data

def parse_json(jsonfile):
    with pkg_resources.open_text(json_data, jsonfile+'.json') as json_file:
        json_data_parsed = json.load(json_file)
    return json_data_parsed
    
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def singleton(self, *args, **kw):
    """
    The decorator is used to make sure that only one instance of the class is created in the program.
    """
    instances = {}

    def _singleton(*args, **kw):
        if self not in instances:
            instances[self] = self(*args, **kw)
        return instances[self]
    return _singleton