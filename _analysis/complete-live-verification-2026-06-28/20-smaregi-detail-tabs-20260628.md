# スマレジ接続済み詳細 実機確認 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration`
- 方針: 外部アクセストークン領域があるため、トークン値・全文本文・入力値は保存しない。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 詳細画面に商品連携設定 | `True` |
| 詳細画面に在庫設定 | `True` |
| 詳細画面に取引連携設定 | `True` |
| 詳細画面に外部アクセストークン領域 | `True` |
| 詳細画面に連携解除領域 | `True` |
| タブリンク `店舗設定` | `True` |
| タブリンク `商品管理` | `True` |
| タブリンク `顧客管理` | `True` |

## 基本設定のラベル

- `カタログ`
- `在庫同期の方向`
- `注文による在庫変動を起こさない`
- `取引の連携を有効にする`
- `プラン`

## タブURL

- `店舗設定`: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration/location_links`
- `商品管理`: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration/products`
- `顧客管理`: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration/customers`

## 判断

- 接続済みスマレジ連携の詳細画面構成は確認済みとして扱う。
- 実際の同期方向・頻度・スマレジ側アプリインストール導線・トークン作成後の挙動は未確認として残す。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-smaregi-detail-tabs-20260628.json`
