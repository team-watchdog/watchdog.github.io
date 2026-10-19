import json, re, os
SITE='/home/claude/site'
H=json.load(open('/home/claude/tools/pages.json'))
PEOPLE={f.lower():f for f in 'aisha-1.png amalini-1.png brownie.jpg fairooz.jpeg Ishan.png joshua.jpeg k7.png lara.png Minoli.png nabeela.jpg nadim.jpeg nimesha.jpg nisal.JPG nishadi.jpg rukshana.png sachinta.jpeg sahan.jpg sathyajit.jpeg tee.jpeg umesh-1.jpg yudha.jpg'.split()}
IMGMAP=json.load(open(f'{SITE}/watchdog-scrape/data/imgmap.json'))
KNOWN_PEOPLE=['brownie.jpg','yudha.jpg','nisal.jpg','fairooz.jpeg']
unresolved=[]
def fix_img(m):
    src=m.group(1)
    name=re.sub(r'%20',' ',src.rsplit('/',1)[-1]); name=re.sub(r'%28','(',name); name=re.sub(r'%29',')',name)
    if name=='use-commas.png': return 'src="/images/general/use-commas.png"'
    if name.lower() in PEOPLE: return f'src="/images/people/{PEOPLE[name.lower()]}"'
    unresolved.append(src); return f'src="{src}" loading="lazy"'
def demote(h):
    return re.sub(r'<(/?)h([1-5])\b', lambda m: f'<{m.group(1)}h{int(m.group(2))+1}', h)
def convert(h):
    h=re.sub(r'src="([^"]+)"', fix_img, h)
    h=h.replace('<img ','<img loading="lazy" ') if 'loading=' not in h else h
    h=re.sub(r'<table>', '<div class="table-wrap"><table>', h); h=h.replace('</table>','</table></div>')
    h=re.sub(r'https?://(?:www\.)?watchdog\.team/article/([^"\s]+)', lambda m: m.group(0), h)
    return demote(h)
# contributor pages referenced from static pages, and person cards on the About page
import urllib.parse, html as _html
PERSON = re.compile(r'<p><img[^>]*src="([^"]+)"[^>]*></p>\s*<p><a href="/contributor/([^"]+)"><strong>(.*?)</strong></a>\s*-?\s*(?:<em>(.*?)</em>)?</p>\s*<p>(.*?)</p>', re.S)
def person_card(m):
    src, slug, name, role, bio = m.groups()
    fn=urllib.parse.unquote(src.rsplit('/',1)[-1])
    image=f'/images/people/{PEOPLE[fn.lower()]}' if fn.lower() in PEOPLE else ''
    path=f'{SITE}/_contributors/{slug}.md'
    if not os.path.exists(path):
        plain=re.sub(r'<[^>]+>','',bio)
        open(path,'w',encoding='utf-8').write('---\nname: '+json.dumps(_html.unescape(re.sub(r'<[^>]+>','',name)),ensure_ascii=False)+f'\nslug: {json.dumps(slug)}\npermalink: /contributor/{slug}/\n'+(f'image: "{image}"\n' if image else '')+'---\n'+_html.unescape(plain)+'\n')
    img=f'<img class="avatar avatar--lg" src="{image}" alt="" loading="lazy" width="72" height="72">' if image else ''
    r=f'<span class="person-role">{role}</span>' if role else ''
    return f'<div class="person-card">{img}<div><h3><a href="/contributor/{slug}/">{name}</a></h3>{r}<p>{bio}</p></div></div>'


PAGES=[
 ('/about-us','about.md','About us','/about-us/',['/about/'],'Watchdog is a multidisciplinary team of journalists, researchers and software engineers, operating under the Appendix umbrella.'),
 ('/operational-ethics','op-ethics.md','Operational ethics','/operational-ethics/',['/op-ethics/'],'How Watchdog approaches information, sources, quotations, anonymity and images.'),
 ('/handling-conflicts','handling-conflicts.md','Handling conflicts','/handling-conflicts/',[],'Our guidance on conflicts of interest, sources and hospitality.'),
 ('/language-guide','language-guide.md','Language guide','/language-guide/',[],'How we write numbers, names and technical terms in Sinhala, Tamil and English.'),
 ('/privacy-policy','privacy-policy.md','Privacy policy','/privacy-policy/',[],'How Watchdog handles personal information.'),
]
for key,fn,title,perm,redir,desc in PAGES:
    body=convert(H[key])
    if key=='/about-us': body=PERSON.sub(person_card, body.replace('<h2','<h2')).replace('<hr>','')
    fm=['---','layout: page',f'title: "{title}"',f'description: "{desc}"',f'permalink: {perm}']
    if redir: fm.append('redirect_from: ['+', '.join(f'"{r}"' for r in redir)+']')
    fm.append('---')
    open(f'{SITE}/_pages/{fn}','w',encoding='utf-8').write('\n'.join(fm)+'\n\n'+body+'\n')
# obsolete files of the first port: cannot be deleted from here, so unpublish them
for fn in ['authors.html','contact.html','elements.md','tags.html','tools.html','category-special-reports.html']:
    open(f'{SITE}/_pages/{fn}','w').write('---\npublished: false\n---\nObsolete file from the first port. Safe to delete.\n')
print('unresolved page images:',unresolved)
