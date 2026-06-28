# TODO/未実装表示の現行再確認 2026-06-28

## 検証方法

- 対象環境: `https://www.sqstackstaging.com/admin`
- ログインユーザー: `stack-ps-yosuke`
- 実行方法: 既存ブラウザのCDP接続で対象URLを直接巡回
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/visible-state-recheck-20260628.json`

## 結果

| URL | 結果 |
|:--|:--|
| `/admin/analytics` | h1 `分析`、本文 `TODO` |
| `/admin/analytics/revenue` | h1 `売上`、本文 `TODO`。左ナビ名は `収益` |
| `/admin/analytics/reports` | h1 `レポート`、本文 `TODO` |
| `/admin/b2b` | h1 `卸売`、本文 `TODO` |
| `/admin/order_returns` | h1 `返品`、空一覧。`アイテムが見つかりませんでした` |
| `/admin/order_returns/create` | `このページは存在しないようです` |
| `/admin/orders` | h1 `注文管理`、空一覧。`アイテムが見つかりませんでした` |
| `/admin/orders/create` | `予期せぬエラーが発生しました` |
| `/admin/pdf_export` | h1 `PDFエクスポート`、出荷グループに `納品書`。説明は `指定された出荷指示の納品書をエクスポートできます。` |
| `/admin/pdf_export/pdf_export_operation_packing_slips/create` | `このページは存在しないようです` |
| `/admin/settings/metafield_definitions` | h1 `メタフィールド定義`、本文に `TODO` なし |
| `/admin/settings/translation` | h1 `翻訳`、本文に `TODO` なし |
| `/admin/settings/translation/translation_rules` | h1 `翻訳ルール`、本文に `TODO` なし |
| `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App/admin_api` | h1 `リクエストログ`、補足 `Admin API - TEST_FAQ_20260624_APP_113636`、本文 `TODO` |
| `/admin_api` | `このページは存在しないようです` |

## 反映方針

- 分析3画面、卸売、APIリクエストログは現時点でも未実装/TODO表示として扱う。
- 返品作成直URL、PDF納品書作成直URL、`/admin_api` は存在しない画面として扱う。
- 注文作成直URLは404ではなく予期せぬエラー画面として扱う。
- メタフィールド定義・翻訳トップ・翻訳ルール一覧は本文に `TODO` がないため、04-notion本文の残課題表現を「TODO」ではなく「未実装プレースホルダーなし」「残課題」に寄せる。
