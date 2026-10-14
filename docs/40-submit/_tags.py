import re, glob, os

VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'path', 'circle', 'line',
        'rect', 'ellipse', 'polygon', 'use', 'stop', 'marker', 'area', 'col'}
SKIP = re.compile(r'<!--.*?-->', re.S)
SCRIPT = re.compile(r'<script\b.*?</script>|<style\b.*?</style>', re.S | re.I)

d = '/home/bons/ssss/web'
for p in sorted(glob.glob(os.path.join(d, '_p*.html'))):
    s = open(p, encoding='utf-8').read()
    s = SKIP.sub('', s)
    s = SCRIPT.sub('', s)
    stack = []
    errs = []
    for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>', s):
        close, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or attrs.rstrip().endswith('/'):
            continue
        line = s[:m.start()].count('\n') + 1
        if close:
            if stack and stack[-1][0] == tag:
                stack.pop()
            else:
                errs.append(f'line {line}: unexpected </{tag}> (open={stack[-1] if stack else None})')
                if stack and any(t == tag for t, _ in stack):
                    while stack and stack.pop()[0] != tag:
                        pass
        else:
            stack.append((tag, line))
    print(f'{os.path.basename(p)}: {"OK" if not errs and not stack else "PROBLEM"}')
    for t, l in stack:
        print(f'  unclosed <{t}> opened line {l}')
    for e in errs[:10]:
        print('  ' + e)