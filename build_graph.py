#!/usr/bin/env python3
"""SQ データ相関図: データ事典①②で確認した関係を、インタラクティブなネットワーク図(vis-network)に描く。
- ノード: カテゴリ別に色分け（マスタ/伝票/ルール/システム生成/連携設定）
- エッジ: 関係の種類で描き分け（必須・選択肢・自動生成・在庫・同期・参照）
- 実線 = 実機で確認できた構造・社内在庫フロー / 点線 = チャネル接続が前提で未検証
出力: SQ-データ相関図.html（SQ-FAQ.html の事典①②へリンク）"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

# 事典①②の記事アンカー（build_help.py のキー生成則に一致）
DOC1 = 'a-00-getting-started----------------'           # データ事典①
DOC2 = 'a-00-getting-started--------------------------'  # データ事典②

CATS = {
    'master':      ('マスタ',       '#2864f0'),
    'voucher':     ('伝票',         '#d97706'),
    'rule':        ('ルール',       '#0891b2'),
    'system':      ('システム生成', '#6b7280'),
    'integration': ('連携設定',     '#16a34a'),
}

# id, ラベル, カテゴリ, 事典(1/2)
NODES = [
    # マスタ
    ('tenant', 'テナント', 'master', 1),
    ('loc', 'ロケーション', 'master', 1),
    ('locgroup', 'ロケーショングループ', 'master', 1),
    ('brand', 'ブランド', 'master', 1),
    ('supplier', '取引先', 'master', 1),
    ('payment', '決済方法', 'master', 1),
    ('staff', '販売員', 'master', 1),
    ('member', '管理メンバー', 'master', 1),
    ('permgroup', '権限グループ', 'master', 1),
    ('metafield', 'メタフィールド定義', 'master', 1),
    ('translation', '翻訳ルール', 'master', 1),
    ('product', '商品', 'master', 2),
    ('variant', 'バリエーション(SKU)', 'master', 2),
    ('catalog', 'カタログ', 'master', 2),
    ('company', '会社(法人顧客)', 'master', 2),
    ('companyloc', '会社ロケーション', 'master', 2),
    ('rank', '会員ランク(段階)', 'master', 2),
    # 伝票
    ('adjust', '調整伝票', 'voucher', 2),
    ('reserve', '取置伝票', 'voucher', 2),
    ('move', '移動伝票', 'voucher', 2),
    ('allocreq', '在庫依頼', 'voucher', 2),
    ('purchase', '発注伝票', 'voucher', 2),
    ('order', '注文', 'voucher', 2),
    ('draft', '下書き注文', 'voucher', 2),
    ('ret', '返品', 'voucher', 2),
    # ルール
    ('pricerule', '販売価格ルール', 'rule', 1),
    ('backorder', '予約販売ルール', 'rule', 1),
    ('salelimit', '販売上限ルール', 'rule', 1),
    ('threshold', '販売閾値ルール', 'rule', 1),
    ('autoadd', '自動追加ルール', 'rule', 2),
    ('discount', 'ディスカウント', 'rule', 2),
    ('pointrule', '注文ポイント付与ルール', 'rule', 2),
    ('pointcamp', 'ポイントキャンペーン', 'rule', 2),
    ('rankrule', '会員ランク算出ルール', 'rule', 2),
    # システム生成
    ('inventory', '在庫区分', 'system', 2),
    ('secured', '確保済み', 'system', 2),
    ('outbound', '出荷指示', 'system', 2),
    ('inbound', '入荷指示', 'system', 2),
    ('outresult', '出荷実績', 'system', 2),
    ('inresult', '入荷実績', 'system', 2),
    ('screq', '在庫リクエスト(EC自動)', 'system', 2),
    ('customer', '顧客(購入顧客)', 'system', 2),
    ('sales', '売上実績', 'system', 2),
    ('adjhist', '調整履歴', 'system', 2),
    ('pickup', '店舗受取バリエーション', 'system', 2),
    # 連携設定
    ('shopify', 'Shopify連携', 'integration', 1),
    ('omnibus', 'OmnibusCore連携', 'integration', 1),
    ('smaregi', 'スマレジ連携', 'integration', 1),
    ('retail', 'リテールポータル連携', 'integration', 1),
    ('logizard', 'ロジザード連携', 'integration', 1),
    ('recustomer', 'Recustomer連携', 'integration', 1),
    ('app', 'アプリ / API', 'integration', 1),
    ('webhook', 'Webhook', 'integration', 1),
]

# from, to, ラベル, kind(dep/spine/sync), verified
EDGES = [
    # ── マスタ依存（フォームの必須・選択肢・参照） ──
    ('tenant', 'purchase', '必須', 'dep', True),
    ('tenant', 'discount', '必須', 'dep', True),
    ('tenant', 'shopify', '必須', 'dep', True),
    ('tenant', 'omnibus', '必須', 'dep', True),
    ('tenant', 'smaregi', '必須', 'dep', True),
    ('tenant', 'retail', '必須', 'dep', True),
    ('tenant', 'member', 'アクセス範囲', 'dep', True),
    ('tenant', 'pointrule', '参照', 'dep', True),
    ('tenant', 'rankrule', '参照', 'dep', True),
    ('loc', 'inventory', '在庫はSKU×ロケ', 'dep', True),
    ('loc', 'locgroup', '所属', 'dep', True),
    ('loc', 'adjust', '選択肢', 'dep', True),
    ('loc', 'move', '配送元/先', 'dep', True),
    ('loc', 'reserve', '選択肢', 'dep', True),
    ('loc', 'allocreq', '移動先/依頼先', 'dep', True),
    ('loc', 'staff', '担当', 'dep', True),
    ('loc', 'retail', '店舗/在庫ロケ', 'dep', True),
    ('locgroup', 'shopify', '必須', 'dep', True),
    ('locgroup', 'omnibus', '在庫設定', 'dep', True),
    ('brand', 'product', '選択肢', 'dep', True),
    ('brand', 'autoadd', 'コード一致', 'dep', True),
    ('brand', 'threshold', 'コード一致(自動追加)', 'dep', True),
    ('supplier', 'purchase', '必須選択肢', 'dep', True),
    ('payment', 'order', '決済手段', 'dep', True),
    ('staff', 'retail', '販売実績', 'dep', True),
    ('member', 'permgroup', '権限割当', 'dep', True),
    ('permgroup', 'app', '同一権限体系', 'dep', True),
    ('metafield', 'product', '入力欄追加', 'dep', True),
    ('metafield', 'customer', '絞り込み', 'dep', True),
    ('metafield', 'translation', '翻訳対象', 'dep', True),
    ('translation', 'product', '翻訳生成', 'dep', True),
    ('product', 'variant', '1:N', 'dep', True),
    ('product', 'catalog', '追加', 'dep', True),
    ('product', 'autoadd', '製造元/ブランド一致', 'dep', True),
    ('variant', 'inventory', 'SKU単位', 'dep', True),
    ('variant', 'pricerule', 'SKU紐づけ', 'dep', True),
    ('variant', 'backorder', 'SKU+販売数', 'dep', True),
    ('variant', 'salelimit', 'SKU+上限', 'dep', True),
    ('variant', 'threshold', 'SKU+閾値', 'dep', True),
    ('variant', 'pickup', '対象SKU', 'dep', True),
    ('variant', 'purchase', '明細', 'dep', True),
    ('variant', 'reserve', '明細', 'dep', True),
    ('variant', 'adjust', '明細', 'dep', True),
    ('catalog', 'shopify', '必須(出す商品)', 'dep', True),
    ('catalog', 'omnibus', '出す商品', 'dep', True),
    ('catalog', 'smaregi', '出す商品', 'dep', True),
    ('catalog', 'retail', '扱う商品', 'dep', True),
    # ── ルールの適用先 ──
    ('pricerule', 'shopify', '販売価格', 'dep', True),
    ('pricerule', 'omnibus', 'サイト価格', 'dep', True),
    ('backorder', 'omnibus', '在庫予約ルール', 'dep', True),
    ('shopify', 'salelimit', 'チャネル必須', 'dep', True),
    ('threshold', 'retail', '販売可否', 'dep', True),
    ('rankrule', 'pointrule', '紐づけ', 'dep', True),
    ('rankrule', 'pointcamp', '種別:会員ランク', 'dep', True),
    ('rankrule', 'rank', '段階を定義', 'dep', True),
    ('pointrule', 'pointcamp', '対象ルール', 'dep', True),
    ('discount', 'customer', '対象顧客', 'dep', True),
    ('discount', 'variant', '対象商品', 'dep', True),
    ('discount', 'shopify', '連携する', 'dep', False),
    # ── CRM ──
    ('company', 'companyloc', '納品先', 'dep', True),
    ('company', 'order', '法人顧客', 'dep', True),
    ('companyloc', 'omnibus', '連携サイト', 'dep', True),
    ('customer', 'order', '顧客', 'dep', True),
    # ── 社内在庫フロー（実機検証済みの背骨） ──
    ('allocreq', 'secured', '引当て', 'spine', True),
    ('secured', 'move', '移動伝票を作成', 'spine', True),
    ('move', 'outbound', '自動生成', 'spine', True),
    ('move', 'inbound', '自動生成', 'spine', True),
    ('move', 'inventory', '販売可能→取置中', 'spine', True),
    ('outbound', 'outresult', '実績登録', 'spine', True),
    ('outresult', 'inventory', '手持ち −', 'spine', True),
    ('inbound', 'inresult', '実績登録', 'spine', True),
    ('inresult', 'inventory', '手持ち +', 'spine', True),
    ('inresult', 'move', '完了', 'spine', True),
    ('reserve', 'inventory', '取置中へ', 'spine', True),
    ('adjust', 'inventory', '増減を反映', 'spine', True),
    ('inventory', 'adjhist', '変更を記録', 'dep', True),
    ('purchase', 'supplier', '発注先', 'dep', True),
    # ── EC注文起点（チャネル接続が前提＝未検証） ──
    ('shopify', 'order', '注文流入', 'sync', False),
    ('shopify', 'customer', '顧客流入', 'sync', False),
    ('shopify', 'inventory', '在庫同期', 'sync', False),
    ('shopify', 'product', '商品同期', 'sync', False),
    ('smaregi', 'inventory', '在庫同期(方向)', 'sync', False),
    ('smaregi', 'order', '注文流入', 'sync', False),
    ('omnibus', 'draft', '下書き注文流入', 'sync', False),
    ('omnibus', 'outbound', '初期ステータス設定', 'sync', False),
    ('logizard', 'inbound', 'WMS入荷', 'sync', False),
    ('logizard', 'outbound', 'WMS出荷', 'sync', False),
    ('recustomer', 'ret', '返品・交換を委譲', 'sync', False),
    ('app', 'webhook', '配下に作成', 'dep', True),
    ('webhook', 'order', 'イベント通知', 'sync', True),
    ('webhook', 'inventory', 'イベント通知', 'sync', True),
    ('order', 'inventory', '引当(引当済み)', 'spine', False),
    ('order', 'outbound', '出荷', 'spine', False),
    ('order', 'ret', '返品', 'dep', False),
    ('order', 'sales', '売上実績(自動生成)', 'spine', False),
    ('order', 'screq', '在庫不足→在庫リクエスト', 'spine', False),
    ('screq', 'retail', '店舗へ通知', 'sync', False),
    ('screq', 'move', '取り寄せ→移動伝票', 'spine', False),
    ('customer', 'draft', '作成可に(解放条件)', 'dep', False),
]


def build():
    ids = {n[0] for n in NODES}
    for e in EDGES:
        assert e[0] in ids, f'未定義ノード: {e[0]}'
        assert e[1] in ids, f'未定義ノード: {e[1]}'

    nodes = [{'id': i, 'label': lbl, 'cat': cat, 'doc': doc} for (i, lbl, cat, doc) in NODES]
    edges = [{'from': f, 'to': t, 'label': lbl, 'kind': k, 'verified': v}
             for (f, t, lbl, k, v) in EDGES]

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    cats_json = json.dumps({k: {'name': v[0], 'color': v[1]} for k, v in CATS.items()}, ensure_ascii=False)

    html = TEMPLATE.replace('__NODES__', nodes_json).replace('__EDGES__', edges_json)\
        .replace('__CATS__', cats_json).replace('__DOC1__', DOC1).replace('__DOC2__', DOC2)
    out = os.path.join(BASE, 'SQ-データ相関図.html')
    with open(out, 'w', encoding='utf-8') as fp:
        fp.write(html)
    print(f'OK: {out} nodes={len(nodes)} edges={len(edges)} bytes={len(html.encode())}')


TEMPLATE = r'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQ データ相関図</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
:root{ --main:#2864f0; --ink:#323232; --grey:#8c8989; --line:#e9e7e7; --bg:#f7f5f5; --white:#fff; --pale:#ebf3ff; }
*{ box-sizing:border-box; }
html,body{ margin:0; height:100%; font-family:'-apple-system',BlinkMacSystemFont,'Helvetica Neue','ヒラギノ角ゴ ProN','Hiragino Kaku Gothic ProN',Arial,'メイリオ',Meiryo,sans-serif; color:var(--ink); background:var(--bg); }
header{ position:fixed; top:0; left:0; right:0; height:54px; z-index:30; background:var(--white); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:14px; padding:0 16px; flex-wrap:wrap; }
header .logo{ font-weight:700; font-size:15px; white-space:nowrap; }
header .logo span{ color:var(--main); }
header .sub{ font-size:11.5px; color:var(--grey); }
.searchwrap{ position:relative; flex:1; min-width:180px; max-width:380px; }
#q{ width:100%; padding:8px 12px 8px 32px; border:1px solid #ccc; border-radius:8px; font-size:13.5px; font-family:inherit; color:var(--ink); outline:none; }
#q:focus{ border-color:var(--main); box-shadow:0 0 0 3px #dce8ff; }
.searchwrap::before{ content:"🔍"; position:absolute; left:10px; top:50%; transform:translateY(-50%); font-size:12px; opacity:.6; }
.helplink{ font-size:12.5px; white-space:nowrap; }
a{ color:var(--main); text-decoration:none; } a:hover{ text-decoration:underline; }
#net{ position:fixed; top:54px; left:0; right:300px; bottom:0; background:
  radial-gradient(circle at 1px 1px, #e4e1dd 1px, transparent 0) 0 0/22px 22px, var(--bg); }
aside{ position:fixed; top:54px; right:0; width:300px; bottom:0; background:var(--white); border-left:1px solid var(--line); overflow-y:auto; padding:16px; z-index:20; }
aside h2{ font-size:14px; margin:0 0 4px; }
aside .cat-badge{ display:inline-block; font-size:11px; color:#fff; padding:2px 9px; border-radius:10px; margin-bottom:10px; }
.legend{ margin-bottom:14px; }
.legend h3{ font-size:11.5px; color:var(--grey); margin:14px 0 6px; font-weight:600; letter-spacing:.04em; }
.legend label{ display:flex; align-items:center; gap:7px; font-size:12.5px; padding:3px 0; cursor:pointer; }
.legend .dot{ width:13px; height:13px; border-radius:50%; flex:none; }
.legend .ln{ width:22px; height:0; flex:none; border-top-width:3px; border-top-style:solid; }
.hint{ font-size:11.5px; color:var(--grey); line-height:1.6; margin:6px 0 0; }
.panel-empty{ color:var(--grey); font-size:12.5px; line-height:1.7; }
.rel-group{ margin-top:12px; }
.rel-group h3{ font-size:11.5px; color:var(--grey); margin:0 0 5px; font-weight:600; }
.rel-item{ font-size:12.5px; line-height:1.55; padding:4px 0; border-bottom:1px dashed var(--line); }
.rel-item .arrow{ color:var(--main); font-weight:700; }
.rel-item .rel-label{ color:var(--grey); font-size:11px; }
.rel-item.unverified .rel-label::after{ content:" ⚠未検証"; color:#c2792e; }
.docbtn{ display:inline-block; margin-top:14px; font-size:12.5px; padding:7px 12px; background:var(--pale); border-radius:8px; }
.controls{ display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
.btn{ font-size:12px; border:1px solid var(--line); background:var(--white); border-radius:8px; padding:6px 11px; cursor:pointer; font-family:inherit; color:var(--ink); }
.btn:hover{ background:var(--pale); }
@media(max-width:760px){ #net{ right:0; bottom:46%; } aside{ top:auto; width:auto; left:0; height:46%; border-left:none; border-top:1px solid var(--line);} }
</style></head>
<body>
<header>
  <div><div class="logo">SQ <span>データ相関図</span></div><div class="sub">データ同士のつながり（依存・生成・在庫・同期）</div></div>
  <div class="searchwrap"><input id="q" type="search" placeholder="データ名で探す（例: 移動伝票 / 在庫）"></div>
  <div class="controls">
    <button class="btn" id="reset">全体表示</button>
    <button class="btn" id="spineBtn">在庫フローだけ</button>
  </div>
  <a class="helplink" href="SQ-FAQ.html" target="_blank">📖 ヘルプセンター ↗</a>
</header>
<div id="net"></div>
<aside id="side">
  <div class="legend">
    <h3>カテゴリ（クリックで表示切替）</h3>
    <div id="catfilter"></div>
    <h3>線の種類</h3>
    <label><span class="ln" style="border-color:#2864f0"></span> 社内フロー・在庫の流れ（確認済み）</label>
    <label><span class="ln" style="border-color:#b8b4ae"></span> 依存・参照（必須/選択肢/紐づけ）</label>
    <label><span class="ln" style="border-color:#8c8989;border-top-style:dashed"></span> 同期・未検証（チャネル接続が前提）</label>
    <p class="hint">点線は、Shopify等への接続後でないと実機確認できていない関係です（チャネル未接続のため）。</p>
  </div>
  <div id="detail"><p class="panel-empty">ノード（データ）をクリックすると、そのデータが<b>何につながっているか</b>を一覧表示します。線をたどると、設定が後続の機能にどう効くかが見えます。</p></div>
</aside>
<script>
const NODES = __NODES__;
const EDGES = __EDGES__;
const CATS = __CATS__;
const DOC = { 1: '__DOC1__', 2: '__DOC2__' };

// 次数でサイズ調整
const deg = {};
EDGES.forEach(e => { deg[e.from]=(deg[e.from]||0)+1; deg[e.to]=(deg[e.to]||0)+1; });

const nodeColor = id => CATS[NODES.find(n=>n.id===id).cat].color;

const visNodes = new vis.DataSet(NODES.map(n => {
  const c = CATS[n.cat].color;
  const d = deg[n.id]||1;
  return { id:n.id, label:n.label, cat:n.cat, doc:n.doc,
    shape:'dot', size: 9 + Math.min(d,14)*1.7,
    color:{ background:c, border:c, highlight:{background:c,border:'#1a1a1a'} },
    font:{ size:13, color:'#2a2a2a', face:'-apple-system, Hiragino Kaku Gothic ProN, Meiryo, sans-serif', strokeWidth:4, strokeColor:'#f7f5f5' } };
}));

function edgeStyle(e){
  if(e.kind==='spine'){
    return { color:{color: e.verified?'#2864f0':'#9bb6f0', highlight:'#1e46aa'}, width: e.verified?2.4:1.6,
      dashes: !e.verified, arrows:{to:{enabled:true,scaleFactor:0.6}} };
  }
  if(e.kind==='sync'){
    return { color:{color:'#a9a6a1', highlight:'#6b7280'}, width:1.3, dashes:[4,4], arrows:{to:{enabled:true,scaleFactor:0.5}} };
  }
  // dep
  return { color:{color: e.verified?'#c9c5bf':'#d8c39a', highlight:'#8c8989'}, width:1, dashes:!e.verified, arrows:{to:{enabled:true,scaleFactor:0.45}} };
}
const visEdges = new vis.DataSet(EDGES.map((e,i) => Object.assign({
  id:'e'+i, from:e.from, to:e.to, label:e.label, kind:e.kind, verified:e.verified,
  font:{ size:9.5, color:'#8c8989', strokeWidth:3, strokeColor:'#f7f5f5', align:'middle' },
  smooth:{ type:'dynamic' }
}, edgeStyle(e))));

const container = document.getElementById('net');
const data = { nodes: visNodes, edges: visEdges };
const options = {
  physics:{ solver:'forceAtlas2Based',
    forceAtlas2Based:{ gravitationalConstant:-46, centralGravity:0.008, springLength:130, springConstant:0.08, avoidOverlap:0.6 },
    stabilization:{ iterations:300 }, minVelocity:0.6 },
  interaction:{ hover:true, tooltipDelay:120, navigationButtons:false, keyboard:false },
  edges:{ selectionWidth: 1.6 },
};
const network = new vis.Network(container, data, options);
network.once('stabilizationIterationsDone', ()=> network.setOptions({ physics:false }));

// 隣接マップ
const adj = {}; NODES.forEach(n=> adj[n.id]={out:[],inc:[]});
EDGES.forEach((e,i)=>{ adj[e.from].out.push({i,e}); adj[e.to].inc.push({i,e}); });

const detail = document.getElementById('detail');
function nodeLabel(id){ return NODES.find(n=>n.id===id).label; }

function showDetail(id){
  const n = NODES.find(x=>x.id===id);
  const c = CATS[n.cat];
  const out = adj[id].out, inc = adj[id].inc;
  const relRow = (e, dir) => {
    const other = dir==='out'? e.to : e.from;
    const verb = dir==='out'? '→' : '←';
    return `<div class="rel-item ${e.verified?'':'unverified'}"><span class="arrow">${verb}</span> ${nodeLabel(other)} <span class="rel-label">（${e.label}）</span></div>`;
  };
  let h = `<h2>${n.label}</h2><span class="cat-badge" style="background:${c.color}">${c.name}</span>`;
  if(out.length) h += `<div class="rel-group"><h3>このデータがつくる / 効く先（${out.length}）</h3>` + out.map(o=>relRow(o.e,'out')).join('') + `</div>`;
  if(inc.length) h += `<div class="rel-group"><h3>このデータを使う / 前提にするもの（${inc.length}）</h3>` + inc.map(o=>relRow(o.e,'inc')).join('') + `</div>`;
  if(!out.length && !inc.length) h += `<p class="panel-empty">記録された関連はありません。</p>`;
  h += `<a class="docbtn" href="SQ-FAQ.html#${DOC[n.doc]}" target="_blank">📖 データ事典${n.doc==1?'①':'②'}で詳しく ↗</a>`;
  detail.innerHTML = h;
}

function focusNode(id){
  const keep = new Set([id]);
  const keepEdges = new Set();
  adj[id].out.forEach(o=>{ keep.add(o.e.to); keepEdges.add('e'+o.i); });
  adj[id].inc.forEach(o=>{ keep.add(o.e.from); keepEdges.add('e'+o.i); });
  visNodes.update(NODES.map(n=>({ id:n.id, opacity: keep.has(n.id)?1:0.12 })));
  visEdges.update(EDGES.map((e,i)=>({ id:'e'+i, hidden:false,
    color: keepEdges.has('e'+i)? edgeStyle(e).color : {color:'rgba(180,176,170,0.12)'} })));
  network.selectNodes([id]);
  showDetail(id);
}
function resetView(){
  visNodes.update(NODES.map(n=>({id:n.id, opacity:1})));
  visEdges.update(EDGES.map((e,i)=>Object.assign({id:'e'+i, hidden:false}, edgeStyle(e))));
  network.unselectAll();
}

network.on('click', p=>{ if(p.nodes.length) focusNode(p.nodes[0]); else { resetView(); detail.innerHTML='<p class="panel-empty">ノード（データ）をクリックすると、そのデータが<b>何につながっているか</b>を一覧表示します。</p>'; } });

// カテゴリフィルタ
const hiddenCats = new Set();
const cf = document.getElementById('catfilter');
Object.entries(CATS).forEach(([k,v])=>{
  const id='cf_'+k;
  const lab=document.createElement('label');
  lab.innerHTML=`<input type="checkbox" id="${id}" checked><span class="dot" style="background:${v.color}"></span>${v.name}`;
  cf.appendChild(lab);
  lab.querySelector('input').addEventListener('change', ev=>{
    if(ev.target.checked) hiddenCats.delete(k); else hiddenCats.add(k);
    visNodes.update(NODES.map(n=>({id:n.id, hidden: hiddenCats.has(n.cat)})));
  });
});

// 在庫フローだけ
let spineOn=false;
document.getElementById('spineBtn').addEventListener('click', ()=>{
  spineOn=!spineOn;
  if(spineOn){
    const keep=new Set();
    EDGES.forEach(e=>{ if(e.kind==='spine'){ keep.add(e.from); keep.add(e.to); } });
    visNodes.update(NODES.map(n=>({id:n.id, hidden:!keep.has(n.id)})));
    visEdges.update(EDGES.map((e,i)=>({id:'e'+i, hidden: e.kind!=='spine'})));
    document.getElementById('spineBtn').style.background='#dce8ff';
  } else { resetView(); document.getElementById('spineBtn').style.background='';
    visNodes.update(NODES.map(n=>({id:n.id, hidden:hiddenCats.has(n.cat)}))); }
});

document.getElementById('reset').addEventListener('click', ()=>{ spineOn=false; document.getElementById('spineBtn').style.background=''; hiddenCats.clear(); cf.querySelectorAll('input').forEach(i=>i.checked=true); resetView(); visNodes.update(NODES.map(n=>({id:n.id,hidden:false}))); network.fit({animation:true}); });

// 検索
const q=document.getElementById('q');
q.addEventListener('keydown', ev=>{ if(ev.key!=='Enter') return;
  const t=q.value.trim(); if(!t) return;
  const hit = NODES.find(n=> n.label.includes(t));
  if(hit){ network.focus(hit.id,{scale:1.1,animation:true}); focusNode(hit.id); }
});
</script>
</body></html>'''


if __name__ == '__main__':
    build()
