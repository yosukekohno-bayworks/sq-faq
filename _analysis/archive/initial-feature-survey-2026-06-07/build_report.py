#!/usr/bin/env python3
"""SQ調査報告 _analysis/*.md を単一HTMLに統合（外部依存なし・自前md変換）。"""
import os, re, html as H

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    ("SUMMARY.md", "総括レポート", "overview"),
    ("COMPLEX-OPERATIONS.md", "難しい操作（複雑オペレーション）", "overview"),
    ("CONFIRMATION-LIST.md", "開発元への確認リスト（残る不確実性）", "overview"),
    ("00-admin-sitemap.md", "サイトマップ・接続情報", "base"),
    ("01-helpcenter-coverage-gap.md", "現行ヘルプ ギャップ分析", "base"),
    ("02-helpcenter-pages.md", "現行ヘルプ ページ品質", "base"),
    ("02-home.md", "ホーム", "feature"),
    ("03-products.md", "商品管理", "feature"),
    ("04-inventory.md", "在庫管理", "feature"),
    ("05-orders.md", "注文管理", "feature"),
    ("06-customers.md", "顧客管理", "feature"),
    ("07-purchase-orders.md", "発注管理", "feature"),
    ("08-sales-settings.md", "販売設定", "feature"),
    ("09-accounting.md", "会計", "feature"),
    ("10-analytics.md", "分析", "feature"),
    ("11-operations.md", "オペレーション（取り寄せ販売）", "feature"),
    ("12-crm.md", "CRM", "feature"),
    ("13-channels.md", "販売チャネル連携", "feature"),
    ("14-settings.md", "設定", "feature"),
    ("15-csv-pdf.md", "CSV/PDF", "feature"),
]
GROUPS = [("overview", "総括・難しい操作"), ("base", "全体像・現行ヘルプ"), ("feature", "機能別（画面・ボタン挙動）")]


def inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" loading="lazy" class="ss">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    return s


def cells(row):
    r = row.strip()
    if r.startswith('|'):
        r = r[1:]
    if r.endswith('|'):
        r = r[:-1]
    return [c.strip() for c in r.split('|')]


