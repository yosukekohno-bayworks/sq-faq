# SQ実機 全ページ項目・選択肢監査サマリー 2026-06-21

## 実施範囲

| 項目 | 結果 |
|:--|:--|
| 対象環境 | `https://www.sqstackstaging.com/admin` |
| スキャン対象 | 256ページ |
| DOM取得成功 | 256ページ |
| 項目抽出あり | 119ページ |
| テーブル抽出あり | 35ページ |
| 存在しないページ | 17ページ |
| アプリエラー画面 | 2ページ |
| TODO表示 | 5ページ |

保存・削除・実行など状態変更を伴うボタンは、広域スキャンでは押していません。別途、在庫追跡OFF・在庫依頼フラグOFFなどの重点項目は実操作で検証し、必要箇所をFAQ本文へ反映しました。

## 重点確認結果

| 項目 | 実機で確認したこと | FAQ反映 |
|:--|:--|:--|
| バリエーションの「在庫を追跡する」 | 作成フォーム初期値はOFF。OFFでも在庫一覧・SKU詳細・在庫編集・移動/調整/取置/在庫依頼/発注/店舗受取/販売設定候補から除外されない。外部チャネル連携時の影響は未確認 | 商品、在庫、在庫伝票、入出荷、販売設定、データ事典② |
| バリエーション作成時の価格欄 | 作成フォームにある価格欄は「上代」のみ。「仕入価格」「原価」は作成時に出ない。編集画面には「原価」セクションと「原価を登録する」がある | 商品管理、商品作成/編集、05-商品・SKU、データ事典② |
| ロケーションの「在庫依頼を受け付ける」 | 作成フォーム初期値はOFF。手動在庫依頼ではOFFでもリクエスト先に選択・保存できる。自動在庫リクエスト送付対象の制御は連携環境で要確認 | 設定、初期設定、取り寄せ販売、基本マスタ、FAQ |
| 発注後の入荷連動 | `#IP-1004` は発注済み詳細まで確認。`#IP-1000` / `#IP-1001` / `#IP-1003` / `#IP-1004` の範囲で、入荷管理一覧への発注起点入荷指示表示・SKU入荷予定増加は確認できず | 発注管理、14-発注・仕入、データ事典②、support台帳 |
| ヤマトB2/PDF | ヤマトB2条件指定エクスポートフォームには「ヤマトB2クラウド取り込み用CSV」「同梱する納品書PDF」と表示。PDFエクスポート単体の新規作成URLは存在しない。実メールリンク・PDF実ファイルは未確認 | CSV/PDF、出荷管理、20-物流、21-CSV/PDF |
| CSVエクスポートURL | 在庫=`inventory_logical_quantities`、ロケーション=`location_by_location_group`、セール価格=`product_price_rule_sale_prices`、ポイント変動履歴=`point_changes`。旧URLは存在しない | CSV/PDF、21-CSV/PDF |

## 存在しないページ

- `/admin/order_returns/create`
- `/admin/sale_change_line_items/create`
- `/admin/b2b/create`
- `/admin/csv_import/csv_import_operation_customer_rank_rules`
- `/admin/csv_import/csv_import_operation_customer_rank_rules/create`
- `/admin/csv_import/csv_import_settings_suppliers`
- `/admin/csv_import/csv_import_settings_suppliers/create`
- `/admin/csv_export/csv_export_operation_inventory_items`
- `/admin/csv_export/csv_export_operation_inventory_items/create`
- `/admin/csv_export/csv_export_operation_locations`
- `/admin/csv_export/csv_export_operation_locations/create`
- `/admin/csv_export/csv_export_operation_sale_prices`
- `/admin/csv_export/csv_export_operation_sale_prices/create`
- `/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds/create`
- `/admin/csv_export/csv_export_operation_point_histories`
- `/admin/csv_export/csv_export_operation_point_histories/create`
- `/admin/pdf_export/pdf_export_operation_packing_slips/create`

## アプリエラー / TODO

| 種別 | ページ |
|:--|:--|
| アプリエラー | `/admin/draft_orders/create` |
| アプリエラー | `/admin/purchasing_customers/create` |
| TODO | `/admin/analytics` |
| TODO | `/admin/analytics/revenue` |
| TODO | `/admin/analytics/reports` |
| TODO | `/admin/b2b` |
| TODO | `/admin/settings/apps/9081ef6c-dc90-50be-9bb8-d869eb02f44f_App/admin_api` |

## 生成物

- `scan-results.json`: 実機DOM抽出の生データ
- `scan-results.md`: ページ別の項目・選択肢・テーブル要約
- `tools/sq_live_option_scan.py`: 再実行用スキャナ

