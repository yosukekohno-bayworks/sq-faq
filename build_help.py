#!/usr/bin/env python3
"""SQヘルプセンター: FAQ群を読みやすい単一HTMLに統合する（外部依存なし）。
デザイン: freee Vibes Design System のトークンに準拠（親しみやすい業務UI・初心者配慮）。
出力は SQ-FAQ.html を上書き。"""
import os, re, html as H, json

BASE = os.path.dirname(os.path.abspath(__file__))
GROUPS = [
    ('00-getting-started', 'はじめに', '🚀', 'SQの全体像をつかむ'),
    ('01-by-feature', '機能ガイド', '📖', '画面ごとの説明書'),
    ('02-by-task', '操作手順', '🛠', 'やりたい作業の手順書'),
    ('03-faq', 'よくある質問', '💬', 'Q&A形式で探す'),
]
START_HERE = ['SQ実測学習ガイド', 'SQ完全ガイド', 'SQをはじめる-全機能ガイド', 'セットアップガイド', 'データ事典①-設定で作るデータ', 'データ事典②-商品・在庫・運用のデータとステータス', 'データの流れ-図解', '取り寄せ販売の処理手順']


def parse_fm(md):
    meta, body = {}, md
    m = re.match(r'^\s*---\s*\n(.*?)\n---\s*\n?(.*)$', md, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                k, v = line.split(':', 1)
                v = re.sub(r'\s+#.*$', '', v).strip()
                meta[k.strip()] = v
        body = m.group(2)
    return meta, body


def inline(s, linkmap):
    s = H.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<figure><img src="\2" alt="\1" loading="lazy"><figcaption>\1</figcaption></figure>', s)

    def link(m):
        text, href = m.group(1), m.group(2)
        base = os.path.basename(href.split('#')[0])
        if base.endswith('.md') and base in linkmap:
            return f'<a href="#{linkmap[base]}" class="ilink">{text}</a>'
        if href.startswith('http'):
            return f'<a href="{href}" target="_blank" rel="noopener">{text} ↗</a>'
        if base.endswith('.html'):
            return f'<a href="{base}" target="_blank" rel="noopener">{text} ↗</a>'
        return text
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    return s


def cells(row):
    r = row.strip().strip('|')
    return [c.strip() for c in r.split('|')]


def md_to_html(md, key, linkmap):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.DOTALL)
    lines = md.split('\n')
    out, toc = [], []
    i, in_code, code_buf, code_lang, hn = 0, False, [], '', 0
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
                rows.append(lines[k]); k += 1
            t = ['<div class="tablewrap"><table><thead><tr>']
            t += [f'<th>{inline(c, linkmap)}</th>' for c in cells(header)]
            t.append('</tr></thead><tbody>')
            for r in rows:
                t.append('<tr>' + ''.join(f'<td>{inline(c, linkmap)}</td>' for c in cells(r)) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            i = k
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            lvl = len(m.group(1))
            text = m.group(2).strip()
            if lvl == 1:
                i += 1
                continue
            hn += 1
            hid = f'{key}-h{hn}'
            if lvl == 2:
                toc.append((hid, re.sub(r'<[^>]+>', '', inline(text, linkmap))))
            out.append(f'<h{lvl} id="{hid}">{inline(text, linkmap)}</h{lvl}>')
            i += 1
            continue
        if re.match(r'^\s*>\s?', line):
            buf = []
            while i < len(lines) and re.match(r'^\s*>\s?', lines[i]):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            joined = ' '.join(buf)
            warn = any(w in joined for w in ['注意', '警告', '巻き戻', '取り消せ', '行き止まり'])
            cls = 'callout warn' if warn else 'callout'
            icon = '⚠️' if warn else '💡'
            body = '<br>'.join(inline(b, linkmap) for b in buf if b.strip() != '')
            out.append(f'<div class="{cls}"><span class="cicon">{icon}</span><div>{body}</div></div>')
            continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', line)
        if m:
            ordered = m.group(2)[0].isdigit()
            tag = 'ol' if ordered else 'ul'
            buf = []
            while i < len(lines):
                mm = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', lines[i])
                if mm:
                    buf.append(mm.group(3))
                    i += 1
                elif lines[i].startswith(('   ', '\t')) and lines[i].strip() and buf:
                    buf[-1] += '<br>' + lines[i].strip()
                    i += 1
                else:
                    break
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(b, linkmap)}</li>' for b in buf) + f'</{tag}>')
            continue
        if line.strip() == '---':
            out.append('<hr>')
            i += 1
            continue
        if line.strip():
            out.append(f'<p>{inline(line.strip(), linkmap)}</p>')
        i += 1
    return ''.join(out), toc


