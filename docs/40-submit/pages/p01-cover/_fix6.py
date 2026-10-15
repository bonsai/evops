p = '/home/bons/ssss/web/_p10.html'
s = open(p, encoding='utf-8').read()

s = s.replace('実績を入れない反射。工数（h）は見積ではなく実測。',
              '実績をそのまま書く。工数（h）は見積ではなく実測。')
s = s.replace('背景の色を「背景 Hamparts  graphics」で印刷',
              '背景の色を「Graphics」で印刷')

open(p, 'w', encoding='utf-8').write(s)
for line in s.split('\n'):
    if any(k in line for k in ('実績を', '背景')):
        print(line.strip()[:160])