#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup

def __get_content(url: str, text: bool, encoding: str=None):
    try:
        if url.startswith("file:"):
            mode = "r" if text else "rb"
            with open(url[5:], mode=mode, encoding=encoding) as f:
                content = f.read()
        else:
            response = requests.get(url)
            if text:
                response.encoding = encoding if encoding else response.apparent_encoding
                content = response.text
            else:
                content = response.content
        return content
    except Exception as ex:
        print(ex)
        return None

def __get_content_cached(url: str, cache_path: str, text: bool, encoding: str=None):
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            content = f.read()
    else:
        content = __get_content(url, text, encoding)
        mode = "w" if text else "wb"
        if cache_path:
            with open(cache_path, mode, encoding="utf-8") as f:
                f.write(content)
    return content

def get_blob(url: str, cache_path=None) -> bytes:
    return __get_content_cached(url, cache_path, False)

def get_bsoup(url: str, cache_path=None, encoding: str=None) -> BeautifulSoup:
    """指定のURLが指すリソースをテキストとして取得します。
    file:で始まるURLを指定するとローカルファイルを扱うことができます。"""
    content = __get_content_cached(url, cache_path, True, encoding)
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
