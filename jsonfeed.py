#!/usr/bin/env python3

import json
from datetime import datetime
import dataclasses
from typing import List

@dataclasses.dataclass
class Element:
    def to_json(self, indent=None):
        d = self.__filter_none(dataclasses.asdict(self))
        return json.dumps(d, indent=indent, ensure_ascii=False, default=self.__json_default)

    def __filter_none(self, d: dict) -> dict:
        if isinstance(d, dict):
            return {k: self.__filter_none(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return list(self.__filter_none(v) for v in d)
        elif isinstance(d, tuple):
            return tuple(self.__filter_none(v) for v in d)
        else:
            return d

    def __remove_none_in_dict(self, d: dict):
        for key, value in list(d.items()):
            if isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    self.__remove_none_in_dict(v)
            else:
                if value is None:
                    del d[key]

    def __json_default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError()

@dataclasses.dataclass
class Parson(Element):
    name: str
    url: str = dataclasses.field(default=None)
    avatar: str = dataclasses.field(default=None)

@dataclasses.dataclass
class Attachment(Element):
    url: str
    mime_type: str
    title: str = dataclasses.field(default=None)
    size_in_bytes: int = dataclasses.field(default=None)
    duration_in_seconds: int = dataclasses.field(default=None)

@dataclasses.dataclass
class Item(Element):
    id: str
    url: str = dataclasses.field(default=None)
    external_url: str = dataclasses.field(default=None)
    title: str = dataclasses.field(default=None)
    content_html: str = dataclasses.field(default=None)
    content_text: str = dataclasses.field(default=None)
    summary: str = dataclasses.field(default=None)
    image: str = dataclasses.field(default=None)
    banner_image: str = dataclasses.field(default=None)
    date_published: datetime = dataclasses.field(default=None)
    date_modified: datetime = dataclasses.field(default=None)
    authors: List[Parson] = dataclasses.field(default=None)
    tags: List[str] = dataclasses.field(default=None)
    language: str = dataclasses.field(default=None)
    attachments: List[Attachment] = dataclasses.field(default=None)

@dataclasses.dataclass
class Feed(Element):
    version: str = dataclasses.field(default="https://jsonfeed.org/version/1.1", init=False)
    title: str
    home_page_url: str = dataclasses.field(default=None)
    feed_url: str = dataclasses.field(default=None)
    description: str = dataclasses.field(default=None)
    user_comment: str = dataclasses.field(default=None)
    next_url: str = dataclasses.field(default=None)
    icon: str = dataclasses.field(default=None)
    favicon: str = dataclasses.field(default=None)
    authors: List[str] = dataclasses.field(default=None)
    next_url: str = dataclasses.field(default=None)
    language: str = dataclasses.field(default=None)
    expired: bool = dataclasses.field(default=None)
    items: List[Item] = dataclasses.field(default=None)
    hubs: List[object] = dataclasses.field(default=None)

def test():
    feed = Feed(
        title="sample-feed",
        items=[
            Item(
                id="0001",
                title="one",
                date_modified=datetime.strptime("2000-01-01", r"%Y-%m-%d")
            ),
            Item(
                id="0002",
                date_modified=datetime.strptime("2000-12-31", r"%Y-%m-%d")
            )
        ]
    )
    feed.icon = "icon.png"
    print(feed.to_json(indent=2))

if __name__ == "__main__":
    test()
