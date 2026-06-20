#!/usr/bin/env python3
"""SQサポートデスク: _support/ の索引データから、サポート担当者向けの逆引きHTMLを生成。
関連記事リンクは SQ-FAQ.html（build_help.py出力）の記事アンカーへ接続する。"""
import os, re, html as H, json

BASE = os.path.dirname(os.path.abspath(__file__))
SUP = os.path.join(BASE, '_support')
DIRS = ['00-getting-started', '01-by-feature', '02-by-task', '03-faq']

TABS = [
    ('symptoms.md', '🔎 症状から探す', 'symptom'),
    ('errors.md', '⚠️ エラー文言', 'error'),
    ('screens.md', '🗺 画面・URL', 'screen'),
    ('statuses.md', '📊 ステータス早見', 'status'),
    ('constraints.md', '🚧 制約・既知の問題', 'constraint'),
]


def article_keys():
    """build_help.py と同じロジックで 記事ファイル名→アンカーkey を作る"""
    keys, seen = {}, {}
    for d in DIRS:
        dd = os.path.join(BASE, d)
        if not os.path.isdir(dd):
            continue
        for fn in sorted(os.listdir(dd)):
            if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md':
                continue
            key = 'a-' + re.sub(r'[^a-zA-Z0-9]', '-', d + '-' + fn[:-3])[:70]
            if key in seen:
                seen[key] += 1
                key = f"{key}-{seen[key]}"
            else:
                seen[key] = 0
            keys[fn] = key
    return keys


def parse_table_md(path):
    """`# title` + markdown表 → (title, headers, rows)"""
    text = open(path, encoding='utf-8').read()
    title = (re.search(r'^#\s+(.+)$', text, re.M) or [None, os.path.basename(path)])[1]
    headers, rows = [], []
    for line in text.split('\n'):
        ls = line.strip()
        if not ls.startswith('|'):
            continue
        if re.match(r'^\|[\s:|-]+\|$', ls):
            continue
        cells = [c.strip() for c in ls.strip('|').split('|')]
        if not headers:
            headers = cells
        else:
            # 列数を揃える
            cells += [''] * (len(headers) - len(cells))
            rows.append(cells[:len(headers)])
    return title, headers, rows


def linkify_articles(cell, keys):
    parts = [p.strip() for p in cell.split('/') if p.strip()]
    out = []
    for p in parts:
        fn = p if p.endswith('.md') else p + '.md'
        if p == '-':
            return '<span class="dim">—</span>'
        if fn in keys:
            out.append(f'<a href="SQ-FAQ.html#{keys[fn]}" target="_blank">{H.escape(fn[:-3])}</a>')
        else:
            out.append(H.escape(p))
    return '<br>'.join(out) if out else '<span class="dim">—</span>'


def build():
    keys = article_keys()
    panels, tab_btns, search_rows = [], [], []
    for i, (fn, label, kind) in enumerate(TABS):
        path = os.path.join(SUP, fn)
        if not os.path.exists(path):
            print(f'WARN: {fn} がありません')
            continue
        title, headers, rows = parse_table_md(path)
        link_cols = [j for j, h in enumerate(headers) if '関連' in h or 'ガイド' in h]
        body = []
        for r in rows:
            tds = []
            plain = []
            for j, c in enumerate(r):
                if j in link_cols:
                    tds.append(f'<td class="lnk">{linkify_articles(c, keys)}</td>')
                else:
                    rendered = H.escape(c)
                    rendered = re.sub(r'「([^」]+)」', r'「<strong>\1</strong>」', rendered)
                    cls = ' class="first"' if j == 0 else ''
                    tds.append(f'<td{cls}>{rendered}</td>')
                    plain.append(c)
            body.append(f'<tr data-q="{H.escape(" ".join(plain))}">{"".join(tds)}</tr>')
            search_rows.append({'k': kind, 't': r[0][:60], 'x': ' '.join(r)[:300]})
        thead = ''.join(f'<th>{H.escape(h)}</th>' for h in headers)
        active = ' active' if i == 0 else ''
        panels.append(f'''<section class="panel{active}" data-kind="{kind}">
          <div class="tablewrap"><table><thead><tr>{thead}</tr></thead><tbody>{''.join(body)}</tbody></table></div>
          <p class="empty" style="display:none">この条件に一致する行はありません</p>
        </section>''')
        tab_btns.append(f'<button class="tab{active}" data-kind="{kind}">{label}<span class="cnt">{len(rows)}</span></button>')

    page = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQ サポートデスク（逆引き）</title>
<style>
:root {{ --main:#2864f0; --link:#2864f0; --accent:#1e46aa; --ink:#323232; --grey:#8c8989;
  --line:#e9e7e7; --bg:#f7f5f5; --head:#f0eded; --white:#fff; --warnbg:#fff7e0; --pale:#ebf3ff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:'-apple-system',BlinkMacSystemFont,'Helvetica Neue','ヒラギノ角ゴ ProN','Hiragino Kaku Gothic ProN',Arial,'メイリオ',Meiryo,sans-serif;
  color:var(--ink); background:var(--bg); line-height:1.7; font-feature-settings:"palt"; font-size:13.5px; }}
