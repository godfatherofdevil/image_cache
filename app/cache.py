from collections import defaultdict
import threading

from app.singletonmeta import SingletonMeta

search_terms = {"author", "camera", "tags"}


class PictureCache(metaclass=SingletonMeta):
    def __init__(self, pictures, metadata):
        self.pictures = pictures  # dict
        self.metadata = metadata  # dict
        self.search_index = defaultdict(list)

        self.build_search_index()

    def build_search_index(self):
        for meta in self.metadata:
            for term in search_terms:
                try:
                    _id, cropped, full = meta["id"], meta["cropped_picture"], meta["full_picture"]
                except KeyError:
                    continue
                self.search_index[term].append({
                    "id": _id, "cropped_picture": cropped, "full_picture": full
                })

    def get_term(self, term):
        return self.search_index.get(term, [])

    def rebuild_search_index(self, pictures, metadata):
        _lock = threading.Lock()
        with _lock:
            self.pictures = pictures
            self.metadata = metadata
            self.build_search_index()

