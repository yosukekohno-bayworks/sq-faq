#!/usr/bin/env python3
"""SQ完全ガイドを、単体で開ける1ファイルHTMLに変換する（目次サイドバー付き・自己完結）。
レンダリングは build_help.py の md_to_html を再利用。出力: SQ完全ガイド.html"""
import os, re, html as H
import build_help as bh

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '00-getting-started', 'SQ完全ガイド.md')


def build():
    meta, body = bh.parse_fm(open(SRC, encoding='utf-8').read())
    html, toc = bh.md_to_html(body, 'g', {})  # .mdリンク・画像なし → linkmap不要

    # 目次（## 見出し）。部見出し（第N部）は階層の親として太字、章はインデント
    toc_items = []
    for hid, text in toc:
        cls = 'tpart' if text.startswith('第') and '部' in text[:4] else 'tchap'
        toc_items.append(f'<a class="{cls}" href="#{hid}">{H.escape(text)}</a>')
    toc_html = ''.join(toc_items)

    title = meta.get('title', 'SQ完全ガイド')
    page = TEMPLATE.replace('__TITLE__', H.escape(title)) \
        .replace('__TOC__', toc_html).replace('__BODY__', html)
    out = os.path.join(BASE, 'SQ完全ガイド.html')
    open(out, 'w', encoding='utf-8').write(page)
    print(f'OK: {out} sections={len(toc)} bytes={len(page.encode())}')


TEMPLATE = r'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{ --primary:#2864f0; --primary-dark:#1e46aa; --primary-pale:#ebf3ff; --ink:#323232; --body:#42454d;
  --muted:#8c8989; --line:#e9e7e7; --bg:#f7f5f5; --white:#fff; --warnbg:#fff7e0; --warnline:#f0c14b; }
*{ box-sizing:border-box; }
html{ scroll-behavior:smooth; }
body{ margin:0; font-family:'-apple-system',BlinkMacSystemFont,'Helvetica Neue','ヒラギノ角ゴ ProN','Hiragino Kaku Gothic ProN',Arial,'メイリオ',Meiryo,sans-serif;
  color:var(--ink); background:var(--bg); line-height:1.85; font-feature-settings:"palt"; font-size:15px; -webkit-text-size-adjust:100%; }
a{ color:var(--primary); text-decoration:none; } a:hover{ text-decoration:underline; }
header{ position:sticky; top:0; z-index:30; background:var(--white); border-bottom:1px solid var(--line);
  padding:12px 22px; display:flex; align-items:center; gap:14px; }
header .logo{ font-weight:700; font-size:15px; } header .logo span{ color:var(--primary); }
header .back{ font-size:12.5px; margin-left:auto; }
.wrap{ display:flex; max-width:1180px; margin:0 auto; align-items:flex-start; }
nav.toc{ position:sticky; top:53px; width:300px; flex:none; max-height:calc(100vh - 53px); overflow-y:auto;
  padding:22px 12px 60px 18px; }
nav.toc .tlabel{ font-size:11px; color:var(--muted); font-weight:700; letter-spacing:.06em; margin:0 0 8px 6px; }
nav.toc a{ display:block; font-size:12.8px; color:var(--body); padding:4px 8px; border-radius:7px; line-height:1.5; }
nav.toc a:hover{ background:var(--primary-pale); text-decoration:none; }
nav.toc a.tpart{ font-weight:700; color:var(--ink); margin-top:10px; }
nav.toc a.tchap{ padding-left:20px; color:var(--body); }
nav.toc a.active{ background:var(--primary-pale); color:var(--primary-dark); font-weight:600; }
main{ flex:1; min-width:0; background:var(--white); border-left:1px solid var(--line); border-right:1px solid var(--line);
  padding:34px 48px 90px; }
main h1{ font-size:27px; line-height:1.45; margin:0 0 6px; letter-spacing:.01em; }
main h2{ font-size:20px; margin:46px 0 14px; padding-bottom:8px; border-bottom:2px solid var(--primary-pale); scroll-margin-top:66px; }
main h2:first-of-type{ margin-top:24px; }
main h3{ font-size:16.5px; margin:30px 0 10px; color:var(--primary-dark); scroll-margin-top:66px; }
main h4{ font-size:15px; margin:20px 0 8px; }
main p{ margin:11px 0; }
main ul,main ol{ margin:11px 0; padding-left:1.5em; } main li{ margin:5px 0; }
main strong{ color:var(--primary-dark); font-weight:700; }
main code{ background:#f0eef0; padding:1px 6px; border-radius:5px; font-size:.9em;
  font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace; color:#b5316b; }
main pre{ background:#2b2b33; color:#eaeaf0; padding:14px 16px; border-radius:10px; overflow-x:auto; font-size:13px; line-height:1.6; }
main pre code{ background:none; color:inherit; padding:0; }
.tablewrap{ overflow-x:auto; margin:14px 0; }
main table{ border-collapse:collapse; width:100%; font-size:13.5px; }
main th{ background:var(--primary-pale); text-align:left; padding:9px 12px; border:1px solid #d7e2fb; white-space:nowrap; }
main td{ padding:8px 12px; border:1px solid var(--line); vertical-align:top; line-height:1.7; }
main tbody tr:nth-child(even){ background:#fcfbfa; }
main hr{ border:none; border-top:1px solid var(--line); margin:34px 0; }
.callout{ display:flex; gap:11px; background:var(--primary-pale); border:1px solid #d7e2fb; border-radius:10px; padding:13px 15px; margin:15px 0; }
.callout.warn{ background:var(--warnbg); border-color:var(--warnline); }
.callout .cicon{ flex:none; font-size:17px; line-height:1.6; }
.callout > div{ font-size:13.7px; }
.backtop{ position:fixed; right:22px; bottom:22px; background:var(--primary); color:#fff; width:44px; height:44px;
  border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 .25rem .75rem rgba(40,100,240,.35); z-index:20; }
.backtop:hover{ background:var(--primary-dark); text-decoration:none; }
@media(max-width:900px){ nav.toc{ display:none; } main{ border:none; padding:24px 18px 80px; } }
</style></head>
<body>
<header>
  <div class="logo">SQ <span>完全ガイド</span></div>
  <a class="back" href="SQ-FAQ.html">📖 ヘルプセンターへ ↗</a>
</header>
<div class="wrap">
  <nav class="toc"><p class="tlabel">もくじ</p>__TOC__</nav>
  <main>
    <h1>__TITLE__</h1>
    __BODY__
  </main>
</div>
<a class="backtop" href="#" aria-label="先頭へ戻る">↑</a>
<script>
// 目次のスクロール追従ハイライト
const links=[...document.querySelectorAll('nav.toc a')];
const map=new Map(links.map(a=>[a.getAttribute('href').slice(1),a]));
const heads=[...document.querySelectorAll('main h2, main h3')];
const obs=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){ const a=map.get(e.target.id); if(a){ links.forEach(x=>x.classList.remove('active')); a.classList.add('active'); } } });
},{ rootMargin:'-60px 0px -70% 0px' });
heads.forEach(h=>obs.observe(h));
</script>
</body></html>'''


if __name__ == '__main__':
    build()
