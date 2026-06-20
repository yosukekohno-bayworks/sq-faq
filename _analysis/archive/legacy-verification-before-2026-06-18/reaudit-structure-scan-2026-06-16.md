# SQ実機構造スキャン

## /admin

- finalUrl: `https://www.sqstackstaging.com/admin`
- headings: stack-ps-yosuke / 商品管理 / 在庫管理 / 注文管理 / 顧客管理 / CSVでデータをインポートする
- status/alert: stack-ps-yosuke。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/products

- finalUrl: `https://www.sqstackstaging.com/admin/products`
- headings: 商品管理
- status/alert: 商品管理。このページの準備が整いました
- tabs: すべて / 公開中 / 下書き / アーカイブ済み
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / 公開中 / 下書き / アーカイブ済み / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / カタログ -> /admin/catalogs / 店舗受取 -> /admin/local_pickup_product_variants / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 商品 | ステータス | 商品コード | 在庫 | カタログ | 商品タイプ | 製造元
  - row: アイテムを選択する | product thumbnail TEST_FAQ_CSV_RECHECK_20260608_商品 | 成功 公開中 | TEST_FAQ_CSV_RECHECK_20260608_01 | 0個のバリエーション | 0
  - row: アイテムを選択する | product thumbnail TEST_FAQ_DEEP2_202606080343_商品 | 成功 公開中 | test_faq_deep2_202606080343_product | 0個のバリエーション | 0 | 検証 | TEST_FAQ
  - row: アイテムを選択する | product thumbnail TEST_FAQ_非公開ステータス確認用 | 成功 公開中 | TEST-FAQ-HIDDEN-001 | 0個のバリエーション | 0

## /admin/products/create

- finalUrl: `https://www.sqstackstaging.com/admin/products/create`
- headings: 商品を作成する / メディア / バリエーション / 検索エンジンリスティング / メタフィールド / TEST_FAQ_テキストフィールド
- status/alert: 商品を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 追加 / 削除 / 追加 / 別のオプションを追加する / 選択 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / カタログ -> /admin/catalogs / 店舗受取 -> /admin/local_pickup_product_variants / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules
- fields: input:商品コード required=False disabled=False / input:商品名 required=False disabled=False / textarea:説明文 required=False disabled=False / input:画像をアップロード required=False disabled=False / input:オプション名 required=False disabled=False / select:種別 required=False disabled=False options=['選択してください', 'サイズ', 'カラー', 'その他'] / input:オプション値 required=False disabled=False / input:コード required=False disabled=False / input:ページタイトル required=False disabled=False / textarea:メタディスクリプション required=False disabled=False / select: required=False disabled=False options=['下書き', '公開', '非公開'] / input:商品タイプ required=False disabled=False / input:製造元 required=False disabled=False / input:ブランド required=False disabled=False

## /admin/catalogs

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs`
- headings: カタログ
- status/alert: カタログ。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 検索結果を並べ替える / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / カタログ -> /admin/catalogs / 店舗受取 -> /admin/local_pickup_product_variants / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | 商品 | 販売先
  - row: アイテムを選択する | TEST_FAQ_カタログ001 | 1個の商品 | 0つの販売先
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_カタログ | 0個の商品 | 0つの販売先
  - row: アイテムを選択する | UNIQLO | 4個の商品 | 0つの販売先

## /admin/local_pickup_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/local_pickup_product_variants`
- headings: 店舗受取
- status/alert: 店舗受取。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / バリエーションを追加する / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / カタログ -> /admin/catalogs / 店舗受取 -> /admin/local_pickup_product_variants / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
  - row: アイテムを選択する | エアリズムコットンクルーネックTシャツ DARK GRAY / XL | 486102 | 486102-08-XL
  - row: アイテムを選択する | オーバーサイズスウェットシャツ GRAY / M | 486125 | 486125-03-M
  - row: アイテムを選択する | UVカットペーパーブレイドハット NATURAL / ONE SIZE | 482787 | 482787-30-ONE

## /admin/inventory_items

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items`
- headings: 在庫管理 :
- status/alert: 在庫管理 : 。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / 物流倉庫 / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 商品 | 品番(SKU) | 販売可能 | 引当済み | 取置中 | 手持ち
  - row: アイテムを選択する | バギーカーブジーンズ BLUE / 36 | 487973-64-36 | 100 | 0 | 0 | 100
  - row: アイテムを選択する | エアリズムコットンクルーネックTシャツ GREEN / XL | 486102-52-XL | 0 | 0 | 0 | 0
  - row: アイテムを選択する | オーバーサイズスウェットシャツ BLACK / XL | 486125-09-XL | 7 | 0 | 0 | 7

## /admin/inventory_movement_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders`
- headings: 移動伝票
- status/alert: 移動伝票。このページの準備が整いました
- tabs: すべて / 出荷作業 / 一部受領済み / 受領済み / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 出荷作業 / 一部受領済み / 受領済み / キャンセル / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- table1 headers: 管理番号 | 配送元 | 配送先 | ステータス | 作成日時
  - row: #IM-1007 | 物流倉庫 | 物流倉庫 | キャンセル | 2026年06月16日 09:26
  - row: #IM-1006 | 物流倉庫 | ユニクロ - 銀座店 | 成功 完了 入荷完了 | 2026年06月15日 18:11
  - row: #IM-1005 | 物流倉庫 | ユニクロ - 銀座店 | 成功 完了 入荷完了 | 2026年06月14日 01:24

