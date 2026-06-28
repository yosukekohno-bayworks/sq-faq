#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
AUDIT_DIR = ROOT / "_analysis" / "live-notion-verification-2026-06-27" / "full-04-audit"
INDEX = OUT_DIR / "unverified-claim-index.json"
INDEX_MD = OUT_DIR / "unverified-claim-index.md"
OUT_JSON = OUT_DIR / "verification-backlog.json"
OUT_MD = OUT_DIR / "verification-backlog.md"

NON_PENDING_STATUSES = {
    "not-a-claim",
    "verified-by-live-execution",
    "verified-by-route-crawl",
}

URL_RE = re.compile(r"`(/admin[^`\s]*)`|(/admin[\w/{}\[\]-]*)")
EXTRACT_TERMS = [
    "未確認",
    "要確認",
    "未検証",
    "TODO",
    "検証待ち",
    "連携待ち",
    "開発元確認",
    "未接続",
    "対象外",
    "巻き戻し不可",
    "別権限",
    "別アカウント",
    "実注文",
    "実顧客",
    "売上データ0件",
    "顧客データ0件",
    "チャネル未接続",
]

ROUTE_FILES = [
    OUT_DIR / "route-crawl-20260628.json",
    OUT_DIR / "visible-state-recheck-20260628.json",
    "route-crawl-20260627.json",
    "route-crawl-refetch-20260627.json",
    "route-crawl-trailing-20260627.json",
]

route_text = {}
route_meta = {}
for name in ROUTE_FILES:
    path = name if isinstance(name, Path) else AUDIT_DIR / name
    if not path.exists():
        continue
    data = json.loads(path.read_text())
    for row in data.get("results", []):
        route = row.get("route")
        if not route:
            continue
        parts = []
        for key in ["h1", "h2", "alerts", "buttons", "tabs", "tableHeaders", "inputs", "selects", "bodySample"]:
            val = row.get(key)
            if isinstance(val, list):
                parts.extend(str(x) for x in val)
            elif val:
                parts.append(str(val))
        route_text[route] = " ".join(parts)
        route_meta[route] = {
            "file": str(path.relative_to(ROOT)),
            "finalUrl": row.get("finalUrl"),
            "title": row.get("title"),
            "error": row.get("error"),
        }

def extract_rows():
    rows = []
    for path in sorted((ROOT / "04-notion").glob("*.md")):
        in_code = False
        for line_no, raw in enumerate(path.read_text().splitlines(), start=1):
            stripped = raw.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code or not stripped:
                continue
            if stripped.startswith("- [ ]") or any(term in stripped for term in EXTRACT_TERMS):
                rows.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line_no,
                    "text": stripped,
                })
    return rows

rows = extract_rows()
INDEX.write_text(json.dumps({"count": len(rows), "rows": rows}, ensure_ascii=False, indent=2))

index_md = [
    "# 04-notion 未確認・連携待ち抽出 2026-06-28",
    "",
    f"抽出件数: {len(rows)}",
    "",
]
for row in rows:
    index_md.append(f"- `{row['file']}:{row['line']}` {row['text']}")
INDEX_MD.write_text("\n".join(index_md) + "\n")

def urls_in(text):
    out = []
    for match in URL_RE.finditer(text):
        url = match.group(1) or match.group(2)
        if url and "{" not in url and "[" not in url:
            out.append(url.rstrip(".,)"))
    return out

