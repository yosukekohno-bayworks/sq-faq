# Webhookイベント選択肢 実機確認 2026-06-28

- 対象: `TEST_FAQ_20260624_APP_113636` `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- 操作: アプリ詳細で `Webhookを作成する` を開き、保存せずにイベント欄の候補と選択可否を確認
- 選択可能イベント数: 3
- 選択可能イベント: 注文の作成, 注文の更新, 在庫の更新
- 期待3種のみ: True
- ダイアログ閉鎖確認: True

## select option

- value=`` text=`選択してください` disabled=True
- value=`ORDER_CREATE` text=`注文の作成` disabled=False
- value=`ORDER_UPDATE` text=`注文の更新` disabled=False
- value=`INVENTORY_LOGICAL_CHANGE_CREATE` text=`在庫の更新` disabled=False

## selection checks

- `注文の作成`: value `ORDER_CREATE` -> selected `注文の作成` / `ORDER_CREATE` matched=True
- `注文の更新`: value `ORDER_UPDATE` -> selected `注文の更新` / `ORDER_UPDATE` matched=True
- `在庫の更新`: value `INVENTORY_LOGICAL_CHANGE_CREATE` -> selected `在庫の更新` / `INVENTORY_LOGICAL_CHANGE_CREATE` matched=True

## 結論

- 2026-06-28時点のWebhook作成ダイアログで選択できるイベントは `注文の作成` / `注文の更新` / `在庫の更新` の3種のみ。
- API直叩きや非公開仕様の追加イベントは確認対象外。管理画面UIでユーザーが設定できるイベントとしては上記3種に限定して案内する。
