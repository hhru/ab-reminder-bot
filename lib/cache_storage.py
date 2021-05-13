from lib.utils import load_json_file, save_json_file


class Storage:
    def __init__(self, storage_key):
        self.__cache_file = f'storage_{storage_key}.json'
        self.__cache = load_json_file(self.__cache_file, {})

    def __len__(self):
        return len(self.__cache)

    def __getitem__(self, key):
        if key not in self.__cache:
            return {}

        return self.__cache[key]

    def __setitem__(self, key, value):
        self.__cache[key] = value
        save_json_file(self.__cache_file, self.__cache)

    def __delitem__(self, key):
        if key not in self.__cache:
            raise KeyError

        del self.__cache[key]
        save_json_file(self.__cache_file, self.__cache)

    def __iter__(self):
        return self.__cache.__iter__()

    def __reversed__(self):
        return self.__cache.__reversed__()

    def __contains__(self, item):
        return item in self.__cache

    def get(self, key, default=None):
        return self.__cache.get(key, default)

    def update(self, value):
        self.__cache.update(value)
        save_json_file(self.__cache_file, self.__cache)
