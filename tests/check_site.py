#!/usr/bin/env python3
"""Post-build checks for the Watchdog Jekyll site.

Usage:  python3 tests/check_site.py <built-site-dir> [baseurl]
  e.g.  jekyll build --baseurl /watchdog.github.io -d _site && python3 tests/check_site.py _site /watchdog.github.io

Checks: every internal link and image resolves, every article declares its
language and has a working language switcher, translation siblings link both
ways, and article pages have exactly one h1.  Exit code 1 on failure.
"""
import os, re, sys, html, urllib.parse, collections

args = [a for a in sys.argv[1:] if not a.startswith('--')]
site = args[0] if args else '_site'
base = (args[1] if len(args) > 1 else '').rstrip('/')
# --known FILE: newline separated site paths (e.g. images/library/x.webp) that exist in the
# real repo but not in this checkout; used when verifying a partial copy of the site.
KNOWN = set()
for a in sys.argv[1:]:
    if a.startswith('--known='):
        KNOWN = {l.strip().lstrip('/') for l in open(a.split('=', 1)[1], encoding='utf-8') if l.strip()}
errors, warnings = [], []


def page_path(url):
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    if base and path.startswith(base):
        path = path[len(base):]
    path = path.lstrip('/')
    for c in (os.path.join(site, path), os.path.join(site, path, 'index.html'), os.path.join(site, path + '.html')):
        if os.path.isfile(c):
            return c
    if path in KNOWN:
        return path
    return None


pages = []
for dp, _, fs in os.walk(site):
    for f in fs:
        if f.endswith('.html'):
            pages.append(os.path.join(dp, f))

link_re = re.compile(r'<(?:a|link)\b[^>]*?\bhref="([^"]+)"', re.I)
img_re = re.compile(r'<(?:img|script|source)\b[^>]*?\bsrc="([^"]+)"', re.I)
stats = collections.Counter()
articles = {}

for p in sorted(pages):
    t = open(p, encoding='utf-8').read()
    if 'http-equiv="refresh"' in t and len(t) < 800:
        continue  # redirect stub from jekyll-redirect-from
    rel = os.path.relpath(p, site)
    for m in link_re.finditer(t):
        u = html.unescape(m.group(1))
        if u.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')) or re.match(r'^[a-z]+://', u) or u.startswith('//'):
            continue
        stats['links'] += 1
        if not u.startswith('/'):
            continue
        if base and not u.startswith(base + '/') and u != base:
            errors.append(f'{rel}: link ignores baseurl: {u}')
            continue
        if not page_path(u.split('#')[0].split('?')[0] or '/'):
            errors.append(f'{rel}: broken link {u}')
    for m in img_re.finditer(t):
        u = html.unescape(m.group(1))
        if re.match(r'^[a-z]+://', u) or u.startswith(('data:', '//')):
            if 'digitaloceanspaces.com' in u and '/attachments/' not in u:
                warnings.append(f'{rel}: remote bucket image {u[:90]}')
            continue
        stats['images'] += 1
        if base and not u.startswith(base + '/'):
            errors.append(f'{rel}: asset ignores baseurl: {u}')
            continue
        if not page_path(u.split('?')[0]):
            errors.append(f'{rel}: missing asset {u}')
    if 'class="article"' in t:
        lang = re.search(r'<html lang="(\w+)"', t)
        if not lang or lang.group(1) not in ('en', 'si', 'ta'):
            errors.append(f'{rel}: bad html lang')
        if 'article-langs' not in t:
            errors.append(f'{rel}: missing language switcher')
        h1 = len(re.findall(r'<h1\b', t))
        if h1 != 1:
            errors.append(f'{rel}: {h1} h1 elements')
        sibs = dict(re.findall(r'<link rel="alternate" hreflang="(\w+)" href="([^"]+)"', t))
        articles[rel] = (lang.group(1) if lang else None, sibs)
        stats['articles'] += 1

# reciprocity: every sibling an article advertises must advertise it back
by_url = {}
for rel, (lang, sibs) in articles.items():
    by_url['/' + os.path.dirname(rel).replace(os.sep, '/') + '/'] = sibs


def norm(u):
    path = urllib.parse.unquote(urllib.parse.urlparse(u).path)
    if base and path.startswith(base):
        path = path[len(base):]
    return path


for me, sibs in by_url.items():
    for l, u in sibs.items():
        path = norm(u)
        if path == me:
            continue
        back = {norm(x) for x in by_url.get(path, {}).values()}
        if me not in back:
            errors.append(f'translation not reciprocal: {me} -> {path}')

print(dict(stats))
for w in warnings[:20]:
    print('warn:', w)
if len(warnings) > 20:
    print(f'... {len(warnings) - 20} more warnings')
for e in errors[:60]:
    print('ERROR:', e)
if len(errors) > 60:
    print(f'... {len(errors) - 60} more errors')
print('FAILED' if errors else 'OK', f'({len(errors)} errors, {len(warnings)} warnings)')
sys.exit(1 if errors else 0)
