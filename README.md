# obentoget

お弁当屋さんのウェブサイトにあるメニュー情報・店舗情報を [JSON Feed](https://jsonfeed.org/) 形式で保存します。

データ例：
```json
{
  "version": "https://jsonfeed.org/version/1.1",
  "title": "どんどん",
  "home_page_url": "http://www.dondon.co.jp/index.html",
  "icon": "image/icon.png",
  "favicon": "image/favicon.ico",
  "items": [
    {
      "id": "dondon.morokoshidonburi",
      "title": "もろこし丼",
      "image": "image/menu__image__morokoshidon__20200806.jpg",
      "date_modified": "2020-08-06T00:00:00",
      "_price": 480
    }
  ]
}
```
