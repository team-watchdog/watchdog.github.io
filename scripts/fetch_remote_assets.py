#!/usr/bin/env python3
"""Download hotlinked images and attachments and point the articles at the local copies.

Handles two kinds of remote URL found in _articles/, _pages/ and _data/:
  * Google-hosted images (*.googleusercontent.com)
  * the old DigitalOcean bucket (watchdog-public-assets)

Images are saved to images/remote/, everything else (PDFs and so on) to files/.
Source files are only edited for URLs that downloaded successfully, so you can
re-run the script safely. Standard library only.

Usage, from the repo root:
    python3 scripts/fetch_remote_assets.py           # download and rewrite
    python3 scripts/fetch_remote_assets.py --dry-run # list what it would fetch
"""
import hashlib, mimetypes, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [*ROOT.glob('_articles/*.md'), *ROOT.glob('_pages/*'), *ROOT.glob('_data/*'), ROOT / 'index.html']
HOSTS = ('googleusercontent.com', 'digitaloceanspaces.com')
URL_RE = re.compile(r'https?://[^\s)"\'<>\]]+')
EXT = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif',
       'image/svg+xml': '.svg', 'application/pdf': '.pdf'}
UA = {'User-Agent': 'Mozilla/5.0 (watchdog-site asset fetch)'}


def find_urls():
    found = {}
    for f in SOURCES:
        if not f.is_file():
            continue
        for u in URL_RE.findall(f.read_text(encoding='utf-8')):
            u = u.rstrip('.,;')
            if any(h in u for h in HOSTS):
                found.setdefault(u, set()).add(f)
    return found


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        ctype = r.headers.get_content_type()
        disp = r.headers.get('Content-Disposition', '')
        return r.read(), ctype, disp


def main():
    dry = '--dry-run' in sys.argv
    urls = find_urls()
    print(f'{len(urls)} remote URLs in {len({f for s in urls.values() for f in s})} files')
    if dry:
        for u in sorted(urls):
            print(' ', u)
        return
    done, failed = {}, []
    for i, u in enumerate(sorted(urls), 1):
        try:
            data, ctype, disp = fetch(u)
        except Exception as e:
            failed.append((u, str(e)))
            print(f'[{i}/{len(urls)}] FAIL {u[:90]}  {e}')
            continue
        ext = EXT.get(ctype) or mimetypes.guess_extension(ctype) or ''
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', disp)
        if not ext and m:
            ext = Path(m.group(1)).suffix
        is_img = ctype.startswith('image/')
        folder = 'images/remote' if is_img else 'files'
        name = hashlib.sha1(u.encode()).hexdigest()[:12] + ext
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
        (ROOT / folder / name).write_bytes(data)
        done[u] = f'/{folder}/{name}'
        print(f'[{i}/{len(urls)}] ok   {ctype:<16} {len(data)//1024:>6} KB  {done[u]}')
        time.sleep(0.2)
    # Rewrite longest URLs first so one URL that prefixes another cannot clobber it.
    for f in {f for u in done for f in urls[u]}:
        text = f.read_text(encoding='utf-8')
        for u in sorted((u for u in done if f in urls[u]), key=len, reverse=True):
            text = text.replace(u, done[u])
        f.write_text(text, encoding='utf-8')
    print(f'\nDownloaded {len(done)}, failed {len(failed)}.')
    for u, e in failed:
        print('  still remote:', u, '-', e)


if __name__ == '__main__':
    main()
