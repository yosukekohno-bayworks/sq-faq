# 23 API・Webhook 追加実機確認 2026-07-01

## 対象

- アプリ: `TEST_FAQ_20260624_APP_113636`
- 詳細画面: `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- 秘密値: アクセストークン、シークレット、Storefrontトークン値は証跡に記録しない

## 結果

| 確認項目 | 結果 |
|:--|:--|
| Webhook作成済み行の操作 | 行右側のゴミ箱アイコンから削除できる |
| Webhook削除確認 | ダイアログ `Webhookを削除する`、本文 `Webhookを削除します。この処理は巻き戻すことができません。` |
| Webhook削除後 | トースト `Webhookを削除しました`。Webhook行は詳細画面から消える |
| Webhook編集/停止 | 編集・停止・送信成功/失敗ステータスは画面上に表示なし |
| Storefront API発行モーダル | `トークンを発行する` で `ストアフロント用のトークンを発行する` モーダルが開く |
| Storefront API発行モーダルの項目 | `カタログ` select、`ロケーショングループ` 選択 |
| Storefront API空保存エラー | `カタログを選択してください` / `ロケーショングループを選択してください` |
| Storefront APIロケーショングループ候補 | `テスト`、既存グループ1件（名称は証跡でマスク）、`ユニクログループ`、`GU グループ` |
| Storefront API発行実行 | `UNIQLO` + `ユニクログループ` 選択後に `発行する` を押しても通信は発生せず、モーダルが閉じない。トークン発行完了は未確認 |
| Storefront API発行未完了の理由 | フロント実装上、未表示の `tenantID` フィールドに必須バリデーションが残っている。画面上にテナント選択欄は表示されない |
| Admin APIログ | `/admin/settings/apps/{id}/admin_api` は `リクエストログ` / `Admin API - <APP>` / `TODO` |
| Storefront APIログ | `/admin/settings/apps/{id}/storefront_api` は `リクエストログ` / `Storefront API - <APP>` / `TODO` |
| 直URL `/admin_api` | `このページは存在しないようです` |
| アプリ削除/失効/再発行 | 詳細画面、一覧カード、上部 `その他の操作` でもアプリ削除・トークン失効・Admin APIアクセストークン/シークレット再発行導線は確認できない |

## 判断

- 2026-06-28時点の「Webhook削除導線なし」は誤り。作成済みWebhook行のゴミ箱アイコンから削除できる。
- Storefront APIトークンは、モーダルの表示・項目・必須エラー・ロケーショングループ選択までは確認済み。ただし現行UIでは発行完了まで進めないため、発行後のトークン表示・削除/失効導線は未確認のまま扱う。
- APIリクエストログはAdmin APIとStorefront APIで別URLだが、どちらも本文は `TODO`。
