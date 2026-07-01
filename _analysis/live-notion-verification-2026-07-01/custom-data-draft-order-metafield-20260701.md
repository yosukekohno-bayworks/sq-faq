# 08 カスタムデータ: 下書き注文メタフィールド再確認 2026-07-01

## 対象

- `/admin/draft_orders`
- `/admin/draft_orders/create`
- `/admin/settings/metafield_definitions?ownerType=draft_order`
- `/admin/settings/metafield_definitions/draft_order/create`

## 確認結果

### 下書き注文本体

- 下書き注文一覧は `注文が見つかりませんでした` の空状態。
- 画面上に `注文を作成する` の表示はあるが、クリックしてもURLは `/admin/draft_orders` のまま変わらない。
- 直URL `/admin/draft_orders/create` は `予期せぬエラーが発生しました` / `エラーが発生しました。しばらくしてから再度お試しください` を表示する。

結論: 現行UIでは、下書き注文レコードの作成・詳細表示・メタフィールド値入力画面は確認できない。

### 下書き注文メタフィールド定義

検証用定義:

- 名前: `TEST_FAQ_20260701_DRAFT_ORDER_META`
- 説明: `FAQ live verification draft order metafield`
- ネームスペース: `faqmeta`
- キー: `draft_order_20260701`
- タイプ: `trueまたはfalse`

確認結果:

- `下書き注文メタフィールドの定義を追加する` フォームで保存できた。
- 保存後は `/admin/settings/metafield_definitions?ownerType=draft_order` の一覧へ戻った。
- 一覧行は `TEST_FAQ_20260701_DRAFT_ORDER_META` / `faqmeta.draft_order_20260701` / `trueまたはfalse` / `編集可` / `0個の下書き注文` と表示された。
- 行選択で `定義を削除` が表示された。
- 削除確認ダイアログは `メタフィールドの定義を削除しますか？`、本文は `関連するメタフィールドの値は削除されません` を含む。
- `削除する` 実行後、トースト `メタフィールドの定義を削除しました` が表示され、一覧は `アイテムが見つかりませんでした` に戻った。

## 資料への反映方針

- 下書き注文は「定義作成可」までは確定。
- ただし下書き注文本体の作成・詳細画面を開けないため、「詳細画面にメタフィールド欄が出る」「値入力できる」とは案内しない。
- 16対象すべてで詳細画面に即時表示されるような一般化表現を避ける。
