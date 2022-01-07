import io
import zipfile
import requests


def download_zip(url: str, filename):
    response = requests.post(url)
    with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
        zip_ref.extractall("")
    return f"./{filename}"


def create_storage():
    download_zip(url="https://vk.com/doc57748892_625663153?hash=9e069afd77f65a322d&dl=10c1aacc09d43a2c6f",
                 filename="storage")
    return True


def create_static():
    download_zip(url="https://vk.com/doc57748892_625662964?hash=c8debf1a5446760d7e&dl=28666bef7036f07881",
                 filename="static")
    return True
