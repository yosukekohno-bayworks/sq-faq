# 未確認項目 追加進捗レビュー 20（Codex / Playwright）

対象: 発注伝票保存バグ・発注から入荷指示生成の再確認  
確認日: 2026-06-09  
対象URL: `https://www.sqstackstaging.com/admin`

## 証跡

- 実行スクリプト: `faq/_analysis/deep-screen-verification-20260609/purchase_order_current_behavior_probe.mjs`
- 記録JSON: `faq/_analysis/deep-screen-verification-20260609/purchase-order-current-behavior-records.json`
- スクショ: `faq/_analysis/deep-screen-verification-20260609/purchase-order-current-screenshots/`
- 記録数: 9
- スクショ数: 9
- 失敗: なし
- 400以上のネットワーク応答: なし
- 補足: 記録スクリプトはClerk系レスポンス本文を保存しないよう安全化済み。

## 実操作した内容

| 項目 | 値 |
|:--|:--|
| 取引先 | `TEST_FAQ_DEEP_202606080340_取引先` |
| テナント | `ユニクロ` |
| 通貨 | `日本円 / JPY` |
| SKU | `486125-31-L` |
| 単価 | `100` |
| 数量 | `1` |
| 税率 | `1` |

## 確認結果

| 項目 | 実画面での現在挙動 | 判定 |
|:--|:--|:--|
| 発注作成フォーム | `/admin/inventory_purchase_orders/create` は `発注伝票を作成`。取引先、テナント、通貨、商品追加、単価、数量、税率、金額、作成ボタンを確認。 | フォームUIは書ける |
| 商品選択 | SKU `486125-31-L` を選択し、発注行に追加できた。 | 商品追加UIは書ける |
| 作成実行 | `作成する` 押下後、画面に `エラーが発生しました。しばらくしてから再度お試しください` が表示。 | 保存不可 |
| GraphQL | `InventoryPurchaseOrderCreate` はHTTP 200だが、レスポンスは `lineItems[0].inventoryItemID` に対する `unknown field` エラー。 | 既存バグ継続 |
| 発注一覧 | 作成試行後も `/admin/inventory_purchase_orders` は空状態。 | 発注作成完了は未確認 |
| 入荷一覧 | 作成試行後も `/admin/inventory_inbound_orders` は空状態。 | 発注から入荷指示生成は未確認 |

## GraphQLエラー要約

```text
operationName: InventoryPurchaseOrderCreate
path: variable.input.lineItems.0.inventoryItemID
original_error: unknown field
message: エラーが発生しました。しばらくしてから再度お試しください
```

## 判断

- `発注伝票を作成できます` は現時点では断定不可。
- `発注から入荷指示が自動生成される` も、今回の再確認後も未実証のまま。
- FAQでは、作成画面の存在と入力項目に限定し、保存完了・入荷連携・在庫反映は未確認として扱うのが安全。

## FAQ本文に使うなら安全な表現

- 発注管理には、取引先、テナント、通貨、商品、数量、単価などを入力する発注伝票作成画面があります。
- ただし今回のstaging検証では、作成実行時にGraphQLエラーが発生し、発注伝票の保存完了は確認できていません。
- 発注伝票から入荷指示が作られるか、在庫へ反映されるかは、保存バグ修正後に再確認が必要です。
