# 17 顧客・会社: 会社一覧インポートボタン再確認 2026-06-28

## 対象

- 画面: 会社一覧
- URL: `https://www.sqstackstaging.com/admin/companies`
- 操作: 右上の `インポート` ボタンをクリック

## 結果

- クリック後もURLは `/admin/companies` のまま。
- ダイアログ、ドロップダウン、トースト、画面遷移は表示されない。
- 画面本文の表示内容もクリック前後で変化なし。

## 反映先

- `04-notion/17-顧客・会社.md`
- `_analysis/complete-live-verification-2026-06-28/SUMMARY.md`

## 判定

会社一覧の `インポート` ボタンは、2026-06-28時点のstaging実機では無反応。現行FAQ/Notionでは、会社CSVインポート手順として扱わず、未実装または未接続のUIとして扱う。
