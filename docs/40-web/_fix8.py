fixes = {
    '/home/bons/ssss/web/_p2.html': [
        ('A4 横・全 32 ページ／ウェブ発表と印刷提出を兼用',
         'A4 横・全 33 ページ／ウェブ発表と印刷提出を兼用'),
    ],
    '/home/bons/ssss/web/_p9.html': [
        ('（A4 横・32 枚）', '（A4 横・33 枚）'),
    ],
    '/home/bons/ssss/web/_p10.html': [
        ('要求モデル完成（p.12–15）', '要求モデル完成（p.11–14）'),
        ('分析モデル完成（p.16–18）', '分析モデル完成（p.15–17）'),
        ('設計モデル完成（p.19–21）', '設計モデル完成（p.18–20）'),
        ('総枚数 32 枚（ stapling で左綴じ）', '総枚数 33 枚'),
    ],
}

for path, pairs in fixes.items():
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in s:
            print('MISS', path.split('/')[-1], repr(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print('fixed', path.split('/')[-1])