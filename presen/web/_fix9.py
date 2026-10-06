subs = {
    '/home/bons/ssss/web/_p2.html': [
        ('<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.02（金）</span>',
         '<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.02（金）　／　p.03</span>'),
        ('<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.28（水）</span>',
         '<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.28（水）　／　p.09</span>'),
        ('<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.28（水）</span>'.replace('提出', '発表 2026.10.29（木）'),
         '<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>発表 2026.10.29（木）　／　p.25</span>'),
        ('<span>A4 横・全 33 ページ／ウェブ発表と印刷提出を兼用</span>',
         '<span>A4 横・全 33 ページ／ウェブ発表と印刷提出を兼用</span>'),
        ('<span>印刷：Ctrl / ⌘ + P　→　向き「横」・倍率 100%・余白「なし」</span>',
         '<span>印刷：Ctrl / ⌘ + P　→　向き「横」・倍率 100%・余白「なし」　／　p.01</span>'),
    ],
    '/home/bons/ssss/web/_p3.html': [
        ('<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.28（水）</span>',
         '<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>提出 2026.10.28（水）　／　p.09</span>'),
    ],
    '/home/bons/ssss/web/_p6.html': [
        ('<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>発表 2026.10.29（木）</span>',
         '<span>総合演習（卒業制作）／ 西尾 公伸 先生</span>\n      <span>発表 2026.10.29（木）　／　p.25</span>'),
    ],
}

for path, pairs in subs.items():
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in s:
            print('MISS', path.split('/')[-1], repr(a[:60]))
            continue
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path.split('/')[-1])