import re

p = '/home/bons/ssss/web/_p6.html'
s = open(p, encoding='utf-8').read()

s = s.replace('10/29（木）発表・実演　／　時間配分は p.25', '10/29（木）発表・実演　／　時間配分は p.32')
s = s.replace('簡単な説明（p.26）', '簡単な説明（p.27）')
s = s.replace('問題意識（p.27）', '問題意識（p.28）')
s = s.replace('機能説明（p.28）', '機能説明（p.29）')
s = s.replace('構造の説明（p.29）', '構造の説明（p.30）')
s = s.replace('実演（p.30）', '実演（p.31）')
s = s.replace('p.25–31 を埋めて', 'p.26–32 を埋めて')
s = s.replace('<span class="hd-no">25</span>', '<span class="hd-no">26</span>')
s = s.replace('data-t="発表 カバー"', 'data-t="発表 カバー"')

divider = '''<!-- ============ 03 セッション扉 ============ -->
<section class="sheet divider cat-present" data-t="発表 扉">
  <div class="divider-in">
    <div class="divider-num">PART 03 — 発表資料</div>
    <h1 class="divider-h1">発表資料 7 枚</h1>
    <p class="divider-h2">5 分の発表と実演のための 7 枚。<br>
      10/29（木）発表。印刷版をそのまま PDF にして 화면に流す。</p>
    <div class="divider-list">
      <div><b>26</b>発表カバー（氏名・システム名）</div>
      <div><b>27</b>システムの簡単な説明</div>
      <div><b>28</b>問題意識</div>
      <div><b>29</b>機能説明（ユースケース）</div>
      <div><b>30</b>構造の説明（設計モデル）</div>
      <div><b>31</b>実演</div>
      <div><b>32</b>全体スケジュールと振り返り</div>
    </div>
    <div class="divider-foot">
      <span>総合演習（卒業制作）／ 西尾 公伸 先生</span>
      <span>発表 2026.10.29（木）</span>
    </div>
  </div>
</section>

'''
if 'PART 03' not in s:
    idx = s.index('<section class="sheet cat-present"')
    s = s[:idx] + divider + s[idx:]

s = s.replace('印刷版をそのまま PDF にして 화면に流す', '印刷版をそのまま PDF にして画面に出す')

open(p, 'w', encoding='utf-8').write(s)
for line in s.split('\n'):
    if 'hd-no' in line or 'p.2' in line or 'p.3' in line or 'PART 03' in line:
        print(line.strip()[:150])