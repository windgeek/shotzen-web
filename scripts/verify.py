#!/usr/bin/env python3
"""Validate generated documents and optionally compare app locale coverage."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from build import ROOT, LANGS, build


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.articles = []
        self.buttons = []
        self.links = []
        self.ids = []
        self.active = None
        self.questions = {}
        self.assets = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        if tag == 'article':
            self.active = attributes['lang']
            self.articles.append(self.active)
            self.questions[self.active] = 0
        if tag == 'h3' and self.active:
            self.questions[self.active] += 1
        if tag == 'button':
            self.buttons.append(attributes['data-lang'])
        if tag == 'a':
            self.links.append(attributes['href'])
        if tag == 'script' and 'src' in attributes:
            self.assets.append(attributes['src'])
        if tag == 'link':
            self.assets.append(attributes['href'])

    def handle_endtag(self, tag):
        if tag == 'article':
            self.active = None


def verify():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, help='Optional ShotZen app project root')
    args = parser.parse_args()
    paths = [ROOT / 'index.html', ROOT / 'privacy.html']
    previous = [path.read_bytes() for path in paths]
    build()
    assert previous == [path.read_bytes() for path in paths], 'Generated pages were out of date; regenerated them'
    for path in paths:
        content = path.read_text()
        assert '⇧⌘W' not in content, 'Obsolete window shortcut'
        assert '�' not in content and '{{' not in content
        page = Page()
        page.feed(content)
        assert page.articles == LANGS and page.buttons == LANGS
        assert len(set(page.ids)) == len(page.ids), 'Duplicate IDs'
        assert all(not urlparse(asset).scheme and (ROOT / asset).is_file() for asset in page.assets)
        for link in page.links:
            parsed = urlparse(link)
            if not parsed.scheme:
                assert (ROOT / parsed.path).is_file(), f'Broken link: {link}'
                assert parse_qs(parsed.query).get('lang', [None])[0] in LANGS
        if path.name == 'index.html':
            assert all(count == 11 for count in page.questions.values())
            for lang in LANGS:
                text = json.loads((ROOT / 'content/locales.json').read_text())[lang]
                assert all(key in text['faqs'][1][1] for key in ['⇧⌘A', '⇧⌘P', '⇧⌘R', '⇧⌘F'])
                assert '30' in text['faqs'][2][1] and 'MP4' in text['faqs'][2][1]
        print(f'PASS {path.name}: nine complete locales, local assets, valid language links')
    if args.app:
        for filename in ['Localizable.xcstrings', 'InfoPlist.xcstrings']:
            data = json.loads((args.app / 'ShotZen' / filename).read_text())
            locales = {locale for value in data['strings'].values() for locale in value.get('localizations', {})}
            assert locales == set(LANGS), f'{filename}: app and website locales differ'
        print('PASS website language coverage matches both app catalogs')


if __name__ == '__main__':
    verify()
