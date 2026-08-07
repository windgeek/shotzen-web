# ShotZen — support and privacy pages

The two pages App Store Connect requires for [ShotZen](https://apps.apple.com/app/shotzen),
a quiet screenshot tool for macOS.

| Page | File | Used for |
|---|---|---|
| Support | `index.html` | App Store Connect → Support URL |
| Privacy Policy | `privacy.html` | App Store Connect → Privacy Policy URL |

Both are static, dependency-free, and hosted with GitHub Pages.

## Six languages, two URLs

The app ships in English, 简体中文, 繁體中文, 日本語, Deutsch and Français. Rather
than six pages per document, every translation lives in the same file inside its
own `<article lang="…">`, and `shotzen.js` reveals one of them. The choice order
is `?lang=` → last choice in `localStorage` → the browser's own preference →
English.

That keeps App Store Connect down to one Support URL and one Privacy Policy URL
regardless of how many localisations the app adds.

## Editing

`shotzen.css` holds the palette, taken from the app's `Theme/ZenTheme.swift` so
the pages and the app stay one object seen twice.

One thing to watch when editing the CJK translations: a newline in the HTML
source becomes a space in the rendered text. Between two Latin words that is
what you want; between two Han characters it is a visible gap mid-sentence. Keep
each CJK paragraph on a single source line.
