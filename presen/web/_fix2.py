p = '/home/bons/ssss/web/_p3.html'
s = open(p, encoding='utf-8').read()

divider = '''<!-- ============ 02 セッション扉 ============ -->
<section class="sheet divider cat-deliver" data-t="納品物 扉">
  <div class="divider-in">
    <div class="divider-num">PART 02 — 納品物</div>
    <h1 class="divider-h1">納品物 6 項目</h1>
    <p class="divider-h2">要求 → 分析 → 設計 → 実装 → マニュアル → 実行イメージ。<br>
      10/28（水）提出分。 UML は分析与設計で 2 段階に分けて書く。</p>
    <div class="divider-list">
      <div><b>10</b>提出物一覧・チェックリスト</div>
      <div><b>11</b>要求：システム境界とアクター</div>
      <div><b>12</b>要求：ユースケース図</div>
      <div><b>13</b>要求：ユースケース仕様 UC1</div>
      <div><b>14</b>要求：ユースケース仕様 UC2 ほか</div>
      <div><b>15</b>分析：ロバストネス分析</div>
      <div><b>16</b>分析：分析クラス一覧</div>
      <div><b>17</b>分析：シーケンス図</div>
      <div><b>18</b>設計：パッケージ構成</div>
      <div><b>19</b>設計：クラス図</div>
      <div><b>20</b>設計：シーケンス図</div>
      <div><b>21</b>プログラム：構成と実行方法</div>
      <div><b>22</b>プログラム：主要ソースと導通テスト</div>
      <div><b>23</b>操作マニュアル</div>
      <div><b>24</b>実行イメージ（画面キャプチャ）</div>
    </div>
    <div class="divider-foot">
      <span>総合演習（卒業制作）／ 西尾 公伸 先生</span>
      <span>提出 2026.10.28（水）</span>
    </div>
  </div>
</section>

'''
marker = '<!-- ============ 02 納品物一覧 ============ -->'
assert marker in s
s = s.replace(marker, divider + marker, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok, divider inserted:', 'PART 02' in s)