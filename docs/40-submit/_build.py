import os, re

D = os.path.dirname(os.path.abspath(__file__))
parts = ['_p1', '_p2', '_p3', '_p4', '_p5', '_p6', '_p7', '_p8', '_p9', '_p10', '_p11']
out = []
for p in parts:
    path = os.path.join(D, p + '.html')
    s = open(path, encoding='utf-8').read().rstrip('\n')
    out.append(s)

html = '\n\n'.join(out) + '\n'

# 素朴なタグ整合チェック
stack = []
void = {'meta', 'br', 'hr', 'img', 'input', 'link', 'source', 'col', 'area', 'base', 'wbr'}
for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>', html):
    closing, name, attrs, selfc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
    if name in void or selfc:
        continue
    if closing:
        if stack and stack[-1][0] == name:
            stack.pop()
        else:
            print('MISMATCH close', name, 'top=', stack[-1] if stack else None)
    else:
        stack.append((name, m.start()))

print('unclosed:', [(n, html[:p].count('\n') + 1) for n, p in stack])
print('sheets:', html.count('<section class="sheet'))
print('divider sheets:', html.count('class="sheet divider'))
print('bytes:', len(html.encode('utf-8')))

target = os.path.join(D, 'index.html')
open(target, 'w', encoding='utf-8').write(html)
print('written:', target)