def md_to_html(md, key):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.DOTALL)
    lines = md.split('\n')
    out, h2s = [], []
    i, n, in_code, code_buf = 0, 0, False, []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('```'):
            if not in_code:
                in_code, code_buf = True, []
            else:
                in_code = False
                out.append('<pre><code>' + H.escape('\n'.join(code_buf)) + '</code></pre>')
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if line.lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            header = line
            k = i + 2
            rows = []
            while k < len(lines) and lines[k].lstrip().startswith('|'):
                rows.append(lines[k])
                k += 1
            t = ['<div class="tablewrap"><table><thead><tr>']
            t += [f'<th>{inline(c)}</th>' for c in cells(header)]
            t.append('</tr></thead><tbody>')
            for r in rows:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells(r)) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            i = k
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level, txt = len(m.group(1)), m.group(2).strip()
            n += 1
            hid = f'{key}__{n}'
            out.append(f'<h{level} id="{hid}">{inline(txt)}</h{level}>')
            if level == 2:
                h2s.append((hid, txt))
            i += 1
            continue
        if re.match(r'^\s*---+\s*$', line):
            out.append('<hr>')
            i += 1
            continue
        if line.lstrip().startswith('>'):
            q = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                q.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            out.append('<blockquote>' + inline(' '.join(q)) + '</blockquote>')
            continue
        if re.match(r'^\s*[-*]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
            ordered = bool(re.match(r'^\s*\d+\.\s+', line))
            items = []
            while i < len(lines) and (re.match(r'^\s*[-*]\s+', lines[i]) or re.match(r'^\s*\d+\.\s+', lines[i])):
                it = re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', lines[i])
                items.append(f'<li>{inline(it)}</li>')
                i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
            continue
        if line.strip() == '':
            i += 1
            continue
        para = [line]
        i += 1
        while (i < len(lines) and lines[i].strip() != ''
               and not re.match(r'^(#{1,6}\s|>|\s*[-*]\s|\s*\d+\.\s|```|\s*---+\s*$)', lines[i])
               and not lines[i].lstrip().startswith('|')):
            para.append(lines[i])
            i += 1
        out.append('<p>' + inline(' '.join(para)) + '</p>')
    return '\n'.join(out), h2s


def build():
    sections = []
    for fname, title, group in FILES:
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as f:
            md = f.read()
        key = re.sub(r'[^a-zA-Z0-9]', '_', fname)
        body, h2s = md_to_html(md, key)
        sections.append({'key': key, 'title': title, 'group': group, 'body': body, 'h2s': h2s, 'file': fname})

    nav = []
    for gkey, gtitle in GROUPS:
        nav.append(f'<div class="navgroup">{H.escape(gtitle)}</div>')
        for s in sections:
            if s['group'] != gkey:
                continue
            nav.append(f'<a class="navfile" href="#{s["key"]}__0">{H.escape(s["title"])}</a>')
            if s['h2s']:
                nav.append('<div class="navsub">')
                for hid, txt in s['h2s']:
                    nav.append(f'<a href="#{hid}">{H.escape(txt)}</a>')
                nav.append('</div>')
    nav_html = '\n'.join(nav)

    body_parts = []
    for s in sections:
        body_parts.append(f'<section class="filesec"><a id="{s["key"]}__0"></a><h1 class="filetitle">{H.escape(s["title"])} '
                          f'<span class="fname">{H.escape(s["file"])}</span></h1>{s["body"]}</section>')
    body_html = '\n'.join(body_parts)

    total_screens = len([f for f in os.listdir(os.path.join(BASE, 'screenshots'))]) if os.path.isdir(os.path.join(BASE, 'screenshots')) else 0

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQ 調査報告</title>
<style>
:root{{--bg:#0f1419;--panel:#1a2027;--ink:#e6edf3;--muted:#8b98a5;--line:#2d3640;--accent:#4a9eff;--accent2:#2ea043;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;line-height:1.8;color:#1a1f26;background:#f5f7fa;font-feature-settings:"palt";}}
.layout{{display:flex;align-items:flex-start}}
nav.side{{position:sticky;top:0;height:100vh;width:300px;flex:0 0 300px;overflow-y:auto;background:var(--bg);color:var(--ink);padding:18px 0;font-size:13px}}
nav.side .brand{{font-weight:700;font-size:16px;padding:0 18px 14px;color:#fff;border-bottom:1px solid var(--line);margin-bottom:10px}}
nav.side .brand small{{display:block;color:var(--muted);font-weight:400;font-size:11px;margin-top:4px}}
.navgroup{{color:var(--muted);font-size:11px;letter-spacing:.08em;padding:14px 18px 4px;text-transform:uppercase}}
a.navfile{{display:block;color:var(--ink);text-decoration:none;padding:6px 18px;font-weight:600}}
a.navfile:hover{{background:var(--panel);color:#fff}}
.navsub{{padding:2px 0 6px}}
.navsub a{{display:block;color:var(--muted);text-decoration:none;padding:3px 18px 3px 30px;font-size:12px;border-left:2px solid transparent}}
.navsub a:hover{{color:#fff;border-left-color:var(--accent)}}
main{{flex:1;min-width:0;padding:32px 48px 120px;max-width:1100px}}
.filesec{{margin-bottom:40px;background:#fff;border:1px solid #e3e8ee;border-radius:12px;padding:28px 34px;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
h1.filetitle{{font-size:24px;border-bottom:3px solid var(--accent);padding-bottom:10px;margin:0 0 18px;scroll-margin-top:16px}}
h1.filetitle .fname{{font-size:12px;color:#9aa6b2;font-weight:400;margin-left:8px}}
h2{{font-size:19px;margin:30px 0 12px;padding:8px 12px;background:linear-gradient(90deg,#eef5ff,transparent);border-left:4px solid var(--accent);scroll-margin-top:16px}}
h3{{font-size:16px;margin:22px 0 8px;color:#0b3d66;scroll-margin-top:16px}}
h4{{font-size:14px;margin:16px 0 6px;color:#33424f}}
p{{margin:8px 0}}
code{{background:#eef1f5;padding:1px 6px;border-radius:5px;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.88em;color:#bb2e55}}
pre{{background:#0f1419;color:#e6edf3;padding:14px 16px;border-radius:8px;overflow-x:auto}}
pre code{{background:none;color:inherit;padding:0}}
.tablewrap{{overflow-x:auto;margin:12px 0}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #dde3ea;padding:7px 10px;text-align:left;vertical-align:top}}
th{{background:#0b3d66;color:#fff;font-weight:600;position:sticky;top:0}}
tr:nth-child(even) td{{background:#f7f9fc}}
blockquote{{margin:12px 0;padding:10px 16px;background:#fff8e6;border-left:4px solid #f0b400;border-radius:0 8px 8px 0;color:#5a4a00}}
ul,ol{{margin:8px 0;padding-left:24px}}
li{{margin:3px 0}}
hr{{border:none;border-top:1px solid #e3e8ee;margin:20px 0}}
img.ss{{max-width:340px;max-height:240px;border:1px solid #d0d7de;border-radius:8px;cursor:zoom-in;margin:6px 8px 6px 0;vertical-align:top;background:#fff;transition:transform .1s}}
img.ss:hover{{transform:scale(1.02);border-color:var(--accent)}}
strong{{color:#0b2d4d}}
a{{color:#1a66c2}}
#lb{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:99;cursor:zoom-out;align-items:center;justify-content:center;padding:24px}}
#lb img{{max-width:96vw;max-height:94vh;border-radius:8px}}
.summary-bar{{background:var(--bg);color:var(--ink);padding:10px 48px;font-size:12px;color:var(--muted);position:sticky;top:0;z-index:10}}
@media(max-width:900px){{.layout{{flex-direction:column}}nav.side{{position:static;height:auto;width:100%;flex:none}}main{{padding:20px}}}}
</style></head>
<body>
<div class="layout">
<nav class="side">
<div class="brand">SQ 調査報告<small>ステージング全機能・画面別 / スクショ{total_screens}枚</small></div>
{nav_html}
</nav>
<main>
<div class="summary-bar">読み取り＋実機テスト（2026-06-05〜06）｜画像クリックで拡大</div>
{body_html}
</main>
</div>
<div id="lb"><img src="" alt=""></div>
<script>
document.addEventListener('click',function(e){{
  if(e.target.classList.contains('ss')){{var lb=document.getElementById('lb');lb.querySelector('img').src=e.target.src;lb.style.display='flex';}}
  else if(e.target.id==='lb'||e.target.parentNode.id==='lb'){{document.getElementById('lb').style.display='none';}}
}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')document.getElementById('lb').style.display='none';}});
</script>
</body></html>'''

    out_path = os.path.join(BASE, 'SQ-調査報告.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK: {out_path}')
    print(f'sections={len(sections)} screenshots={total_screens} bytes={len(html)}')


if __name__ == '__main__':
    build()