## /admin/inventory_movement_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- headings: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- status/alert: 移動伝票を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 選択 / 参照 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- fields: input:配送元 required=False disabled=False / input:配送先 required=False disabled=False / input:商品を追加する required=False disabled=True

## /admin/inventory_adjustment_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders`
- headings: 調整伝票
- status/alert: 調整伝票。このページの準備が整いました
- tabs: すべて / 未実施 / 実施済み / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 未実施 / 実施済み / キャンセル / その他のビュー / 検索と絞り込みの結果 / 検索結果を並べ替える / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 管理番号 | ロケーション | ステータス | 作成日 | 実施日
  - row: アイテムを選択する | #IA-1004 | 物流倉庫 | 完了 実施済み | 2026年06月16日 17:44 | 2026年06月16日 17:45
  - row: アイテムを選択する | #IA-1003 | TEST_FAQ_店舗在庫EC販売用 | 完了 実施済み | 2026年06月15日 18:16 | 2026年06月15日 18:16
  - row: アイテムを選択する | #IA-1002 | TEST_FAQ_店舗在庫EC販売用 | 完了 実施済み | 2026年06月15日 18:14 | 2026年06月15日 18:15

## /admin/inventory_adjustment_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- headings: 調整伝票を作成する / ロケーション / 理由 / 商品
- status/alert: 調整伝票を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 参照 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- fields: input:ロケーション required=False disabled=False / select: required=False disabled=False options=['選択してください', '廃棄', '見本', '紛失', '棚卸差異', 'その他'] / input:商品を検索する required=False disabled=False

## /admin/inventory_reservation_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_reservation_orders`
- headings: 取置伝票
- status/alert: 取置伝票。このページの準備が整いました
- tabs: すべて / 未処理 / 処理済み
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 未処理 / 処理済み / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- table1 headers: 伝票番号 | ロケーション | ステータス | 作成日
  - row: #IR-1005 | ユニクロ - 銀座店 | 情報 未完了 未処理 | 2026年06月16日 17:47
  - row: #IR-1004 | ユニクロ - 銀座店 | 情報 未完了 未処理 | 2026年06月16日 17:47
  - row: #IR-1003 | 物流倉庫 | 完了 処理済み | 2026年06月16日 09:20

## /admin/inventory_reservation_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_reservation_orders/create`
- headings: 取置伝票を作成する / 商品
- status/alert: 取置伝票を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 参照 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 移動伝票 -> /admin/inventory_movement_orders / 調整伝票 -> /admin/inventory_adjustment_orders / 取置伝票 -> /admin/inventory_reservation_orders / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules
- fields: input:ロケーション required=False disabled=False / textarea:メモ required=False disabled=False / input:商品を検索する required=False disabled=False

## /admin/orders

- finalUrl: `https://www.sqstackstaging.com/admin/orders`
- headings: 注文管理
- status/alert: 注文管理。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 下書き -> /admin/draft_orders / 返品 -> /admin/order_returns / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/draft_orders

- finalUrl: `https://www.sqstackstaging.com/admin/draft_orders`
- headings: 下書き
- status/alert: 下書き。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 下書き -> /admin/draft_orders / 返品 -> /admin/order_returns / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/order_returns

- finalUrl: `https://www.sqstackstaging.com/admin/order_returns`
- headings: 返品
- status/alert: 返品。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 下書き -> /admin/draft_orders / 返品 -> /admin/order_returns / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/purchasing_customers

- finalUrl: `https://www.sqstackstaging.com/admin/purchasing_customers`
- headings: 顧客管理
- status/alert: 顧客管理。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 会社 -> /admin/companies / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules

## /admin/purchasing_customers/create

- finalUrl: `https://www.sqstackstaging.com/admin/purchasing_customers/create`
- headings: 予期せぬエラーが発生しました
- buttons: stack-ps-yosuke 陽介 河野 / 再実行
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 会社 -> /admin/companies / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules

## /admin/companies

- finalUrl: `https://www.sqstackstaging.com/admin/companies`
- headings: 会社
- status/alert: 会社。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 会社 -> /admin/companies / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 会社 | ロケーション | 総注文数 | 販売合計 | 作成日
  - row: アイテムを選択する | TEST_FAQ_COVERAGE_20260615_809686_会社 | 3箇所のロケーション | 0個の注文 | ¥0 | 2026年06月15日 21:51
  - row: アイテムを選択する | TEST_FAQ_DEEP3_202606080345_会社 | 1箇所のロケーション | 0個の注文 | ¥0 | 2026年06月08日 12:45
  - row: アイテムを選択する | TEST_FAQ_株式会社テスト | 1箇所のロケーション | 0個の注文 | ¥0 | 2026年06月06日 17:39

## /admin/companies/create

