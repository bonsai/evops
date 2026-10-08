import re

P = '/home/bons/ssss/presen/web/index.html'
s = open(P, encoding='utf-8').read()

gos = sorted(set(int(g) for g in re.findall(r'data-go="(\d+)"', s)))
print('data-go values:', gos)
bad = [g for g in gos if not (1 <= g <= 33)]
print('out of range:', bad)

ids = ['id="stage"', 'id="sheets"', 'id="nav"', 'id="curNo"', 'id="curAll"', 'id="curTtl"',
       'id="first"', 'id="prev"', 'id="next"', 'id="last"']
for i in ids:
    print(('OK  ' if i in s else 'MISS'), i)

# 目次表示と実ページの突き合わせ
titles = re.findall(r'<span class="tg">([^<]+)</span>', s)
pg = re.findall(r'<span class="pg">([^<]+)</span>', s)
titles = [t for t in titles if t.strip()]
print('toc entries:', len(titles))
for t, p in list(zip(titles, pg))[:5]:
    print(' ', p, t)
for t, p in list(zip(titles, pg))[-8:]:
    print(' ', p, t)

# 要約
print('total bytes:', len(s.encode('utf-8')))
print('script blocks:', s.count('<script>'))
print('closing html:', s.rstrip().endswith('</html>'))