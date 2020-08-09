#!/usr/bin/env python3

import re
import sys
import dataclasses
import urllib.parse
from typing import List
from pathlib import Path
from datetime import datetime
from functools import reduce
import kanautil
import readutil
from jsonfeed import Feed, Item, Element

@dataclasses.dataclass
class MenuItem(Item):
    _price: int = dataclasses.field(default=None)

@dataclasses.dataclass
class StoreItem(Item):
    _address: str = dataclasses.field(default=None)
    _phoneno: str = dataclasses.field(default=None)

def get_dondon_menuitems(bsoup, updated: datetime, page_url: str) -> List[Item]:
    text = bsoup.get_text()
    text = kanautil.to_halfwidth(text, digit=True, ascii=False, kana=False)
    text = re.sub(r"new!|\s+(?=円)", "", text)
    text = re.sub(r"各(\d+)", r"各 \1", text)
    tokens = text.split()
    if not tokens:
        return []

    itemsources = []
    names = []
    prefix = None
    for i, token in enumerate(tokens):
        if token == "各":
            for t in tokens[0:i]:
                names.append(t)
        elif token.endswith("円"):
            if names:
                for name in names:
                    itemsources.append({"name": name, "price": token})
            else:
                if prefix is None:
                    prefix = " ".join(tokens[0:i - 1])
                itemsources.append({"name": f"{prefix} {tokens[i - 1]}".strip(), "price": token})

    img_bsoup = bsoup.select_one("img")
    image_url = urllib.parse.urljoin(page_url, img_bsoup.get("src")) if img_bsoup else None

    items = []
    for itemsource in itemsources:
        id = re.sub("[\s\.()]", "_", kanautil.to_roman(itemsource['name']))
        price = int(re.sub(r"\D*(\d+)円", r"\1", itemsource["price"]))
        items.append(MenuItem(
            id=f"dondon.{id}",
            title=itemsource["name"],
            date_modified=updated,
            image=image_url,
            _price=price
        ))
    return items

def get_dondon_menufeed(url: str, basefeed: Feed) -> Feed:
    top_bsoup = readutil.get_bsoup(url, cache_path="readcache/dondon_menu.html", encoding="sjis")

    # Last updated this content
    updated_match = re.search(r"(\d{4}\.\d{2}\.\d{2})更新", top_bsoup.get_text())
    if updated_match:
        updated = datetime.strptime(updated_match.group(1), r"%Y.%m.%d")

    items = []
    for entry_bsoup in top_bsoup.select("td > div"):
        items.extend(get_dondon_menuitems(entry_bsoup, updated, url))

    return dataclasses.replace(basefeed, items=items)

def get_dondon(to: str):
    favicon_url = "http://www.dondon.co.jp/favicon.ico"
    icon_url = "https://dondon-recruit.jp/static_contents/dondon-recruit.jp/contents/root/production/pc/common/img/pc/header_logo.png"
    menu_url = "http://www.dondon.co.jp/menu/index.html"

    save_to = Path(to)
    basefeed = Feed(title="どんどん")
    basefeed.home_page_url = "http://www.dondon.co.jp/index.html"
    basefeed.favicon = str(Path("image", "favicon.ico"))
    basefeed.icon = str(Path("image", "icon.png"))

    readutil.get_blob(favicon_url, cache_path=save_to / basefeed.favicon)
    readutil.get_blob(icon_url, cache_path=save_to / basefeed.icon)

    print(f"{basefeed.title} -> {save_to.resolve()}")

    # Get menu feed
    print(f"(1/3) Getting menu info from '{menu_url}'...", end="")
    menufeed = get_dondon_menufeed(menu_url, basefeed)
    print(f" ({len(menufeed.items)} items)")

    # Save menu image files
    print(f"(2/3) Saving or confirming menu images...", end="")
    for item in menufeed.items:
        image_url = item.image
        if image_url:
            image_name = Path(urllib.parse.urlparse(image_url).path[1:].replace("/", "__"))
            image_path = Path(
                "image",
                image_name.stem + item.date_modified.strftime("__%Y%m%d") + image_name.suffix)
            readutil.get_blob(image_url, cache_path=save_to / image_path)
            item.image = str(image_path)
    print(f" ({len(list(filter(lambda x: x.image, menufeed.items)))} files)")

    # Output menu feed
    menufeed_path = save_to / "menu.json"
    print(f"(3/3) Writing menu feed to '{menufeed_path}'...", end="")
    with open(menufeed_path, "w", encoding="utf-8") as f:
        f.write(menufeed.to_json(indent=2))
        print(f" ({menufeed_path.stat().st_size} bytes)")

    print(f"Finished")

def main(argv):
    get_dondon("./dondon")

if __name__ == "__main__":
    main(sys.argv)