def classify(row):
    text = row["text"]
    urls = urls_in(text)
    lowered = text.lower()
    if "## 残課題" in text or text.startswith("### ") or "完成寄り" in text or "対象外・データ依存" in text:
        return "not-a-claim", "見出し/導入行であり検証対象の主張ではない", urls
    if text.startswith("!["):
        return "not-a-claim", "スクリーンショット参照行であり未検証主張ではない", urls
    if "TODO" in text and "2026-06-28" in text and ("再確認" in text or "確認" in text):
        return "verified-by-route-crawl", "2026-06-28の実機再確認済みTODO表示", urls
    pending_markers = ["未確認", "未検証", "要確認", "連携待ち", "未接続", "対象外", "開発元確認"]
    if ("✅ 確定" in text or "2026-06-28実機確認" in text or "2026-06-28確認" in text or "2026-06-28再確認" in text) and not any(k in text for k in pending_markers):
        return "verified-by-live-execution", "2026-06-28の実機操作証跡で確認済み", urls
    if "ヤマトB2" in text and any(k in text for k in ["CSV保存", "詳細作成", "検証成功 0件", "実CSVサンプル", "出荷完了遷移"]):
        return "needs-seeded-business-data", "実CSVサンプルまたは出荷実績データが必要", urls
    if any(k in text for k in ["staging環境のみ", "本番環境", "公式", "開発元", "別アカウント", "別権限", "権限グループ別", "write権限", "ON時の具体的挙動", "接続環境", "接続済み環境", "連携環境", "連携待ち", "連携前提", "接続前提", "接続後", "未接続", "チャネル未接続", "外部接続", "外部連携", "外部システム", "外部側", "外部影響", "同期イベント", "同期開始", "同期時", "双方向同期", "在庫同期", "ロジザード", "読み取り先", "税計算", "販売可否表示", "POS売上連動", "起因イベント", "運用理由", "実機未確認部分", "実API認証", "生成成功条件", "既存マスタ削除", "連携に残したまま組織除外", "本人がログイン"]):
        return "blocked-by-environment", "現在のstaging管理画面単体では検証できない", urls
    if any(k in text for k in ["実注文", "実通知", "実データ", "データあり", "データ前提", "データが0件", "0件のため", "注文データ前提", "注文データ0件", "注文データが0件", "売上データ0件", "顧客データ0件", "顧客データが入った状態", "ポイント実", "実付与", "実適用", "会員ランク", "返品時", "出荷完了から", "決済完了", "実ファイル", "出力結果が必要", "翻訳生成結果", "翻訳出力結果", "生成結果が必要", "成功例", "閾値到達時", "販売停止", "連動のタイミング", "受注時"]):
        return "needs-seeded-business-data", "注文/顧客/ポイント/売上などの業務データが必要", urls
    if ("注文" in text or "受注" in text) and any(k in text for k in ["未確認", "未検証", "想定", "要確認"]):
        return "needs-seeded-business-data", "注文/顧客/ポイント/売上などの業務データが必要", urls
    if any(k in text for k in ["API経由", "API直接", "GraphQL", "Playground", "Webhook署名", "実際の送信"]):
        return "blocked-by-environment", "現在のstaging管理画面単体では検証できない", urls
    if "CSVインポート" in text and ("巻き戻し不可" in text or "取り消し不可" in text):
        return "verified-by-live-execution", "CSV実行証跡で確認済み（販売可能在庫・商品CSV・カタログ商品CSV）", urls
    if "未確認" in text and any(k in text for k in ["通常導線", "入口", "UI", "ボタン", "フォーム"]):
        return "needs-ui-recheck", "画面操作/導線の再確認が必要", urls
    if any(k in text for k in ["削除", "除外", "失効", "再発行", "巻き戻し不可", "実作成", "CSVインポートの実行", "取込", "発行操作"]):
        return "risky-operation", "影響操作または巻き戻し困難な操作を含む", urls
    for url in urls:
        evidence = route_text.get(url)
        if evidence:
            tokens = [t for t in re.split(r"[`|、。\\s/（）()・:：]+", text) if len(t) >= 2]
            hits = [t for t in tokens if t in evidence][:5]
            if hits:
                return "verified-by-route-crawl", f"URL巡回証跡に該当語あり: {', '.join(hits)}", urls
    if "TODO" in text:
        return "needs-recheck-visible-state", "TODO/未実装表示の現時点再確認が必要", urls
    if "導線" in text or "ボタン" in text or "フォーム" in text or "選択肢" in text or "UI" in text:
        return "needs-ui-recheck", "画面操作/導線の再確認が必要", urls
    if "未確認" in text or "要確認" in text or "未検証" in text:
        return "needs-specific-test", "個別テスト設計が必要", urls
    return "needs-review", "分類不能", urls

classified = []
summary = {}
for row in rows:
    status, reason, urls = classify(row)
    new = dict(row)
    new.update({"verification_status": status, "verification_reason": reason, "urls": urls})
    classified.append(new)
    summary[status] = summary.get(status, 0) + 1

pending = [row for row in classified if row["verification_status"] not in NON_PENDING_STATUSES]
pending_summary = {}
for row in pending:
    status = row["verification_status"]
    pending_summary[status] = pending_summary.get(status, 0) + 1

OUT_JSON.write_text(json.dumps({
    "source_count": len(classified),
    "pending_count": len(pending),
    "classified_summary": summary,
    "pending_summary": pending_summary,
    "rows": pending,
}, ensure_ascii=False, indent=2))

md = [
    "# 04-notion 完全実機検証バックログ 2026-06-28",
    "",
    f"抽出した未確認系行: {len(classified)}",
    f"実際の未完了バックログ: {len(pending)}",
    "",
    "## 未完了件数",
    "",
    "| 状態 | 件数 |",
    "|:--|--:|",
]
for key, count in sorted(pending_summary.items(), key=lambda x: (-x[1], x[0])):
    md.append(f"| {key} | {count} |")

md.extend([
    "",
    "## 残件外に分離した分類",
    "",
    "| 状態 | 件数 | 理由 |",
    "|:--|--:|:--|",
])
for key in sorted(NON_PENDING_STATUSES):
    count = summary.get(key, 0)
    if key == "verified-by-route-crawl":
        reason = "URL巡回/再確認証跡で確認済み"
    elif key == "verified-by-live-execution":
        reason = "実行証跡で確認済み"
    else:
        reason = "見出しなど検証対象の主張ではない"
    md.append(f"| {key} | {count} | {reason} |")

for status in sorted(pending_summary):
    md.append("")
    md.append(f"## {status}")
    for row in pending:
        if row["verification_status"] == status:
            md.append(f"- `{row['file']}:{row['line']}` {row['verification_reason']} / {row['text']}")

OUT_MD.write_text("\n".join(md) + "\n")
print(json.dumps({
    "source_count": len(classified),
    "pending_count": len(pending),
    "classified_summary": summary,
    "pending_summary": pending_summary,
}, ensure_ascii=False, indent=2))
