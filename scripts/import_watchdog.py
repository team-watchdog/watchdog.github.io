#!/usr/bin/env python3
"""Convert the scraped watchdog.team data into Jekyll content.

Reads  watchdog-scrape/data/*.json
Writes _articles/*.md, _contributors/*.md, _data/categories.yml, _data/redirects report
"""
import json, re, os, sys, urllib.parse, collections, datetime, unicodedata

SITE = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site'
D = os.path.join(SITE, 'watchdog-scrape', 'data')
P = json.load(open(f'{D}/posts.json'))
M = json.load(open(f'{D}/misc.json'))
IMGMAP = json.load(open(f'{D}/imgmap.json'))
HOME = {p['slug']: p for p in M['/']['posts']}
CATS = M['/']['categories']
LIB = '/images/library/'

report = collections.defaultdict(list)


def y(s):
    """YAML-safe double quoted scalar."""
    return json.dumps(s, ensure_ascii=False)


# ------------------------------------------------------------------ language
def detect_lang(title, body):
    if re.search(r'[\u0D80-\u0DFF]', title):
        return 'si'
    if re.search(r'[\u0B80-\u0BFF]', title):
        return 'ta'
    text = re.sub(r'Read this article in[^\n]*', '', (body or '')[:4000])
    text = re.sub(r'\]\([^)]*\)', ']', text)
    text = re.sub(r'https?://\S+', '', text)
    si = len(re.findall(r'[\u0D80-\u0DFF]', text))
    ta = len(re.findall(r'[\u0B80-\u0BFF]', text))
    la = len(re.findall(r'[A-Za-z]', text))
    tot = si + ta + la + 1
    if si / tot > 0.4:
        return 'si'
    if ta / tot > 0.4:
        return 'ta'
    return 'en'


# ------------------------------------------------------------------ groups
parent = {s: s for s in P}


def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def union(a, b):
    a, b = find(a), find(b)
    if a != b:
        parent[b] = a


def slug_from_url(u):
    m = re.search(r'/article/([^)\s]+)', u)
    if not m:
        return None
    return urllib.parse.unquote(m.group(1))


META_RE = re.compile(r'\A\s*```javascript\n(.*?)\n```\s*', re.S)
for s, p in P.items():
    b = p.get('markdownBody') or ''
    line = re.search(r'Read this article in[^\n]*', b[:3000])
    if line:
        for u in re.findall(r'\((https?://watchdog\.team/article/[^)]+)\)', line.group(0)):
            t = slug_from_url(u)
            if t in P:
                union(s, t)

# manual groups for posts whose bodies carry no translation line
MANUAL = {
    ':': 'sri-lanka\'s-changing-landscape:-a-call-to-arms-for-journalists',
    'i': 'the-green-death-part-i',
    'ii': 'the-green-death-part-ii',
    'හරිත-මරණය-i': 'the-green-death-part-i',
    'හරිත-මරණය-ii': 'the-green-death-part-ii',
    'සන්නද්ධ-වීමට-මාධ්‍යවේදීන්ට-කරන-ඇරයුම': 'sri-lanka\'s-changing-landscape:-a-call-to-arms-for-journalists',
}
for a, b in MANUAL.items():
    if a in P and b in P:
        union(a, b)
for pair in [
    ('explainer-what-is-this-state-of-emergency', 'පැහැදිලි-කිරීම-මොකක්-ද-මේ-හදිසි-තත්ත්වය'),
    ('explainer-what-is-this-state-of-emergency', 'அவசரநிலை-அ-முதல்-ஃ-வரை'),
    ('going-organic-the-farmers-tales', next((k for k in P if k.startswith('කාබනික')), 'going-organic-the-farmers-tales')),
]:
    if all(x in P for x in pair):
        union(*pair)

lang = {s: detect_lang(p['title'], p.get('markdownBody')) for s, p in P.items()}

# heuristic pairing for translations that carry no explicit link line:
# same publication day, then identical cover image, then overlapping contributors.
def day_of(s):
    return (P[s].get('publishedDate') or HOME.get(s, {}).get('publishedDate') or '')[:10]


def cover_of(s):
    return (P[s].get('coverImage') or {}).get('url')


def contribs_of(s):
    return {c['slug'] for c in (P[s].get('contributors') or [])}


def group_langs(root):
    return {lang[m] for m in P if find(m) == root}


by_day = collections.defaultdict(list)
for s in P:
    if P[s]['postType'] != 'tool':
        by_day[day_of(s)].append(s)


def try_union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return
    la, lb = group_langs(ra), group_langs(rb)
    if la & lb:
        return
    union(a, b)


