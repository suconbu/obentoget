#!/usr/bin/env python3

import re
import sys
import requests
import pykakasi
import mojimoji
from datetime import datetime

class Internal(object):
    alphabet_to_hiragana = {
        "a": "えー", "b": "びー", "c": "しー", "d": "でぃー", "e": "いー",
        "f": "えふ", "g": "じー", "h": "えいち", "i": "あい", "j": "じぇー",
        "k": "けー", "l": "える", "m": "えむ", "n": "えぬ", "o": "おー",
        "p": "ぴー", "q": "きゅー", "r": "あーる", "s": "えす", "t": "てぃー",
        "u": "ゆー", "v": "ぶい", "w": "だぶりゅ", "x": "えっくす", "y": "わい",
        "z": "ぜっと"
    }

    kakasi_hiragana = pykakasi.kakasi()
    kakasi_hiragana.setMode("K", "H")
    kakasi_hiragana.setMode("J", "H")
    hiragana_converter = kakasi_hiragana.getConverter()

    kakasi_roman = pykakasi.kakasi()
    kakasi_roman.setMode("H", "a")
    kakasi_roman.setMode("K", "a")
    kakasi_roman.setMode("J", "a")
    roman_converter = kakasi_roman.getConverter()

def to_halfwidth(text: str, digit: bool, ascii: bool, kana: bool) -> str:
    """半角文字に変換します。"""
    return mojimoji.zen_to_han(text, digit=digit, ascii=ascii, kana=kana)

def to_fullwidth(text: str, digit: bool, ascii: bool, kana: bool) -> str:
    """全角文字に変換します。"""
    return mojimoji.han_to_zen(text, digit=digit, ascii=ascii, kana=kana)

def normalized(text: str) -> str:
    """数字/英字は半角、カタカナは全角に揃えます。"""
    t = to_fullwidth(text, digit=False, ascii=False, kana=True)
    t = to_halfwidth(text, digit=True, ascii=True, kana=False)
    return t

def to_hiragana(text: str) -> str:
    """漢字かな英字まじり文字列をひらがなに変換します。"""
    t = Internal.hiragana_converter.do(normalized(text))
    return "".join(map(lambda c: Internal.alphabet_to_hiragana.get(c, c), t.lower()))

def to_roman(text: str) -> str:
    """漢字かな英字まじり文字列をローマ字(ヘボン式)に変換します。"""
    return Internal.roman_converter.do(normalized(text)).lower()

def on_jpera_matched(match) -> str:
    jperas = {"昭和": 1926 - 1, "平成": 1989 - 1, "令和": 2019 - 1}
    year = jperas.get(match.group(1))
    return str(year + int(match.group(2))) if year else match.group()

def strptime(text: str, pattern: str) -> datetime:
    text = re.sub(r"(\S\S)\s*(\d+)", on_jpera_matched, text)
    return datetime.strptime(text, pattern)

def test():
    hiragana = to_hiragana("ひラ仮Na")
    assert(hiragana == "ひらかりえぬえー")
    roman = to_roman("ひラ仮Ｎa")
    assert(roman == "hirakarina")
    date = strptime("最終更新日平成25年11月21日", "最終更新日%Y年%m月%d日")
    assert(date.strftime("%Y-%m-%d") == "2013-11-21")
    date = strptime("最終更新日2025年11月21日", "最終更新日%Y年%m月%d日")
    assert(date.strftime("%Y-%m-%d") == "2025-11-21")
    print("Success")

if __name__ == "__main__":
    test()
