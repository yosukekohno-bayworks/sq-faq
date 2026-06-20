# 未確認項目 追加進捗レビュー 6（Codex / Playwright）

作成日: 2026-06-09

方針: 元のFAQ/分析ファイルは変更せず、残っていた高リスク項目「発注伝票を作成できるか」「発注保存後に入荷指示へ連携するか」を実画面で再確認した。

## 今回の追加証跡

- `faq/_analysis/deep-screen-verification-20260609/purchase_order_current_behavior_probe.mjs`
- `faq/_analysis/deep-screen-verification-20260609/purchase-order-current-behavior-records.json`
- `faq/_analysis/deep-screen-verification-20260609/purchase-order-current-screenshots/`

## 実操作した内容

| 項目 | 値 |
|---|---|
| 画面 | `/admin/inventory_purchase_orders/create` |
| 取引先 | `TEST_FAQ_DEEP_202606080340_取引先` |
| テナント | `ユニクロ` |
| 通貨 | `日本円` |
| SKU | `486125-31-L` |
| 単価 | `100` |
| 数量 | `1` |
| 税率 | `1` |

## 確認できたこと

| 確認項目 | 実画面結果 | FAQでの扱い |
|---|---|---|
| 発注作成フォーム | `発注伝票を作成` 画面は表示される。取引先・テナント・通貨を選択できる。 | 作成フォームの存在・主要入力項目は確認済み。 |
| 商品追加 | `商品を追加する` からバリエーション選択モーダルに入り、SKU `486125-31-L` を選択できる。 | 商品バリエーションを追加するUIは確認済み。 |
| 金額入力 | 商品行に `単価`、`数量`、`税率`、`金額` が表示され、数値入力できる。 | 入力項目としては確認済み。 |
| 作成実行 | `作成する` 押下後も作成画面に留まり、`エラーが発生しました。しばらくしてから再度お試しください` が表示された。 | 「発注伝票を作成できます」とは断定不可。 |
| GraphQL応答 | `InventoryPurchaseOrderCreate` mutation はHTTP 200だが、本文は `lineItems[0].inventoryItemID` に対する `unknown field` エラー。 | 2026-06-08の既存証跡と同じ原因が継続。 |
| 発注一覧 | `/admin/inventory_purchase_orders` は作成後も `アイテムが見つかりませんでした`。 | 発注保存後の一覧・詳細は未確認。 |
| 入荷一覧 | `/admin/inventory_inbound_orders` も作成後は空状態。 | 発注から入荷指示が自動生成される挙動は未確認。 |

## GraphQLエラー要約

保存時のmutation:

```text
InventoryPurchaseOrderCreate
```

レスポンス要点:

```text
path: variable.input.lineItems.0.inventoryItemID
original_error: unknown field
message: エラーが発生しました。しばらくしてから再度お試しください
```

## FAQ本文への判断

`faq/SQ-FAQ.html` の「発注管理」説明は、次のように弱めるのが安全。

> 発注管理には、仕入先・テナント・通貨・商品・数量・単価を入力する発注伝票作成画面があります。ただし、今回のstaging検証では保存時にGraphQLエラーが発生し、発注伝票の作成完了および入荷指示への連携は確認できていません。

`faq/_analysis/11-operations.md` / `faq/_analysis/SUMMARY.md` の「発注経由の入荷連携は未実証」という扱いは、今回の再実行後も正しい。

## 今回も残す未確認

| 項目 | 理由 |
|---|---|
| 発注伝票の作成完了 | GraphQL `inventoryItemID unknown field` で保存不可。 |
| 発注詳細画面 | 発注伝票が作成されなかったため未確認。 |
| 発注から入荷指示の自動生成 | 発注保存に失敗したため未確認。 |
| 発注後の在庫反映 | 同上。 |