def build():
    arts = []
    for d, glabel, gicon, gdesc in GROUPS:
        dd = os.path.join(BASE, d)
        if not os.path.isdir(dd):
            continue
        for fn in sorted(os.listdir(dd)):
            if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md':
                continue
            meta, body = parse_fm(open(os.path.join(dd, fn), encoding='utf-8').read())
            key = 'a-' + re.sub(r'[^a-zA-Z0-9]', '-', d + '-' + fn[:-3])[:70]
            arts.append({'key': key, 'dir': d, 'glabel': glabel, 'gicon': gicon, 'fn': fn,
                         'title': meta.get('title', fn[:-3]), 'status': meta.get('status', ''),
                         'body': body})
    seen = {}
    for a in arts:
        k = a['key']
        if k in seen:
            seen[k] += 1
            a['key'] = f"{k}-{seen[k]}"
        else:
            seen[k] = 0
    linkmap = {a['fn']: a['key'] for a in arts}

    for a in arts:
        html, toc = md_to_html(a['body'], a['key'], linkmap)
        def fix_src(m, d=a['dir']):
            src = m.group(1)
            if src.startswith('http'):
                return m.group(0)
            p = os.path.normpath(os.path.join(d, src))
            return m.group(0).replace(src, p.replace(os.sep, '/'))
        html = re.sub(r'<img src="([^"]+)"', fix_src, html)
        a['html'], a['toc'] = html, toc
        a['plain'] = re.sub(r'<[^>]+>', ' ', html)[:6000]

    # ---- sidebar（折りたたみグループ） ----
    nav = []
    for gi, (d, glabel, gicon, gdesc) in enumerate(GROUPS):
        items = [a for a in arts if a['dir'] == d]
        opened = ' open' if gi == 0 else ''
        nav.append(f'''<details class="navgroup" data-dir="{d}"{opened}>
          <summary><span class="gicon">{gicon}</span>{glabel}<span class="navcount">{len(items)}</span></summary><ul>''')
        for a in items:
            nav.append(f'<li><a href="#{a["key"]}" data-key="{a["key"]}">{H.escape(a["title"])}</a></li>')
        nav.append('</ul></details>')
    nav_html = ''.join(nav)

    # ---- home ----
    cards = []
    for d, glabel, gicon, gdesc in GROUPS:
        items = [a for a in arts if a['dir'] == d]
        first = items[0]['key'] if items else ''
        cards.append(f'''<a class="card" href="#{first}" data-group="{d}">
          <span class="cardicon">{gicon}</span>
          <span class="cardbody"><span class="cardtitle">{glabel}</span>
          <span class="carddesc">{gdesc}</span></span>
          <span class="cardcount">{len(items)}件 ›</span></a>''')
    start_links = []
    for name in START_HERE:
        hit = next((a for a in arts if a['fn'][:-3] == name), None)
        if hit:
            start_links.append(f'''<a class="startitem" href="#{hit["key"]}">
              <span class="startnum">{len(start_links)+1}</span>
              <span>{H.escape(hit["title"])}</span><span class="startarrow">›</span></a>''')
    guide = next((a for a in arts if a['fn'] == 'SQ実測学習ガイド.md'), None) or next((a for a in arts if a['fn'] == 'SQ完全ガイド.md'), None)
    guide_key = guide['key'] if guide else ''
    faq_qs = []
    for a in [x for x in arts if x['dir'] == '03-faq']:
        for hid, t in a['toc']:
            if t.startswith('Q.'):
                q = t[2:].strip()
                faq_qs.append(f'<li><a href="#{a["key"]}" data-anchor="{hid}"><span class="qmark">Q</span>{H.escape(q)}</a></li>')
    home = f'''
    <div class="home">
      <div class="hero">
        <p class="heroeyebrow">SQ ヘルプセンター</p>
        <h1>お困りごとを、すぐ解決</h1>
        <div class="herosearch"><input id="hsearch" type="search" placeholder="キーワードで探す（例: 在庫 マイナス）" aria-label="記事を検索"></div>
        <p class="herohint">よく検索されるテーマ:
          <button class="chip" data-q="取り寄せ">取り寄せ販売</button>
          <button class="chip" data-q="在庫">在庫</button>
          <button class="chip" data-q="CSV">CSV</button>
          <button class="chip" data-q="商品">商品登録</button>
        </p>
      </div>
      <a class="guidebanner" href="#{guide_key}">
        <span class="gb-ico">📕</span>
        <span class="gb-txt"><b>はじめての方へ — SQ実測学習ガイド</b><br><span class="gb-sub">実際に押して確認した挙動をもとに、SQの全体像・データ・注意点を先に把握する入口資料</span></span>
        <span class="gb-arrow">›</span>
      </a>
      <a class="graphbanner" href="SQ-データ相関図.html">
        <span class="gb-ico">🕸</span>
        <span class="gb-txt"><b>データ相関図を開く</b><br><span class="gb-sub">どのデータがどのデータにつながるか（依存・自動生成・在庫の流れ）を線で見る</span></span>
        <span class="gb-arrow">›</span>
      </a>
      <h2 class="homesec">カテゴリから探す</h2>
      <div class="cards">{''.join(cards)}</div>
      <div class="homecols">
        <section>
          <h2 class="homesec">はじめての方は、この順に</h2>
          <div class="startlist">{''.join(start_links)}</div>
        </section>
        <section>
          <h2 class="homesec">よくある質問</h2>
          <ul class="faqlist">{''.join(faq_qs[:10])}</ul>
        </section>
      </div>
    </div>'''

    # ---- articles ----
    art_html = []
    for a in arts:
        toc_html = ''
        if len(a['toc']) >= 2:
            toc_html = '<nav class="toc" aria-label="このページの内容"><p class="tochead">このページの内容</p><ol>' + ''.join(
                f'<li><a href="#{hid}">{H.escape(t)}</a></li>' for hid, t in a['toc']) + '</ol></nav>'
        group_items = [x for x in arts if x['dir'] == a['dir']]
        gi = group_items.index(a)
        prev_a = group_items[gi - 1] if gi > 0 else None
        next_a = group_items[gi + 1] if gi < len(group_items) - 1 else None
        pn = '<nav class="prevnext">'
        if prev_a:
            pn += f'<a class="pn" href="#{prev_a["key"]}"><span class="pnlabel">‹ 前の記事</span><span class="pntitle">{H.escape(prev_a["title"])}</span></a>'
        else:
            pn += '<span></span>'
        if next_a:
            pn += f'<a class="pn pnr" href="#{next_a["key"]}"><span class="pnlabel">次の記事 ›</span><span class="pntitle">{H.escape(next_a["title"])}</span></a>'
        else:
            pn += '<span></span>'
        pn += '</nav>'
        badge = '<span class="badge partial">一部確認中の項目があります</span>' if '要確認' in a['status'] else ''
        art_html.append(f'''<article id="art-{a['key']}" class="article" data-key="{a['key']}">
          <div class="crumb"><a href="#home">ホーム</a><span class="sep">›</span><span>{a['gicon']} {a['glabel']}</span></div>
          <h1>{H.escape(a['title'])}</h1>
          {badge}
          {toc_html}
          <div class="artbody">{a['html']}</div>
          {pn}
        </article>''')

    search_index = json.dumps(
        [{'k': a['key'], 't': a['title'], 'g': a['glabel'], 'x': a['plain']} for a in arts],
        ensure_ascii=False)

    page = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQ ヘルプセンター</title>
