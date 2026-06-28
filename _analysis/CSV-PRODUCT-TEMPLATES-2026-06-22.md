# 商品一覧インポート5項目テンプレート確認 2026-06-22

## 確認範囲

- 環境: `https://www.sqstackstaging.com`
- 対象: 商品一覧（`/admin/products`）の「インポート」ドロップダウン、および遷移先のCSVインポート5項目
- 確認方法: 実機画面で各CSVインポート一覧を開き、`テンプレート` リンクを取得。Googleスプレッドシートの `定義書` / `フォーマット` シートをCSVとして取得。

## 商品一覧のインポート5項目

| メニュー項目 | CSVインポートURL | テンプレート |
|:--|:--|:--|
| 商品 | `/admin/csv_import/csv_import_operation_products` | `https://docs.google.com/spreadsheets/d/1b2lGs4s6MDIzqTumUDt6WEE42oMv6pJ1leEoMRY4Evk` |
| 商品画像 | `/admin/csv_import/csv_import_operation_product_images` | `https://docs.google.com/spreadsheets/d/14KGrR98eR0-i4uGmdDtE-d_fl-qOIpkKlvNUX9cyEo0` |
| 商品バリエーション | `/admin/csv_import/csv_import_operation_product_variants` | `https://docs.google.com/spreadsheets/d/1SK2yszMNpwOqIfHelNyLJnbLilJg4q9J0iLccKf0Uu0` |
| 商品メタフィールド | `/admin/csv_import/csv_import_operation_product_metafields` | `https://docs.google.com/spreadsheets/d/17hVV5-F3aOQn_gNoBJjRcuoRC6k0r62vdbP2MBM_NbA` |
| 商品バリエーションメタフィールド | `/admin/csv_import/csv_import_operation_product_variant_metafields` | `https://docs.google.com/spreadsheets/d/1E5EX2jkhxkCZmK55el1eP_ZGOrr0SCnjujMZ1tZrfxQ` |

## テンプレートの列

| 対象 | フォーマット列 | 必須列 |
|:--|:--|:--|
| 商品 | `command`, `product_code`, `title`, `description`, `product_status`, `brand_code`, `product_vendor`, `product_type`, `tags`, `option1_name`, `option1_type`, `option2_name`, `option2_type`, `option3_name`, `option3_type`, `seo_title`, `seo_description`, `is_outlet`, `sale_start_date`, `sale_end_date` | `command`, `product_code`, `title`, `product_status`, `option1_name` |
| 商品画像 | `product_code`, `image_url`, `position`, `alt`, `filename` | `product_code`, `image_url` |
| 商品バリエーション | `command`, `sku`, `product_code`, `supplier_sku`, `option1_value`, `option1_value_code`, `option1_value_index`, `option2_value`, `option2_value_code`, `option2_value_index`, `option3_value`, `option3_value_code`, `option3_value_index`, `price`, `price_currency_code`, `weight_value`, `weight_unit`, `inventory_policy`, `is_tracked`, `requires_shipping`, `barcode`, `jan`, `upc`, `harmonized_system_code`, `country_code_of_origin` | `command`, `sku`, `product_code`, `option1_value`, `price`, `price_currency_code` |
| 商品メタフィールド | `product_code`, `namespace`, `key`, `value_type`, `value` | 全列 |
| 商品バリエーションメタフィールド | `sku`, `namespace`, `key`, `value_type`, `value` | 全列 |

## 注意

- 商品一覧の「インポート」メニューは上記5項目。
- CSVインポートトップの「商品」グループは別で、`商品 / 商品バリエーション / 商品画像 / 商品バリエーション画像 / カタログ` の5項目。メタフィールド2項目はCSVインポートトップでは「メタフィールド」グループにある。
- 商品画像インポートの新規作成フォームには、反映方法 `画像を追加する` / `画像を上書きする` がある。
