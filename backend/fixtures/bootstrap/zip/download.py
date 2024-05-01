import io
import os
import zipfile
import requests


def download_zip(url: str, filename):
    response = requests.post(url)
    with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
        zip_ref.extractall("")
    return f"./{filename}"


def create_storage():
    download_zip(url=os.environ.get("STORAGE_ZIP_URL"),
                 filename="storage")
    return True


def create_static():
    download_zip(url=os.environ.get("STATIC_ZIP_URL"),
                 filename="static")
    return True