- finalUrl: `https://www.sqstackstaging.com/admin/companies/create`
- headings: 会社を作成する / 担当者 / ロケーション / 配送先住所 / 請求先住所
- status/alert: 会社を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 会社 -> /admin/companies / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules
- fields: input:会社名 required=False disabled=False / input:会社ID required=False disabled=False / input:検索 required=False disabled=False / input:ロケーション名 required=False disabled=False / input:ロケーションID required=False disabled=False / input:コード required=False disabled=False / select:国/地域 required=False disabled=False options=['国/地域', 'エチオピア', 'アイルランド', 'マカオ', 'タジキスタン', 'トケラウ', 'オーランド諸島', 'バングラデシュ', '香港', 'ノーフォーク島', 'イエメン', 'アルゼンチン', 'チリ', 'カメルーン', 'ベルギー', 'サン・マルタン', 'ルーマニア', 'タンザニア', 'サモア', '南アフリカ', 'ソロモン諸島', 'シエラレオネ', 'トンガ', 'モロッコ', 'パラグアイ', 'トーゴ', 'イギリス領インド洋地域', 'リビア', 'レユニオン', 'ジンバブエ', 'ブルガリア', 'オランダ領カリブ', 'ジョージア', 'コモロ', 'ケイマン諸島', 'モナコ', 'ネパール', 'パナマ', 'ジャージー', 'キリバス', 'マレーシア', 'ポルトガル', 'コンゴ共和国', '西サハラ', 'マン島', 'キルギス', 'レソト', 'その他の地域', 'スリナム', '韓国', 'スリランカ', 'ウルグアイ', 'コスタリカ', 'フランス', 'ボリビア', 'カナダ', 'デンマーク', 'ケニア', 'モントセラト', 'メキシコ', 'ロシア', 'セントヘレナ', 'グレナダ', 'インド', 'モンゴル', 'スロベニア', 'ブータン', 'フィジー', '北マケドニア', 'ナイジェリア', 'ソマリア', 'トリニダード・トバゴ', 'コソボ', 'マヨット', '中国', 'ギニア', 'カタール', 'ルワンダ', 'モンテネグロ', 'チャド', 'ベネズエラ', 'ザンビア', 'アフガニスタン', 'イラン', '日本', 'ウガンダ', 'キューバ', 'フィンランド', 'グアドループ', 'ベナン', 'インドネシア', 'イスラエル', 'ニウエ', 'スヴァールバル諸島およびヤンマイエン島', 'サン・バルテルミー', 'イラク', 'マルタ', 'パプアニューギニア', 'アンドラ', 'パレスチナ', 'タイ', 'ウズベキスタン', 'スペイン', 'ホンジュラス', 'スロバキア', 'キプロス', 'チェコ', 'ポーランド', 'ウォリス・フツナ', 'ジブチ', 'ラトビア', 'タークス・カイコス諸島', 'ブルンジ', 'ブラジル', 'イギリス', 'イタリア', 'カザフスタン', 'リベリア', 'シリア', 'ベラルーシ', 'モルドバ', 'セントビンセント・グレナディーン', 'アンギラ', 'オランダ領アンティル', 'マダガスカル', 'ペルー', 'パキスタン', 'ノルウェー', 'フランス領ポリネシア', '東ティモール', 'イギリス領ヴァージン諸島', 'アルメニア', 'エストニア', 'マルティニーク', 'ブルキナファソ', 'ガボン', 'アルバ', '北朝鮮', 'ナウル', 'ニュージーランド', 'オマーン', 'フィリピン', 'シンガポール', 'ガーナ', 'ガンビア', '赤道ギニア', 'バヌアツ', 'グアテマラ', 'ヨルダン', 'マリ', 'マラウイ', 'サンピエール・ミクロン', 'サントメ・プリンシペ', 'エスワティニ', '台湾', 'フェロー諸島', 'ギリシャ', 'ハード島とマクドナルド諸島', 'サウジアラビア', 'ウクライナ', 'ベリーズ', 'スイス', 'リヒテンシュタイン', 'バミューダ', 'クック諸島', 'ブーベ島', 'ジャマイカ', 'クウェート', 'ルクセンブルク', 'モザンビーク', 'クロアチア', 'アイスランド', 'ミャンマー', 'サンマリノ', 'ドミニカ共和国', 'セルビア', 'スウェーデン', 'ボスニア・ヘルツェゴビナ', 'クリスマス島', 'モルディブ', 'セントルシア', 'トルクメニスタン', 'ツバル', '合衆国領有小離島', 'ナミビア', 'アンティグア・バーブーダ', 'オーストラリア', 'アゼルバイジャン', 'バルバドス', 'バハマ', 'コンゴ民主共和国', 'ジブラルタル', 'セントクリストファー・ネイビス', 'アラブ首長国連邦', 'セネガル', 'ブルネイ', 'エクアドル', 'フランス領ギアナ', 'サウスジョージア・サウスサンドウィッチ諸島', 'ニューカレドニア', 'オーストリア', 'シント・マールテン', 'トリスタン・ダ・クーニャ', 'エリトリア', 'カンボジア', 'モーリシャス', 'バチカン市国', 'バーレーン', 'ニジェール', 'セーシェル', 'アルバニア', 'コロンビア', 'ガーンジー', 'ギニアビサウ', 'モーリタニア', 'ピトケアン諸島', 'アメリカ合衆国', 'アンゴラ', 'キュラソー', 'ハイチ', 'ラオス', 'レバノン', 'ボツワナ', 'カーボベルデ', 'ニカラグア', 'アルジェリア', 'グリーンランド', '南スーダン', 'アセンション島', 'ドイツ', 'フォークランド諸島', 'ハンガリー', 'トルコ', 'ココス諸島', '中央アフリカ共和国', 'リトアニア', 'フランス南方・南極地域', 'ベトナム', 'エジプト', 'ガイアナ', 'スーダン', 'エルサルバドル', 'コートジボワール', 'オランダ', 'チュニジア', 'ドミニカ国'] / input:性 required=False disabled=False / input:名 required=False disabled=False / input:会社 required=False disabled=False / input:郵便番号 required=False disabled=False / select:都道府県 required=False disabled=False options=['選択してください', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'] / input:市区町村 required=False disabled=False / input:住所 required=False disabled=False / input:建物名、部屋番号など required=False disabled=False / input:電話番号 required=False disabled=False / input:配送先住所と同じ required=False disabled=False

## /admin/inventory_purchase_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_purchase_orders`
- headings: 発注管理
- status/alert: 発注管理。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/inventory_purchase_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/create`
- headings: 発注伝票を作成 / 取引先 / 商品
- status/alert: 発注伝票を作成。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 参照 / 取り消す / 作成する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: select:取引先 required=False disabled=False options=['選択してください', 'TEST_FAQ_Supplier', 'TEST_FAQ_Supplier2', 'TEST_FAQ_DEEP_202606080340_取引先'] / select:テナント required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / select:通貨 required=False disabled=False options=['米ドル', 'ユーロ', '日本円', 'タイ バーツ', 'シンガポール ドル'] / input:商品を追加する required=False disabled=False

## /admin/product_price_rules

- finalUrl: `https://www.sqstackstaging.com/admin/product_price_rules`
- headings: 販売価格
- status/alert: 販売価格。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | 通貨 | 作成日時
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_販売価格ルール | 日本円 | 2026年06月08日 12:41
  - row: アイテムを選択する | TEST_FAQ_販売価格ルール_遷移確認_20260607 | 日本円 | 2026年06月07日 08:29
  - row: アイテムを選択する | TEST_FAQ_販売価格ルール | 日本円 | 2026年06月05日 19:18

## /admin/product_price_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/product_price_rules/create`
- headings: 販売価格ルールを作成する / 基本設定
- status/alert: 販売価格ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:ルール名 required=False disabled=False / select:通貨 required=False disabled=False options=['通貨を選択してください', '米ドル', 'ユーロ', '日本円', 'タイ バーツ', 'シンガポール ドル']

## /admin/inventory_back_order_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_back_order_rules`
- headings: 予約販売
- status/alert: 予約販売。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前
  - row: アイテムを選択する | TEST_FAQ_予約販売ルール
  - row: アイテムを選択する | TEST_FAQ_予約販売ルール_遷移確認_20260607
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_予約販売ルール

## /admin/inventory_back_order_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_back_order_rules/create`
- headings: 予約販売のルールを作成する
- status/alert: 予約販売のルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:タイトル required=False disabled=False

## /admin/inventory_sale_limit_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_sale_limit_rules`
- headings: 販売上限
- status/alert: 販売上限。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests

## /admin/inventory_sale_limit_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_sale_limit_rules/create`
- headings: 販売上限ルールを作成する
- status/alert: 販売上限ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:販売上限ルール名 required=False disabled=False

## /admin/inventory_threshold_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_threshold_rules`
- headings: 販売閾値
- status/alert: 販売閾値。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_販売閾値ルール
  - row: アイテムを選択する | TEST_FAQ_販売閾値ルール_遷移確認_20260607
  - row: アイテムを選択する | TEST_FAQ_販売閾値ルール

## /admin/inventory_threshold_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_threshold_rules/create`
- headings: 販売閾値ルールを作成する
- status/alert: 販売閾値ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 販売価格 -> /admin/product_price_rules / 予約販売 -> /admin/inventory_back_order_rules / 販売上限 -> /admin/inventory_sale_limit_rules / 販売閾値 -> /admin/inventory_threshold_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests
- fields: input:ルール名 required=False disabled=False / input:デフォルトの閾値を設定する required=False disabled=False

## /admin/sale_change_line_items

- finalUrl: `https://www.sqstackstaging.com/admin/sale_change_line_items`
- headings: 売上実績
- status/alert: 売上実績。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / エクスポート / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 売上実績 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules

## /admin/analytics

- finalUrl: `https://www.sqstackstaging.com/admin/analytics`
- headings: 分析
- status/alert: 分析。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 収益 -> /admin/analytics/revenue / レポート -> /admin/analytics/reports / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/inventory_inbound_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_inbound_orders`
- headings: 入荷管理
- status/alert: 入荷管理。このページの準備が整いました
- tabs: 入荷待ち 1 / 入荷依頼済み 新規 0 / 入荷作業中 新規 0 / 要対応 新規 0 / 入荷完了 / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / 入荷待ち 1 / 入荷依頼済み 新規 0 / 入荷作業中 新規 0 / 要対応 新規 0 / 入荷完了 / キャンセル / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: 管理番号 | 到着ロケーション | 種別 | 作業ステータス | 作成日時
  - row: #II-1004 | ユニクロ - 銀座店 | 移動 | 情報 入荷待ち | 2026年06月12日 08:48

## /admin/inventory_outbound_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_outbound_orders`
- headings: 出荷管理
- status/alert: 出荷管理。このページの準備が整いました
- tabs: 保留中 新規 0 / 出荷待ち 1 / 依頼済み 新規 0 / 作業中 新規 0 / 欠品・要対応 新規 0 / 出荷完了
- buttons: stack-ps-yosuke 陽介 河野 / インポート / 条件指定でエクスポート / 保留中 新規 0 / 出荷待ち 1 / 依頼済み 新規 0 / 作業中 新規 0 / 欠品・要対応 新規 0 / 出荷完了 / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 管理番号 | 作業ステータス | 引当ステータス | 作成元 | 出荷場所 | アイテム | 出荷方法 | 決済種別 | 作成日時
  - row: アイテムを選択する | #IO-1004 | 情報 未完了 出荷待ち | 成功 完了 引当済み | 物流倉庫 | 1個 | 配送 | - | 2026年06月12日 08:48

## /admin/inventory_allocation_requests

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests`
- headings: 在庫依頼
- status/alert: 在庫依頼。このページの準備が整いました
- tabs: 確認待ち / 確保済み / 終了
- buttons: stack-ps-yosuke 陽介 河野 / 確認待ち / 確保済み / 終了 / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / 確保済み -> /admin/inventory_allocation_request_confirmations / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules

## /admin/inventory_allocation_requests/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- headings: 在庫依頼を作成する / 商品 / リクエスト内容
- status/alert: 在庫依頼を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 選択 / 選択 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / 確保済み -> /admin/inventory_allocation_request_confirmations / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules
- fields: input:商品バリエーション required=False disabled=False / input:希望数 required=False disabled=False / input:移動先ロケーション required=False disabled=False / input:リクエスト先ロケーション required=False disabled=False

## /admin/inventory_allocation_request_confirmations

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_request_confirmations`
- headings: 確保済み
- status/alert: 確保済み。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / 移動伝票を作成する / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / 確保済み -> /admin/inventory_allocation_request_confirmations / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules

## /admin/order_price_adjustment_rules

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules`
- headings: ディスカウント
- status/alert: ディスカウント。このページの準備が整いました
- tabs: すべて / 有効 / スケジュール済み / 期限切れ
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 有効 / スケジュール済み / 期限切れ / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | タイトル | クーポンコード | ステータス | 有効期間 | 対象顧客 | 対象店舗 | 利用回数 | テナント
  - row: アイテムを選択する | TEST_FAQ_DEEP3_202606080345_ディスカウント | TEST-FAQ-DEEP3-202606080345-DISC | 成功 有効 | 2026年06月08日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ
  - row: アイテムを選択する | TEST_FAQ_ディスカウント_対象商品テスト | TEST-FAQ-001 | 成功 有効 | 2026年01月01日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ

## /admin/order_price_adjustment_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/create`
- headings: ディスカウントを作成する / 基本情報 / 割引設定 / 適用条件 / 割引要件 / 対象商品
- status/alert: ディスカウントを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:タイトル required=False disabled=False / textarea:説明文 required=False disabled=False / input:クーポンコード required=False disabled=False / select:テナント required=False disabled=False options=['テナントを選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / select:割引方法 required=False disabled=False options=['選択してください', '割引率', '割引額'] / input:割引率 required=False disabled=False / input:割引が適用可能な最高購入額を設定する required=False disabled=False / input:最低購入額 required=False disabled=False / input:1000 required=False disabled=False / input:最低購入数量 required=False disabled=False / input:すべての商品を割引対象に設定する required=False disabled=False / input:お客様1人につき1回のみの使用とする required=False disabled=False / input:開始日時 required=False disabled=False / input:終了日時 required=False disabled=False

## /admin/point_calculation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules`
- headings: 注文ポイント
- status/alert: 注文ポイント。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | ルール | 利用テナント数
  - row: アイテムを選択する | TEST_FAQ_注文ポイント付与ルール | 0件

## /admin/point_calculation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules/create`
- headings: 注文ポイント付与ルールを作成する / ルール / 有効期限 / オンライン注文のポイント有効までの日数 / 店舗注文のポイント有効までの日数 / 会員ランク算出ルール
- status/alert: 注文ポイント付与ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:タイトル required=False disabled=False / input:購入金額 required=False disabled=False / input:ポイント required=False disabled=False / input:ポイントを付与してから有効な日数 required=False disabled=False / input: required=False disabled=False / input: required=False disabled=False / select:会員ランク算出ルール required=False disabled=False options=['選択してください', 'TEST_FAQ_会員ランク算出ルール', 'TEST_FAQ_RANK_20260615081841'] / input:開始日時が新しいキャンペーンを優先する required=False disabled=False / input:開始日時が古いキャンペーンを優先する required=False disabled=False

## /admin/point_campaign_order_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_campaign_order_rules`
- headings: ポイントキャンペーン
- status/alert: ポイントキャンペーン。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | タイトル | 種別 | 注文ポイント付与ルール | 開始日時 | 終了日時 | 作成日時
  - row: アイテムを選択する | TEST_FAQ_DEEP3_202606080345_ポイントCP | なし | TEST_FAQ_注文ポイント付与ルール | 2026年06月08日 00:00 | 2026年12月31日 23:59 | 2026年06月08日 12:46
  - row: アイテムを選択する | TEST_FAQ_ランク別ポイントキャンペーン | 会員ランク | TEST_FAQ_注文ポイント付与ルール | 2026年01月01日 00:00 | 2026年12月31日 23:59 | 2026年06月06日 18:21

## /admin/point_campaign_order_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_campaign_order_rules/create`
- headings: ポイントキャンペーンを作成する
- status/alert: ポイントキャンペーンを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:タイトル required=False disabled=False / input:開始日時 required=False disabled=False / input:終了日時 required=False disabled=False / select:ポイントキャンペーン種別 required=False disabled=False options=['選択してください', 'なし', '会員ランク', '購入金額', '商品']

## /admin/point_calculation_birthday_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_birthday_rules`
- headings: 誕生日ポイント
- status/alert: 誕生日ポイント。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | タイトル
  - row: アイテムを選択する | TEST_FAQ_DEEP2_202606080343_誕生日ポイント

## /admin/point_calculation_birthday_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_birthday_rules/create`
- headings: 誕生日ポイント付与ルールを作成する
- status/alert: 誕生日ポイント付与ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:タイトル required=False disabled=False / input:表示タイトル required=False disabled=False / input:ポイント required=False disabled=False / input:有効期間 required=False disabled=False

## /admin/point_application_excluded_products

- finalUrl: `https://www.sqstackstaging.com/admin/point_application_excluded_products`
- headings: 利用外商品
- status/alert: 利用外商品。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules

## /admin/point_application_excluded_products/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_application_excluded_products/create`
- headings: 利用外商品を追加する
- status/alert: 利用外商品を追加する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:商品を選択する required=False disabled=False

## /admin/point_expiration_notification_rule

- finalUrl: `https://www.sqstackstaging.com/admin/point_expiration_notification_rule`
- headings: 失効通知
- status/alert: 失効通知。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | タイトル | 通知予定日 | 利用テナント数
  - row: アイテムを選択する | TEST_FAQ_DEEP2_202606080343_失効通知 | 30日前 | 0

## /admin/point_expiration_notification_rule/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_expiration_notification_rule/create`
- headings: ポイント失効通知ルールを作成する
- status/alert: ポイント失効通知ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / キャンペーン -> /admin/point_campaign_order_rules / 誕生日 -> /admin/point_calculation_birthday_rules
- fields: input:タイトル required=False disabled=False / input:通知予定日 required=False disabled=False

## /admin/customer_rank_calculation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules`
- headings: 会員ランク
- status/alert: 会員ランク。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | ルール | 利用テナント数
  - row: アイテムを選択する | TEST_FAQ_会員ランク算出ルール | 0件
  - row: アイテムを選択する | TEST_FAQ_RANK_20260615081841 | 0件

## /admin/customer_rank_calculation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules/create`
- headings: 会員ランク算出ルールを作成する / ルール / 算出期間 / 詳細
- status/alert: 会員ランク算出ルールを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:タイトル required=False disabled=False / input:購入金額 required=False disabled=True / input:獲得ポイント required=False disabled=True / input:税抜き価格でランクを算出する required=False disabled=False / select:期間 required=False disabled=False options=['1年間', '直近365日', '無期限'] / select:開始月 required=False disabled=False options=['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'] / input:会員ランクを月初に算出する required=False disabled=False / input:会員ランクを次の算出期間に持ち越す required=False disabled=False

## /admin/shopify_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/shopify_integrations`
- headings: Shopify
- status/alert: Shopify。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/shopify_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/shopify_integrations/create`
- headings: ストアを連携する
- status/alert: ストアを連携する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 連携する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:ストア名 required=False disabled=False / input:ショップドメイン required=False disabled=False / select:テナント required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / select:カタログ required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO'] / select:ロケーショングループ required=False disabled=False options=['選択してください', 'TEST_FAQ_ロケーショングループ', 'TEST_FAQ_COVERAGE_20260615_403698_ロケーショングループ'] / select:販売価格ルール required=False disabled=False options=['選択してください', 'TEST_FAQ_販売価格ルール', 'TEST_FAQ_販売価格ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_販売価格ルール'] / select:会員証バーコードのフォーマット required=False disabled=False options=['Shopify ID（数値部分）', 'JAN-13コード（モジュラス10/ウェイト3方式）'] / input:商品価格は税込価格を連携する required=False disabled=False / input:0円の商品バリエーションを連携する required=False disabled=False / input:送料は税込として処理する required=False disabled=False / input:注文による在庫変動を起こさない required=False disabled=False

## /admin/omnibus_core_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations`
- headings: OmnibusCore
- status/alert: OmnibusCore。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: メーカーコード | テナント | カタログ | ロケーショングループ | 連携日時
  - row: TEST_MAKER_001 | ユニクロ | - | - | 2026年06月06日 18:46

## /admin/omnibus_core_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/create`
- headings: OmnibusCore連携を作成する / 商品同期設定 / 在庫設定 / 注文設定
- status/alert: OmnibusCore連携を作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / オプションを追加 / オプションを追加 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: select:テナント required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / input:メーカーコード required=False disabled=False / select:カタログ required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO'] / input:カラーオプション名 required=False disabled=False / input:サイズオプション名 required=False disabled=False / select:ロケーショングループ required=False disabled=False options=['選択してください', 'TEST_FAQ_ロケーショングループ', 'TEST_FAQ_COVERAGE_20260615_403698_ロケーショングループ'] / select:在庫予約ルール required=False disabled=False options=['選択してください', 'TEST_FAQ_予約販売ルール', 'TEST_FAQ_予約販売ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_予約販売ルール'] / select:販売上限ルール required=False disabled=False options=['選択してください'] / input:下書き注文の有効期限日数 required=False disabled=False

## /admin/smaregi_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/smaregi_integrations`
- headings: スマレジ連携
- status/alert: スマレジ連携。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/smaregi_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/smaregi_integrations/create`
- headings: スマレジ連携を作成する / 基本情報 / 商品連携設定 / 在庫設定 / 取引連携設定
- status/alert: スマレジ連携を作成する。このページの準備が整いました / スマレジ連携を利用するには、スマレジにアプリをインストールする必要があります。
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:名前 required=False disabled=False / select:テナント required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / input:契約ID required=False disabled=False / select:プラン required=False disabled=False options=['スタンダード', 'プレミアム', 'プレミアムプラス', 'フードビジネス', 'リテールビジネス'] / select:カタログ required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO'] / select:在庫同期の方向 required=False disabled=False options=['スマレジからSQへ在庫を同期する', 'SQからスマレジへ在庫を同期する', '在庫を同期しない'] / input:注文による在庫変動を起こさない required=False disabled=False / input:取引の連携を有効にする required=False disabled=False

## /admin/retail_portal_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations`
- headings: リテールポータル
- status/alert: リテールポータル。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:場所コードを入力してください required=False disabled=False / input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 店舗
  - row: アイテムを選択する | ユニクロ - 銀座店

## /admin/retail_portal_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations/create`
- headings: リテールポータル
- status/alert: リテールポータル。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 選択 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:店舗ロケーション required=False disabled=False / input:在庫ロケーション required=False disabled=False / select:テナント required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT'] / select:カタログ required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO'] / select:販売閾値ルール required=False disabled=False options=['選択してください', 'TEST_FAQ_販売閾値ルール', 'TEST_FAQ_販売閾値ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_販売閾値ルール'] / input:リテールポータルで販売員の選択を必須にする required=False disabled=False / input:配送先住所の編集を許可する required=False disabled=False / input:下書き注文の送料明細の編集を許可する required=False disabled=False / input:下書き注文の注文明細の価格の編集を許可する required=False disabled=False / input:下書き注文の完了を許可する required=False disabled=False

## /admin/b2b

- finalUrl: `https://www.sqstackstaging.com/admin/b2b`
- headings: 卸売
- status/alert: 卸売。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings

- finalUrl: `https://www.sqstackstaging.com/admin/settings`
- headings: 設定 / 組織ID / データ管理 / テンプレート / 通知 / 外部連携
- status/alert: 設定。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input: required=False disabled=False

## /admin/csv_import

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import`
- headings: CSVインポート / 商品 / 商品 / 商品バリエーション / 商品画像 / 商品バリエーション画像
- status/alert: CSVインポート。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/csv_export

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export`
- headings: CSVエクスポート / マスターデータ / 在庫 / ロケーション / ディスカウントの利用履歴 / 商品バリエーション
- status/alert: CSVエクスポート。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/pdf_export

- finalUrl: `https://www.sqstackstaging.com/admin/pdf_export`
- headings: PDFエクスポート / 納品書
- status/alert: PDFエクスポート。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/analytics/reports

- finalUrl: `https://www.sqstackstaging.com/admin/analytics/reports`
- headings: レポート
- status/alert: レポート。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 収益 -> /admin/analytics/revenue / レポート -> /admin/analytics/reports / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/analytics/revenue

- finalUrl: `https://www.sqstackstaging.com/admin/analytics/revenue`
- headings: 売上
- status/alert: 売上。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 収益 -> /admin/analytics/revenue / レポート -> /admin/analytics/reports / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules

## /admin/catalogs/create

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/create`
- headings: カタログを作成する
- status/alert: カタログを作成する。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / カタログ -> /admin/catalogs / 店舗受取 -> /admin/local_pickup_product_variants / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules
- fields: input:タイトル required=False disabled=False

## /admin/csv_export/csv_export_operation_inventory_logical_quantities

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_logical_quantities`
- headings: 在庫をCSVでエクスポートする
- status/alert: 在庫をCSVでエクスポートする。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities`
- headings: 販売可能在庫をCSVでインポートする
- status/alert: 販売可能在庫をCSVでインポートする。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: 作成日 | 実行ステータス
  - row: 2026年06月15日 | 成功 完了 完了
  - row: 2026年06月15日 | 成功 完了 完了

## /admin/local_pickup_retail_location_rules

- finalUrl: `https://www.sqstackstaging.com/admin/local_pickup_retail_location_rules`
- headings: 店舗受取
- status/alert: 店舗受取。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/logizard_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/logizard_integrations`
- headings: ロジザード連携
- status/alert: ロジザード連携。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/recustomer_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/recustomer_integrations`
- headings: Recustomer
- status/alert: Recustomer。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings/apps

- finalUrl: `https://www.sqstackstaging.com/admin/settings/apps`
- headings: アプリ
- status/alert: アプリ。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings/brands

- finalUrl: `https://www.sqstackstaging.com/admin/settings/brands`
- headings: ブランド
- status/alert: ブランド。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | コード | 外部ID | 更新日時
  - row: アイテムを選択する | TEST_FAQ_ブランドGAP | TEST_FAQ_GAP_B | TEST_FAQ_GAP_001 | 2026年06月06日
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_ブランド | test_faq_deep_202606080340_brand | 2026年06月08日
  - row: アイテムを選択する | UNIQLO | 1234543 | 2026年06月16日

## /admin/settings/location_groups

- finalUrl: `https://www.sqstackstaging.com/admin/settings/location_groups`
- headings: ロケーショングループ
- status/alert: ロケーショングループ。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 前へ / 次へ / ロケーショングループ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: グループ名 | デフォルト | ロケーション
  - row: TEST_FAQ_COVERAGE_20260615_403698_ロケーショングループ | TEST_FAQ_COVERAGE_20260615_403698_ロケーション | 1個のロケーション
  - row: TEST_FAQ_ロケーショングループ | 物流倉庫 | 4個のロケーション

## /admin/settings/locations

- finalUrl: `https://www.sqstackstaging.com/admin/settings/locations`
- headings: ロケーション
- status/alert: ロケーション。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: 名前 | コード | 場所種別 | 公開 | アーカイブ | ロケーショングループ | タグ
  - row: TEST_FAQ_COVERAGE_20260615_403698_ロケーション | TFCLOC3698 | 倉庫 | 情報 非公開 | 1個のグループ
  - row: TEST_FAQ_DEEP2_202606080343_ロケーション | test_faq_deep2_202606080343_loc | 情報 店舗 | 成功 公開中 | 0個のグループ
  - row: TEST_FAQ_店舗在庫EC販売用 | TESTEC01 | 情報 店舗 | 成功 公開中 | 1個のグループ

## /admin/settings/metafield_definitions

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions`
- headings: メタフィールド定義 / 組織 / 商品 / バリエーション / 顧客 / 注文
- status/alert: メタフィールド定義。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings/organization_notification_emails

- finalUrl: `https://www.sqstackstaging.com/admin/settings/organization_notification_emails`
- headings: 通知用メールアドレス
- status/alert: 通知用メールアドレス。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings/payment_methods

- finalUrl: `https://www.sqstackstaging.com/admin/settings/payment_methods`
- headings: 決済方法
- status/alert: 決済方法。このページの準備が整いました
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / その他のビュー / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | コード | ゲートウェイ
  - row: アイテムを選択する | TEST_FAQ_決済 | test_faq_payment | test_gateway
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_決済 | test_faq_deep_202606080340_payment | test_faq_deep_202606080340_gateway

## /admin/settings/pdf_template_package_slip

- finalUrl: `https://www.sqstackstaging.com/admin/settings/pdf_template_package_slip`
- headings: PDF納品書テンプレート
- status/alert: PDF納品書テンプレート。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: textarea:HTMLテンプレート required=False disabled=False

## /admin/settings/product_measurement_rules

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules`
- headings: 採寸ルール
- status/alert: 採寸ルール。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: ルール名 | 単位 | 採寸項目
  - row: TEST_FAQ_COVERAGE_20260615_159330_採寸 | センチメートル | 肩幅
  - row: TEST_FAQ_DEEP_202606080340_採寸ルール | センチメートル | 肩幅
  - row: TEST_FAQ_採寸ルール_トップス | センチメートル | 肩幅

## /admin/settings/retail_staff_members

- finalUrl: `https://www.sqstackstaging.com/admin/settings/retail_staff_members`
- headings: 販売員
- status/alert: 販売員。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:販売員コードで検索する required=False disabled=False / input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | 販売員コード | 外部ID
  - row: アイテムを選択する | 銀座ユニクロ | 123
  - row: アイテムを選択する | TEST_APPCHECK販売員 | APPCHK-20260616212742

## /admin/settings/suppliers

- finalUrl: `https://www.sqstackstaging.com/admin/settings/suppliers`
- headings: 取引先
- status/alert: 取引先。このページの準備が整いました
- tabs: すべて / アーカイブ
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / アーカイブ / その他のビュー / 検索と絞り込みの結果 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:すべてのアイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False / input:アイテムを選択する required=False disabled=False
- table1 headers: すべてのアイテムを選択する | 名前 | コード
  - row: アイテムを選択する | TEST_FAQ_DEEP_202606080340_取引先 | 0dabc6a0-93aa-5f3e-8044-7c4daa44d9f4_InventorySupplier
  - row: アイテムを選択する | TEST_FAQ_Supplier2 | 4fc9262b-9c99-5d50-a4dd-613cc724e014_InventorySupplier
  - row: アイテムを選択する | TEST_FAQ_Supplier | e7233b1a-c53d-56e4-b8c6-b1c7a32b8f15_InventorySupplier

## /admin/settings/tenants

- finalUrl: `https://www.sqstackstaging.com/admin/settings/tenants`
- headings: テナント
- status/alert: テナント。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- table1 headers: 名前
  - row: TEST_FAQ_COVERAGE_20260615_テナント_EDIT
  - row: ユニクロ

## /admin/settings/translation

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation`
- headings: 翻訳 / 未選択：翻訳ルールを選択するとリソースを選択できます / 商品
- status/alert: 翻訳。このページの準備が整いました / 未選択：翻訳ルールを選択するとリソースを選択できます
- buttons: stack-ps-yosuke 陽介 河野 / 選択してください
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations

## /admin/settings/users

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users`
- headings: 管理メンバー
- status/alert: 管理メンバー。このページの準備が整いました
- buttons: stack-ps-yosuke 陽介 河野 / 絞り込みを追加 / 前へ / 次へ
- admin links: (no text) -> /admin / (no text) -> /admin / ホーム -> /admin / 商品管理 -> /admin/products / 在庫管理 -> /admin/inventory_items / 注文管理 -> /admin/orders / 顧客管理 -> /admin/purchasing_customers / 発注管理 -> /admin/inventory_purchase_orders / 販売設定 -> /admin/product_price_rules / 会計 -> /admin/sale_change_line_items / 分析 -> /admin/analytics / 入荷管理 未完了の入荷指示 1件 1 -> /admin/inventory_inbound_orders / 出荷管理 未完了の出荷指示 1件 1 -> /admin/inventory_outbound_orders / 在庫依頼 -> /admin/inventory_allocation_requests / ディスカウント -> /admin/order_price_adjustment_rules / ポイント -> /admin/point_calculation_rules / 会員ランク -> /admin/customer_rank_calculation_rules / Shopify -> /admin/shopify_integrations
- fields: input:キーワードで検索する required=False disabled=False
- table1 headers: 名前 | メールアドレス | 権限グループ
  - row: サポートアカウントStack | erp.delivery.admin@stack.inc | 特権管理者
  - row: 福田涼介 | yz@stack.inc | 特権管理者
  - row: 菅野将貴 | sugano@stack.inc | 特権管理者
