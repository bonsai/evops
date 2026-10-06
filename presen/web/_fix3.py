import re

p = '/home/bons/ssss/web/_p8.html'
s = open(p, encoding='utf-8').read()

s = re.sub(r'<li>「詳細は資料[^<]*</li>',
           '<li>「詳細は資料に_instructions_error」__PLACEHOLDER__</li>', s)
s = s.replace('__PLACEHOLDER__', 'と一言で締める。')
s = s.replace('_instructions_error', '書いてあります')

s = re.sub(r'p\.13 の例外フローが実演で_possibleか確認する。',
           'p.13 の例外フローが実演で見せられるか確認する。', s)

open(p, 'w', encoding='utf-8').write(s)
for line in s.split('\n'):
    if '詳細は資料' in line or '例外フロー' in line:
        print(line.strip())