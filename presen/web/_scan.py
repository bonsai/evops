import re, glob

CJK = r'\u3040-\u30ff\u4e00-\u9fff\u3000-\u303f\uff01-\uff60\uffe0-\uffe6'
PATS = [
    ('cjk+ascii', re.compile(r'(?:[' + CJK + r']+[A-Za-z]+[CJK]*)|(?:[A-Za-z]+[' + CJK + r']+[A-Za-z]*)|(?:[' + CJK + r']+[A-Za-z]{2,})')),
    ('latin-ext', re.compile(r'[\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff]')),
    ('full-extra', re.compile(r'[\uff61-\uffdc]')),
]

for f in sorted(glob.glob('/home/bons/ssss/web/_p*.html')):
    for i, line in enumerate(open(f, encoding='utf-8'), 1):
        s = re.sub(r'<[^>]*>', '\x00', line)
        for name, p in PATS:
            for m in p.finditer(s):
                ctx = s[max(0, m.start()-30):m.end()+30].replace('\x00', '|')
                print(f'{f.split("/")[-1]}:{i} [{name}] {m.group(0)!r}   << {ctx}')