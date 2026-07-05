# -*- coding: utf-8 -*-
"""
noteのRSSから最新記事URLを取得して、index.html(リダイレクトページ)を書き換える。
GitHub Actionsが毎日実行 → QRコードやインスタのリンクは固定のまま、
飛び先だけが最新記事に更新される仕組み。
"""
import urllib.request
import xml.etree.ElementTree as ET
import sys

RSS_URL = "https://note.com/starducktony/rss"
FALLBACK_URL = "https://note.com/starducktony"  # RSSが取れない時はプロフィールへ

def get_latest():
    try:
        req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as res:
            root = ET.fromstring(res.read())
        item = root.find("./channel/item")
        if item is None:
            return FALLBACK_URL, "スターダックトニーのnote"
        link = item.findtext("link", FALLBACK_URL).strip()
        title = item.findtext("title", "最新記事").strip()
        return link, title
    except Exception as e:
        print(f"RSS取得失敗: {e}", file=sys.stderr)
        return FALLBACK_URL, "スターダックトニーのnote"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>スターダックトニー | 今日の旅の話</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<style>
  body {{ font-family: sans-serif; text-align: center; padding: 3em 1em; background: #111; color: #fff; }}
  a {{ color: #ffd700; }}
</style>
</head>
<body>
<p>最新の記事に移動中…</p>
<p><a href="{url}">自動で移動しない場合はこちら</a></p>
<script>location.replace("{url}");</script>
</body>
</html>
"""

if __name__ == "__main__":
    url, title = get_latest()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(url=url))
    print(f"リダイレクト先を更新: {title} -> {url}")
