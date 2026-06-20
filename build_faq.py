#!/usr/bin/env python3
"""FAQを多軸(機能/作業/動作/ロール/FAQ)で切り替えられる単一HTMLに統合。外部依存なし。"""
import os, re, html as H

BASE = os.path.dirname(os.path.abspath(__file__))  # faq/
DIRS = ['00-getting-started', '01-by-feature', '02-by-task', '03-faq', '04-tips']


def inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
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
    out = []
    i, n, in_code, code_buf, code_lang = 0, 0, False, [], ''
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('```'):
            if not in_code:
                in_code, code_buf = True, []
                code_lang = line.strip()[3:].strip()
            else:
                in_code = False
                if code_lang == 'mermaid':
                    out.append('<pre class="mermaid">' + H.escape('\n'.join(code_buf)) + '</pre>')
                else:
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
            out.append(f'<h{min(level + 1, 6)} id="{key}__{n}">{inline(txt)}</h{min(level + 1, 6)}>')
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
    return '\n'.join(out)


def parse_fm(md):
    meta = {}
    body = md
    m = re.match(r'^\s*---\s*\n(.*?)\n---\s*\n?(.*)$', md, re.DOTALL)
    if m:
        fm_text, body = m.group(1), m.group(2)
        for line in fm_text.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                k, v = line.split(':', 1)
                k = k.strip()
                v = re.sub(r'\s+#.*$', '', v).strip()
                if v.startswith('[') and v.endswith(']'):
                    meta[k] = [x.strip() for x in v[1:-1].split(',') if x.strip()]
                else:
                    meta[k] = v
    return meta, body


def aslist(v):
    if isinstance(v, list):
        return v
    return [v] if v else []


def status_badge(s):
    if '要確認' in s:
        return '<span class="badge warn">⚠ 要確認</span>'
    if '確定' in s:
        return '<span class="badge ok">✓ 確定</span>'
    return ''