for day, ss in by_day.items():
    ss = sorted(ss)
    # pass 1: identical cover
    for i, a in enumerate(ss):
        for b in ss[i + 1:]:
            if lang[a] != lang[b] and cover_of(a) and cover_of(a) == cover_of(b):
                try_union(a, b)
    # pass 2: contributor overlap (jaccard), best first
    pairs = []
    for i, a in enumerate(ss):
        for b in ss[i + 1:]:
            if lang[a] == lang[b]:
                continue
            ca, cb = contribs_of(a), contribs_of(b)
            if not ca or not cb:
                continue
            j = len(ca & cb) / len(ca | cb)
            if j >= 0.5:
                pairs.append((j, a, b))
    for j, a, b in sorted(pairs, reverse=True):
        try_union(a, b)

groups = collections.defaultdict(list)
for s in P:
    groups[find(s)].append(s)

# ------------------------------------------------------------------ slugs
def ascii_slug(s):
    s = urllib.parse.unquote(s)
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode()
    s = s.lower().replace("'", '').replace('’', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:90].strip('-')


new_slug = {}
tkey = {}
for root, members in groups.items():
    en = [m for m in members if lang[m] == 'en']
    base = None
    if en:
        # prefer the longest english member as the canonical one
        base = ascii_slug(sorted(en, key=lambda m: -len(m))[0])
    if not base:
        base = 'article-' + P[members[0]]['id'][-6:]
        report['no_english_group'].append(members)
    for m in members:
        tkey[m] = base
    by_lang = collections.defaultdict(list)
    for m in members:
        by_lang[lang[m]].append(m)
    for l, ms in by_lang.items():
        for i, m in enumerate(sorted(ms)):
            slug = base if l == 'en' else f'{base}-{l}'
            if i:
                slug += f'-{i+1}'
            new_slug[m] = slug
            if i:
                report['dup_lang_in_group'].append((m, slug))

# reverse map for link rewriting: old url slug -> new slug
old2new = {s: new_slug[s] for s in P}

# ------------------------------------------------------------------ helpers
def local_img(url):
    if not url:
        return None
    if url in IMGMAP:
        return LIB + os.path.basename(IMGMAP[url])
    clean = re.split(r'\s+["\'=]', url)[0].strip()
    if clean in IMGMAP:
        return LIB + os.path.basename(IMGMAP[clean])
    return None


KEYS = sorted(IMGMAP.keys(), key=len, reverse=True)
LOCAL_RE = re.compile(r'!\[([^\]]*)\]\(\s*<?([^)\n]*?(?:\([^)\n]*\)[^)\n]*?)*)>?\s*\)')


def fix_images(body, slug):
    for k in KEYS:
        if k in body:
            body = body.replace(k, LIB + os.path.basename(IMGMAP[k]))
    # drop markdown image title / size suffixes: ![a](/images/x.webp "t =100x100")
    body = re.sub(r'(\(/images/library/[0-9a-f]+\.\w+)\s+"[^"]*"\)', r'\1)', body)
    body = re.sub(r'(\(/images/library/[0-9a-f]+\.\w+)\s+=\d+x\d+\)', r'\1)', body)
    for m in re.finditer(r'https?://[^\s)"]*digitaloceanspaces[^\s)"]*', body):
        report['unmapped_do_images'].append((slug, m.group(0)[:120]))
    return body


YT = re.compile(r'^\s*\[?(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})[^\s\])]*)\]?(?:\([^)]*\))?\s*$')


def video_embeds(body):
    out = []
    for line in body.split('\n'):
        m = YT.match(line)
        if m:
            vid = m.group(2)
            out.append(f'<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="YouTube video" loading="lazy" allowfullscreen></iframe></div>')
        else:
            out.append(line)
    return '\n'.join(out)


def rewrite_internal_links(body, slug):
    def repl(m):
        old = urllib.parse.unquote(m.group(1))
        old = old.split('#')[0]
        if old in old2new:
            return f'](/article/{old2new[old]}/)'
        report['unresolved_internal_links'].append((slug, old))
        return m.group(0)
    body = re.sub(r'\]\(https?://(?:www\.)?watchdog\.team/article/([^)\s]+)\)', repl, body)
    # bare-url link text: [https://watchdog.team/article/x](...) handled by the above; leave text
    return body


def demote_headings(body):
    if not re.search(r'^# ', body, re.M):
        return body
    out, fence = [], False
    for line in body.split('\n'):
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'^#{1,5} ', line):
            line = '#' + line
        out.append(line)
    return '\n'.join(out)


