# SQ FAQ

SQアプリのFAQ。最終的に **Notion** へ投入する。

## 構成

| 分類 | ディレクトリ | 内容 |
|:--|:--|:--|
| 機能別 | `01-by-feature/` | 各機能の概要・できること・画面/項目の説明 |
| 作業別 | `02-by-task/` | ユーザーがやりたい作業ごとの手順（タスク指向） |
| FAQ別 | `03-faq/` | よくある質問と回答（Q&A） |
| はじめに | `00-getting-started/` | 初学者向けガイド・データ事典・全体像 |
| 調査記録 | `_analysis/` | app-analyzer が残すアプリ調査の一次記録・スクショ（FAQの根拠） |

各分類の `_TEMPLATE.md` をコピーして執筆する。

## 現在の正本

| 用途 | 正本 |
|:--|:--|
| 初学者が最初に読む入口 | `00-getting-started/SQ学習・FAQ制作整理マップ.md` |
| 全体理解 | `00-getting-started/SQ完全ガイド.md` |
| データ・ステータス理解 | `00-getting-started/データ事典①-設定で作るデータ.md` / `00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md` |
| 最新の実機検証ログ | `_analysis/LIVE-VERIFICATION-2026-06-19.md`（最優先の正本） |
| FAQ監査・整理レポート | `_analysis/FAQ-AUDIT-REPORT-2026-06-19.md`（齟齬一覧・整理提案）／生データ `_analysis/FAQ-AUDIT-FINDINGS-2026-06-19.json` |
| 実機操作ログ | `_analysis/CODEX-OPS-PLAYWRIGHT-VERIFICATION-2026-06-18.md` |
| 旧検証ログとの照合結果 | `_analysis/CODEX-LEGACY-RECONCILIATION-2026-06-18.md` |

在庫・発注・入荷・出荷・調整・取置・在庫依頼について、過去ログと説明が食い違う場合は、**2026-06-19の実機検証ログ**を最優先し、次に2026-06-18の実機操作ログ・旧検証ログ照合結果を優先する。古い `_analysis/SUMMARY.md`・`07-purchase-orders.md`・`14-settings.md`・`CONFIRMATION-LIST.md` 等（2026-06-05〜07基準）は陳腐化箇所があり、`FAQ-AUDIT-REPORT-2026-06-19.md` §3 を参照のこと。

## キックオフで決まった制作方針

2026-06-12のキックオフでは、FAQをいきなり量産せず、まずSQの製品理解・情報設計を固める方針になった。根拠は `_analysis/KICKOFF-MEETING-2026-06-12.md`。

2ヶ月の進行計画は `_analysis/FAQ-PROJECT-2MONTH-GUIDELINE-2026-06-16.md` に置く。詳細WBSのHTML版は `_analysis/FAQ-PROJECT-DETAILED-WBS-2026-06-16.html` に置く。

| 方針 | 書き方への反映 |
|:--|:--|
| 製品理解を優先する | 機能、データ、依存関係、実測ステータスを先に整理する |
| 操作方法だけで終わらせない | 「いつ使うか」「何を先に設定するか」「何に影響するか」を書く |
| 標準機能と個別開発を分ける | SQ標準機能として確認できることと、顧客別の連携・バックエンド処理を混ぜない |
| stagingの状態を区別する | 未実装、不具合、外部連携不足、実データ不足を分けて記録する |
| 初学者と顧客の両方に使える形にする | 通読用の完全ガイドと、検索用のFAQ/作業別ページを併用する |

## 制作フロー
1. `app-analyzer` がSQアプリを調査 → `_analysis/` に記録
2. `faq-writer` が記録を根拠に3分類で執筆
3. `faq-reviewer` がレビュー → 指摘を反映
4. Notion へインポート

## Notion投入メモ
- 各 `.md` ファイルはNotionの「Import > Markdown」で個別ページとして取り込める
- 見出し（#/##/###）・番号リスト・表はNotionブロックに変換される
- 画像はインポート後にリンク切れになりやすいので、Notion側で貼り直すか手動アップロードする

## ルール
- 実機で確認した事実のみ記載（憶測禁止）。未確認は `<!-- TODO: 要確認 -->`
- UIラベルはアプリ画面の表記をそのまま使う
- 手順は番号付き・1ステップ1動作
- 実測の入口資料は `00-getting-started/SQ学習・FAQ制作整理マップ.md`。初学者にはまずこの資料を渡す
