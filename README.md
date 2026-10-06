# ShotZen — support and privacy pages

Official support and privacy pages for ShotZen, the native macOS screenshot,
region-recording, scrolling-capture, annotation, and floating-reference utility.

| Page | GitHub Pages URL | App Store Connect field |
|---|---|---|
| Support | https://windgeek.github.io/shotzen-web/ | Support URL |
| Privacy | https://windgeek.github.io/shotzen-web/privacy.html | Privacy Policy URL |

GitHub Pages publishes the repository root from `main`. Both existing URLs remain
valid. The site is static and has no runtime dependencies, analytics, external
fonts, or remote translation requests.

## Nine languages

English (`en`), 简体中文 (`zh-Hans`), 繁體中文 (`zh-Hant`), 日本語 (`ja`),
한국어 (`ko`), Deutsch (`de`), Français (`fr`), Español (`es`), and
Português (Brasil) (`pt-BR`) match ShotZen's app catalogs.

Every translated document is embedded in its HTML page. `shotzen.js` selects
`?lang=` first, then the saved browser choice, browser languages, and English.
Regional language tags are normalized, including `zh-TW`, `ko-KR`, `es-ES`, and
`pt-BR`. Portuguese preferences use the available Brazilian Portuguese locale.
The title, description, header, language control, and footer are localized.
Switching updates the URL, and links between documents preserve the language
without depending on browser storage. With JavaScript disabled, all translations
remain readable; with scripts enabled, only the selected article is exposed.

## Editing and verification

1. Edit `content/locales.json`. Each locale has the same 11 support questions and
   8 privacy sections. Copy was reviewed against ShotZen 1.3.1 source, entitlements,
   privacy manifest, and store metadata on 6 October 2026.
2. Run `python3 scripts/build.py` to regenerate `index.html` and `privacy.html`.
3. Run `python3 scripts/verify.py` for content, HTML, and language coverage checks.
4. Preview with `python3 -m http.server 8765 --bind 127.0.0.1` and check both
   documents at desktop and mobile widths. Exercise all language controls,
   cross-page links, browser preferences, blocked storage, and JavaScript disabled.
5. Commit generated HTML together with its source. Push to `main` to publish,
   then verify the Pages build and both public URLs.

`templates/page.html` contains the original ShotZen mark and shared structure.
`shotzen.css` retains the app's violet, gold, and frosted-panel visual language.
The privacy policy covers local temporary recordings, clipboard GIF caching,
user-selected destinations, support email, and GitHub Pages hosting separately.
CJK paragraphs are generated on single source lines to avoid inserted spaces.