a {{ color:var(--link); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
header {{ position:sticky; top:0; z-index:20; background:var(--white); border-bottom:1px solid var(--line); padding:10px 20px;
  display:flex; align-items:center; gap:16px; flex-wrap:wrap; }}
header .logo {{ font-weight:700; font-size:15px; white-space:nowrap; }}
header .logo span {{ color:var(--main); }}
header .sub {{ font-size:11.5px; color:var(--grey); }}
.searchwrap {{ position:relative; flex:1; min-width:260px; max-width:560px; }}
.searchwrap input {{ width:100%; padding:9px 14px 9px 36px; border:1px solid #ccc; border-radius:8px;
  font-size:14px; background:var(--white); outline:none; font-family:inherit; color:var(--ink); }}
.searchwrap input:focus {{ border-color:var(--main); box-shadow:0 0 0 3px #dce8ff; }}
.searchwrap::before {{ content:"🔍"; position:absolute; left:12px; top:50%; transform:translateY(-50%); font-size:13px; opacity:.6; }}
.helplink {{ font-size:12.5px; white-space:nowrap; }}
nav.tabs {{ display:flex; gap:6px; padding:10px 20px 0; max-width:1400px; margin:0 auto; flex-wrap:wrap; }}
.tab {{ border:1px solid var(--line); border-bottom:none; background:var(--head); padding:9px 16px; border-radius:12px 12px 0 0;
  font-size:13px; cursor:pointer; font-family:inherit; color:var(--grey); font-weight:600; }}
.tab.active {{ background:var(--white); color:var(--ink); }}
.tab .cnt {{ margin-left:6px; font-size:11px; background:var(--bg); border-radius:8px; padding:0 6px; color:var(--grey); }}
.tab.active .cnt {{ background:var(--pale); color:var(--main); }}
main {{ max-width:1400px; margin:0 auto; padding:0 20px 60px; }}
.panel {{ display:none; background:var(--white); border:1px solid var(--line); border-radius:0 12px 12px 12px; padding:6px; box-shadow:0 0 1rem rgba(0,0,0,.06), 0 .125rem .25rem rgba(0,0,0,.1); }}
.panel.active {{ display:block; }}
.tablewrap {{ overflow-x:auto; max-height:calc(100vh - 150px); }}
table {{ border-collapse:collapse; width:100%; }}
th {{ background:var(--head); text-align:left; padding:8px 12px; border:1px solid #ddd9d3; font-size:12px; white-space:nowrap;
  position:sticky; top:0; z-index:5; }}
td {{ padding:7px 12px; border:1px solid var(--line); vertical-align:top; }}
td.first {{ font-weight:600; min-width:180px; }}
td.lnk {{ white-space:nowrap; font-size:12.5px; }}
tbody tr:nth-child(even) {{ background:#fcfbfa; }}
tbody tr.hit {{ background:var(--pale); }}
tbody tr.hidden {{ display:none; }}
.dim {{ color:#c1bdb7; }}
strong {{ color:var(--accent); font-weight:700; }}
td.first strong {{ color:inherit; }}
.empty {{ text-align:center; color:var(--grey); padding:30px; }}
@media (max-width:800px) {{ td.lnk {{ white-space:normal; }} }}
</style></head>
<body>
<header>
  <div><div class="logo">SQ <span>サポートデスク</span></div><div class="sub">問い合わせ対応用の逆引きリファレンス</div></div>
  <div class="searchwrap"><input id="q" type="search" placeholder="全タブを横断絞り込み（例: 巻き戻す / マイナス / 500 / 売上実績）"></div>
  <a class="helplink" href="SQ-FAQ.html" target="_blank">📖 ヘルプセンターを開く ↗</a>
</header>
<nav class="tabs">{''.join(tab_btns)}</nav>
<main>{''.join(panels)}</main>
<script>
const tabs = document.querySelectorAll('.tab'), panels = document.querySelectorAll('.panel');
tabs.forEach(t => t.addEventListener('click', () => {{
  tabs.forEach(x => x.classList.toggle('active', x === t));
  panels.forEach(p => p.classList.toggle('active', p.dataset.kind === t.dataset.kind));
}}));
const q = document.getElementById('q');
q.addEventListener('input', () => {{
  const terms = q.value.trim().split(/\\s+/).filter(Boolean);
  const counts = {{}};
  panels.forEach(p => {{
    let visible = 0;
    p.querySelectorAll('tbody tr').forEach(tr => {{
      const text = tr.dataset.q + ' ' + tr.innerText;
      const ok = terms.every(t => text.includes(t));
      tr.classList.toggle('hidden', !ok);
      tr.classList.toggle('hit', ok && terms.length > 0);
      if (ok) visible++;
    }});
    counts[p.dataset.kind] = visible;
    p.querySelector('.empty').style.display = visible ? 'none' : '';
  }});
  tabs.forEach(t => {{ t.querySelector('.cnt').textContent = counts[t.dataset.kind] ?? 0; }});
  // ヒットが現在タブに無ければ、最初にヒットがあるタブへ自動切替
  if (terms.length) {{
    const cur = document.querySelector('.panel.active');
    if (counts[cur.dataset.kind] === 0) {{
      for (const t of tabs) {{ if (counts[t.dataset.kind] > 0) {{ t.click(); break; }} }}
    }}
  }}
}});
</script>
</body></html>'''
    out = os.path.join(BASE, 'SQ-サポートデスク.html')
    open(out, 'w', encoding='utf-8').write(page)
    total = sum(1 for _ in re.finditer(r'<tr data-q', page))
    print(f'OK: {out} rows={total} bytes={len(page.encode())}')


if __name__ == '__main__':
    build()
