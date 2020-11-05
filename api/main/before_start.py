import time

from app.get_images import get_pictures, get_images_metadata
from app.cache import PictureCache


CACHE_TIMEOUT = 60*60   # update cache every one hour


def before_start(reload=False):
    """
    populate the cache and store it
    :return:
    """
    pictures = get_pictures()
    picture_ids = [picture["id"] for picture in pictures["pictures"]]
    metadata = get_images_metadata(picture_ids)
    cache = PictureCache(pictures=pictures, metadata=metadata)
    if reload:
        cache.rebuild_search_index(pictures, metadata)

    return cache


def cache_manager():
    while True:
        time.sleep(CACHE_TIMEOUT)
        print("reloading cache")
        before_start(reload=True)

