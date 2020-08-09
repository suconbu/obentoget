#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup

def _get_content(url: str, text: bool, content_encoding: str=None):
    try:
        if url.startswith("file:"):
            mode = "r" if text else "rb"
            with open(url[5:], mode=mode, encoding=content_encoding) as f:
                content = f.read()
        else:
            response = requests.get(url)
            if text:
                response.encoding = content_encoding if content_encoding else response.apparent_encoding
                content = response.text
            else:
                content = response.content
        return content
    except Exception as ex:
        print(ex)
        return None

def _get_content_cached(url: str, cache_path: str, text: bool, content_encoding: str=None):
    content = None
    cache_encoding = "utf-8" if text else None
    if cache_path and os.path.exists(cache_path):
        mode = "r" if text else "rb"
        with open(cache_path, mode, encoding=cache_encoding) as f:
            content = f.read()
    if content is None:
        content = _get_content(url, text, content_encoding)
        if cache_path:
            dirname = os.path.dirname(cache_path)
            os.makedirs(dirname, exist_ok=True)
            mode = "w" if text else "wb"
            with open(cache_path, mode, encoding=cache_encoding) as f:
                f.write(content)
    return content

def get_blob(url: str, cache_path=None) -> bytes:
    return _get_content_cached(url, cache_path, False)

def get_bsoup(url: str, cache_path=None, encoding: str=None) -> BeautifulSoup:
    """指定のURLが指すリソースをテキストとして取得します。
    file:で始まるURLを指定するとローカルファイルを扱うことができます。"""
    content = _get_content_cached(url, cache_path, True, encoding)
    return BeautifulSoup(content, "html.parser") if content else None

def test():
    bs = get_bsoup("https://www.google.com/")
    assert(bs != None)
    title = bs.select_one("title").get_text()
    assert(title == "Google")
    print("Success")

    bs = get_bsoup("https://www.google.com/", "cache/www_google_com.html")
    assert(bs != None)
    title = bs.select_one("title").get_text()
    assert(title == "Google")
    print("Success")

    bs = get_bsoup("file:./test_google.html")
    assert(bs != None)
    title = bs.select_one("title").get_text()
    assert(title == "Google")

if __name__ == "__main__":
    test()
