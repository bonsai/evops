import re

p = '/home/bons/ssss/web/_p9.html'
s = open(p, encoding='utf-8').read()
s = s.replace('（clic は使わない）', '（クリック操作は使わない）')
s = s.replace('<b>実演の Zero：</b>', '<b>実演の前提：</b>')
open(p, 'w', encoding='utf-8').write(s)
for line in s.split('\n'):
    if 'クリック操作' in line or '実演の前提' in line:
        print(line.strip())