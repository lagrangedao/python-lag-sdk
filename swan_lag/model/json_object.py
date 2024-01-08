import json


class JsonDictObject(object):
    def __setattr__(self, key, value):
        if key == '__dict__' and isinstance(value, dict):
            for k, v in value.items():
                if k not in class_key_dict:
                    self.__dict__[k] = v
                    continue

                if isinstance(v, list):
                    cls = class_key_dict[k]
                    data_list = []
                    for data in v:
                        obj = cls()
                        obj.__dict__ = data
                        data_list.append(obj)

                    self.__dict__[k] = data_list
                elif isinstance(v, dict):
                    cls = class_key_dict[k]
                    obj = cls()
                    obj.__dict__ = v
                    self.__dict__[k] = obj
                else:
                    self.__dict__[k] = v
        else:
            self.__dict__[key] = value

    def parse_dict_to_obj(self, data: dict):
        self.__dict__ = data

    def parse_json_to_obj(self, data: str):
        parseData = json.loads(data.strip('\t\r\n'))
        self.__dict__ = parseData


class_key_dict = {}
