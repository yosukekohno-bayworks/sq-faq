# 検索・絞り込み 横断確認

- 実行日時: 2026-06-27T19:26:09.264867+00:00
- 方法: 主要一覧を開き、検索入力・`絞り込みを追加` の候補・代表クエリの結果件数を実機確認。

## 管理メンバー `/admin/settings/users`

- h1: ['管理メンバー']
- 初期行数: 5
- 検索パネル表示: initial
- 検索入力: キーワードで検索する
- 絞り込み候補: メールアドレス

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `河野` | 1 | False | `/admin/settings/users?query=%E6%B2%B3%E9%87%8E` |
| `陽介` | 1 | False | `/admin/settings/users?query=%E9%99%BD%E4%BB%8B` |
| `kohno` | 1 | False | `/admin/settings/users?query=kohno` |
| `特権管理者` | 0 | True | `/admin/settings/users?query=%E7%89%B9%E6%A8%A9%E7%AE%A1%E7%90%86%E8%80%85` |
| `河野 kohno` | 0 | True | `/admin/settings/users?query=%E6%B2%B3%E9%87%8E+kohno` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/settings/users?query=__NO_MATCH_FAQ_20260628__` |

## 商品 `/admin/products`

- h1: ['商品管理']
- 初期行数: 17
- 検索パネル表示: keyboard_f
- 検索入力: 商品コードで検索する
- 絞り込み候補: なし

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `486125` | 2 | False | `/admin/products?product_code=486125` |
| `UNIQLO` | 0 | True | `/admin/products?product_code=UNIQLO` |
| `TEST_E2E` | 6 | False | `/admin/products?product_code=TEST_E2E` |
| `486125 UNIQLO` | 0 | True | `/admin/products?product_code=486125+UNIQLO` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/products?product_code=__NO_MATCH_FAQ_20260628__` |

## 在庫 `/admin/inventory_items`

- h1: ['在庫管理 :']
- 初期行数: 9
- 検索パネル表示: keyboard_f
- 検索入力: SKUコードで検索する
- 絞り込み候補: 商品コード

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `486125` | 1 | False | `/admin/inventory_items?sku=486125` |
| `486125-31-XL` | 1 | False | `/admin/inventory_items?sku=486125-31-XL` |
| `ユニクロ` | 0 | True | `/admin/inventory_items?sku=%E3%83%A6%E3%83%8B%E3%82%AF%E3%83%AD` |
| `486125 ユニクロ` | 0 | True | `/admin/inventory_items?sku=486125+%E3%83%A6%E3%83%8B%E3%82%AF%E3%83%AD` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/inventory_items?sku=__NO_MATCH_FAQ_20260628__` |

## ロケーション `/admin/settings/locations`

- h1: ['ロケーション']
- 初期行数: 1
- 検索パネル表示: keyboard_f
- 検索入力: 場所コードで検索する
- 絞り込み候補: 場所種別

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `R0001` | 1 | False | `/admin/settings/locations?code=R0001` |
| `W0001` | 1 | False | `/admin/settings/locations?code=W0001` |
| `銀座` | 0 | True | `/admin/settings/locations?code=%E9%8A%80%E5%BA%A7` |
| `R0001 銀座` | 0 | True | `/admin/settings/locations?code=R0001+%E9%8A%80%E5%BA%A7` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/settings/locations?code=__NO_MATCH_FAQ_20260628__` |

## カタログ `/admin/catalogs`

- h1: ['カタログ']
- 初期行数: 3
- 検索パネル表示: not_found
- 検索入力: なし
- 絞り込み候補: なし

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `TEST_FAQ` | - | skipped | search input not found |
| `UNIQLO` | - | skipped | search input not found |
| `__NO_MATCH_FAQ_20260628__` | - | skipped | search input not found |

## 移動伝票 `/admin/inventory_movement_orders`

- h1: ['移動伝票']
- 初期行数: 29
- 検索パネル表示: not_found
- 検索入力: なし
- 絞り込み候補: なし

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `IM-1027` | - | skipped | search input not found |
| `#IM-1027` | - | skipped | search input not found |
| `入荷完了` | - | skipped | search input not found |
| `__NO_MATCH_FAQ_20260628__` | - | skipped | search input not found |

## 出荷管理 `/admin/inventory_outbound_orders`

- h1: ['出荷管理']
- 初期行数: 28
- 検索パネル表示: keyboard_f
- 検索入力: 管理番号で検索する
- 絞り込み候補: 作業ステータス, 出荷方法, 代引き, 配送先(国)

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `IO-1027` | 0 | True | `/admin/inventory_outbound_orders?management_code=IO-1027` |
| `#IO-1027` | 1 | False | `/admin/inventory_outbound_orders?management_code=%23IO-1027` |
| `出荷完了` | 0 | True | `/admin/inventory_outbound_orders?management_code=%E5%87%BA%E8%8D%B7%E5%AE%8C%E4%BA%86` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/inventory_outbound_orders?management_code=__NO_MATCH_FAQ_20260628__` |

## 入荷管理 `/admin/inventory_inbound_orders`

- h1: ['入荷管理']
- 初期行数: 30
- 検索パネル表示: keyboard_f
- 検索入力: 管理番号で検索する
- 絞り込み候補: 作業ステータス, ロケーション

| クエリ | 件数 | 空状態 | URL変化 |
|:--|--:|:--|:--|
| `II-1029` | 0 | True | `/admin/inventory_inbound_orders?management_code=II-1029` |
| `#II-1029` | 1 | False | `/admin/inventory_inbound_orders?management_code=%23II-1029` |
| `入荷完了` | 0 | True | `/admin/inventory_inbound_orders?management_code=%E5%85%A5%E8%8D%B7%E5%AE%8C%E4%BA%86` |
| `__NO_MATCH_FAQ_20260628__` | 0 | True | `/admin/inventory_inbound_orders?management_code=__NO_MATCH_FAQ_20260628__` |

## 証跡

- JSON: `/Users/kounoyousuke/App Building/SQ/faq/_analysis/complete-live-verification-2026-06-28/23-search-filter-cross-check-20260628.json`
