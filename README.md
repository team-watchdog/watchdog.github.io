# Watchdog

Jekyll port of [watchdog.team](https://watchdog.team/). Articles exist in English, Sinhala and Tamil; each language version is its own page, and pages in the same `translation_key` group link to each other.

## Run it

```
bundle install
bundle exec jekyll serve
```

The site is configured for `https://team-watchdog.github.io/watchdog.github.io`. When it moves to its own domain, set `url` and an empty `baseurl` in `_config.yml`.

## Deploy

Pushes to `main` build through `.github/workflows/pages.yml`. In the repository settings, set Pages > Source to **GitHub Actions**. The workflow runs `tests/check_site.py`, which fails the build on broken links or images, missing language switchers, or translation links that are not reciprocal.

## Writing an article

Add `_articles/<slug>.md`:

```
---
title: Title
lang: en            # en, si or ta
translation_key: slug-of-the-english-version
slug: <slug>
permalink: /article/<slug>/
date: 2025-01-31 09:00:00 +0530
kind: story         # or tool
category: economy   # see _data/categories.yml
categories: [economy]
contributors: [contributor-slug]
description: One or two sentences.
image: /images/library/<file>.webp
---
```

Give every language version the same `translation_key` and the site handles the switcher, the language filter and reader-preference swapping (stored in the browser as `wd-lang`). Contributors live in `_contributors/`.

## Layout

- `_layouts`, `_includes`: templates. `assets/css/site.css`, `js/site.js`: styling and behaviour.
- `_data/site.yml`: tagline, nav, footer, social links, newsletter URL (empty until set).
- `scripts/`: the one-off importer that built `_articles` and `_pages` from a scrape of watchdog.team. Kept for reference; it needs the scrape folder, which is not committed.