def clean_body(body):
    body = body.replace('\r\n', '\n')
    body = re.sub(r'^[ \t]*\\[ \t]*$', '', body, flags=re.M)      # lone backslash spacers
    body = re.sub(r'[ \t]+\n', '\n', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip() + '\n'


def parse_meta(body):
    m = META_RE.match(body)
    meta = {'credits': [], 'summary': None, 'published': None}
    if not m:
        return meta, body
    for line in m.group(1).split('\n'):
        line = line.strip().rstrip('\\').strip()
        if not line or line.startswith('Read this article in'):
            continue
        if ':' not in line and '：' not in line:
            continue
        k, v = re.split(r'[:：]', line, maxsplit=1)
        k, v = k.strip(), v.strip()
        kl = k.lower()
        if kl == 'published date':
            meta['published'] = v
        elif kl in ('summary', 'සාරාංශය', 'சுருக்கம்'):
            meta['summary'] = v
        elif v:
            meta['credits'].append([k, v])
    return meta, body[m.end():]


def local_date(iso):
    d = datetime.datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=5, minutes=30)
    return d.strftime('%Y-%m-%d')


# ------------------------------------------------------------------ contributors
contrib = {}
for p in list(P.values()) + list(HOME.values()) + M['/tools']['tools']:
    for c in p.get('contributors') or []:
        contrib[c['slug']] = c['name']

# ------------------------------------------------------------------ doc / notion links
OUTLINE = {}
for _p in HOME.values():
    _u = _p.get('outlineUrl')
    if _u and _u.startswith('/doc/'):
        OUTLINE[urllib.parse.unquote(_u[5:])] = _p['slug']


def slugify_heading(text):
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*_`~]', '', text).strip().lower()
    keep = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat[0] in 'LMN' or ch in ' -':
            keep.append(ch)
    return re.sub(r'\s+', '-', ''.join(keep)).strip('-')


def add_heading_ids(body):
    out, fence, seen = [], False, collections.Counter()
    for line in body.split('\n'):
        if line.startswith('```'):
            fence = not fence
        m = re.match(r'^(#{2,6})\s+(.*?)\s*#*\s*$', line) if not fence else None
        if m and '{#' not in line:
            slug = slugify_heading(m.group(2))
            if slug:
                seen[slug] += 1
                sid = 'h-' + slug + (f'-{seen[slug]}' if seen[slug] > 1 else '')
                line = f'{m.group(1)} {m.group(2)} {{#{sid}}}'
        out.append(line)
    return '\n'.join(out)


def rewrite_doc_links(body, own_old_slug):
    own_outline = next((k for k, v in OUTLINE.items() if v == own_old_slug), None)

    def doc(m):
        text, ident, frag = m.group(1), urllib.parse.unquote(m.group(2)), m.group(3) or ''
        target_old = OUTLINE.get(ident)
        if target_old and target_old in old2new:
            if target_old == own_old_slug:
                return f'[{text}]({frag})' if frag else text
            return f'[{text}](/article/{old2new[target_old]}/{frag})'
        report['dead_doc_links_unlinked'].append((own_old_slug, ident[:40]))
        return text
    body = re.sub(r'\[([^\]]*)\]\(/doc/([^)#\s]+)(#[^)\s]*)?\)', doc, body)
    # notion links point at private pages that no longer resolve: keep the words, drop the link
    def notion(m):
        report['notion_links_unlinked'].append((own_old_slug, m.group(1)[:40]))
        return m.group(1)
    body = re.sub(r'!\[[^\]]*\]\(https://www\.notion\.so/images/[^)]*\)', '', body)
    body = re.sub(r'!\[[^\]]*\]\(/api/attachments\.redirect[^)]*\)', '', body)
    body = re.sub(r'\[([^\]]*)\]\(https://www\.notion\.so/[^)]*\)', notion, body)
    return body


