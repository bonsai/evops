import re, os

d = '/home/bons/ssss/web'
parts = ['_p2', '_p3', '_p4', '_p5', '_p6', '_p7', '_p8', '_p9', '_p10']
idx = 0
rows = []
for p in parts:
    s = open(os.path.join(d, p + '.html'), encoding='utf-8').read()
    for m in re.finditer(r'<section class="([^"]*)" data-t="([^"]*)"', s):
        cls, t = m.group(1), m.group(2)
        start = m.end()
        nxt = s.find('<section class="', start)
        chunk = s[start:nxt if nxt != -1 else len(s)]
        no = re.search(r'<span class="hd-no">([^<]*)</span>', chunk)
        rows.append((idx, t, no.group(1) if no else '—', 'divider' in cls))
        idx += 1

print('idx  hd-no  sheet-title')
for i, t, no, isdiv in rows:
    flag = ' [divider]' if isdiv else ''
    print(f'{i:3d}  {no:>5}  {t}{flag}')
print('TOTAL SHEETS', idx)

nums = [r[2] for r in rows if r[2].isdigit()]
print('numbered pages:', len(nums), 'max', max(int(n) for n in nums))
missing = [n for n in range(1, max(int(n) for n in nums) + 1) if str(n) not in nums]
print('missing numbers:', missing)