from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

base_url = "http://interview.agileengine.com"


def get_auth_token():
    auth_url = base_url + "/auth"
    headers = {"Content-type": "application/json"}
    payload = {"apiKey": "23567b218376f79d9415"}
    with requests.Session() as http_session:
        response = http_session.post(auth_url, json=payload, headers=headers)

    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def get_image_one(page_num):
    images_url = base_url + f"/images?page={page_num}"
    headers = {"Content-type": "application/json"}
    headers.update(get_auth_token())

    with requests.Session() as http_session:
        response = http_session.get(images_url, headers=headers)
    return response.json()


def get_pictures():
    pictures = defaultdict(list)
    page_num = 1
    page = get_image_one(page_num=page_num)
    pictures["pictures"].extend(page["pictures"])
    pageCount = page["pageCount"]
    with ThreadPoolExecutor(max_workers=pageCount) as executor:
        futures = [executor.submit(get_image_one, n) for n in range(2, pageCount)]
        results = [future.result() for future in futures]

    for result in results:
        try:
            pictures["pictures"].extend(result["pictures"])
        except KeyError:
            pass

    return pictures


def get_image_metadata_one(image_id):
    meta_url = base_url + f"/images/{image_id}"
    headers = {"Content-type": "application/json"}
    headers.update(get_auth_token())

    with requests.Session() as http_session:
        response = http_session.get(meta_url, headers=headers)
    return response.json()


def get_images_metadata(ids):
    metadatas = list()
    with ThreadPoolExecutor(max_workers=len(ids)) as executor:
        futures = [executor.submit(get_image_metadata_one, _id) for _id in ids]
        results = [future.result() for future in futures]

    for result in results:
        metadatas.append(result)

    return results


