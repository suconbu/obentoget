#!/usr/bin/env python3

import re
import sys
from datetime import datetime
import kanautil
import readutil
import dataclasses
from typing import List
from functools import reduce
from miniatom import Feed, Entry, Content

@dataclasses.dataclass
class Company:
    id: str
    name: str

@dataclasses.dataclass
class MenuContent(Content):
    price: int
    image: str = dataclasses.field(default=None)

@dataclasses.dataclass
class StoreContent(Content):
    address: str
    phoneno: str

@dataclasses.dataclass
class MenuItem:
    name: str
    price: str

def get_dondon_menu_entry(company: Company, updated: datetime, node):
    text = re.sub(r"new!|\s+(?=円)", "", node.get_text())
    text = kanautil.to_halfwidth(text, digit=True, ascii=False, kana=False)
    text = re.sub(r"各(\d+)", r"各 \1", text)
    tokens = text.split()
    if not tokens:
        return None

    items = []
    names = []
    prefix = None
    for i, token in enumerate(tokens):
        if token == "各":
            for t in tokens[0:i]:
                names.append(t)
        elif token.endswith("円"):
            if names:
                for name in names:
                    items.append(MenuItem(name=name, price=token))
            else:
                if prefix is None:
                    prefix = " ".join(tokens[0:i - 1])
                items.append(MenuItem(name=f"{prefix} {tokens[i - 1]}".strip(), price=token))

    img_node = node.select_one("img")
    image_url = img_node.get("src") if img_node else None

    entries = []
    for item in items:
        id = f"{company.id}:{kanautil.to_roman(item.name).replace(' ', '')}"
        price = int(re.sub(r"\D*(\d+)円", r"\1", item.price))
        entries.append(Entry(id, item.name, updated, MenuContent(price, image=image_url)))
    return entries

def get_dondon_menu_feed(company: Company, url: str) -> Feed:
    bsoup = readutil.get_bsoup_cached(url, cache="cache/dondon_menu.html", encoding="sjis")

    # Last updated this content
    updated_match = re.search(r"(\d{4}\.\d{2}\.\d{2})更新", bsoup.get_text())
    if updated_match:
        updated = datetime.strptime(updated_match.group(1), r"%Y.%m.%d")

    feed_entries = []
    for entry_node in bsoup.select("td > div"):
        entries = get_dondon_menu_entry(company, updated, entry_node)
        if entries:
            feed_entries.extend(entries)

    return Feed(id=company.id, title=company.name, updated=updated, entry=feed_entries)

def main(argv):
    company = Company(id="dondon", name="どんどん")
    menu_feed = get_dondon_menu_feed(company, "http://www.dondon.co.jp/menu/index.html")
    # menu_feed = get_dondon_menu_feed(company, "file:./sample/dondon_menu.txt")
    print(menu_feed.to_json())

def test(argv):
    base_feed = Feed(
        id="http://www.dondon.co.jp/",
        title="どんどん",
        updated="1111-11-11"
    )
    menu_feed = dataclasses.replace(base_feed, entry=[
        Entry(id="id0001", title="entry0001", updated="1111-11-11", content=MenuContent(198))
    ])
    print(menu_feed.to_json())

if __name__ == "__main__":
    main(sys.argv)
