from app.get_images import get_pictures, get_images_metadata
from app.cache import PictureCache


def before_start():
    """
    populate the cache and store it
    :return:
    """
    pictures = get_pictures()
    picture_ids = [picture["id"] for picture in pictures["pictures"]]
    metadata = get_images_metadata(picture_ids)

    cache = PictureCache(pictures=pictures, metadata=metadata)

    return cache