<style>
:root {{
  --primary:#2864f0; --primary-hover:#285ac8; --primary-dark:#1e46aa; --primary-pale:#ebf3ff; --primary-pale2:#dce8ff;
  --ink:#323232; --body:#595959; --muted:#8c8989;
  --danger:#dc1e32; --warning:#ffb91e; --warnbg:#fff7e0; --success:#00963c;
  --bg:#f7f5f5; --bg2:#f0eded; --line:#e9e7e7; --white:#fff;
  --shadow-card:0 0 1rem rgba(0,0,0,.06), 0 .125rem .25rem rgba(0,0,0,.1);
  --shadow-pop:0 0 2rem rgba(0,0,0,.1), 0 .375rem .75rem rgba(0,0,0,.2);
  --z-nav:30; --z-results:50; --z-lightbox:90;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; color:var(--body); background:var(--bg); font-size:16px; line-height:1.5;
  font-family:'-apple-system',BlinkMacSystemFont,'Helvetica Neue','ヒラギノ角ゴ ProN','Hiragino Kaku Gothic ProN',Arial,'メイリオ',Meiryo,sans-serif;
  font-feature-settings:"palt"; overflow-wrap:break-word; }}
a {{ color:var(--primary); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
button {{ font-family:inherit; }}

/* ===== header ===== */
header.top {{ position:sticky; top:0; z-index:var(--z-nav); background:var(--white); border-bottom:1px solid var(--line);
  display:flex; align-items:center; gap:20px; padding:12px 24px; }}
.logo {{ font-weight:700; font-size:17px; color:var(--ink); white-space:nowrap; cursor:pointer; display:flex; align-items:center; gap:8px; }}
.logomark {{ display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; border-radius:8px;
  background:var(--primary); color:#fff; font-size:13px; font-weight:700; }}
.searchwrap {{ position:relative; flex:1; max-width:480px; }}
.searchwrap input, .herosearch input {{ width:100%; padding:10px 16px 10px 40px; border:1px solid #ccc; border-radius:8px;
  font-size:15px; background:var(--white); outline:none; font-family:inherit; color:var(--ink); }}
.searchwrap input:focus, .herosearch input:focus {{ border-color:var(--primary); box-shadow:0 0 0 3px var(--primary-pale2); }}
.searchwrap::before, .herosearch::before {{ content:"🔍"; position:absolute; left:13px; top:50%; transform:translateY(-50%); font-size:14px; opacity:.55; }}
#results {{ position:absolute; top:calc(100% + 8px); left:0; right:0; background:var(--white); border:1px solid var(--line);
  border-radius:12px; box-shadow:var(--shadow-pop); max-height:440px; overflow:auto; display:none; z-index:var(--z-results); }}
#results a {{ display:block; padding:12px 16px; border-bottom:1px solid var(--line); color:var(--body); }}
#results a:last-child {{ border-bottom:none; }}
#results a:hover {{ background:var(--primary-pale); text-decoration:none; }}
#results .rt {{ font-weight:700; font-size:15px; color:var(--ink); }}
#results .rt em, #results .rx em {{ color:var(--primary); font-style:normal; }}
#results .rg {{ font-size:12px; color:var(--primary-dark); font-weight:700; margin-top:2px; }}
#results .rx {{ font-size:13px; color:var(--muted); display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}

/* ===== layout ===== */
.layout {{ display:flex; max-width:1240px; margin:0 auto; gap:0; }}
nav.side {{ width:272px; flex:none; padding:20px 12px 80px 20px; position:sticky; top:55px; height:calc(100dvh - 55px);
  overflow-y:auto; }}
.navgroup {{ margin-bottom:8px; background:var(--white); border:1px solid var(--line); border-radius:12px; overflow:hidden; }}
.navgroup summary {{ list-style:none; cursor:pointer; display:flex; align-items:center; gap:8px; padding:12px 14px;
  font-size:14px; font-weight:700; color:var(--ink); user-select:none; }}
.navgroup summary::-webkit-details-marker {{ display:none; }}
.navgroup summary::after {{ content:"›"; margin-left:auto; color:var(--muted); transition:transform .15s ease-out; }}
.navgroup[open] summary::after {{ transform:rotate(90deg); }}
.navgroup summary:hover {{ background:var(--primary-pale); }}
.gicon {{ font-size:15px; }}
.navcount {{ font-size:11px; color:var(--primary-dark); font-weight:700; background:var(--primary-pale); border-radius:99rem; padding:1px 8px; }}
.navgroup ul {{ list-style:none; margin:0; padding:2px 8px 10px; }}
.navgroup li a {{ display:block; padding:7px 10px 7px 14px; font-size:13.5px; color:var(--body); border-radius:8px; line-height:1.45;
  border-left:3px solid transparent; }}
.navgroup li a:hover {{ background:var(--bg); text-decoration:none; color:var(--ink); }}
.navgroup li a.active {{ background:var(--primary-pale); color:var(--primary-dark); font-weight:700; border-left-color:var(--primary); }}
main {{ flex:1; min-width:0; padding:28px 32px 96px; }}

/* ===== home ===== */
.hero {{ background:var(--white); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow-card);
  text-align:center; padding:48px 24px 36px; }}
.heroeyebrow {{ margin:0 0 4px; font-size:13px; font-weight:700; color:var(--primary); letter-spacing:.04em; }}
.hero h1 {{ font-size:28px; font-weight:700; color:var(--ink); margin:0 0 20px; text-wrap:balance; }}
.herosearch {{ position:relative; max-width:560px; margin:0 auto; }}
.herosearch input {{ padding:14px 18px 14px 44px; font-size:16px; }}
.herohint {{ margin:14px 0 0; font-size:13px; color:var(--muted); }}
.chip {{ border:1px solid var(--primary-pale2); background:var(--primary-pale); color:var(--primary-dark); font-size:12.5px;
  border-radius:99rem; padding:4px 12px; margin:0 3px; cursor:pointer; font-weight:700; }}
.chip:hover {{ background:var(--primary-pale2); }}
.homesec {{ font-size:18px; font-weight:700; color:var(--ink); margin:40px 0 14px; display:flex; align-items:center; gap:10px; }}
.homesec::before {{ content:""; width:4px; height:18px; border-radius:2px; background:var(--primary); }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(195px,1fr)); gap:14px; }}
.card {{ display:flex; align-items:center; gap:12px; background:var(--white); border:1px solid var(--line); border-radius:12px;
  padding:18px 18px; color:var(--body); box-shadow:var(--shadow-card); transition:transform .15s ease-out; }}
