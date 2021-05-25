from lib.utils import load_json_file, save_json_file


class Storage:
    def __init__(self, storage_key):
        self._cache_file = f'storage_{storage_key}.json'
        self._cache = load_json_file(self._cache_file, {})

    def __len__(self):
        return len(self._cache)

    def __getitem__(self, key):
        if key not in self._cache:
            return {}

        return self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value
        save_json_file(self._cache_file, self._cache)

    def __delitem__(self, key):
        if key not in self._cache:
            raise KeyError

        del self._cache[key]
        save_json_file(self._cache_file, self._cache)

    def __iter__(self):
        return self._cache.__iter__()

    def __reversed__(self):
        return self._cache.__reversed__()

    def __contains__(self, item):
        return item in self._cache

    def get(self, key, default=None):
        return self._cache.get(key, default)

    def update(self, value):
        self._cache.update(value)
        save_json_file(self._cache_file, self._cache)
