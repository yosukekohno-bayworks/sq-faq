# SQ実機 全ページ項目・選択肢スキャン

- 実行日: 2026-06-21
- 対象: staging `https://www.sqstackstaging.com/admin`
- 方法: ログイン済みブラウザで各URLを開き、表示DOMから項目・ボタン・タブ・テーブル・安全に開ける選択UIを抽出
- 注意: 保存・削除・実行・登録など状態変更ボタンは押していません

## /admin

- finalUrl: `https://www.sqstackstaging.com/admin`
- headings: stack-ps-yosuke / 商品管理 / 在庫管理 / 注文管理 / 顧客管理 / CSVでデータをインポートする / CSVでデータをエクスポートする / PDFでデータをエクスポートする
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/products

- finalUrl: `https://www.sqstackstaging.com/admin/products`
- headings: 商品管理
- tabs: すべて / 公開中 / 下書き / アーカイブ済み
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / 公開中 / 下書き / アーカイブ済み / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / インポート
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / インポート
- table1: すべてのアイテムを選択する | 商品 | ステータス | 商品コード | 在庫 | カタログ | 商品タイプ | 製造元
  - アイテムを選択する | product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 | 情報 下書き | TEST_FAQ_20260624_GU_092214 | 1個のバリエーション | 0 | Tシャツ | GU
  - アイテムを選択する | product thumbnail TEST_20260622_OPTION | 情報 下書き | TEST_20260622_OPTION | 0個のバリエーション | 0
  - アイテムを選択する | product thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 | アーカイブ済み | TEST_E2E_20260622_GU_1905 | 1個のバリエーション | 0 | Tシャツ | GU

## /admin/products/create

- finalUrl: `https://www.sqstackstaging.com/admin/products/create`
- headings: 商品を作成する / メディア / バリエーション / 検索エンジンリスティング / ステータス / 商品分類 / タグ
- buttons: stack-ps-yosuke 陽介 河野 / 追加 / 削除 (disabled) / 別のオプションを追加する / 選択 / 保存する
- fields:
  - input:text `商品コード` required=False disabled=False
  - input:text `商品名` required=False disabled=False
  - textarea:text `説明文` required=False disabled=False
  - input:file `画像をアップロード` required=False disabled=False
  - input:text `オプション名` required=False disabled=False
  - select:select-one `種別` required=False disabled=False options=['選択してください', 'サイズ', 'カラー', 'その他']
  - input:text `オプション値` required=False disabled=False
  - input:text `コード` required=False disabled=False
  - input:text `ページタイトル` required=False disabled=False
  - textarea:text `メタディスクリプション` required=False disabled=False
  - select:select-one `下書き` required=False disabled=False options=['下書き', '公開', '非公開']
  - input:text `商品タイプ` required=False disabled=False
  - input:text `製造元` required=False disabled=False
  - input:text `ブランド` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ブランド`: stack-ps-yosuke 陽介 河野

## /admin/catalogs

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs`
- headings: カタログ
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 検索結果を並べ替える / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `検索結果を並べ替える`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 商品 | 販売先
  - アイテムを選択する | TEST_FAQ_カタログ001 | 1個の商品 | 0つの販売先
  - アイテムを選択する | UNIQLO | 5個の商品 | 0つの販売先
  - アイテムを選択する | TEST_FAQ_20260624_カタログ_092214 | 0個の商品 | 0つの販売先

## /admin/catalogs/create

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/create`
- headings: カタログを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/local_pickup_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/local_pickup_product_variants`
- headings: 店舗受取
- buttons: stack-ps-yosuke 陽介 河野 / バリエーションを追加する / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
  - アイテムを選択する | オーバーサイズスウェットシャツ BLACK / XL | 486125 | 486125-09-XL
  - アイテムを選択する | オーバーサイズスウェットシャツ BLACK / L | 486125 | 486125-09-L
  - アイテムを選択する | オーバーサイズスウェットシャツ GRAY / L | 486125 | 486125-03-L

## /admin/local_pickup_retail_location_rules

- finalUrl: `https://www.sqstackstaging.com/admin/local_pickup_retail_location_rules`
- headings: 店舗受取
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/local_pickup_retail_location_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/local_pickup_retail_location_rules/create`
- headings: 店舗受取を作成する
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/inventory_items

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items`
- headings: 在庫管理 :
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / ユニクロ物流倉庫 / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 商品 | 品番(SKU) | 販売可能 | 引当済み | 取置中 | 手持ち
  - アイテムを選択する | product variant thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M | TEST_FAQ_20260624_GU_092214_NAVY_M | 0 | 0 | 0 | 0
  - アイテムを選択する | product variant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 NAVY / M | TEST_E2E_20260622_GU_1905_NAVY_M | 0 | 0 | 0 | 0
  - アイテムを選択する | product variant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1845 NAVY / M | TEST_E2E_20260622_GU_1845_NAVY_M | 0 | 0 | 0 | 0

## /admin/inventory_movement_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders`
- headings: 移動伝票
- tabs: すべて / 出荷作業 / 一部受領済み / 受領済み / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 出荷作業 (disabled) / 一部受領済み (disabled) / 受領済み (disabled) / キャンセル / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 管理番号 | 配送元 | 配送先 | ステータス | 作成日時
  - #IM-1024 | TEST_FAQ_20260624_GU倉庫_ON_092214 | TEST_FAQ_20260624_GU店舗_OFF_092214 | 成功 完了 入荷完了 | 2026年06月24日 09:49
  - #IM-1023 | TEST_E2E_20260622_GU倉庫_ON_1905 | TEST_E2E_20260622_GU店舗_OFF_1905 | 成功 完了 入荷完了 | 2026年06月22日 08:41
  - #IM-1022 | ユニクロ物流倉庫 | ユニクロ - 銀座店 | 成功 完了 入荷完了 | 2026年06月21日 14:03

## /admin/inventory_movement_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- headings: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 参照 (disabled) / 保存する
- fields:
  - input:text `配送元` required=False disabled=False
  - input:text `配送先` required=False disabled=False
  - input:text `商品を追加する` required=False disabled=True
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `配送元`: stack-ps-yosuke 陽介 河野
  - `配送先`: stack-ps-yosuke 陽介 河野

## /admin/inventory_adjustment_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders`
- headings: 調整伝票
- tabs: すべて / 未実施 / 実施済み / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 未実施 / 実施済み / キャンセル / 検索と絞り込みの結果 / 検索結果を並べ替える / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `検索結果を並べ替える`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 管理番号 | ロケーション | ステータス | 作成日 | 実施日
  - アイテムを選択する | #IA-1012 | TEST_FAQ_20260624_GU倉庫_ON_092214 | 完了 実施済み | 2026年06月24日 09:46 | 2026年06月24日 09:47
  - アイテムを選択する | #IA-1011 | TEST_E2E_20260622_GU倉庫_ON_1905 | 完了 実施済み | 2026年06月22日 09:14 | 2026年06月22日 09:15
  - アイテムを選択する | #IA-1010 | TEST_E2E_20260622_GU倉庫_ON_1905 | 完了 実施済み | 2026年06月22日 08:37 | 2026年06月22日 08:37

## /admin/inventory_adjustment_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- headings: 調整伝票を作成する / ロケーション / 理由 / 商品
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 参照 / 保存する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - select:select-one `選択してください` required=False disabled=False options=['選択してください', '廃棄', '見本', '紛失', '棚卸差異', 'その他']
  - input:text `商品を検索する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野
  - `商品を検索する`: stack-ps-yosuke 陽介 河野

## /admin/inventory_reservation_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_reservation_orders`
- headings: 取置伝票
- tabs: すべて / 未処理 / 処理済み
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 未処理 / 処理済み / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 伝票番号 | ロケーション | ステータス | 作成日
  - #IR-1008 | ユニクロ - 銀座店 | 情報 未完了 未処理 | 2026年06月21日 12:13
  - #IR-1007 | ユニクロ物流倉庫 | 完了 処理済み | 2026年06月18日 22:34
  - #IR-1006 | ユニクロ物流倉庫 | 完了 処理済み | 2026年06月16日 23:01

## /admin/inventory_reservation_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_reservation_orders/create`
- headings: 取置伝票を作成する / 商品
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 参照 / 保存する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - textarea:text `メモ` required=False disabled=False
  - input:text `商品を検索する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野
  - `商品を検索する`: stack-ps-yosuke 陽介 河野

## /admin/orders

- finalUrl: `https://www.sqstackstaging.com/admin/orders`
- headings: 注文管理
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/draft_orders

- finalUrl: `https://www.sqstackstaging.com/admin/draft_orders`
- headings: 下書き
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/draft_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/draft_orders/create`
- headings: 予期せぬエラーが発生しました
- status: 予期せぬエラー
- buttons: stack-ps-yosuke 陽介 河野 / 再実行
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/order_returns

- finalUrl: `https://www.sqstackstaging.com/admin/order_returns`
- headings: 返品
- buttons: stack-ps-yosuke 陽介 河野 / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/order_returns/create

- finalUrl: `https://www.sqstackstaging.com/admin/order_returns/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/purchasing_customers

- finalUrl: `https://www.sqstackstaging.com/admin/purchasing_customers`
- headings: 顧客管理
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / インポート
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / インポート

## /admin/purchasing_customers/create

- finalUrl: `https://www.sqstackstaging.com/admin/purchasing_customers/create`
- headings: 予期せぬエラーが発生しました
- status: 予期せぬエラー
- buttons: stack-ps-yosuke 陽介 河野 / 再実行
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/companies

- finalUrl: `https://www.sqstackstaging.com/admin/companies`
- headings: 会社
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 会社 | ロケーション | 総注文数 | 販売合計 | 作成日
  - アイテムを選択する | TEST_FAQ_COVERAGE_20260615_809686_会社 | 3箇所のロケーション | 0個の注文 | ¥0 | 2026年06月15日 21:51
  - アイテムを選択する | TEST_FAQ_DEEP3_202606080345_会社 | 1箇所のロケーション | 0個の注文 | ¥0 | 2026年06月08日 12:45
  - アイテムを選択する | TEST_FAQ_株式会社テスト | 1箇所のロケーション | 0個の注文 | ¥0 | 2026年06月06日 17:39

## /admin/companies/create