.card:hover {{ transform:translateY(-2px); text-decoration:none; border-color:var(--primary-pale2); }}
.cardicon {{ display:flex; align-items:center; justify-content:center; width:46px; height:46px; flex:none;
  background:var(--primary-pale); border-radius:12px; font-size:22px; }}
.cardbody {{ display:flex; flex-direction:column; min-width:0; }}
.cardtitle {{ font-weight:700; font-size:16px; color:var(--ink); }}
.carddesc {{ font-size:12.5px; color:var(--muted); }}
.cardcount {{ margin-left:auto; font-size:12.5px; color:var(--primary); font-weight:700; white-space:nowrap; }}
.homecols {{ display:grid; grid-template-columns:1fr 1.15fr; gap:28px; align-items:start; }}
.startlist {{ display:flex; flex-direction:column; gap:10px; }}
.guidebanner {{ display:flex; align-items:center; gap:16px; background:var(--primary); border:1px solid var(--primary);
  border-radius:14px; padding:18px 20px; margin:22px 0 10px; box-shadow:0 .25rem .75rem rgba(40,100,240,.25); }}
.guidebanner:hover {{ background:var(--primary-dark); text-decoration:none; }}
.guidebanner .gb-ico {{ font-size:30px; flex:none; }}
.guidebanner .gb-txt {{ flex:1; font-size:15px; color:#fff; line-height:1.5; }}
.guidebanner .gb-sub {{ font-size:12.5px; color:#dbe6ff; font-weight:400; }}
.guidebanner .gb-arrow {{ font-size:26px; color:#fff; flex:none; }}
.graphbanner {{ display:flex; align-items:center; gap:16px; background:var(--white); border:1px solid var(--line);
  border-radius:14px; padding:16px 20px; margin:4px 0 4px; box-shadow:0 0 1rem rgba(0,0,0,.05), 0 .125rem .25rem rgba(0,0,0,.08); }}
.graphbanner:hover {{ border-color:var(--primary); text-decoration:none; box-shadow:0 .25rem .75rem rgba(40,100,240,.15); }}
.graphbanner .gb-ico {{ font-size:30px; flex:none; }}
.graphbanner .gb-txt {{ flex:1; font-size:15px; color:var(--ink); line-height:1.5; }}
.graphbanner .gb-sub {{ font-size:12.5px; color:var(--muted); font-weight:400; }}
.graphbanner .gb-arrow {{ font-size:26px; color:var(--primary); flex:none; }}
.startitem {{ display:flex; align-items:center; gap:14px; background:var(--white); border:1px solid var(--line);
  border-radius:12px; padding:14px 18px; color:var(--ink); font-weight:700; font-size:15px; box-shadow:var(--shadow-card); }}
.startitem:hover {{ border-color:var(--primary); text-decoration:none; }}
.startnum {{ width:26px; height:26px; flex:none; border-radius:50%; background:var(--primary); color:#fff; font-size:13px;
  display:flex; align-items:center; justify-content:center; }}
.startarrow {{ margin-left:auto; color:var(--primary); }}
.faqlist {{ list-style:none; margin:0; padding:0; background:var(--white); border:1px solid var(--line); border-radius:12px;
  box-shadow:var(--shadow-card); overflow:hidden; }}
.faqlist li + li {{ border-top:1px solid var(--line); }}
.faqlist a {{ display:flex; gap:10px; align-items:baseline; padding:12px 16px; font-size:14px; color:var(--body); line-height:1.55; }}
.faqlist a:hover {{ background:var(--primary-pale); text-decoration:none; color:var(--ink); }}
.qmark {{ flex:none; font-weight:700; color:var(--primary); font-size:13px; }}

/* ===== article ===== */
.article {{ max-width:760px; }}
.crumb {{ font-size:12.5px; color:var(--muted); margin-bottom:14px; }}
.crumb .sep {{ margin:0 7px; }}
.article > h1 {{ font-size:24px; font-weight:700; color:var(--ink); margin:0 0 10px; line-height:1.4; text-wrap:balance; }}
.badge.partial {{ display:inline-block; font-size:12px; border-radius:99rem; padding:3px 12px; font-weight:700;
  background:var(--warnbg); color:#8a6400; border:1px solid #f0dca0; margin-bottom:10px; }}
.toc {{ background:var(--white); border:1px solid var(--line); border-left:4px solid var(--primary); border-radius:8px;
  padding:14px 20px; margin:18px 0 26px; }}
.tochead {{ font-size:12.5px; font-weight:700; color:var(--primary-dark); margin:0 0 6px; }}
.toc ol {{ margin:0; padding-left:20px; columns:2; column-gap:28px; }}
.toc li {{ font-size:13.5px; line-height:2; break-inside:avoid; }}
.toc a {{ color:var(--body); }}
.toc a:hover {{ color:var(--primary); }}
.artbody {{ background:var(--white); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow-card);
  padding:8px 36px 28px; }}
.artbody h2 {{ font-size:19px; font-weight:700; color:var(--ink); margin:40px 0 14px; padding:10px 0 10px 14px;
  border-left:4px solid var(--primary); background:var(--primary-pale); border-radius:0 8px 8px 0; }}
.artbody h3 {{ font-size:16px; font-weight:700; color:var(--primary-dark); margin:30px 0 10px; }}
.artbody h4 {{ font-size:14.5px; font-weight:700; color:var(--ink); margin:22px 0 8px; }}
.artbody p {{ margin:12px 0; font-size:15.5px; line-height:1.9; text-wrap:pretty; }}
.artbody li {{ font-size:15.5px; line-height:1.9; margin:4px 0; }}
.artbody ol, .artbody ul {{ padding-left:26px; }}
.artbody strong {{ color:var(--ink); }}
.artbody code {{ background:var(--bg2); border-radius:4px; padding:2px 6px; font-size:13px; color:var(--ink); }}
.artbody hr {{ border:none; border-top:1px solid var(--line); margin:32px 0; }}
.callout {{ display:flex; gap:12px; margin:18px 0; padding:14px 18px; background:var(--primary-pale);
  border-radius:12px; font-size:14.5px; line-height:1.8; color:var(--ink); }}
.callout.warn {{ background:var(--warnbg); }}
.cicon {{ flex:none; font-size:16px; line-height:1.8; }}
.tablewrap {{ overflow-x:auto; margin:16px 0; border:1px solid var(--line); border-radius:8px; }}
table {{ border-collapse:collapse; width:100%; font-size:14px; background:var(--white); font-variant-numeric:tabular-nums; }}
th {{ background:var(--bg2); text-align:left; padding:10px 14px; font-weight:700; color:var(--ink); white-space:nowrap;
  border-bottom:2px solid var(--line); }}
td {{ padding:10px 14px; border-bottom:1px solid var(--line); vertical-align:top; line-height:1.7; }}
tbody tr:last-child td {{ border-bottom:none; }}
tbody tr:nth-child(even) {{ background:#fbfafa; }}
figure {{ margin:18px 0; }}
.artbody img {{ max-width:100%; border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow-card);
  display:block; cursor:zoom-in; }}
figcaption {{ font-size:12.5px; color:var(--muted); margin-top:6px; }}
pre.mermaid {{ background:var(--white); text-align:center; margin:18px 0; }}
#lightbox {{ position:fixed; inset:0; background:rgba(30,30,30,.85); display:none; align-items:center; justify-content:center;
  z-index:var(--z-lightbox); cursor:zoom-out; padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }}
#lightbox img {{ max-width:94vw; max-height:94dvh; border-radius:8px; }}
.prevnext {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:24px; }}
.pn {{ display:flex; flex-direction:column; gap:2px; background:var(--white); border:1px solid var(--line); border-radius:12px;
  padding:12px 18px; box-shadow:var(--shadow-card); }}
.pn:hover {{ border-color:var(--primary); text-decoration:none; }}
.pnr {{ text-align:right; }}
.pnlabel {{ font-size:11.5px; color:var(--muted); font-weight:700; }}
.pntitle {{ font-size:14px; color:var(--ink); font-weight:700; line-height:1.5; }}

@media (max-width: 920px) {{
  nav.side {{ display:none; }}
  main {{ padding:16px 16px 80px; }}
  .artbody {{ padding:4px 18px 20px; }}
  .homecols {{ grid-template-columns:1fr; }}
  .toc ol {{ columns:1; }}
  .hero h1 {{ font-size:22px; }}
  .prevnext {{ grid-template-columns:1fr; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior:auto; }}
  .card, .navgroup summary::after {{ transition:none; }}
}}
</style></head>
<body>
<header class="top">
  <div class="logo" onclick="location.hash='home'"><span class="logomark">SQ</span>ヘルプセンター</div>
  <div class="searchwrap"><input id="search" type="search" placeholder="キーワードで探す" aria-label="記事を検索"><div id="results"></div></div>
</header>
<div class="layout">
  <nav class="side" aria-label="記事一覧">{nav_html}</nav>
  <main>
    <section id="view-home">{home}</section>
    <section id="view-art" style="display:none">{''.join(art_html)}</section>
  </main>
</div>
<script>const INDEX = {search_index};</script>
<script>
const arts = document.querySelectorAll('.article');
const navLinks = document.querySelectorAll('nav.side a[data-key]');
let mermaidReady = false, renderedKeys = new Set();
function show(key, anchor) {{
  const home = document.getElementById('view-home'), av = document.getElementById('view-art');
  if (!key || key === 'home') {{ home.style.display=''; av.style.display='none'; window.scrollTo(0,0); setActive(null); return; }}
  home.style.display='none'; av.style.display='';
  let found = false;
  arts.forEach(a => {{ const on = a.dataset.key === key; a.style.display = on ? '' : 'none'; if (on) found = true; }});
  if (!found) {{ home.style.display=''; av.style.display='none'; return; }}
  setActive(key);
  if (mermaidReady && !renderedKeys.has(key)) {{
    renderedKeys.add(key);
    try {{ window.mermaid.run({{ nodes: document.querySelectorAll('#art-'+key+' pre.mermaid') }}); }} catch(e) {{}}
  }}
  if (anchor) {{ const el = document.getElementById(anchor); if (el) el.scrollIntoView(); }}
  else window.scrollTo(0,0);
}}
function setActive(key) {{
  navLinks.forEach(l => l.classList.toggle('active', l.dataset.key === key));
  const act = document.querySelector('nav.side a.active');
  if (act) {{
    const g = act.closest('details');
    if (g) g.open = true;
    act.scrollIntoView({{ block:'nearest' }});
  }}
}}
function route() {{
  const h = decodeURIComponent(location.hash.slice(1)) || 'home';
  const m = h.match(/^(a-.*?)(-h\\d+)?$/);
  if (h === 'home' || !m) {{ show('home'); return; }}
  show(m[1], m[2] ? h : null);
}}
window.addEventListener('hashchange', route);
document.querySelectorAll('[data-anchor]').forEach(a => a.addEventListener('click', e => {{
  e.preventDefault(); location.hash = a.dataset.anchor;
}}));
document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', () => {{
  const top = document.getElementById('search');
  top.value = c.dataset.q; top.dispatchEvent(new Event('input')); top.focus();
  window.scrollTo(0,0);
}}));
function attachSearch(inputId) {{
  const inp = document.getElementById(inputId);
  if (!inp) return;
  const box = document.getElementById('results');
  inp.addEventListener('input', () => {{
    const q = inp.value.trim();
    if (inputId === 'hsearch') {{ const top = document.getElementById('search'); top.value = q; top.dispatchEvent(new Event('input')); top.focus(); return; }}
    if (!q) {{ box.style.display='none'; return; }}
    const terms = q.split(/\\s+/).filter(Boolean);
    const hits = [];
    for (const it of INDEX) {{
      let score = 0, ok = true;
      for (const t of terms) {{
        const inT = it.t.includes(t), inX = it.x.includes(t);
        if (!inT && !inX) {{ ok = false; break; }}
        score += inT ? 10 : 1;
      }}
      if (ok) hits.push([score, it]);
    }}
    hits.sort((a,b) => b[0]-a[0]);
    if (!hits.length) {{ box.innerHTML = '<a><span class="rx">見つかりませんでした。別の言葉でお試しください</span></a>'; box.style.display='block'; return; }}
    const mark = (s) => {{ let r = s; for (const t of terms) r = r.split(t).join('<em>'+t+'</em>'); return r; }};
    box.innerHTML = hits.slice(0, 12).map(([_, it]) => {{
      const pos = it.x.indexOf(terms[0]);
      const snip = pos >= 0 ? it.x.slice(Math.max(0, pos-30), pos+90) : it.x.slice(0, 100);
      return `<a href="#${{it.k}}"><div class="rt">${{mark(it.t)}}</div><div class="rg">${{it.g}}</div><div class="rx">…${{mark(snip)}}…</div></a>`;
    }}).join('');
    box.style.display = 'block';
  }});
  document.addEventListener('click', e => {{ if (!e.target.closest('.searchwrap')) box.style.display='none'; }});
  box.addEventListener('click', () => {{ box.style.display='none'; inp.value=''; }});
}}
attachSearch('search'); attachSearch('hsearch');
const lb = document.createElement('div'); lb.id='lightbox'; lb.innerHTML='<img alt="拡大表示">'; document.body.appendChild(lb);
document.addEventListener('click', e => {{
  if (e.target.matches('.artbody img')) {{ lb.querySelector('img').src = e.target.src; lb.style.display='flex'; }}
  else if (e.target.closest('#lightbox')) lb.style.display='none';
}});
route();
</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({{ startOnLoad: false, theme: 'neutral' }});
window.mermaid = mermaid; window.dispatchEvent(new Event('mermaid-ready'));
</script>
<script>
window.addEventListener('mermaid-ready', () => {{
  mermaidReady = true;
  const h = decodeURIComponent(location.hash.slice(1));
  const m = h.match(/^(a-.*?)(-h\\d+)?$/);
  if (m) {{ renderedKeys.add(m[1]); try {{ window.mermaid.run({{ nodes: document.querySelectorAll('#art-'+m[1]+' pre.mermaid') }}); }} catch(e) {{}} }}
}});
</script>
</body></html>'''
    page = '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
    out = os.path.join(BASE, 'SQ-FAQ.html')
    open(out, 'w', encoding='utf-8').write(page)
    print(f'OK: {out} articles={len(arts)} bytes={len(page.encode())}')


if __name__ == '__main__':
    build()
