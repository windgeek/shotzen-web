#!/usr/bin/env python3
"""Generate dependency-free GitHub Pages documents from reviewed locale copy."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ['en', 'zh-Hans', 'zh-Hant', 'ja', 'ko', 'de', 'fr', 'es', 'pt-BR']
EMAIL = 'songlaoshi666@gmail.com'
GITHUB_POLICY = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'


def esc(value):
    return html.escape(value, quote=True)


def prose(value):
    return re.sub(r'(⇧⌘[APRF]|\bOption\b|\bEscape\b)', r'<kbd>\1</kbd>', esc(value))


def paragraph(value):
    return f'<p>{prose(value)}</p>'


def heading(value):
    return f'<h2>{esc(value)}</h2><hr class="rule">'


def card(value):
    return f'<div class="card">{value}</div>'


def mail():
    return f'<p class="mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'


def build():
    data = json.loads((ROOT / 'content/locales.json').read_text())
    assert set(data) == set(LANGS), 'Expected exactly the app’s nine languages'
    reference_keys = set(data['en'])
    template = (ROOT / 'templates/page.html').read_text()
    for privacy in [False, True]:
        articles = []
        for lang in LANGS:
            text = data[lang]
            assert set(text) == reference_keys, f'{lang}: missing translation fields'
            assert len(text['faqs']) == 11 and len(text['privacySections']) == 8
            title = text['policy' if privacy else 'support']
            tagline = f"{title} · {text['date' if privacy else 'tagline']}"
            description = text['privacyIntro' if privacy else 'intro']
            attributes = {
                'lang': lang, 'id': f'content-{lang}', 'data-title': f'ShotZen — {title}',
                'data-tagline': tagline, 'data-description': description,
                'data-footer': text['support' if privacy else 'policy'],
                'data-language-label': text['languageLabel']
            }
            attrs = ' '.join(f'{key}="{esc(value)}"' for key, value in attributes.items())
            active = ' class="on"' if lang == 'en' else ''
            content = [f'<article {attrs}{active}>', f'<p class="lead">{esc(description)}</p>']
            if privacy:
                for index, (label, body) in enumerate(text['privacySections']):
                    extra = ''
                    if index == 6:
                        extra = f'<p><a href="{GITHUB_POLICY}">{esc(text["githubPolicy"])}</a></p>'
                    if index == 7:
                        extra = mail()
                    content += [heading(label), card(paragraph(body) + extra)]
                content += [f'<p><a href="index.html?lang={lang}">{esc(text["support"])}</a></p>']
            else:
                content += [heading(text['contact']), card(mail() + paragraph(text['contactText']))]
                content += [heading(text['questions'])]
                for question, answer in text['faqs']:
                    content += [card(f'<h3>{esc(question)}</h3>' + paragraph(answer))]
                content += [heading(text['requirementsTitle']), card(paragraph(text['requirements']))]
                content += [heading(text['policy']), card(paragraph(text['privacyNote']) + f'<p><a href="privacy.html?lang={lang}">{esc(text["policy"])}</a></p>')]
            content += ['</article>']
            articles.append('\n'.join(content))
        en = data['en']
        title = en['policy' if privacy else 'support']
        values = {
            'TITLE': esc(f'ShotZen — {title}'),
            'DESCRIPTION': esc(en['privacyIntro' if privacy else 'intro']),
            'TAGLINE': esc(f'{title} · {en["date" if privacy else "tagline"]}'),
            'LANGUAGES': '\n'.join(f'<button type="button" data-lang="{lang}" aria-pressed="{"true" if lang == "en" else "false"}">{esc(data[lang]["name"])}</button>' for lang in LANGS),
            'ARTICLES': '\n\n'.join(articles),
            'OTHER_URL': 'index.html?lang=en' if privacy else 'privacy.html?lang=en',
            'OTHER_TITLE': esc(en['support' if privacy else 'policy'])
        }
        result = template
        for key, value in values.items():
            result = result.replace('{{' + key + '}}', value)
        assert '{{' not in result, 'Unresolved template field'
        (ROOT / ('privacy.html' if privacy else 'index.html')).write_text(result)
    print('Generated support and privacy pages in nine languages.')


if __name__ == '__main__':
    build()
