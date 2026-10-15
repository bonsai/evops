p = '/home/bons/ssss/web/_p10.html'
s = open(p, encoding='utf-8').read()

s = s.replace('<li>背景の色を「Graphics」で印刷</li>',
              '<li>背景の色を出力する設定にする（「More settings → Background graphics」）。</li>')

s = s.replace('    <span class="hd-no">—</span>', '    <span class="hd-no">33</span>')
s = s.replace('印刷・提出の前にここを 1 回通す。',
              '印刷・提出の前にここを 1 回通す。／ このページは GitHub Pages で公開中。')

s = s.replace('''<div class="note warn">
          <b>提出前に：</b>ファイル名を <code>総合演習_&lt;氏名&gt;_&lt;システム名&gt;.html</code> にリネームする。
          <code>index.html</code> のままだと内容が分からない。
        </div>''', '''<div class="note warn">
          <b>提出前に：</b>ファイル名を <code>総合演習_&lt;氏名&gt;_&lt;システム名&gt;.html</code> にリネームする。
          <code>index.html</code> のままだと内容が分からない。
        </div>
        <div class="card soft">
          <div class="card-h">この資料の公開先</div>
          <p><small>GitHub Pages で公開している。</small></p>
          <p><code style="font-size:8.4mm">https://bonsai.github.io/ssss/</code></p>
          <p><small>同上。発表・実演のときはこの URL をブラウザで開いた印刷ビュー、または印刷した PDF を使う。</small></p>
        </div>''')

open(p, 'w', encoding='utf-8').write(s)
print('public url added:', 'bonsai.github.io/ssss' in s)