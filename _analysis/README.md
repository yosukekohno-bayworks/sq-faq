# 誃査記録（一次素材）

SQアプリの調査一次記録置き場。FAQ執筆では、最新の実機確認ログと正本資料を優先する。

## 正本（優先順位順）
1. `VERIFIED-FACTS-ONLY-2026-06-19.md` — FAQで断定してよい実機確定事実の台帳
2. `CODEX-OPS-PLAYWRIGHT-VERIFICATION-2026-06-18.md` — 2026-06-18の実機操作ログ
3. `CODEX-LEGACY-RECONCILIATION-2026-06-18.md` — 旧検証ログとの照合結果
4. `LIVE-VERIFICATION-2026-06-19.md` — 実機検証ログ（ground truth）
5. `FAQ-AUDIT-REPORT-2026-06-19.md` / `FAQ-AUDIT-FINDINGS-2026-06-19.json` — 監査レポート・生findings
6. `REMAINING-CONFIRMATION-EXCEPTIONS-2026-06-19.md` — 残存未確認の例外台帳

## 計画・進行管理
`KICKOFF-MEETING-2026-06-12.md` / `FAQ-PROJECT-2MONTH-GUIDELINE-2026-06-16.md` / `FAQ-PROJECT-DETAILED-WBS-2026-06-16.html` / `FAQ-PROJECT-WBS-25AREAS-2026-06-18.html` / `SQ-LEARNING-ROADMAP-AND-CUSTOMER-DIFF-2026-06-16.html`

## 一次情報（開発元）
`MEETING-RECORDING-FINDINGS-2026-05-20.md`（録画精査） / `STACK-TIS-SEMINAR-NOTES-2026-06-12.md`（TIS勉強会）

## 分析・設計
`FEATURE-LIST-GAP-ANALYSIS-2026-06-12.md` / `FEATURE-SWEEP-2026-06-12.md`（公式機能一覧との照合） / `CUSTOMER-DOCS-FAQ-REVIEW-2026-06-16.md`（顧客別差分: MK/CHAMPION） / `logiless-ux-analysis.md`（FAQ設計指針）

## 実機スナップショット
`live-recheck-sale-change-2026-06-19.json` / `live-recheck-2026-06-19-extra.json`

## スクショ
`screenshots/`（FAQ本文が画像リンクで参照）

---

## アーカイブ

### `archive/initial-feature-survey-2026-06-07/`（2026-06-20整理）
2026-06-05基準の初期調査を、実機確認しながらarchive移動（計22ファイル）。
- 機能別初期調査 `00-admin-sitemap.md` 〜 `15-csv-pdf.md`（17）
- 古い集約メモ `SUMMARY.md` / `COMPLEX-OPERATIONS.md` / `CONFIRMATION-LIST.md`（3）
- 依存パイプライン `build_report.py` / `SQ-調査報告.html`（2）

陳腐化ポイント（発注保存不可バグ=実は解消、在庫区分 確定済み/確保済み→引当済み/取置中、権限70→76、CSV 20→22/8→9 等）は正本と FAQ本文(`01-by-feature`)に上書き済み。整理の経緯は同フォルダの `PROGRESS.md` を参照。

### `archive/legacy-verification-before-2026-06-18/`
旧検証ログ（`coverage-*` / `sq-reaudit-*` / `unconfirmed-*` 等、約300ファイル）。2026-06-18より前の細かい検証記録。

---

## ルール
- 実機で確認した事実のみ断定する。未確認は `<!-- TODO: 要確認 -->`
- UIラベルはアプリ画面の表記をそのまま使う
- アーカイブ（`archive/` 配下）の古い記録を参照する場合は、必ず正本または実機で再確認する