# ------------------------------------------------------------------ write articles
os.makedirs(f'{SITE}/_articles', exist_ok=True)
index = []
for s, p in P.items():
    h = HOME.get(s, {})
    cats = [c['slug'] for c in (h.get('category') or [])]
    kind = p['postType']
    body = p.get('markdownBody') or ''
    meta, body = parse_meta(body)
    body = re.sub(r'^[#>\s]*Read this article in[^\n]*\n?', '', body, flags=re.M)
    body = clean_body(body)
    body = fix_images(body, s)
    body = rewrite_internal_links(body, s)
    body = rewrite_doc_links(body, s)
    body = video_embeds(body)
    body = demote_headings(body)
    body = add_heading_ids(body)
    pd = p.get('publishedDate') or h.get('publishedDate')
    date = local_date(pd) if pd else (meta['published'] or '2022-01-01').replace('/', '-')
    if not pd: report['no_date'].append(s)
    if meta['published']:
        try:
            md = datetime.datetime.strptime(meta['published'].replace('-', '/'), '%Y/%m/%d').strftime('%Y-%m-%d')
            if md != date:
                report['date_mismatch'].append((s, date, md))
                date = md
        except ValueError:
            pass
    summary = (p.get('summary') or meta['summary'] or '').strip()
    cover = local_img((p.get('coverImage') or {}).get('url'))
    if (p.get('coverImage') or {}).get('url') and not cover:
        report['unmapped_cover'].append((s, p['coverImage']['url']))
    slug = new_slug[s]
    fm = [
        '---',
        f'title: {y(p["title"].strip())}',
        f'lang: {lang[s]}',
        f'translation_key: {y(tkey[s])}',
        f'slug: {y(slug)}',
        f'permalink: /article/{slug}/',
        f'date: {date}',
        f'kind: {kind}',
    ]
    if cats:
        fm.append(f'category: {cats[0]}')
        fm.append('categories: [' + ', '.join(cats) + ']')
    fm.append('contributors: [' + ', '.join(c['slug'] for c in (p.get('contributors') or [])) + ']')
    if summary:
        fm.append(f'description: {y(summary)}')
    if cover:
        fm.append(f'image: {cover}')
    if h.get('externalLink'):
        fm.append(f'external_link: {y(h["externalLink"])}')
    fm.append(f'original_url: {y("https://watchdog.team/article/" + urllib.parse.quote(s, safe=":\'-"))}')
    if meta['credits']:
        fm.append('credits:')
        for k, v in meta['credits']:
            fm.append(f'  - {{label: {y(k)}, names: {y(v)}}}')
    old = s
    if old != slug and ':' not in old and '/' not in old and "'" not in old:
        fm.append(f'redirect_from: [{y("/article/" + old + "/")}]')
    fm.append('---')
    with open(f'{SITE}/_articles/{slug}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fm) + '\n\n' + body)
    index.append((slug, lang[s], tkey[s], date, kind, cats, len(body)))
    if kind != 'tool' and len(body) < 400:
        report['short_body'].append((s, len(body)))

# ------------------------------------------------------------------ categories data
with open(f'{SITE}/_data/categories.yml', 'w', encoding='utf-8') as f:
    for c in CATS:
        img = local_img((c.get('categoryImage') or {}).get('url'))
        f.write(f'- slug: {c["slug"]}\n  title: {y(c["title"])}\n  description: {y(c["description"])}\n')
        if img:
            f.write(f'  image: {img}\n')

# ------------------------------------------------------------------ contributors
legacy = {}
for fn in os.listdir(f'{SITE}/_authors'):
    t = open(f'{SITE}/_authors/{fn}', encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
    if not m:
        continue
    fmd = dict(re.findall(r'^(\w+):\s*(.*)$', m.group(1), re.M))
    legacy[fmd.get('name', '').strip().lower()] = (fmd, m.group(2).strip(), fn)


def norm(n):
    return re.sub(r'[^a-z ]', '', n.lower())


def match_legacy(name):
    n = norm(name)
    if n in legacy:
        return legacy[n]
    first, last = n.split()[0], n.split()[-1]
    cands = [v for k, v in legacy.items() if norm(k).split()[0] == first and norm(k).split()[-1][:3] == last[:3]]
    return cands[0] if len(cands) == 1 else None


os.makedirs(f'{SITE}/_contributors', exist_ok=True)
counts = collections.Counter()
for s, p in P.items():
    for c in p.get('contributors') or []:
        counts[c['slug']] += 1
for slug, name in sorted(contrib.items()):
    lg = match_legacy(name)
    lines = ['---', f'name: {y(name)}', f'slug: {y(slug)}', f'permalink: /contributor/{slug}/']
    bio = ''
    if lg:
        fmd, bio, fn = lg
        img = fmd.get('image', '').strip().strip("'\"")
        if img:
            lines.append(f'image: {y(img)}')
    else:
        report['contributor_without_legacy_profile'].append(name)
    lines.append('---')
    with open(f'{SITE}/_contributors/{slug}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' + bio + '\n')

json.dump(index, open(f'{SITE}/../tools/index.json', 'w'), ensure_ascii=False, indent=0)
json.dump({k: v for k, v in report.items()}, open(f'{SITE}/../tools/report.json', 'w'), ensure_ascii=False, indent=1)
print('articles', len(index), 'groups', len(groups), 'contributors', len(contrib))
for k, v in report.items():
    print(k, len(v), v[:6])
