#!/usr/bin/env python3

import json
from datetime import datetime
import dataclasses
from typing import List

def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError()

@dataclasses.dataclass
class Element:
    def to_json(self):
        return json.dumps(dataclasses.asdict(self), indent=2, ensure_ascii=False, default=json_default)
    # def to_xml(self):

@dataclasses.dataclass
class Content(Element):
    pass

@dataclasses.dataclass
class Entry(Element):
    id: str
    title: str
    updated: datetime
    content: Content = dataclasses.field(default=None)

@dataclasses.dataclass
class Parson(Element):
    name: str
    uri: str = dataclasses.field(default=None)
    email: str = dataclasses.field(default=None)

@dataclasses.dataclass
class Link(Element):
    href: str
    rel: str = dataclasses.field(default=None)
    type: str = dataclasses.field(default=None)
    hreflang: str = dataclasses.field(default=None)
    title: str = dataclasses.field(default=None)
    length: str = dataclasses.field(default=None)

@dataclasses.dataclass
class Feed(Element):
    id: str
    title: str
    updated: datetime
    author: List[Parson] = dataclasses.field(default=None)
    contributer: List[Parson] = dataclasses.field(default=None)
    category: List[str] = dataclasses.field(default=None)
    generator: str = dataclasses.field(default=None)
    icon: str = dataclasses.field(default=None)
    logo: str = dataclasses.field(default=None)
    link: List[Link] = dataclasses.field(default=None)
    rights: str = dataclasses.field(default=None)
    subtitle: str = dataclasses.field(default=None)
    entry: List[Entry] = dataclasses.field(default=None)

def test():
    feed = Feed(
        id="feed-0001",
        title="sample-feed",
        updated=datetime.strptime("9999-12-31", r"%Y-%m-%d"),
        link=[Link(href="a", rel="a")],
        entry=[
            Entry(
                id="menu-0001",
                title="menu-one",
                updated=datetime.strptime("9999-12-31", r"%Y-%m-%d"),
                content=Content()
            ),
            Entry(
                id="menu-0001",
                title="menu-one",
                updated=datetime.strptime("9999-12-31", r"%Y-%m-%d"),
                content=Content()
            )
        ]
    )
    feed.icon = "icoooooooon"
    print(feed.to_json())

if __name__ == "__main__":
    test()
