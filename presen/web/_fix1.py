import re, io

p = '/home/bons/ssss/web/_p2.html'
s = open(p, encoding='utf-8').read()

s2 = re.sub(r'data-go="(\d+)"', lambda m: 'data-go="%d"' % (int(m.group(1)) + 1), s)
s2 = s2.replace('（p.26–31）だけを使えば', '（p.26–32）だけを使えば')

# 検討項目セッション見開きを、目次（idx 1）の直後、検討1の前に挿入する
divider = '''<!-- ============ 01 セッション扉 ============ -->
<section class="sheet divider cat-plan" data-t="検討項目 扉">
  <div class="divider-in">
    <div class="divider-num">PART 01 — 検討項目</div>
    <h1 class="divider-h1">検討項目 1–5</h1>
    <p class="divider-h2">「何を作るか」から「何をどこまで作るか」まで。<br>
      10/02（金）提出分。この 5 枚が、以後のすべての設計の前提になる。</p>
    <div class="divider-list">
      <div><b>04</b>検討 1　何を作るか？</div>
      <div><b>05</b>検討 2　どんな効果があるか（何を解決するか）</div>
      <div><b>06</b>検討 3　Java か、Python か？</div>
      <div><b>07</b>検討 4　システムの全体像（自然語＋図）</div>
      <div><b>08</b>検討 5　開発対象（部分）機能・構造とスケジュール</div>
    </div>
    <div class="divider-foot">
      <span>総合演習（卒業制作）／ 西尾 公伸 先生</span>
      <span>提出 2026.10.02（金）</span>
    </div>
  </div>
</section>

'''
marker = '<!-- ============ 01 検討 1 ============ -->'
s2 = s2.replace(marker, divider + marker, 1)

open(p, 'w', encoding='utf-8').write(s2)
print('data-go bumped:', len(re.findall(r'data-go="\d+"', s2)))
print('divider inserted:', 'PART 01' in s2)