- finalUrl: `https://www.sqstackstaging.com/admin/companies/create`
- headings: 会社を作成する / 担当者 / ロケーション / 配送先住所 / 請求先住所
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `会社名` required=False disabled=False
  - input:text `会社ID` required=False disabled=False
  - input:text `検索` required=False disabled=False
  - input:text `ロケーション名` required=False disabled=False
  - input:text `ロケーションID` required=False disabled=False
  - input:text `コード` required=False disabled=False
  - select:select-one `国/地域` required=False disabled=False options=['国/地域', 'ブルキナファソ', 'アルジェリア', 'モザンビーク', 'チュニジア', 'モーリタニア', 'パキスタン', '東ティモール', 'ウガンダ', 'フィンランド', 'ジョージア', 'ギニアビサウ', 'オーストラリア', 'カザフスタン', 'ニジェール', 'チャド', 'ボスニア・ヘルツェゴビナ', 'イラン', 'ソロモン諸島', 'エリトリア', 'イタリア', 'モンテネグロ', 'トンガ', 'アルメニア', 'コロンビア', 'スペイン', 'サン・マルタン', 'ニューカレドニア', 'キプロス', 'ガボン', 'ヨルダン', '北朝鮮', 'ポルトガル', 'ブルンジ', 'ミャンマー', 'ネパール', 'バハマ', 'フェロー諸島', 'グアドループ', 'カンボジア', 'ナウル', 'トーゴ', 'アンゴラ', 'アイスランド', 'トルコ', 'スイス', 'サウジアラビア', 'トルクメニスタン', 'イエメン', 'グレナダ', 'ジャマイカ', 'マルティニーク', 'ザンビア', 'アルバニア', '北マケドニア', 'ノーフォーク島', 'サントメ・プリンシペ', '南アフリカ', 'バミューダ', 'イギリス領インド洋地域', 'パプアニューギニア', 'グリーンランド', 'ノルウェー', 'ペルー', 'ルーマニア', 'タンザニア', 'キルギス', 'ラトビア', 'モロッコ', 'イラク', 'ポーランド', '合衆国領有小離島', 'ウルグアイ', 'セントビンセント・グレナディーン', 'ガーンジー', 'クロアチア', 'リビア', 'アメリカ合衆国', 'アゼルバイジャン', 'ケニア', 'ナミビア', 'コスタリカ', 'グアテマラ', 'ケイマン諸島', 'マダガスカル', 'ボツワナ', 'ジブチ', 'ガンビア', 'コモロ', 'スーダン', 'シリア', 'ベネズエラ', 'イギリス領ヴァージン諸島', 'カーボベルデ', 'チェコ', 'クウェート', 'タイ', 'トケラウ', 'コンゴ民主共和国', 'クリスマス島', 'デンマーク', 'セントルシア', 'ピトケアン諸島', 'エスワティニ', 'ブルガリア', 'スロベニア', 'フィジー', 'トリスタン・ダ・クーニャ', 'アンティグア・バーブーダ', 'アルゼンチン', 'ジブラルタル', 'ギニア', '香港', 'ホンジュラス', 'セネガル', 'アフガニスタン', '赤道ギニア', 'アンギラ', 'バルバドス', 'コートジボワール', 'シエラレオネ', 'バングラデシュ', 'マカオ', 'フィリピン', 'チリ', 'インド', 'レバノン', 'モンゴル', 'モルディブ', 'トリニダード・トバゴ', 'フランス', 'シンガポール', 'スロバキア', 'タジキスタン', 'ウズベキスタン', 'バヌアツ', 'マヨット', 'ベナン', 'モルドバ', 'ソマリア', '中国', 'エジプト', 'ニカラグア', 'カタール', 'カメルーン', 'ハンガリー', 'マリ', 'マレーシア', 'パラグアイ', 'スウェーデン', 'オランダ領アンティル', 'オランダ領カリブ', 'ココス諸島', 'イギリス', 'バチカン市国', 'サモア', 'ブラジル', 'ジャージー', 'マラウイ', 'パナマ', 'ルワンダ', 'キュラソー', 'リトアニア', 'ベトナム', 'オランダ', 'スリナム', 'モーリシャス', 'エクアドル', 'マン島', 'ラオス', 'リヒテンシュタイン', 'スヴァールバル諸島およびヤンマイエン島', 'ウォリス・フツナ', 'ベルギー', '西サハラ', 'セントクリストファー・ネイビス', 'サンピエール・ミクロン', 'セルビア', 'アラブ首長国連邦', 'バーレーン', 'ハイチ', 'ルクセンブルク', 'ニュージーランド', 'シント・マールテン', 'コソボ', 'パレスチナ', 'その他の地域', 'オーランド諸島', 'サン・バルテルミー', 'キューバ', 'フォークランド諸島', 'ギリシャ', '日本', 'セントヘレナ', 'ナイジェリア', 'タークス・カイコス諸島', '台湾', 'エルサルバドル', 'アンドラ', 'アルバ', 'コンゴ共和国', 'エチオピア', '韓国', 'セーシェル', 'サンマリノ', 'ウクライナ', 'アセンション島', 'クック諸島', 'キリバス', '中央アフリカ共和国', 'ドミニカ国', 'リベリア', 'ブルネイ', 'ボリビア', 'ブータン', 'ロシア', 'ドミニカ共和国', 'モナコ', 'モントセラト', 'マルタ', 'オーストリア', 'ブーベ島', 'ベラルーシ', 'メキシコ', 'フランス領ポリネシア', '南スーダン', 'ツバル', 'フランス領ギアナ', 'イスラエル', 'スリランカ', 'レソト', 'レユニオン', 'アイルランド', 'ジンバブエ', 'エストニア', 'サウスジョージア・サウスサンドウィッチ諸島', 'ガイアナ', 'ハード島とマクドナルド諸島', 'ベリーズ', 'フランス南方・南極地域', 'カナダ', 'ドイツ', 'ガーナ', 'インドネシア', 'ニウエ', 'オマーン']
  - input:text `性` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:text `会社` required=False disabled=False
  - input:text `郵便番号` required=False disabled=False
  - select:select-one `都道府県` required=False disabled=False options=['選択してください', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
  - input:text `市区町村` required=False disabled=False
  - input:text `住所` required=False disabled=False
  - input:text `建物名、部屋番号など` required=False disabled=False
  - input:tel `電話番号` required=False disabled=False
  - input:checkbox `配送先住所と同じ` required=False disabled=False checked=True
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `検索`: stack-ps-yosuke 陽介 河野

## /admin/inventory_purchase_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_purchase_orders`
- headings: 発注管理
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 管理番号 | 取引先 | ステータス | 合計金額 | 発注日 | 作成日
  - #IP-1004 | TEST_FAQ_Supplier | 情報 発注済み | ￥118,800 | 2026年06月21日 | 2026年06月21日
  - #IP-1003 | TEST_FAQ_Supplier | キャンセル済み | ￥110 | 2026年06月19日 | 2026年06月19日
  - #IP-1002 | TEST_FAQ_Supplier | 情報 発注済み | ￥24,750 | 2026年06月19日 | 2026年06月19日

## /admin/inventory_purchase_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/create`
- headings: 発注伝票を作成 / 取引先 / 商品
- buttons: stack-ps-yosuke 陽介 河野 / 参照 / 取り消す / 作成する
- fields:
  - select:select-one `取引先` required=False disabled=False options=['選択してください', 'TEST_FAQ_Supplier', 'TEST_FAQ_Supplier2', 'TEST_FAQ_DEEP_202606080340_取引先', 'TEST_E2E_20260622_取引先_1740', 'TEST_E2E_20260622_取引先_1755', 'TEST_E2E_20260622_取引先_1830', 'TEST_E2E_20260622_取引先_1845', 'TEST_E2E_20260622_取引先_1905', 'TEST_FAQ_20260624_取引先_092214']
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `通貨` required=False disabled=False options=['米ドル', 'ユーロ', '日本円', 'タイ バーツ', 'シンガポール ドル']
  - input:text `商品を追加する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/product_price_rules

- finalUrl: `https://www.sqstackstaging.com/admin/product_price_rules`
- headings: 販売価格
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 通貨 | 作成日時
  - アイテムを選択する | TEST_FAQ_DEEP_202606080340_販売価格ルール | 日本円 | 2026年06月08日 12:41
  - アイテムを選択する | TEST_FAQ_販売価格ルール_遷移確認_20260607 | 日本円 | 2026年06月07日 08:29
  - アイテムを選択する | TEST_FAQ_販売価格ルール | 日本円 | 2026年06月05日 19:18

## /admin/product_price_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/product_price_rules/create`
- headings: 販売価格ルールを作成する / 基本設定
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `ルール名` required=False disabled=False
  - select:select-one `通貨` required=False disabled=False options=['通貨を選択してください', '米ドル', 'ユーロ', '日本円', 'タイ バーツ', 'シンガポール ドル']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_back_order_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_back_order_rules`
- headings: 予約販売
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前
  - アイテムを選択する | TEST_FAQ_予約販売ルール
  - アイテムを選択する | TEST_FAQ_予約販売ルール_遷移確認_20260607
  - アイテムを選択する | TEST_FAQ_DEEP_202606080340_予約販売ルール

## /admin/inventory_back_order_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_back_order_rules/create`
- headings: 予約販売のルールを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_sale_limit_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_sale_limit_rules`
- headings: 販売上限
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_sale_limit_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_sale_limit_rules/create`
- headings: 販売上限ルールを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `販売上限ルール名` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_threshold_rules

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_threshold_rules`
- headings: 販売閾値
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前
  - アイテムを選択する | TEST_FAQ_DEEP_202606080340_販売閾値ルール
  - アイテムを選択する | TEST_FAQ_販売閾値ルール_遷移確認_20260607
  - アイテムを選択する | TEST_FAQ_販売閾値ルール

## /admin/inventory_threshold_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_threshold_rules/create`
- headings: 販売閾値ルールを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `ルール名` required=False disabled=False
  - input:checkbox `デフォルトの閾値を設定する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/sale_change_line_items

- finalUrl: `https://www.sqstackstaging.com/admin/sale_change_line_items`
- headings: 売上実績
- buttons: stack-ps-yosuke 陽介 河野 / エクスポート / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / エクスポート
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / エクスポート

## /admin/sale_change_line_items/create

- finalUrl: `https://www.sqstackstaging.com/admin/sale_change_line_items/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/analytics

- finalUrl: `https://www.sqstackstaging.com/admin/analytics`
- headings: 分析
- status: TODO表示あり
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/analytics/revenue

- finalUrl: `https://www.sqstackstaging.com/admin/analytics/revenue`
- headings: 売上
- status: TODO表示あり
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/analytics/reports

- finalUrl: `https://www.sqstackstaging.com/admin/analytics/reports`
- headings: レポート
- status: TODO表示あり
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_inbound_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_inbound_orders`
- headings: 入荷管理
- tabs: 入荷待ち 0 / 入荷依頼済み 新規 0 / 入荷作業中 新規 0 / 要対応 新規 0 / 入荷完了 / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / 入荷待ち 0 / 入荷依頼済み 新規 0 / 入荷作業中 新規 0 / 要対応 新規 0 / 入荷完了 / キャンセル / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_outbound_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_outbound_orders`
- headings: 出荷管理
- tabs: 保留中 新規 0 / 出荷待ち 0 / 依頼済み 新規 0 / 作業中 新規 0 / 欠品・要対応 新規 0 / 出荷完了
- buttons: stack-ps-yosuke 陽介 河野 / インポート / 条件指定でエクスポート / 保留中 新規 0 / 出荷待ち 0 / 依頼済み 新規 0 / 作業中 新規 0 / 欠品・要対応 新規 0 / 出荷完了 / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / インポート / 条件指定でエクスポート
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / インポート / 条件指定でエクスポート

## /admin/inventory_outbound_orders/export/yamato_b2_cloud

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_outbound_orders/export/yamato_b2_cloud`
- headings: 条件指定でヤマトB2クラウドのCSVをエクスポートする / エクスポート完了後、メールにて以下のダウンロードリンクをお知らせいたします
- buttons: stack-ps-yosuke 陽介 河野 / 実行する
- fields:
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
  - input:text `配送先 (国)` required=False disabled=False
  - select:select-one `決済方法` required=False disabled=False options=['すべての決済', '代引きのみ', '代引き以外の決済']
  - select:select-one `出荷作業ステータス` required=False disabled=False options=['選択してください', '指定しない', '出荷待ち', '保留中', '依頼済み', '作業中', '欠品・要対応', 'キャンセル済み', '出荷完了']
  - input:text `注文タグ（含む）` required=False disabled=False
  - input:text `注文タグ（除外）` required=False disabled=False
  - input:checkbox `CSVの出力後に出荷指示のステータスを出荷作業中に変更する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `配送先 (国)`: stack-ps-yosuke 陽介 河野

## /admin/inventory_allocation_requests

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests`
- headings: 在庫依頼
- tabs: 確認待ち / 確保済み / 終了
- buttons: stack-ps-yosuke 陽介 河野 / 確認待ち / 確保済み / 終了 / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 依頼先 | ステータス | チャネル | 希望数 | 確保済み | 作成日時
  - product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 | TEST_FAQ_20260624_GU_092214_NAVY_M | 店舗 | 情報 確認待ち | web-admin | 1 | 0 | 2026年06月24日 09:24
  - product thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 | TEST_E2E_20260622_GU_1905_NAVY_M | 店舗 | 情報 確認待ち | web-admin | 1 | 0 | 2026年06月22日 08:33
  - product thumbnail TEST_E2E_20260622 GU検証Tシャツ 1845 | TEST_E2E_20260622_GU_1845_NAVY_M | 店舗 | 情報 確認待ち | web-admin | 1 | 0 | 2026年06月22日 08:29

## /admin/inventory_allocation_requests/create

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- headings: 在庫依頼を作成する / 商品 / リクエスト内容
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `商品バリエーション` required=False disabled=False
  - input:number `希望数` required=False disabled=False
  - input:text `移動先ロケーション` required=False disabled=False
  - input:text `リクエスト先ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `商品バリエーション`: stack-ps-yosuke 陽介 河野
  - `移動先ロケーション`: stack-ps-yosuke 陽介 河野
  - `リクエスト先ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/inventory_allocation_request_confirmations

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_request_confirmations`
- headings: 確保済み
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / 移動伝票を作成する / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 確保数 | 移動元 | 移動先 | 確保日時
  - UVカットペーパーブレイドハット | 482787-30-ONE | 1 | ユニクロEC | ユニクロEC | 2026年06月21日 12:03

## /admin/order_price_adjustment_rules

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules`
- headings: ディスカウント
- tabs: すべて / 有効 / スケジュール済み / 期限切れ
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 有効 / スケジュール済み / 期限切れ / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | タイトル | クーポンコード | ステータス | 有効期間 | 対象顧客 | 対象店舗 | 利用回数 | テナント
  - アイテムを選択する | TEST_FAQ_DEEP3_202606080345_ディスカウント | TEST-FAQ-DEEP3-202606080345-DISC | 成功 有効 | 2026年06月08日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ
  - アイテムを選択する | TEST_FAQ_ディスカウント_対象商品テスト | TEST-FAQ-001 | 成功 有効 | 2026年01月01日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ

## /admin/order_price_adjustment_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/create`
- headings: ディスカウントを作成する / 基本情報 / 割引設定 / 適用条件 / 割引要件 / 対象商品 / 利用制限 / 有効期間
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - textarea:text `説明文` required=False disabled=False
  - input:text `クーポンコード` required=False disabled=False
  - select:select-one `テナント` required=False disabled=False options=['テナントを選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `割引方法` required=False disabled=False options=['選択してください', '割引率', '割引額']
  - input:number `割引率` required=False disabled=False
  - input:checkbox `割引が適用可能な最高購入額を設定する` required=False disabled=False checked=False
  - input:radio `最低購入額` required=False disabled=False checked=True
  - input:number `円` required=False disabled=False
  - input:radio `最低購入数量` required=False disabled=False checked=False
  - input:checkbox `すべての商品を割引対象に設定する` required=False disabled=False checked=False
  - input:checkbox `お客様1人につき1回のみの使用とする` required=False disabled=False checked=False
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/point_calculation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules`
- headings: 注文ポイント
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | ルール | 利用テナント数
  - アイテムを選択する | TEST_FAQ_注文ポイント付与ルール | 0件

## /admin/point_calculation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules/create`
- headings: 注文ポイント付与ルールを作成する / 基本設定 / 付与対象 / ポイントのライフサイクル / 会員ランク算出ルール / ポイントキャンペーン優先ルール
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:number `購入金額` required=False disabled=False
  - input:number `ポイント` required=False disabled=False
  - input:checkbox `ポイント利用分を含める` required=False disabled=False checked=False
  - input:checkbox `セール価格の商品を除外する` required=False disabled=False checked=False
  - input:number `付与までの日数（オンライン）` required=False disabled=False
  - input:number `付与までの日数（店舗）` required=False disabled=False
  - input:number `利用可能になってから有効な日数` required=False disabled=False
  - select:select-one `会員ランク算出ルール` required=False disabled=False options=['未設定', 'TEST_FAQ_会員ランク算出ルール', 'TEST_FAQ_RANK_20260615081841']
  - input:radio `開始日時が新しいキャンペーンを優先する` required=False disabled=False checked=True
  - input:radio `開始日時が古いキャンペーンを優先する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/point_campaign_order_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_campaign_order_rules`
- headings: ポイントキャンペーン
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | タイトル | 種別 | 注文ポイント付与ルール | 開始日時 | 終了日時 | 作成日時
  - アイテムを選択する | TEST_FAQ_DEEP3_202606080345_ポイントCP | なし | TEST_FAQ_注文ポイント付与ルール | 2026年06月08日 00:00 | 2026年12月31日 23:59 | 2026年06月08日 12:46
  - アイテムを選択する | TEST_FAQ_ランク別ポイントキャンペーン | 会員ランク | TEST_FAQ_注文ポイント付与ルール | 2026年01月01日 00:00 | 2026年12月31日 23:59 | 2026年06月06日 18:21

## /admin/point_campaign_order_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_campaign_order_rules/create`
- headings: ポイントキャンペーンを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
  - select:select-one `ポイントキャンペーン種別` required=False disabled=False options=['選択してください', 'なし', '会員ランク', '購入金額', '商品']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/point_calculation_birthday_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_birthday_rules`
- headings: 誕生日ポイント
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | タイトル
  - アイテムを選択する | TEST_FAQ_DEEP2_202606080343_誕生日ポイント

## /admin/point_calculation_birthday_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_birthday_rules/create`
- headings: 誕生日ポイント付与ルールを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:text `表示タイトル` required=False disabled=False
  - input:number `ポイント` required=False disabled=False
  - input:number `有効期間` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/point_application_excluded_products

- finalUrl: `https://www.sqstackstaging.com/admin/point_application_excluded_products`
- headings: 利用外商品
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/point_application_excluded_products/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_application_excluded_products/create`
- headings: 利用外商品を追加する
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `商品を選択する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `商品を選択する`: stack-ps-yosuke 陽介 河野

## /admin/point_expiration_notification_rule

- finalUrl: `https://www.sqstackstaging.com/admin/point_expiration_notification_rule`
- headings: 失効通知
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | タイトル | 通知予定日 | 利用テナント数
  - アイテムを選択する | TEST_FAQ_DEEP2_202606080343_失効通知 | 30日前 | 0

## /admin/point_expiration_notification_rule/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_expiration_notification_rule/create`
- headings: ポイント失効通知ルールを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:number `通知予定日` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/customer_rank_calculation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules`
- headings: 会員ランク
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | ルール | 利用テナント数
  - アイテムを選択する | TEST_FAQ_会員ランク算出ルール | 0件
  - アイテムを選択する | TEST_FAQ_RANK_20260615081841 | 0件

## /admin/customer_rank_calculation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules/create`
- headings: 会員ランク算出ルールを作成する / ルール / 算出期間 / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:radio `購入金額` required=False disabled=True checked=True
  - input:radio `獲得ポイント` required=False disabled=True checked=False
  - input:checkbox `税抜き価格でランクを算出する` required=False disabled=False checked=False
  - select:select-one `期間` required=False disabled=False options=['1年間', '直近365日', '無期限']
  - select:select-one `開始月` required=False disabled=False options=['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  - input:checkbox `会員ランクを月初に算出する` required=False disabled=False checked=False
  - input:checkbox `会員ランクを次の算出期間に持ち越す` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/shopify_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/shopify_integrations`
- headings: Shopify
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/shopify_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/shopify_integrations/create`
- headings: ストアを連携する
- buttons: stack-ps-yosuke 陽介 河野 / 連携する
- fields:
  - input:text `ストア名` required=False disabled=False
  - input:text `ショップドメイン` required=False disabled=False
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - select:select-one `ロケーショングループ` required=False disabled=False options=['選択してください', 'GU グループ', 'ユニクログループ']
  - select:select-one `販売価格ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_販売価格ルール', 'TEST_FAQ_販売価格ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_販売価格ルール']
  - select:select-one `会員番号の生成方法` required=False disabled=False options=['Shopify ID（数値部分）', 'JAN-13コード（モジュラス10/ウェイト3方式）']
  - input:checkbox `商品価格は税込価格を連携する` required=False disabled=False checked=False
  - input:checkbox `0円の商品バリエーションを連携する` required=False disabled=False checked=False
  - input:checkbox `送料は税込として処理する` required=False disabled=False checked=False
  - input:checkbox `注文による在庫変動を起こさない` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/omnibus_core_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations`
- headings: OmnibusCore
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: メーカーコード | テナント | カタログ | ロケーショングループ | 連携日時
  - TEST_MAKER_001 | ユニクロ | - | - | 2026年06月06日 18:46

## /admin/omnibus_core_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/create`
- headings: OmnibusCore連携を作成する / 商品同期設定 / 在庫設定 / 注文設定
- buttons: stack-ps-yosuke 陽介 河野 / オプションを追加 / 保存する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:text `メーカーコード` required=False disabled=False
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - input:text `カラーオプション名` required=False disabled=False
  - input:text `サイズオプション名` required=False disabled=False
  - select:select-one `ロケーショングループ` required=False disabled=False options=['選択してください', 'GU グループ', 'ユニクログループ']
  - select:select-one `在庫予約ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_予約販売ルール', 'TEST_FAQ_予約販売ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_予約販売ルール']
  - select:select-one `販売上限ルール` required=False disabled=False options=['選択してください']
  - input:number `下書き注文の有効期限日数` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/smaregi_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/smaregi_integrations`
- headings: スマレジ連携
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/smaregi_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/smaregi_integrations/create`
- headings: スマレジ連携を作成する / 基本情報 / 商品連携設定 / 在庫設定 / 取引連携設定
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:text `契約ID` required=False disabled=False
  - select:select-one `プラン` required=False disabled=False options=['スタンダード', 'プレミアム', 'プレミアムプラス', 'フードビジネス', 'リテールビジネス']
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - select:select-one `在庫同期の方向` required=False disabled=False options=['スマレジからSQへ在庫を同期する', 'SQからスマレジへ在庫を同期する', '在庫を同期しない']
  - input:checkbox `注文による在庫変動を起こさない` required=False disabled=False checked=False
  - input:checkbox `取引の連携を有効にする` required=False disabled=False checked=True
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/retail_portal_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations`
- headings: リテールポータル
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `場所コードを入力してください` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 店舗
  - アイテムを選択する | ユニクロ - 銀座店

## /admin/retail_portal_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations/create`
- headings: リテールポータル
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `店舗ロケーション` required=False disabled=False
  - input:text `在庫ロケーション` required=False disabled=False
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - select:select-one `販売閾値ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_販売閾値ルール', 'TEST_FAQ_販売閾値ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_販売閾値ルール']
  - input:checkbox `リテールポータルで販売員の選択を必須にする` required=False disabled=False checked=False
  - input:checkbox `配送先住所の編集を許可する` required=False disabled=False checked=False
  - input:checkbox `下書き注文の送料明細の編集を許可する` required=False disabled=False checked=False
  - input:checkbox `下書き注文の注文明細の価格の編集を許可する` required=False disabled=False checked=False
  - input:checkbox `下書き注文の完了を許可する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `店舗ロケーション`: stack-ps-yosuke 陽介 河野
  - `在庫ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/b2b

- finalUrl: `https://www.sqstackstaging.com/admin/b2b`
- headings: 卸売
- status: TODO表示あり
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/b2b/create

- finalUrl: `https://www.sqstackstaging.com/admin/b2b/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/settings

- finalUrl: `https://www.sqstackstaging.com/admin/settings`
- headings: 設定 / 組織ID / データ管理 / テンプレート / 通知 / 外部連携 / カスタムデータ
- buttons: stack-ps-yosuke 陽介 河野
- fields:
  - input:text `` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/users

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users`
- headings: 管理メンバー
- buttons: stack-ps-yosuke 陽介 河野 / 絞り込みを追加 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `キーワードで検索する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 絞り込みを追加
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 絞り込みを追加
  - `キーワードで検索する`: stack-ps-yosuke 陽介 河野 / 絞り込みを追加
- table1: 名前 | メールアドレス | 権限グループ
  - サポートアカウントStack | erp.delivery.admin@stack.inc | 特権管理者
  - 福田涼介 | yz@stack.inc | 特権管理者
  - 菅野将貴 | sugano@stack.inc | 特権管理者

## /admin/settings/users/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/create`
- headings: ユーザーを追加する / 基本情報 / 権限
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:radio `特権管理者` required=False disabled=False checked=False
  - input:radio `TEST_権限検証_20260620` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/permission_groups

- finalUrl: `https://www.sqstackstaging.com/admin/settings/permission_groups`
- headings: 権限グループ
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=True checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=True checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 権限数
  - アイテムを選択する | TEST_権限検証_20260620 | 1
  - アイテムを選択する | 特権管理者 | 76

## /admin/settings/permission_groups/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/permission_groups/create`
- headings: 権限グループを作成する
- buttons: stack-ps-yosuke 陽介 河野 / 作成する
- fields:
  - input:text `グループ名` required=False disabled=False
  - input:checkbox `お知らせの閲覧権限（announcements:read）` required=False disabled=False checked=False
  - input:checkbox `お知らせの編集権限（announcements:write）` required=False disabled=False checked=False
  - input:checkbox `アプリの閲覧権限（apps:read）` required=False disabled=False checked=False
  - input:checkbox `アプリの編集権限（apps:write）` required=False disabled=False checked=False
  - input:checkbox `ブランドの閲覧権限（brands:read）` required=False disabled=False checked=False
  - input:checkbox `ブランドの編集権限（brands:write）` required=False disabled=False checked=False
  - input:checkbox `カタログの閲覧権限（catalogs:read）` required=False disabled=False checked=False
  - input:checkbox `カタログの編集権限（catalogs:write）` required=False disabled=False checked=False
  - input:checkbox `取引先企業の閲覧権限（companies:read）` required=False disabled=False checked=False
  - input:checkbox `取引先企業の編集権限（companies:write）` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの閲覧権限（customer_miles:read）` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの編集権限（customer_miles:write）` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの閲覧権限（customer_points:read）` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの編集権限（customer_points:write）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの閲覧権限（customer_rank_rules:read）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの編集権限（customer_rank_rules:write）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの閲覧権限（customer_ranks:read）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの編集権限（customer_ranks:write）` required=False disabled=False checked=False
  - input:checkbox `顧客の閲覧権限（customers:read）` required=False disabled=False checked=False
  - input:checkbox `顧客の編集権限（customers:write）` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの閲覧権限（discounts:read）` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの編集権限（discounts:write）` required=False disabled=False checked=False
  - input:checkbox `下書き注文の閲覧権限（draft_orders:read）` required=False disabled=False checked=False
  - input:checkbox `下書き注文の編集権限（draft_orders:write）` required=False disabled=False checked=False
  - input:checkbox `在庫の閲覧権限（inventory:read）` required=False disabled=False checked=False
  - input:checkbox `在庫の編集権限（inventory:write）` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの閲覧権限（inventory_allocation_requests:read）` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの編集権限（inventory_allocation_requests:write）` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の閲覧権限（inventory_purchase_order_returns:read）` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の編集権限（inventory_purchase_order_returns:write）` required=False disabled=False checked=False
  - input:checkbox `発注伝票の閲覧権限（inventory_purchase_orders:read）` required=False disabled=False checked=False
  - input:checkbox `発注伝票の編集権限（inventory_purchase_orders:write）` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの閲覧権限（local_pickup_location_rules:read）` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの編集権限（local_pickup_location_rules:write）` required=False disabled=False checked=False
  - input:checkbox `ロケーショングループの閲覧権限（location_groups:read）` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/tenants

- finalUrl: `https://www.sqstackstaging.com/admin/settings/tenants`
- headings: テナント
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 名前
  - テストテナント
  - TEST_FAQ_COVERAGE_20260615_テナント_EDIT
  - ユニクロ

## /admin/settings/tenants/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/tenants/create`
- headings: テナントを作成
- buttons: stack-ps-yosuke 陽介 河野 / 保存する (disabled)
- fields:
  - input:text `テナント名` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/locations

- finalUrl: `https://www.sqstackstaging.com/admin/settings/locations`
- headings: ロケーション
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 名前 | コード | 場所種別 | 公開 | アーカイブ | ロケーショングループ | タグ
  - GU 倉庫 | TFCLOC3698 | 倉庫 | 成功 公開中 | 1個のグループ
  - GU 銀座店 | 12456789098765 | 情報 店舗 | 成功 公開中 | 1個のグループ | 店舗
  - TEST_E2E_20260622_GU倉庫_ON_1740 | TEST_E2E_20260622_WH_1740 | 倉庫 | 成功 公開中 | 0個のグループ

## /admin/settings/locations/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/locations/create`
- headings: ロケーションを作成 / 基本情報 / 所在地・連絡先 / 販売設定
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:text `表示名` required=False disabled=False
  - input:text `コード` required=False disabled=False
  - select:select-one `場所種別` required=False disabled=False options=['選択してください', '倉庫', '店舗']
  - input:checkbox `ロケーションの住所を登録する` required=False disabled=False checked=False
  - input:text `マップ` required=False disabled=False
  - input:text `電話番号` required=False disabled=False
  - input:text `メールアドレス` required=False disabled=False
  - input:checkbox `店舗受け取りを有効にする` required=False disabled=False checked=False
  - input:checkbox `在庫依頼を受け付ける` required=False disabled=False checked=False
  - select:select-one `ポイント利用種別` required=False disabled=False options=['選択してください', '値引き', '金種']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/location_groups

- finalUrl: `https://www.sqstackstaging.com/admin/settings/location_groups`
- headings: ロケーショングループ
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled) / ロケーショングループ
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: グループ名 | デフォルト | ロケーション
  - ユニクログループ | ユニクロ - 銀座店 | 3個のロケーション
  - GU グループ | GU 銀座店 | 2個のロケーション

## /admin/settings/location_groups/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/location_groups/create`
- headings: グループを作成
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/settings/brands

- finalUrl: `https://www.sqstackstaging.com/admin/settings/brands`
- headings: ブランド
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | コード | 外部ID | 更新日時
  - アイテムを選択する | UNIQLO | UNIQLO | 2026年06月21日
  - アイテムを選択する | GU | GU | 2026年06月21日
  - アイテムを選択する | TEST_E2E_20260622_ブランド_1740 | TEST_E2E_20260622_BR_1740 | TEST_E2E_20260622_BR_EXT_1740 | 2026年06月22日

## /admin/settings/brands/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/brands/create`
- headings: ブランド
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:text `外部ID` required=False disabled=False
  - input:text `コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/suppliers

- finalUrl: `https://www.sqstackstaging.com/admin/settings/suppliers`
- headings: 取引先
- tabs: すべて / アーカイブ
- buttons: stack-ps-yosuke 陽介 河野 / インポート / すべて / アーカイブ / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | コード
  - アイテムを選択する | TEST_FAQ_20260624_取引先_092214 | TEST_FAQ_20260624_SUP_092214
  - アイテムを選択する | TEST_E2E_20260622_取引先_1905 | TEST_E2E_20260622_SUP_1905
  - アイテムを選択する | TEST_E2E_20260622_取引先_1845 | TEST_E2E_20260622_SUP_1845

## /admin/settings/suppliers/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/suppliers/create`
- headings: 取引先を作成
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `取引先名` required=False disabled=False
  - input:text `取引先コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/payment_methods

- finalUrl: `https://www.sqstackstaging.com/admin/settings/payment_methods`
- headings: 決済方法
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | コード | ゲートウェイ
  - アイテムを選択する | TEST_FAQ_決済 | test_faq_payment | test_gateway
  - アイテムを選択する | TEST_FAQ_DEEP_202606080340_決済 | test_faq_deep_202606080340_payment | test_faq_deep_202606080340_gateway
  - アイテムを選択する | TEST_E2E_20260622_決済_1740 | TEST_E2E_20260622_PAY_1740 | manual_test

## /admin/settings/payment_methods/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/payment_methods/create`
- headings: 決済方法を作成する / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:text `コード` required=False disabled=False
  - input:text `ゲートウェイ` required=False disabled=False
  - input:checkbox `支払い待ちでも注文を出荷する` required=False disabled=False checked=False
  - input:checkbox `代引き` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/retail_staff_members

- finalUrl: `https://www.sqstackstaging.com/admin/settings/retail_staff_members`
- headings: 販売員
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `販売員コードで検索する` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `販売員コードで検索する`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 販売員コード | 外部ID
  - アイテムを選択する | 銀座ユニクロ | 123
  - アイテムを選択する | TEST_APPCHECK販売員 | APPCHK-20260616212742

## /admin/settings/retail_staff_members/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/retail_staff_members/create`
- headings: 販売員を作成する
- buttons: stack-ps-yosuke 陽介 河野 / 検索する / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:text `コード` required=False disabled=False
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/settings/pdf_template_package_slip

- finalUrl: `https://www.sqstackstaging.com/admin/settings/pdf_template_package_slip`
- headings: PDF納品書テンプレート
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - textarea:text `HTMLテンプレート` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/organization_notification_emails

- finalUrl: `https://www.sqstackstaging.com/admin/settings/organization_notification_emails`
- headings: 通知用メールアドレス
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | メールアドレス
  - アイテムを選択する | test | you.4235@gmail.com

## /admin/settings/organization_notification_emails/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/organization_notification_emails/create`
- headings: 通知用メールアドレス
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/apps

- finalUrl: `https://www.sqstackstaging.com/admin/settings/apps`
- headings: アプリ
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/apps/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/apps/create`
- headings: 新しいアプリ / 権限
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `アプリ名` required=False disabled=False
  - input:checkbox `お知らせの閲覧権限 (announcements:read)` required=False disabled=False checked=False
  - input:checkbox `お知らせの編集権限 (announcements:write)` required=False disabled=False checked=False
  - input:checkbox `アプリの閲覧権限 (apps:read)` required=False disabled=False checked=False
  - input:checkbox `アプリの編集権限 (apps:write)` required=False disabled=False checked=False
  - input:checkbox `ブランドの閲覧権限 (brands:read)` required=False disabled=False checked=False
  - input:checkbox `ブランドの編集権限 (brands:write)` required=False disabled=False checked=False
  - input:checkbox `カタログの閲覧権限 (catalogs:read)` required=False disabled=False checked=False
  - input:checkbox `カタログの編集権限 (catalogs:write)` required=False disabled=False checked=False
  - input:checkbox `取引先企業の閲覧権限 (companies:read)` required=False disabled=False checked=False
  - input:checkbox `取引先企業の編集権限 (companies:write)` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの閲覧権限 (customer_miles:read)` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの編集権限 (customer_miles:write)` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの閲覧権限 (customer_points:read)` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの編集権限 (customer_points:write)` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの閲覧権限 (customer_rank_rules:read)` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの編集権限 (customer_rank_rules:write)` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの閲覧権限 (customer_ranks:read)` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの編集権限 (customer_ranks:write)` required=False disabled=False checked=False
  - input:checkbox `顧客の閲覧権限 (customers:read)` required=False disabled=False checked=False
  - input:checkbox `顧客の編集権限 (customers:write)` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの閲覧権限 (discounts:read)` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの編集権限 (discounts:write)` required=False disabled=False checked=False
  - input:checkbox `下書き注文の閲覧権限 (draft_orders:read)` required=False disabled=False checked=False
  - input:checkbox `下書き注文の編集権限 (draft_orders:write)` required=False disabled=False checked=False
  - input:checkbox `在庫の閲覧権限 (inventory:read)` required=False disabled=False checked=False
  - input:checkbox `在庫の編集権限 (inventory:write)` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの閲覧権限 (inventory_allocation_requests:read)` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの編集権限 (inventory_allocation_requests:write)` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の閲覧権限 (inventory_purchase_order_returns:read)` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の編集権限 (inventory_purchase_order_returns:write)` required=False disabled=False checked=False
  - input:checkbox `発注伝票の閲覧権限 (inventory_purchase_orders:read)` required=False disabled=False checked=False
  - input:checkbox `発注伝票の編集権限 (inventory_purchase_orders:write)` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの閲覧権限 (local_pickup_location_rules:read)` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの編集権限 (local_pickup_location_rules:write)` required=False disabled=False checked=False
  - input:checkbox `ロケーショングループの閲覧権限 (location_groups:read)` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/logizard_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/logizard_integrations`
- headings: ロジザード連携
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/logizard_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/logizard_integrations/create`
- headings: ロジザード連携を作成する / 接続情報 / 認証情報 / 入荷設定 / 出荷設定 / 出荷箱明細実績エクスポート設定 / 商品マッピング設定
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `設定名` required=False disabled=False
  - input:text `グループ番号` required=False disabled=False
  - input:text `接続番号` required=False disabled=False
  - input:checkbox `Partner APIエンドポイントを使用する` required=False disabled=False checked=False
  - input:text `オーナーID` required=False disabled=False
  - input:text `ユーザーID` required=False disabled=False
  - input:password `パスワード` required=False disabled=False
  - input:text `アプリケーションキー` required=False disabled=False
  - input:checkbox `AuthKeyの発行をスキップする` required=False disabled=False checked=False
  - input:text `入荷予定登録ファイルID` required=False disabled=False
  - input:text `入荷予定登録パターンID` required=False disabled=False
  - input:text `出荷予定登録(通販)ファイルID` required=False disabled=False
  - input:text `出荷予定登録(通販)パターンID` required=False disabled=False
  - input:text `出荷予定登録(卸)ファイルID` required=False disabled=False
  - input:text `出荷予定登録(卸)パターンID` required=False disabled=False
  - input:text `出荷箱明細実績エクスポートファイルID` required=False disabled=False
  - input:text `出荷箱明細実績エクスポートパターンID` required=False disabled=False
  - select:select-one `商品バリエーションを特定するキー` required=False disabled=False options=['SKUコード', 'JANコード', 'EANコード', 'UPCコード']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/recustomer_integrations

- finalUrl: `https://www.sqstackstaging.com/admin/recustomer_integrations`
- headings: Recustomer
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/recustomer_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/recustomer_integrations/create`
- headings: アカウントを接続する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `ストアID` required=False disabled=False
  - input:text `シークレット` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/translation

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation`
- headings: 翻訳 / 未選択：翻訳ルールを選択するとリソースを選択できます / 商品
- buttons: stack-ps-yosuke 陽介 河野 / 選択してください
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 選択してください
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 選択してください
  - `選択してください`: stack-ps-yosuke 陽介 河野 / 選択してください

## /admin/settings/translation/translation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation/translation_rules`
- headings: 翻訳ルール
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 言語 | 作成日時
  - アイテムを選択する | TEST_FAQ_20260624_TRANSLATION_CRUD_093701 | 英語 | 2026年06月24日 09:37
  - アイテムを選択する | Test_中国語 | 中国語（簡体字） | 2026年06月16日 17:33
  - アイテムを選択する | TEST_FAQ_翻訳ルール_英語 | 英語 | 2026年06月07日 08:41

## /admin/settings/translation/translation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation/translation_rules/create`
- headings: 翻訳ルールを作成する / 各種設定
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - select:select-one `言語` required=False disabled=False options=['選択してください', '日本語', '英語', '中国語（簡体字）', '中国語（繁体字）', '韓国語', 'スペイン語', 'フランス語', 'ドイツ語', 'ヒンディー語', 'タイ語']
  - input:checkbox `翻訳データを自動で作成する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions`
- headings: メタフィールド定義 / 組織のメタフィールド定義
- buttons: stack-ps-yosuke 陽介 河野 / 組織 / ロケーション / 会社 / 仕入れ先ベンダー / 商品 / バリエーション / 顧客 / 注文 / 下書き注文 / ディスカウント / 在庫移動伝票 / 在庫調整伝票 / 在庫取置伝票 / 発注伝票 / 入荷指示 / 出荷指示
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 組織 / ロケーション / 会社 / 仕入れ先ベンダー / 商品 / バリエーション / 顧客 / 注文 / 下書き注文 / ディスカウント / 在庫移動伝票 / 在庫調整伝票 / 在庫取置伝票 / 発注伝票 / 入荷指示 / 出荷指示
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 組織 / ロケーション / 会社 / 仕入れ先ベンダー / 商品 / バリエーション / 顧客 / 注文 / 下書き注文 / ディスカウント / 在庫移動伝票 / 在庫調整伝票 / 在庫取置伝票 / 発注伝票 / 入荷指示 / 出荷指示

## /admin/settings/metafield_definitions/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/settings/product_measurement_rules

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules`
- headings: 採寸ルール
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: ルール名 | 単位 | 採寸項目
  - TEST_FAQ_20260624_MEASURE_CRUD_093821 | センチメートル | 肩幅
  - TEST_FAQ_COVERAGE_20260615_159330_採寸 | センチメートル | 肩幅
  - TEST_FAQ_DEEP_202606080340_採寸ルール | センチメートル | 肩幅

## /admin/settings/product_measurement_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules/create`
- headings: 採寸ルールを作成する / 基本設定 / 採寸項目
- buttons: stack-ps-yosuke 陽介 河野 / 採寸項目を追加 / 保存する
- fields:
  - input:text `ルール名` required=False disabled=False
  - select:select-one `採寸単位` required=False disabled=False options=['なし', 'センチメートル']
  - input:text `採寸項目1` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import`
- headings: CSVインポート / 商品 / 商品 / 商品画像 / 商品バリエーション / 商品バリエーション画像 / カタログ / 原価
- buttons: stack-ps-yosuke 陽介 河野 / 商品 / 価格 / 販売 / 在庫 / メタフィールド / 出荷 / ポイント / 会員ランク / 各種マスター
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 商品 / 価格 / 販売 / 在庫 / メタフィールド / 出荷 / ポイント / 会員ランク / 各種マスター
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 商品 / 価格 / 販売 / 在庫 / メタフィールド / 出荷 / ポイント / 会員ランク / 各種マスター

## /admin/csv_import/csv_import_operation_products

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products`
- headings: 商品をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | 実行ステータス
  - 2026年06月08日 | 成功 完了 完了
  - 2026年05月20日 | 成功 完了 完了

## /admin/csv_import/csv_import_operation_products/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/create`
- headings: 商品をCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variants`
- headings: 商品バリエーションをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | 実行ステータス
  - 2026年05月20日 | 成功 完了 完了

## /admin/csv_import/csv_import_operation_product_variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variants/create`
- headings: 商品バリエーションをCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_images

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_images`
- headings: 商品画像をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | 実行ステータス
  - 2026年05月20日 | 成功 完了 完了

## /admin/csv_import/csv_import_operation_product_images/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_images/create`
- headings: 商品画像をCSVでインポートする / 反映方法
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:radio `画像を追加する` required=False disabled=False checked=True
  - input:radio `画像を上書きする` required=False disabled=False checked=False
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variant_images

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variant_images`
- headings: 商品バリエーション画像をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variant_images/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variant_images/create`
- headings: 商品バリエーション画像をCSVでインポートする / 反映方法
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:radio `画像を追加する` required=False disabled=False checked=True
  - input:radio `画像を上書きする` required=False disabled=False checked=False
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_catalog_products

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products`
- headings: カタログ商品をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_catalog_products/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/create`
- headings: カタログ商品をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `カタログ` required=False disabled=False options=['カタログを選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_metafields

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_metafields`
- headings: 商品メタフィールドをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_metafields/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_metafields/create`
- headings: 商品メタフィールドをCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variant_metafields

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variant_metafields`
- headings: 商品バリエーションメタフィールドをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variant_metafields/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variant_metafields/create`
- headings: 商品バリエーションメタフィールドをCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities`
- headings: 販売可能在庫をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | 実行ステータス
  - 2026年06月16日 | 成功 完了 完了
  - 2026年06月16日 | 成功 完了 完了
  - 2026年06月15日 | 成功 完了 完了

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities/create`
- headings: 販売可能在庫をCSVでインポートする / 反映方法
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:radio `絶対値で反映する` required=False disabled=False checked=True
  - input:radio `差分値で反映する` required=False disabled=False checked=False
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_back_order_rule_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_back_order_rule_product_variants`
- headings: 予約販売バリエーションをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_back_order_rule_product_variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_back_order_rule_product_variants/create`
- headings: 予約販売バリエーションをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `予約販売ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_予約販売ルール', 'TEST_FAQ_予約販売ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_予約販売ルール']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_movement_orders

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_movement_orders`
- headings: 在庫移動伝票をCSVで一括取り込む
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_movement_orders/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_movement_orders/create`
- headings: 在庫移動をCSVで一括取り込む
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds`
- headings: ヤマトB2クラウドの出荷実績をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds/create`
- headings: ヤマトB2クラウドの出荷実績をCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_fulfillment_by_dhls

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_fulfillment_by_dhls`
- headings: DHLの出荷実績をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_fulfillment_by_dhls/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_fulfillment_by_dhls/create`
- headings: DHLの出荷実績をCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_pluses

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_pluses`
- headings: ポイントをCSVで一括付与する
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_pluses/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_pluses/create`
- headings: ポイントをCSVで一括加算する
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `顧客IDの種別` required=False disabled=False options=['選択してください', 'SQが発番した顧客ID', '外部システムが発番した顧客ID']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_minuses

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_minuses`
- headings: ポイントをCSVで一括減算する
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_minuses/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_minuses/create`
- headings: ポイントをCSVで一括減算する
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_campaign_order_rule_point_value_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_campaign_order_rule_point_value_product_variants`
- headings: キャンペーン対象商品をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_point_campaign_order_rule_point_value_product_variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_point_campaign_order_rule_point_value_product_variants/create`
- headings: キャンペーン対象商品をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 検索 / ファイルを選択する / 保存する
- fields:
  - input:text `ポイントキャンペーン` required=False disabled=False
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ポイントキャンペーン`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_customer_rank_rules

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_customer_rank_rules`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_import/csv_import_operation_customer_rank_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_customer_rank_rules/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_import/csv_import_operation_users

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_users`
- headings: 管理ユーザーをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_users/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_users/create`
- headings: 管理ユーザーをCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_locations

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_locations`
- headings: ロケーションをCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_locations/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_locations/create`
- headings: ロケーションをCSVでインポートする / CSVファイル
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_settings_suppliers

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_settings_suppliers`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_import/csv_import_settings_suppliers/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_settings_suppliers/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export`
- headings: CSVエクスポート / マスターデータ / 在庫 / 商品バリエーション / ロケーション / ディスカウントの利用履歴 / 価格 / セール価格
- buttons: stack-ps-yosuke 陽介 河野 / マスターデータ / 価格 / 出荷 / 実績 / ポイント
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / マスターデータ / 価格 / 出荷 / 実績 / ポイント
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / マスターデータ / 価格 / 出荷 / 実績 / ポイント

## /admin/csv_export/csv_export_operation_inventory_items

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_items`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_inventory_items/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_items/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_product_variants`
- headings: 商品バリエーションをCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_product_variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_product_variants/create`
- headings: 商品バリエーションをCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / エクスポートを開始する
- fields:
  - input:checkbox `商品情報を含める` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_locations

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_locations`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_locations/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_locations/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_location_by_location_group

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_location_by_location_group`
- headings: ロケーションをCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_location_by_location_group/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_location_by_location_group/create`
- headings: ロケーションをCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / エクスポートを開始する
- fields:
  - input:text `ロケーショングループ` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーショングループ`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_order_price_adjustment_usages

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_order_price_adjustment_usages`
- headings: ディスカウントの利用履歴をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_order_price_adjustment_usages/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_order_price_adjustment_usages/create`
- headings: ディスカウントの利用履歴をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / エクスポートを開始する
- fields:
  - input:text `ディスカウント` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ディスカウント`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_sale_prices

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_prices`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_sale_prices/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_prices/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds`
- headings: ヤマトB2クラウドの出荷指示をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_sale_changes

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_changes`
- headings: 売上実績（注文軸）をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | テナント | 対象期間 | ステータス | ダウンロード
  - 2026年06月16日 23:41 | ユニクロ | 2026年06月16日 00:00 〜 2026年06月16日 23:59 | 成功 完了 | ダウンロード
  - 2026年06月15日 18:43 | ユニクロ | 2026年06月15日 00:00 〜 2026年06月15日 23:59 | 成功 完了 | ダウンロード
  - 2026年06月08日 12:49 | ユニクロ | 2026年06月01日 00:00 〜 2026年06月08日 23:59 | 成功 完了 | ダウンロード

## /admin/csv_export/csv_export_operation_sale_changes/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_changes/create`
- headings: 売上実績（注文軸）をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / エクスポートを開始する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_sale_change_line_items

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_change_line_items`
- headings: 売上実績（明細軸）をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | テナント | 対象期間 | ステータス | ダウンロード
  - 2026年06月16日 23:42 | ユニクロ | 2026年06月16日 00:00 〜 2026年06月16日 23:59 | 成功 完了 | ダウンロード

## /admin/csv_export/csv_export_operation_sale_change_line_items/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_sale_change_line_items/create`
- headings: 売上実績（明細軸）をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / エクスポートを開始する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_point_histories

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_point_histories`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/csv_export/csv_export_operation_point_histories/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_point_histories/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/pdf_export

- finalUrl: `https://www.sqstackstaging.com/admin/pdf_export`
- headings: PDFエクスポート / 出荷 / 納品書
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/pdf_export/pdf_export_operation_packing_slips

- finalUrl: `https://www.sqstackstaging.com/admin/pdf_export/pdf_export_operation_packing_slips`
- headings: 納品書をPDFでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/pdf_export/pdf_export_operation_packing_slips/create

- finalUrl: `https://www.sqstackstaging.com/admin/pdf_export/pdf_export_operation_packing_slips/create`
- headings: このページは存在しないようです
- status: 存在しないページ

## /admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product

- finalUrl: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product`
- headings: TEST_FAQ_20260624 GU検証Tシャツ 092214 / 商品コード / メディア（0件） / バリエーション / 検索エンジンリスティング / ステータス / 商品分類 / タグ
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 追加 / カラーを展開する / 選択 / 保存する (disabled)
- fields:
  - input:text `商品名` required=False disabled=False
  - textarea:text `説明文` required=False disabled=False
  - input:file `画像をアップロード` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:text `ページタイトル` required=False disabled=False
  - textarea:text `メタディスクリプション` required=False disabled=False
  - select:select-one `下書き` required=False disabled=False options=['公開中', '下書き']
  - input:text `商品タイプ` required=False disabled=False
  - input:text `製造元` required=False disabled=False
  - input:text `ブランド` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `カラーを展開する`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `ブランド`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: すべてのアイテムを選択する | バリエーション | 価格
  - アイテムを選択する | product variant thumbnail NAVY / M SKU: TEST_FAQ_20260624_GU_092214_NAVY_M | ￥1,990

## /admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog`
- headings: TEST_FAQ_カタログ001
- buttons: stack-ps-yosuke 陽介 河野 / 編集する / その他の操作 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `商品コードで検索する` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `商品コードで検索する`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: すべてのアイテムを選択する | 商品 | 商品コード
  - アイテムを選択する | ポケモン UT | 483674

## /admin/csv_export/csv_export_operation_inventory_logical_quantities

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_logical_quantities`
- headings: 在庫をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_items/9f6a69fe-ed14-580f-8b84-0fdc29a2a94f_InventoryItem

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items/9f6a69fe-ed14-580f-8b84-0fdc29a2a94f_InventoryItem`
- headings: TEST_FAQ_20260624 GU検証Tシャツ 092214 / NAVY / M / 選択中のロケーション：
- tabs: すべて / 店舗 / 倉庫
- buttons: stack-ps-yosuke 陽介 河野 / その他のアクション / 選択してください / すべて / 店舗 / 倉庫 / 検索と絞り込みの結果 / 販売可能数を編集 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他のアクション
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他のアクション
  - `その他のアクション`: stack-ps-yosuke 陽介 河野 / その他のアクション
- table1: ロケーション | 販売可能 | 引当済み | 取置中 | 破損 | 検品 | 予備 | 手持ち | 積送中 | 入荷予定
  - GU 倉庫 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0
  - GU 銀座店 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0
  - TEST_E2E_20260622_GU倉庫_ON_1740 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0

## /admin/inventory_movement_orders/98f0c579-65cc-584b-8442-6cd2633db334_InventoryMovementOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders/98f0c579-65cc-584b-8442-6cd2633db334_InventoryMovementOrder`
- headings: #IM-1024 / 配送元 / 配送先 / 商品 / 詳細 / 関連
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: 商品 | 数量
  - product thumbnail TEST_FAQ_20260624_GU_092214_NAVY_M | 1

## /admin/inventory_adjustment_orders/6d2b8c88-f479-55be-9d96-a3c60eea5e29_InventoryAdjustmentOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/6d2b8c88-f479-55be-9d96-a3c60eea5e29_InventoryAdjustmentOrder`
- headings: #IA-1012 / ロケーション / 商品 / 詳細
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | 商品コード | SKU | 増減数
  - product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M | TEST_FAQ_20260624_GU_092214 | TEST_FAQ_20260624_GU_092214_NAVY_M | 0

## /admin/inventory_reservation_orders/6840941b-88e4-5e80-99e7-093d089ccb10_InventoryReservationOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_reservation_orders/6840941b-88e4-5e80-99e7-093d089ccb10_InventoryReservationOrder`
- headings: #IR-1008 / ロケーション / 商品 / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / 処理済みとしてマークする
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | 商品コード | SKU | 数量
  - オーバーサイズスウェットシャツ BEIGE / XL | 486125 | 486125-31-XL | 1
  - オーバーサイズスウェットシャツ BLACK / XL | 486125 | 486125-09-XL | 3
  - オーバーサイズスウェットシャツ BLACK / XL | 486125 | 486125-09-XL | 1

## /admin/inventory_purchase_orders/beec5511-d7f6-5918-a088-a5fcc7b0f44f_InventoryPurchaseOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/beec5511-d7f6-5918-a088-a5fcc7b0f44f_InventoryPurchaseOrder`
- headings: #IP-1004 / 取引先 / 発注済み商品 / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作
- fields:
  - input:text `取引先` required=False disabled=False
  - input:text `テナント` required=False disabled=False
  - input:text `通貨` required=False disabled=False
  - input:number `単価` required=False disabled=False
  - input:number `数量` required=False disabled=False
  - input:number `税率` required=False disabled=False
  - input:number `単価` required=False disabled=False
  - input:number `数量` required=False disabled=False
  - input:number `税率` required=False disabled=False
  - input:number `単価` required=False disabled=False
  - input:number `数量` required=False disabled=False
  - input:number `税率` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: SKU | 単価 | 数量 | 税率 | 金額
  - 486125-03-XL | 単価 ￥ | 数量 | 税率 % | ￥39,600
  - 486125-31-XL | 単価 ￥ | 数量 | 税率 % | ￥39,600
  - 486125-03-M | 単価 ￥ | 数量 | 税率 % | ￥39,600

## /admin/product_price_rules/407b1402-6d11-5672-bc33-5de49d5ce9bc_ProductPriceRule

- finalUrl: `https://www.sqstackstaging.com/admin/product_price_rules/407b1402-6d11-5672-bc33-5de49d5ce9bc_ProductPriceRule`
- headings: 販売価格ルール / 通常価格 / セール価格
- buttons: stack-ps-yosuke 陽介 河野 / ルールを編集
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 通常価格 通常価格を設定することができます。 / セール価格 セール価格を設定することができます。
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 通常価格 通常価格を設定することができます。 / セール価格 セール価格を設定することができます。

## /admin/inventory_allocation_requests/726d9d8e-929b-533d-a875-a3a474cd18a0_InventoryAllocationRequest

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/726d9d8e-929b-533d-a875-a3a474cd18a0_InventoryAllocationRequest`
- headings: 在庫依頼 / 対象商品 / 確保済み在庫 / 依頼先
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 在庫を引当てる / 依頼先の操作
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `依頼先の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: すべてのアイテムを選択する | ロケーション | 販売可能数
  - アイテムを選択する | TEST_FAQ_20260624_GU店舗_OFF_092214 | 1

## /admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule`
- headings: TEST_FAQ_DEEP3_202606080345_ディスカウント / 基本情報 / 割引設定 / 適用条件 / 有効期間 / Shopify連携
- tabs: 基本情報
- buttons: stack-ps-yosuke 陽介 河野 / 基本情報 / 連携する
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration`
- headings: OmnibusCore連携 (TEST_MAKER_001) / 商品同期設定 / 在庫設定 / 注文設定 / アクセストークン / 連携削除 / 基本情報
- tabs: 基本設定
- buttons: stack-ps-yosuke 陽介 河野 / 基本設定 / オプションを追加 / トークンを作成 / 連携を削除する / 保存する (disabled)
- fields:
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'UNIQLO', 'TEST_FAQ_20260624_カタログ_092214']
  - input:text `カラーオプション名` required=False disabled=False
  - input:text `サイズオプション名` required=False disabled=False
  - select:select-one `ロケーショングループ` required=False disabled=False options=['選択してください', 'GU グループ', 'ユニクログループ']
  - select:select-one `在庫予約ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_予約販売ルール', 'TEST_FAQ_予約販売ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_予約販売ルール']
  - select:select-one `販売上限ルール` required=False disabled=False options=['選択してください']
  - input:number `下書き注文の有効期限日数` required=False disabled=False
  - input:radio `出荷待ち` required=False disabled=False checked=True
  - input:radio `保留中` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/retail_portal_integrations/65104d5a-e12a-5c06-9716-48bf6cf4a67d_RetailPortalIntegration

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations/65104d5a-e12a-5c06-9716-48bf6cf4a67d_RetailPortalIntegration`
- headings: ユニクロ - 銀座店
- buttons: stack-ps-yosuke 陽介 河野 / 編集する / ユーザーを追加する / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | メールアドレス
  - アイテムを選択する | 河野陽介 | yosuke.kohno@bay-works.com

## /admin/settings/users/user_358DNqj6iJtcvMhxAwTLlCzyGWU

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_358DNqj6iJtcvMhxAwTLlCzyGWU`
- headings: サポートアカウントStack / 基本情報 / ユーザーテナント / 権限 / ユーザーを組織から除外
- buttons: stack-ps-yosuke 陽介 河野 / 保存する / 組織から除外する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=False
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['未設定', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/users/user_35E68KNK1pCOobD4ZwdoaHsnNo0

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_35E68KNK1pCOobD4ZwdoaHsnNo0`
- headings: 福田涼介 / 基本情報 / ユーザーテナント / 権限 / ユーザーを組織から除外
- buttons: stack-ps-yosuke 陽介 河野 / 保存する / 組織から除外する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['未設定', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/users/user_3CbpZwl1x5ohfuyFmuv1t8VQXyo

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3CbpZwl1x5ohfuyFmuv1t8VQXyo`
- headings: 菅野将貴 / 基本情報 / ユーザーテナント / 権限 / ユーザーを組織から除外
- buttons: stack-ps-yosuke 陽介 河野 / 保存する / 組織から除外する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['未設定', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/users/user_3Dz5ZnyYjoaDwlnz2ffJE7NZTGb

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3Dz5ZnyYjoaDwlnz2ffJE7NZTGb`
- headings: 河野陽介 / 基本情報 / ユーザーテナント / 権限 / ユーザーを組織から除外
- buttons: stack-ps-yosuke 陽介 河野 / 保存する / 組織から除外する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['未設定', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/users/user_3FOeZAow9g1pTX8HYyjifwXk4re

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3FOeZAow9g1pTX8HYyjifwXk4re`
- headings: 権限テスト / 基本情報 / ユーザーテナント / 権限 / ユーザーを組織から除外
- buttons: stack-ps-yosuke 陽介 河野 / 保存する / 組織から除外する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=True
  - input:checkbox `テストテナント` required=False disabled=False checked=True
  - select:select-one `権限グループ` required=False disabled=False options=['未設定', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/permission_groups/ced25bd4-f743-5b58-a17a-0dad097bd704_PermissionGroup

- finalUrl: `https://www.sqstackstaging.com/admin/settings/permission_groups/ced25bd4-f743-5b58-a17a-0dad097bd704_PermissionGroup`
- headings: TEST_権限検証_20260620
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `グループ名` required=False disabled=False
  - input:checkbox `お知らせの閲覧権限（announcements:read）` required=False disabled=False checked=False
  - input:checkbox `お知らせの編集権限（announcements:write）` required=False disabled=False checked=False
  - input:checkbox `アプリの閲覧権限（apps:read）` required=False disabled=False checked=False
  - input:checkbox `アプリの編集権限（apps:write）` required=False disabled=False checked=False
  - input:checkbox `ブランドの閲覧権限（brands:read）` required=False disabled=False checked=False
  - input:checkbox `ブランドの編集権限（brands:write）` required=False disabled=False checked=False
  - input:checkbox `カタログの閲覧権限（catalogs:read）` required=False disabled=False checked=False
  - input:checkbox `カタログの編集権限（catalogs:write）` required=False disabled=False checked=False
  - input:checkbox `取引先企業の閲覧権限（companies:read）` required=False disabled=False checked=False
  - input:checkbox `取引先企業の編集権限（companies:write）` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの閲覧権限（customer_miles:read）` required=False disabled=False checked=False
  - input:checkbox `顧客マイルの編集権限（customer_miles:write）` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの閲覧権限（customer_points:read）` required=False disabled=False checked=False
  - input:checkbox `顧客ポイントの編集権限（customer_points:write）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの閲覧権限（customer_rank_rules:read）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクルールの編集権限（customer_rank_rules:write）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの閲覧権限（customer_ranks:read）` required=False disabled=False checked=False
  - input:checkbox `顧客会員ランクの編集権限（customer_ranks:write）` required=False disabled=False checked=False
  - input:checkbox `顧客の閲覧権限（customers:read）` required=False disabled=False checked=False
  - input:checkbox `顧客の編集権限（customers:write）` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの閲覧権限（discounts:read）` required=False disabled=False checked=False
  - input:checkbox `ディスカウントの編集権限（discounts:write）` required=False disabled=False checked=False
  - input:checkbox `下書き注文の閲覧権限（draft_orders:read）` required=False disabled=False checked=False
  - input:checkbox `下書き注文の編集権限（draft_orders:write）` required=False disabled=False checked=False
  - input:checkbox `在庫の閲覧権限（inventory:read）` required=False disabled=False checked=False
  - input:checkbox `在庫の編集権限（inventory:write）` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの閲覧権限（inventory_allocation_requests:read）` required=False disabled=False checked=False
  - input:checkbox `在庫リクエストの編集権限（inventory_allocation_requests:write）` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の閲覧権限（inventory_purchase_order_returns:read）` required=False disabled=False checked=False
  - input:checkbox `発注返品伝票の編集権限（inventory_purchase_order_returns:write）` required=False disabled=False checked=False
  - input:checkbox `発注伝票の閲覧権限（inventory_purchase_orders:read）` required=False disabled=False checked=False
  - input:checkbox `発注伝票の編集権限（inventory_purchase_orders:write）` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの閲覧権限（local_pickup_location_rules:read）` required=False disabled=False checked=False
  - input:checkbox `店舗受取ロケーションルールの編集権限（local_pickup_location_rules:write）` required=False disabled=False checked=False
  - input:checkbox `ロケーショングループの閲覧権限（location_groups:read）` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/tenants/cee012a1-a15a-5ec5-871f-5e41a330617f_Tenant

- finalUrl: `https://www.sqstackstaging.com/admin/settings/tenants/cee012a1-a15a-5ec5-871f-5e41a330617f_Tenant`
- headings: テストテナント / 基本情報 / CRM
- buttons: stack-ps-yosuke 陽介 河野 / テナントIDをコピーする / 保存する (disabled)
- fields:
  - input:text `テナント名` required=False disabled=False
  - input:text `注文IDプレフィックス` required=False disabled=False
  - select:select-one `ポイントルール` required=False disabled=False options=['ポイントルールを選択してください', 'TEST_FAQ_注文ポイント付与ルール']
  - select:select-one `ランクルール` required=False disabled=False options=['ランクルールを選択してください', 'TEST_FAQ_会員ランク算出ルール', 'TEST_FAQ_RANK_20260615081841']
  - select:select-one `誕生日ポイント付与ルール` required=False disabled=False options=['誕生日ポイント付与ルールを選択してください', 'TEST_FAQ_DEEP2_202606080343_誕生日ポイント']
  - select:select-one `失効予定通知ルール` required=False disabled=False options=['失効予定通知ルールを選択してください', 'TEST_FAQ_DEEP2_202606080343_失効通知']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/apps/9081ef6c-dc90-50be-9bb8-d869eb02f44f_App

- finalUrl: `https://www.sqstackstaging.com/admin/settings/apps/9081ef6c-dc90-50be-9bb8-d869eb02f44f_App`
- headings: TEST_FAQ_アプリ / Admin API / 検証方法 / リクエストログ / Storefront API / Webhook
- buttons: stack-ps-yosuke 陽介 河野 / トークンを発行する / Webhookを作成する
- fields:
  - input:text `アクセストークン` required=False disabled=False
  - input:text `シークレット` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/translation/translation_rules/b98afc2f-97b7-5964-aeaf-a330c9f38a27_TranslationRule

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation/translation_rules/b98afc2f-97b7-5964-aeaf-a330c9f38a27_TranslationRule`
- headings: TEST_FAQ_20260624_TRANSLATION_CRUD_093701 / 各種設定 / 商品 / カスタマイズ項目を追加する / 商品オプション / カスタマイズ項目を追加する / 商品オプション値 / カスタマイズ項目を追加する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する (disabled)
- fields:
  - input:text `名前` required=False disabled=False
  - select:select-one `言語` required=False disabled=True options=['日本語', '英語', '中国語（簡体字）', '中国語（繁体字）', '韓国語', 'スペイン語', 'フランス語', 'ドイツ語', 'ヒンディー語', 'タイ語']
  - input:checkbox `翻訳データを自動で作成する` required=False disabled=False checked=False
  - textarea:text `親プロンプト` required=False disabled=False
  - textarea:text `カスタムプロンプト` required=False disabled=False
  - textarea:text `親プロンプト` required=False disabled=False
  - textarea:text `カスタムプロンプト` required=False disabled=False
  - textarea:text `親プロンプト` required=False disabled=False
  - textarea:text `カスタムプロンプト` required=False disabled=False
  - textarea:text `親プロンプト` required=False disabled=False
  - textarea:text `カスタムプロンプト` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/organization/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/organization/create`
- headings: 組織メタフィールドの定義を追加する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する
- fields:
  - input:text `名前` required=False disabled=False
  - input:text `説明` required=False disabled=False
  - input:text `ネームスペース` required=False disabled=False
  - input:text `キー` required=False disabled=False
  - select:select-one `メタフィールドのタイプ` required=False disabled=False options=['選択してください', '単一行のテキスト', '単一行のテキスト(リスト)', '複数行のテキスト', '日付と時刻', '日付', 'trueまたはfalse', 'バーコード(NW7)', '整数', '小数', 'JSON', 'ID', 'リッチテキスト']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/product_measurement_rules/c3cce272-31c9-50c6-9af2-95e7be3ec25a_ProductMeasurementRule

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules/c3cce272-31c9-50c6-9af2-95e7be3ec25a_ProductMeasurementRule`
- headings: 採寸ルール / 基本設定 / 採寸項目
- buttons: stack-ps-yosuke 陽介 河野
- fields:
  - input:text `ルール名` required=False disabled=False
  - input:text `採寸単位` required=False disabled=False
  - input:text `採寸項目1` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_unit_costs

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_unit_costs`
- headings: 原価をCSVで一括取り込みする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_price_rule_regular_prices

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_price_rule_regular_prices`
- headings: 通常価格をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_price_rule_sale_prices

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_price_rule_sale_prices`
- headings: セール価格をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_threshold_rule_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_threshold_rule_product_variants`
- headings: 販売閾値をCSVで一括取り込みする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_customer_rank_baselines

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_customer_rank_baselines`
- headings: 基準ランクをCSVで一括設定する
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_products/43a9a5c7-2508-57e2-a635-f00e74e8f388_CSVImportOperationProduct

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/43a9a5c7-2508-57e2-a635-f00e74e8f388_CSVImportOperationProduct`
- headings: CSVインポート操作の詳細 / 作成日 / 検証ステータス / 実行ステータス / 検証成功 / 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 実行する (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variants/b5f17d05-6079-5458-8a15-d27d35384046_CSVImportOperationProductVariant

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variants/b5f17d05-6079-5458-8a15-d27d35384046_CSVImportOperationProductVariant`
- headings: CSVインポート操作の詳細 / 作成日 / 検証ステータス / 実行ステータス / 検証成功 / 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 実行する (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_images/f0d331a0-11dc-52f6-a94b-c4a7f8ee8652_CSVImportOperationProductImage

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_images/f0d331a0-11dc-52f6-a94b-c4a7f8ee8652_CSVImportOperationProductImage`
- headings: CSVインポート操作の詳細 / 作成日 / 検証ステータス / 実行ステータス / 検証成功 / 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 実行する (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity`
- headings: CSVインポート操作の詳細 / 作成日 / 検証ステータス / 実行ステータス / 検証成功 / 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 実行する (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_product_price_rule_sale_prices

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_product_price_rule_sale_prices`
- headings: セール価格をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_point_changes

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_point_changes`
- headings: ポイント変動履歴をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 作成日 | テナント | 対象期間 | ステータス | ダウンロード
  - 2026年06月08日 12:49 | ユニクロ | 2026年06月01日 00:00 〜 2026年06月08日 23:59 | 成功 完了 | ダウンロード

## /admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/create`
- headings: バリエーションを追加する / オプション / メディア / 価格設定 / 在庫 / 販売 / 配送 / 関税情報
- buttons: stack-ps-yosuke 陽介 河野 / 画像を選択する / 作成する
- fields:
  - select:select-one `カラー` required=False disabled=False options=['選択してください', 'NAVY / M']
  - input:number `上代` required=False disabled=False
  - input:text `SKU (最小管理単位)` required=False disabled=False
  - input:text `メーカーSKU` required=False disabled=False
  - input:checkbox `在庫を追跡する` required=False disabled=False checked=False
  - input:checkbox `在庫切れの場合でも販売を続ける` required=False disabled=False checked=False
  - input:text `バーコード` required=False disabled=False
  - input:text `JAN` required=False disabled=False
  - input:text `EAN` required=False disabled=False
  - input:number `重量` required=False disabled=False
  - select:select-one `単位` required=False disabled=False options=['グラム', 'キログラム', 'オンス', 'ポンド']
  - input:checkbox `配送を必須にする` required=False disabled=False checked=True
  - select:select-one `原産国コード` required=False disabled=False options=['選択してください', 'インドネシア', 'モルドバ', 'マレーシア', 'パナマ', 'パラグアイ', 'バヌアツ', 'アンギラ', 'ニュージーランド', 'スーダン', 'コートジボワール', 'スロバキア', 'ジンバブエ', 'ブルキナファソ', 'メキシコ', 'エスワティニ', 'オランダ領アンティル', 'ジャマイカ', 'ミャンマー', 'サウジアラビア', 'アゼルバイジャン', 'アイルランド', 'マダガスカル', 'オーランド諸島', 'ブラジル', 'ラトビア', 'サンピエール・ミクロン', 'その他の地域', 'アンゴラ', 'チェコ', 'ギリシャ', 'イラン', 'サンマリノ', 'チャド', 'ハンガリー', 'カンボジア', 'オランダ', 'アンドラ', 'エクアドル', 'パプアニューギニア', 'ポルトガル', 'トリスタン・ダ・クーニャ', 'サモア', 'アルゼンチン', 'モナコ', 'マルタ', 'ペルー', 'サントメ・プリンシペ', 'ツバル', 'キューバ', 'リビア', 'アルメニア', 'コロンビア', 'モルディブ', 'アフガニスタン', 'アンティグア・バーブーダ', 'クウェート', 'サウスジョージア・サウスサンドウィッチ諸島', 'ソマリア', '台湾', 'ボツワナ', 'フィジー', 'スヴァールバル諸島およびヤンマイエン島', 'ベリーズ', 'フォークランド諸島', '赤道ギニア', '日本', 'ナミビア', 'スウェーデン', 'トルクメニスタン', 'ガーンジー', 'ジャージー', 'ナイジェリア', 'ポーランド', 'セントヘレナ', 'ウルグアイ', 'マヨット', '南アフリカ', 'コンゴ共和国', 'エリトリア', 'ジョージア', 'グリーンランド', 'イギリス領インド洋地域', 'モーリタニア', 'ルワンダ', 'ブータン', 'ガイアナ', 'オマーン', 'トケラウ', 'チリ', 'ドミニカ国', 'グレナダ', 'ギニア', 'ハイチ', 'エチオピア', 'ソロモン諸島', 'スリランカ', 'タジキスタン', 'グアドループ', 'ケイマン諸島', 'ルクセンブルク', 'タンザニア', 'ザンビア', 'フランス', 'モンテネグロ', 'マカオ', 'アラブ首長国連邦', 'バルバドス', 'ウズベキスタン', 'フェロー諸島', 'ジブラルタル', '香港', 'リヒテンシュタイン', 'マルティニーク', 'ノーフォーク島', 'イエメン', 'アルバニア', 'ヨルダン', 'ニジェール', 'バチカン市国', 'ハード島とマクドナルド諸島', 'レソト', '合衆国領有小離島', 'スイス', 'クック諸島', 'キュラソー', 'スペイン', 'ギニアビサウ', 'マン島', 'カザフスタン', 'リトアニア', 'サン・マルタン', 'キプロス', 'エストニア', 'インド', 'キルギス', 'オーストラリア', 'モントセラト', 'シエラレオネ', 'スリナム', 'オランダ領カリブ', 'カナダ', 'コスタリカ', 'ガボン', 'フランス南方・南極地域', '東ティモール', 'クロアチア', 'トーゴ', 'エジプト', 'セントルシア', 'セーシェル', 'シンガポール', 'ボリビア', 'カーボベルデ', 'ドミニカ共和国', 'ニウエ', 'トンガ', 'ニカラグア', 'ピトケアン諸島', 'セルビア', 'イギリス領ヴァージン諸島', 'フランス領ギアナ', 'イラク', 'レバノン', 'パキスタン', 'シント・マールテン', 'チュニジア', 'イギリス', 'アイスランド', 'セネガル', '韓国', 'ベネズエラ', 'サン・バルテルミー', 'ニューカレドニア', 'ノルウェー', 'ナウル', 'ボスニア・ヘルツェゴビナ', '西サハラ', 'フィンランド', 'ガーナ', '北マケドニア', 'モザンビーク', 'ネパール', 'ウクライナ', 'アルバ', 'バングラデシュ', '中央アフリカ共和国', 'モンゴル', 'ロシア', 'バーレーン', 'クリスマス島', 'デンマーク', 'ガンビア', 'キリバス', 'トルコ', 'ココス諸島', '北朝鮮', 'コソボ', '中国', 'イスラエル', 'カタール', 'オーストリア', 'フィリピン', 'リベリア', 'ルーマニア', 'コモロ', 'ラオス', 'モロッコ', 'エルサルバドル', 'シリア', 'ウォリス・フツナ', 'モーリシャス', 'レユニオン', 'スロベニア', '南スーダン', 'アルジェリア', 'ウガンダ', 'セントビンセント・グレナディーン', 'アセンション島', 'ホンジュラス', 'マリ', 'ブルンジ', 'マラウイ', 'タークス・カイコス諸島', 'タイ', 'ベルギー', 'ベラルーシ', 'ケニア', 'ベトナム', 'バミューダ', 'バハマ', 'セントクリストファー・ネイビス', 'ベナン', 'ブルネイ', 'ドイツ', 'トリニダード・トバゴ', 'ブルガリア', 'パレスチナ', 'アメリカ合衆国', 'コンゴ民主共和国', 'カメルーン', 'ジブチ', 'イタリア', 'フランス領ポリネシア', 'ブーベ島', 'グアテマラ']
  - input:text `統計品目 (HS) コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / variant thumbnail NAVY / M
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / variant thumbnail NAVY / M

## /admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/automatic_add_rules

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/automatic_add_rules`
- headings: 自動追加ルール
- buttons: stack-ps-yosuke 陽介 河野 / 追加する
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/catalog_product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/catalog_product_variants`
- headings: SKU一覧
- tabs: すべて
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 商品 | 品番(SKU)
  - アイテムを選択する | ポケモン UT RED / 120(6-7歳) | 483674-15-120
  - アイテムを選択する | ポケモン UT RED / 140(10-11歳) | 483674-15-140
  - アイテムを選択する | ポケモン UT RED / 110(4-5歳) | 483674-15-110

## /admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/create

- finalUrl: `https://www.sqstackstaging.com/admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog/create`
- headings: カタログに商品を追加する
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `商品コードで検索する` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `商品コードで検索する`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 商品 | 商品コード
  - アイテムを選択する | product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 | TEST_FAQ_20260624_GU_092214
  - アイテムを選択する | product thumbnail TEST_20260622_OPTION | TEST_20260622_OPTION
  - アイテムを選択する | product thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 | TEST_E2E_20260622_GU_1905

## /admin/csv_export/csv_export_operation_inventory_logical_quantities/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_logical_quantities/create`
- headings: 在庫をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / エクスポートを開始する
- fields:
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/inventory_items/9f6a69fe-ed14-580f-8b84-0fdc29a2a94f_InventoryItem/history

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items/9f6a69fe-ed14-580f-8b84-0fdc29a2a94f_InventoryItem/history`
- headings: TEST_FAQ_20260624 GU検証Tシャツ 092214
- buttons: stack-ps-yosuke 陽介 河野 / 選択
- fields:
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant

- finalUrl: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- headings: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価 / 販売 / 配送
- buttons: stack-ps-yosuke 陽介 河野 / 画像を選択する / 原価を登録する / 更新する
- fields:
  - select:select-one `カラー` required=False disabled=False options=['選択してください', 'NAVY / M']
  - input:number `上代` required=False disabled=False
  - input:text `SKU (最小管理単位)` required=False disabled=False
  - input:text `メーカーSKU` required=False disabled=False
  - input:checkbox `在庫を追跡する` required=False disabled=False checked=True
  - input:checkbox `在庫切れの場合でも販売を続ける` required=False disabled=False checked=False
  - input:text `バーコード` required=False disabled=False
  - input:text `JAN` required=False disabled=False
  - input:text `EAN` required=False disabled=False
  - input:text `UPC` required=False disabled=False
  - input:number `重量` required=False disabled=False
  - select:select-one `単位` required=False disabled=False options=['グラム', 'キログラム', 'オンス', 'ポンド']
  - input:checkbox `配送を必須にする` required=False disabled=False checked=True
  - select:select-one `原産国コード` required=False disabled=False options=['選択してください', 'アルメニア', 'フィジー', 'カタール', 'セントヘレナ', 'トーゴ', 'トルコ', 'タンザニア', 'セルビア', 'エスワティニ', 'イエメン', 'ボツワナ', 'ギニアビサウ', '南アフリカ', 'アンドラ', 'ドミニカ国', '赤道ギニア', 'サン・マルタン', 'マダガスカル', 'フランス南方・南極地域', 'サン・バルテルミー', 'ウクライナ', 'エクアドル', 'ジャマイカ', 'アルジェリア', 'フランス', 'サンマリノ', 'フィンランド', 'グレナダ', 'アフガニスタン', 'ブーベ島', 'リベリア', 'モルディブ', 'アンティグア・バーブーダ', 'ベリーズ', 'ニカラグア', 'フィリピン', 'オーランド諸島', 'イラン', 'キリバス', 'スリランカ', 'シント・マールテン', 'ザンビア', 'チリ', 'モンゴル', 'シンガポール', 'トリニダード・トバゴ', 'スイス', 'エチオピア', 'バングラデシュ', 'コンゴ民主共和国', 'グリーンランド', 'カーボベルデ', 'ノーフォーク島', 'イスラエル', 'パレスチナ', 'スヴァールバル諸島およびヤンマイエン島', 'ボスニア・ヘルツェゴビナ', 'バミューダ', 'ベラルーシ', 'コートジボワール', 'イギリス', 'チュニジア', 'ウズベキスタン', 'ブルガリア', 'クウェート', 'ミャンマー', 'チェコ', 'フォークランド諸島', 'モルドバ', 'ペルー', '合衆国領有小離島', 'ジンバブエ', '香港', 'モーリシャス', 'スロベニア', 'バヌアツ', 'マヨット', 'ブルネイ', 'ブータン', 'デンマーク', 'サウスジョージア・サウスサンドウィッチ諸島', 'ハイチ', 'リトアニア', '南スーダン', 'スペイン', 'ジブラルタル', 'ガイアナ', 'メキシコ', '中央アフリカ共和国', 'ヨルダン', 'モナコ', 'コンゴ共和国', 'クック諸島', 'グアドループ', 'アイスランド', 'モンテネグロ', 'レユニオン', '台湾', 'オーストリア', 'ブルキナファソ', 'オランダ領カリブ', 'キューバ', 'ハンガリー', 'ウォリス・フツナ', 'ガボン', 'フランス領ポリネシア', 'サウジアラビア', 'エリトリア', '韓国', 'モントセラト', 'ナウル', 'ジブチ', 'ナミビア', 'ドミニカ共和国', 'ハード島とマクドナルド諸島', 'オランダ', 'ピトケアン諸島', 'ソマリア', '西サハラ', 'イラク', 'ポーランド', 'アンゴラ', 'アイルランド', 'カンボジア', 'コモロ', 'カザフスタン', 'ラオス', 'バチカン市国', 'ケニア', '北マケドニア', 'エルサルバドル', 'トルクメニスタン', 'バーレーン', '中国', 'リビア', 'パナマ', 'タークス・カイコス諸島', 'セネガル', 'フランス領ギアナ', 'モザンビーク', 'オマーン', 'タイ', 'アセンション島', 'キプロス', 'マン島', 'ルーマニア', 'ホンジュラス', 'セントクリストファー・ネイビス', 'アメリカ合衆国', 'カナダ', 'エジプト', 'キルギス', 'ニュージーランド', 'パラグアイ', 'アルゼンチン', 'ブラジル', 'キュラソー', 'トリスタン・ダ・クーニャ', 'ラトビア', 'スロバキア', 'ウルグアイ', 'バルバドス', 'ルクセンブルク', 'マルティニーク', 'ギニア', 'イギリス領インド洋地域', 'マルタ', 'ブルンジ', 'クリスマス島', 'ケイマン諸島', 'ベネズエラ', 'コソボ', 'アルバニア', 'オランダ領アンティル', 'インドネシア', 'ニジェール', 'スリナム', 'ベトナム', 'サモア', 'ガーンジー', 'ギリシャ', 'パキスタン', 'サンピエール・ミクロン', 'ジョージア', 'ポルトガル', 'トンガ', 'アゼルバイジャン', 'トケラウ', 'ウガンダ', 'アンギラ', 'マリ', 'パプアニューギニア', 'チャド', 'アルバ', 'ココス諸島', 'クロアチア', 'イタリア', 'ソロモン諸島', 'セントビンセント・グレナディーン', 'エストニア', 'リヒテンシュタイン', '東ティモール', 'コスタリカ', 'ガーナ', 'モロッコ', 'ネパール', 'サントメ・プリンシペ', 'ジャージー', 'レバノン', 'レソト', 'マラウイ', 'アラブ首長国連邦', 'ベナン', 'インド', 'セントルシア', 'ニューカレドニア', 'カメルーン', 'モーリタニア', 'セーシェル', 'シエラレオネ', 'バハマ', 'ドイツ', 'フェロー諸島', 'スウェーデン', 'シリア', 'ツバル', 'コロンビア', 'ナイジェリア', 'ロシア', 'その他の地域', '日本', 'ルワンダ', 'ガンビア', 'グアテマラ', 'スーダン', 'タジキスタン', 'ベルギー', 'ボリビア', '北朝鮮', 'オーストラリア', 'マカオ', 'マレーシア', 'ノルウェー', 'ニウエ', 'イギリス領ヴァージン諸島']
  - input:text `統計品目 (HS) コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / variant thumbnail NAVY / M
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / variant thumbnail NAVY / M

## /admin/inventory_outbound_orders/9adf7a2b-802f-5b6c-9d05-ea3e07a7c5f7_InventoryOutboundOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_outbound_orders/9adf7a2b-802f-5b6c-9d05-ea3e07a7c5f7_InventoryOutboundOrder`
- headings: #IO-1024 / 出荷明細 / 出荷履歴 / 詳細 / 出荷先ロケーション / 作成元
- buttons: stack-ps-yosuke 陽介 河野 / 出荷実績を登録する (disabled) / 出荷実績の明細を展開する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - input:text `配送方法` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 出荷予定 | 出荷済み
  - product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M | TEST_FAQ_20260624_GU_092214_NAVY_M | 1 | 1

## /admin/inventory_inbound_orders/02acb020-1de9-50f6-b342-d539b2998d1b_InventoryInboundOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_inbound_orders/02acb020-1de9-50f6-b342-d539b2998d1b_InventoryInboundOrder`
- headings: #II-1024 / 入荷明細 / 入荷履歴 / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / 入荷実績の明細を展開する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - input:text `種別` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `入荷実績の明細を展開する`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 入荷予定 | 入荷済み
  - product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M | TEST_FAQ_20260624_GU_092214_NAVY_M | 1 | 1

## /admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/usages

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/usages`
- headings: TEST_FAQ_DEEP3_202606080345_ディスカウント / 利用履歴
- tabs: 利用履歴
- buttons: stack-ps-yosuke 陽介 河野 / 利用履歴 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/customers

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/customers`
- headings: TEST_FAQ_DEEP3_202606080345_ディスカウント / 顧客管理
- tabs: 顧客管理
- buttons: stack-ps-yosuke 陽介 河野 / 顧客管理 / 追加する / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:text `メールアドレスで検索する` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 追加する
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 追加する
  - `メールアドレスで検索する`: stack-ps-yosuke 陽介 河野 / 追加する

## /admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/locations

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/locations`
- headings: TEST_FAQ_DEEP3_202606080345_ディスカウント / 店舗管理
- tabs: 店舗管理
- buttons: stack-ps-yosuke 陽介 河野 / 店舗管理 / 追加する / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / 追加する
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / 追加する

## /admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/product_variants

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/product_variants`
- headings: TEST_FAQ_DEEP3_202606080345_ディスカウント / 商品管理
- tabs: 商品管理
- buttons: stack-ps-yosuke 陽介 河野 / 商品管理 / 追加する / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration/sites

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration/sites`
- headings: OmnibusCore連携 (TEST_MAKER_001) / 連携サイト
- tabs: 連携サイト
- buttons: stack-ps-yosuke 陽介 河野 / 連携サイト / 追加する / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration/notification_emails

- finalUrl: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration/notification_emails`
- headings: OmnibusCore連携 (TEST_MAKER_001) / 通知メール
- tabs: 通知メール
- buttons: stack-ps-yosuke 陽介 河野 / 通知メール / 追加する / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/apps/9081ef6c-dc90-50be-9bb8-d869eb02f44f_App/admin_api

- finalUrl: `https://www.sqstackstaging.com/admin/settings/apps/9081ef6c-dc90-50be-9bb8-d869eb02f44f_App/admin_api`
- headings: リクエストログ
- status: TODO表示あり
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_unit_costs/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_unit_costs/create`
- headings: 原価をCSVで一括取り込みする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_price_rule_regular_prices/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_price_rule_regular_prices/create`
- headings: 通常価格をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `販売価格ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_販売価格ルール (JPY)', 'TEST_FAQ_販売価格ルール_遷移確認_20260607 (JPY)', 'TEST_FAQ_DEEP_202606080340_販売価格ルール (JPY)']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_price_rule_sale_prices/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_price_rule_sale_prices/create`
- headings: セール価格をCSVでインポートする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `販売価格ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_販売価格ルール (JPY)', 'TEST_FAQ_販売価格ルール_遷移確認_20260607 (JPY)', 'TEST_FAQ_DEEP_202606080340_販売価格ルール (JPY)']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_threshold_rule_product_variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_threshold_rule_product_variants/create`
- headings: 販売閾値をCSVで一括取り込みする
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `販売閾値ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_販売閾値ルール', 'TEST_FAQ_販売閾値ルール_遷移確認_20260607', 'TEST_FAQ_DEEP_202606080340_販売閾値ルール']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_customer_rank_baselines/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_customer_rank_baselines/create`
- headings: 基準ランクをCSVで一括設定する
- buttons: stack-ps-yosuke 陽介 河野 / ファイルを選択する / 保存する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:file `ファイルをアップロード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_products/43a9a5c7-2508-57e2-a635-f00e74e8f388_CSVImportOperationProduct/validation_failure

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/43a9a5c7-2508-57e2-a635-f00e74e8f388_CSVImportOperationProduct/validation_failure`
- headings: 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_variants/b5f17d05-6079-5458-8a15-d27d35384046_CSVImportOperationProductVariant/validation_failure

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_variants/b5f17d05-6079-5458-8a15-d27d35384046_CSVImportOperationProductVariant/validation_failure`
- headings: 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_product_images/f0d331a0-11dc-52f6-a94b-c4a7f8ee8652_CSVImportOperationProductImage/validation_failure

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_product_images/f0d331a0-11dc-52f6-a94b-c4a7f8ee8652_CSVImportOperationProductImage/validation_failure`
- headings: 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity/validation_success

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity/validation_success`
- headings: 検証成功
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: バリエーション | SKU | ロケーション | ロケーションコード | 数量
  - オーバーサイズスウェットシャツ BLACK / XL | 486125-09-XL | ユニクロEC | TESTEC01 | 0

## /admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity/validation_failure

- finalUrl: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_inventory_logical_available_quantities/79645096-e1de-599f-a34d-df63662d3be3_CSVImportOperationInventoryLogicalAvailableQuantity/validation_failure`
- headings: 検証失敗
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_product_price_rule_sale_prices/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_product_price_rule_sale_prices/create`
- headings: セール価格をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / エクスポートを開始する
- fields:
  - select:select-one `販売価格ルール` required=False disabled=False options=['販売価格ルールを選択してください', 'TEST_FAQ_販売価格ルール (JPY)', 'TEST_FAQ_販売価格ルール_遷移確認_20260607 (JPY)', 'TEST_FAQ_DEEP_202606080340_販売価格ルール (JPY)']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/csv_export/csv_export_operation_point_changes/create

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_point_changes/create`
- headings: ポイント変動履歴をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / エクスポートを開始する
- fields:
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - input:datetime-local `開始日時` required=False disabled=False
  - input:datetime-local `終了日時` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