def build():
    articles = []
    for d in DIRS:
        dd = os.path.join(BASE, d)
        if not os.path.isdir(dd):
            continue
        for fn in sorted(os.listdir(dd)):
            if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md':
                continue
            with open(os.path.join(dd, fn), encoding='utf-8') as f:
                md = f.read()
            meta, body = parse_fm(md)
            key = re.sub(r'[^a-zA-Z0-9]', '_', d + '_' + fn)[:60]
            articles.append({
                'key': key, 'dir': d, 'file': fn,
                'title': meta.get('title', fn[:-3]),
                'type': meta.get('type', ''),
                'task': meta.get('task', ''),
                'feature': aslist(meta.get('feature')),
                'action': aslist(meta.get('action')),
                'role': aslist(meta.get('role')),
                'status': meta.get('status', ''),
                'tags': aslist(meta.get('tags')),
                'body': md_to_html(body, key),
            })

    AXES = [
        ('start', '🚀 はじめに', lambda a: ['はじめに'] if a['type'] in ('はじめに',) else []),
        ('role', '👤 ロール別', lambda a: a['role']),
        ('action', '🛠 作業手順', lambda a: a['action'] or ([a['task']] if a['task'] else [])),
        ('feature', '📖 機能説明書', lambda a: a['feature']),
        ('tips', '💡 活用Tips', lambda a: ['活用Tips'] if a['type'] in ('活用Tips', 'Tips') else []),
        ('faq', '❓ よくある質問', lambda a: ['FAQ'] if a['type'] in ('FAQ別', 'FAQ') else []),
    ]

    nav_panels = []
    tab_btns = []
    for idx, (akey, label, getter) in enumerate(AXES):
        groups = {}
        for a in articles:
            cats = getter(a) or ['（未分類）']
            for c in cats:
                groups.setdefault(c, []).append(a)
        rows = []
        for cat in sorted(groups):
            rows.append(f'<div class="navgroup">{H.escape(str(cat))}</div>')
            for a in groups[cat]:
                rows.append(f'<a class="navfile" href="#{a["key"]}">{H.escape(a["title"])}</a>')
        active = ' active' if idx == 0 else ''
        nav_panels.append(f'<div class="navpanel{active}" data-axis="{akey}">{"".join(rows)}</div>')
        tab_btns.append(f'<button class="tab{active}" data-axis="{akey}">{label}</button>')

    body_html = '\n'.join(
        f'<section class="art"><a id="{a["key"]}"></a><h1>{H.escape(a["title"])} {status_badge(a["status"])}</h1>'
        f'<div class="meta">作業: {H.escape(a["task"] or "—")}　|　動作: {H.escape("・".join(a["action"]) or "—")}　|　ロール: {H.escape("・".join(a["role"]) or "—")}</div>'
        f'{a["body"]}</section>'
        for a in articles)

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQ FAQ（多軸ビュー）</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;line-height:1.8;color:#1a1f26;background:#f5f7fa;font-feature-settings:"palt"}}
.layout{{display:flex;align-items:flex-start}}
nav.side{{position:sticky;top:0;height:100vh;width:300px;flex:0 0 300px;overflow-y:auto;background:#0f1419;color:#e6edf3;padding:0 0 24px}}
.brand{{font-weight:700;font-size:16px;padding:18px 18px 12px;color:#fff;border-bottom:1px solid #2d3640}}
.brand small{{display:block;color:#8b98a5;font-weight:400;font-size:11px;margin-top:4px}}
.tabs{{display:flex;flex-wrap:wrap;gap:4px;padding:10px 12px;border-bottom:1px solid #2d3640;position:sticky;top:0;background:#0f1419;z-index:2}}
.tab{{flex:1 0 auto;background:#1a2027;color:#8b98a5;border:1px solid #2d3640;border-radius:6px;padding:6px 8px;font-size:12px;cursor:pointer;white-space:nowrap}}
.tab.active{{background:#4a9eff;color:#fff;border-color:#4a9eff}}
.navpanel{{display:none;padding:8px 0}}
.navpanel.active{{display:block}}
.navgroup{{color:#8b98a5;font-size:11px;letter-spacing:.06em;padding:12px 18px 4px;text-transform:uppercase}}
a.navfile{{display:block;color:#e6edf3;text-decoration:none;padding:5px 18px 5px 26px;font-size:13px;border-left:2px solid transparent}}
a.navfile:hover{{background:#1a2027;color:#fff;border-left-color:#4a9eff}}
main{{flex:1;min-width:0;padding:28px 44px 120px;max-width:980px}}
.art{{background:#fff;border:1px solid #e3e8ee;border-radius:12px;padding:26px 32px;margin-bottom:28px;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.art h1{{font-size:23px;border-bottom:3px solid #4a9eff;padding-bottom:10px;margin:0 0 6px;scroll-margin-top:12px}}
.meta{{font-size:12px;color:#6b7785;margin-bottom:16px}}
.badge{{font-size:12px;padding:2px 8px;border-radius:10px;vertical-align:middle}}
.badge.ok{{background:#e3f6e8;color:#1a7f37}}
.badge.warn{{background:#fff4d6;color:#9a6700}}
h2{{font-size:18px;margin:26px 0 10px;padding:7px 12px;background:linear-gradient(90deg,#eef5ff,transparent);border-left:4px solid #4a9eff;scroll-margin-top:12px}}
h3{{font-size:15px;margin:18px 0 6px;color:#0b3d66}}
p{{margin:8px 0}}
code{{background:#eef1f5;padding:1px 6px;border-radius:5px;font-size:.88em;color:#bb2e55}}
pre{{background:#0f1419;color:#e6edf3;padding:14px 16px;border-radius:8px;overflow-x:auto}}
pre code{{background:none;color:inherit;padding:0}}
.tablewrap{{overflow-x:auto;margin:12px 0}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #dde3ea;padding:7px 10px;text-align:left;vertical-align:top}}
th{{background:#0b3d66;color:#fff}}
tr:nth-child(even) td{{background:#f7f9fc}}
blockquote{{margin:12px 0;padding:10px 16px;background:#fff8e6;border-left:4px solid #f0b400;border-radius:0 8px 8px 0;color:#5a4a00}}
ul,ol{{margin:8px 0;padding-left:24px}}
li{{margin:3px 0}}
hr{{border:none;border-top:1px solid #e3e8ee;margin:18px 0}}
strong{{color:#0b2d4d}}
.mermaid{{background:#fff;border:1px solid #dde3ea;border-radius:10px;padding:20px;margin:16px 0;overflow-x:auto;text-align:center;font-size:15px}}
.mermaid svg{{max-width:100%;height:auto}}
@media(max-width:880px){{.layout{{flex-direction:column}}nav.side{{position:static;height:auto;width:100%;flex:none}}main{{padding:18px}}}}
</style></head>
<body>
<div class="layout">
<nav class="side">
<div class="brand">SQ FAQ<small>多軸ビュー（{len(articles)}記事）</small></div>
<div class="tabs">{"".join(tab_btns)}</div>
{"".join(nav_panels)}
</nav>
<main>{body_html}</main>
</div>
<script>
document.querySelectorAll('.tab').forEach(function(t){{
  t.addEventListener('click',function(){{
    var ax=t.dataset.axis;
    document.querySelectorAll('.tab').forEach(function(x){{x.classList.toggle('active',x.dataset.axis===ax)}});
    document.querySelectorAll('.navpanel').forEach(function(p){{p.classList.toggle('active',p.dataset.axis===ax)}});
  }});
}});
</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({{ startOnLoad: true, theme: 'default', flowchart: {{ curve: 'basis', nodeSpacing: 50, rankSpacing: 60, padding: 14, useMaxWidth: true }} }});
</script>
</body></html>'''

    out_path = os.path.join(BASE, 'SQ-FAQ.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK: {out_path}')
    print(f'articles={len(articles)} bytes={len(html)}')


if __name__ == '__main__':
    build()
