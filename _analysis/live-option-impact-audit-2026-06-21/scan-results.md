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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / インポート
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / インポート
- table1: すべてのアイテムを選択する | 商品 | ステータス | 商品コード | 在庫 | カタログ | 商品タイプ | 製造元
  - アイテムを選択する | product thumbnail 半袖シャツ | 成功 公開中 | 8128502395 | 2個のバリエーション | 0 | GU
  - アイテムを選択する | product thumbnail GU3 | 成功 公開中 | TEST_FAQ_CSV_RECHECK_20260608_01 | 0個のバリエーション | 0 | GU
  - アイテムを選択する | product thumbnail GU2 | 成功 公開中 | test_faq_deep2_202606080343_product | 0個のバリエーション | 0 | 検証 | GU

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `検索結果を並べ替える`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
  - アイテムを選択する | product variant thumbnail 半袖シャツ M / グレー | 21 | 0 | 0 | 0 | 0
  - アイテムを選択する | product variant thumbnail 半袖シャツ S / グレー | 124 | 0 | 0 | 0 | 0
  - アイテムを選択する | バギーカーブジーンズ BLUE / 36 | 487973-64-36 | 97 | 0 | 0 | 97

## /admin/inventory_movement_orders

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders`
- headings: 移動伝票
- tabs: すべて / 出荷作業 / 一部受領済み / 受領済み / キャンセル
- buttons: stack-ps-yosuke 陽介 河野 / すべて / 出荷作業 (disabled) / 一部受領済み (disabled) / 受領済み (disabled) / キャンセル / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 管理番号 | 配送元 | 配送先 | ステータス | 作成日時
  - #IM-1022 | ユニクロ物流倉庫 | ユニクロ - 銀座店 | 成功 完了 入荷完了 | 2026年06月21日 14:03
  - #IM-1021 | TEST_FAQ_DEEP2_202606080343_ロケーション | GU 銀座店 | 成功 完了 入荷完了 | 2026年06月21日 13:57
  - #IM-1020 | ユニクロ - 銀座店 | ユニクロ物流倉庫 | 成功 完了 入荷完了 | 2026年06月21日 12:34

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `検索結果を並べ替える`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 管理番号 | ロケーション | ステータス | 作成日 | 実施日
  - アイテムを選択する | #IA-1009 | ユニクロ物流倉庫 | 完了 実施済み | 2026年06月18日 22:33 | 2026年06月18日 22:33
  - アイテムを選択する | #IA-1008 | ユニクロ物流倉庫 | 完了 実施済み | 2026年06月18日 22:32 | 2026年06月18日 22:32
  - アイテムを選択する | #IA-1007 | ユニクロ物流倉庫 | 警告 キャンセル | 2026年06月18日 22:30

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
  - select:select-one `国/地域` required=False disabled=False options=['国/地域', 'フィジー', 'セントクリストファー・ネイビス', 'モルディブ', 'アンゴラ', 'ボスニア・ヘルツェゴビナ', 'カメルーン', 'ジョージア', 'タンザニア', 'フィンランド', 'ナミビア', 'セルビア', 'ウォリス・フツナ', 'コソボ', 'アンギラ', 'チェコ', 'ラトビア', 'ベリーズ', 'サウジアラビア', 'チュニジア', 'トリニダード・トバゴ', 'コモロ', 'エルサルバドル', 'フェロー諸島', 'ガイアナ', 'ネパール', 'セントヘレナ', 'オーストリア', 'ベラルーシ', 'ココス諸島', 'ジブラルタル', 'インド', 'ソマリア', 'ドイツ', 'セントルシア', '東ティモール', 'バーレーン', 'バハマ', 'パラグアイ', 'アセンション島', 'ブルンジ', 'ブータン', 'ブーベ島', 'グアテマラ', 'サン・マルタン', 'トーゴ', 'ブルネイ', 'インドネシア', 'リトアニア', 'レユニオン', 'セントビンセント・グレナディーン', 'マヨット', 'ノーフォーク島', 'ウガンダ', 'イギリス領ヴァージン諸島', 'アラブ首長国連邦', 'アルバ', 'コスタリカ', 'キューバ', 'ホンジュラス', 'スリランカ', '合衆国領有小離島', 'ギニア', 'タイ', 'チリ', 'ドミニカ共和国', 'エクアドル', 'ジャージー', 'オーストラリア', 'チャド', 'マルティニーク', 'ピトケアン諸島', 'シンガポール', 'バチカン市国', 'フランス', 'キリバス', 'モルドバ', 'ナイジェリア', 'トルクメニスタン', 'ジブチ', 'ガーンジー', 'ハード島とマクドナルド諸島', 'アイスランド', 'マラウイ', 'ニューカレドニア', 'スウェーデン', 'コートジボワール', 'リビア', 'ポルトガル', 'トケラウ', 'フォークランド諸島', 'ハイチ', 'カザフスタン', 'モンテネグロ', 'エストニア', 'モンゴル', 'キュラソー', 'ガーナ', 'グリーンランド', 'ペルー', 'バングラデシュ', '西サハラ', 'イラン', '北朝鮮', '韓国', 'レソト', 'その他の地域', 'ボリビア', 'ニカラグア', 'ブルキナファソ', 'サン・バルテルミー', 'モーリタニア', 'ツバル', 'アフガニスタン', 'ドミニカ国', 'タジキスタン', 'タークス・カイコス諸島', 'ギリシャ', 'サモア', 'ベルギー', 'ブラジル', 'サンマリノ', 'トルコ', '北マケドニア', 'ノルウェー', 'パプアニューギニア', 'ルーマニア', 'セーシェル', 'シリア', 'コロンビア', 'カーボベルデ', 'クリスマス島', 'キプロス', 'ヨルダン', 'マカオ', 'ナウル', 'アルメニア', 'バミューダ', 'エジプト', 'ニウエ', 'オマーン', 'シエラレオネ', 'モロッコ', '南スーダン', 'パキスタン', 'セネガル', 'イエメン', 'ベナン', '日本', 'シント・マールテン', 'オランダ領カリブ', 'サウスジョージア・サウスサンドウィッチ諸島', 'エスワティニ', 'ガンビア', 'イタリア', 'マリ', 'オーランド諸島', '中央アフリカ共和国', 'エチオピア', 'モザンビーク', 'リベリア', 'ニュージーランド', 'スヴァールバル諸島およびヤンマイエン島', 'ザンビア', 'マルタ', 'コンゴ民主共和国', 'スペイン', 'グアドループ', 'カンボジア', 'クウェート', 'スロベニア', 'カナダ', 'スイス', 'フランス領ギアナ', 'イギリス領インド洋地域', 'キルギス', 'ルクセンブルク', 'モーリシャス', 'パナマ', 'アンティグア・バーブーダ', 'クロアチア', '台湾', 'アルジェリア', 'エリトリア', 'イギリス', 'マン島', 'マレーシア', 'フィリピン', 'パレスチナ', 'オランダ領アンティル', 'ニジェール', 'ベトナム', 'ジンバブエ', 'ギニアビサウ', 'イラク', 'ラオス', 'モナコ', 'ロシア', 'ルワンダ', 'ウルグアイ', 'バヌアツ', 'メキシコ', 'フランス南方・南極地域', 'アメリカ合衆国', 'アンドラ', 'コンゴ共和国', 'アイルランド', 'オランダ', 'フランス領ポリネシア', 'サンピエール・ミクロン', 'サントメ・プリンシペ', 'トリスタン・ダ・クーニャ', 'アルバニア', 'アゼルバイジャン', 'スーダン', 'スロバキア', 'ケイマン諸島', 'モントセラト', 'トンガ', '赤道ギニア', 'ケニア', 'ボツワナ', 'デンマーク', 'イスラエル', 'レバノン', 'スリナム', 'クック諸島', 'リヒテンシュタイン', 'マダガスカル', 'ガボン', 'ハンガリー', 'ジャマイカ', 'ポーランド', 'ソロモン諸島', 'ウクライナ', 'ウズベキスタン', 'ベネズエラ', 'アルゼンチン', '中国', 'ミャンマー', 'バルバドス', 'ブルガリア', 'グレナダ', '香港', 'カタール', '南アフリカ']
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
  - select:select-one `取引先` required=False disabled=False options=['選択してください', 'TEST_FAQ_Supplier', 'TEST_FAQ_Supplier2', 'TEST_FAQ_DEEP_202606080340_取引先']
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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- buttons: 情報取得中... S / すべて / 有効 / スケジュール済み / 期限切れ / 検索と絞り込みの結果 / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: 情報取得中... S
  - `情報取得中...`: 情報取得中... S
- table1: すべてのアイテムを選択する | タイトル | クーポンコード | ステータス | 有効期間 | 対象顧客 | 対象店舗 | 利用回数 | テナント
  - アイテムを選択する | TEST_FAQ_DEEP3_202606080345_ディスカウント | TEST-FAQ-DEEP3-202606080345-DISC | 成功 有効 | 2026年06月08日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ
  - アイテムを選択する | TEST_FAQ_ディスカウント_対象商品テスト | TEST-FAQ-001 | 成功 有効 | 2026年01月01日 00:00 - 2026年12月31日 23:59 | 0人 | 0件 | 0回 | ユニクロ

## /admin/order_price_adjustment_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/order_price_adjustment_rules/create`
- headings: ディスカウントを作成する / 基本情報 / 割引設定 / 適用条件 / 割引要件 / 対象商品 / 利用制限 / 有効期間
- buttons: 情報取得中... S / 保存する
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
  - `button`: 情報取得中... S
  - `情報取得中...`: 情報取得中... S

## /admin/point_calculation_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules`
- headings: 注文ポイント
- buttons: 情報取得中... S / 前へ (disabled) / 次へ (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: 情報取得中... S
  - `情報取得中...`: 情報取得中... S
- table1: すべてのアイテムを選択する | ルール | 利用テナント数
  - アイテムを選択する | TEST_FAQ_注文ポイント付与ルール | 0件

## /admin/point_calculation_rules/create

- finalUrl: `https://www.sqstackstaging.com/admin/point_calculation_rules/create`
- headings: 注文ポイント付与ルールを作成する / ルール / 有効期限 / オンライン注文のポイント有効までの日数 / 店舗注文のポイント有効までの日数 / 会員ランク算出ルール / ポイントキャンペーン
- buttons: 情報取得中... S / 保存する
- fields:
  - input:text `タイトル` required=False disabled=False
  - input:number `購入金額` required=False disabled=False
  - input:number `ポイント` required=False disabled=False
  - input:checkbox `付与対象にポイント利用分を含める` required=False disabled=False checked=False
  - input:number `ポイントを付与してから有効な日数` required=False disabled=False
  - input:number `日後` required=False disabled=False
  - input:number `日後` required=False disabled=False
  - select:select-one `会員ランク算出ルール` required=False disabled=False options=['選択してください', 'TEST_FAQ_会員ランク算出ルール', 'TEST_FAQ_RANK_20260615081841']
  - input:radio `開始日時が新しいキャンペーンを優先する` required=False disabled=False checked=True
  - input:radio `開始日時が古いキャンペーンを優先する` required=False disabled=False checked=False
- opened choices:
  - `button`: 情報取得中... S
  - `情報取得中...`: 情報取得中... S

## /admin/point_campaign_order_rules

- finalUrl: `https://www.sqstackstaging.com/admin/point_campaign_order_rules`
- headings: ポイントキャンペーン
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/retail_portal_integrations/create

- finalUrl: `https://www.sqstackstaging.com/admin/retail_portal_integrations/create`
- headings: リテールポータル
- buttons: stack-ps-yosuke 陽介 河野 / 選択 / 保存する
- fields:
  - input:text `店舗ロケーション` required=False disabled=False
  - input:text `在庫ロケーション` required=False disabled=False
  - select:select-one `テナント` required=False disabled=False options=['選択してください', 'ユニクロ', 'TEST_FAQ_COVERAGE_20260615_テナント_EDIT', 'テストテナント']
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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
- headings: ユーザーを追加する / 権限
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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- headings: なし

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
  - TEST_FAQ_DEEP2_202606080343_ロケーション | test_faq_deep2_202606080343_loc | 情報 店舗 | 情報 非公開 | アーカイブ済み | 0個のグループ

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | コード
  - アイテムを選択する | TEST_FAQ_DEEP_202606080340_取引先 | 0dabc6a0-93aa-5f3e-8044-7c4daa44d9f4_InventorySupplier
  - アイテムを選択する | TEST_FAQ_Supplier2 | 4fc9262b-9c99-5d50-a4dd-613cc724e014_InventorySupplier
  - アイテムを選択する | TEST_FAQ_Supplier | e7233b1a-c53d-56e4-b8c6-b1c7a32b8f15_InventorySupplier

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `販売員コードで検索する`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

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
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: すべてのアイテムを選択する | 名前 | 言語 | 作成日時
  - アイテムを選択する | Test_中国語 | 中国語（簡体字） | 2026年06月16日 17:33
  - アイテムを選択する | TEST_FAQ_翻訳ルール_英語 | 英語 | 2026年06月07日 08:41
  - アイテムを選択する | TEST_FAQ_英語翻訳ルール | 英語 | 2026年06月06日 18:57

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
- headings: メタフィールド定義 / 組織 / 商品 / バリエーション / 顧客 / 注文 / 下書き注文 / 会社
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/create`
- headings: undefinedメタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/product_measurement_rules

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules`
- headings: 採寸ルール
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: ルール名 | 単位 | 採寸項目
  - TEST_FAQ_COVERAGE_20260615_159330_採寸 | センチメートル | 肩幅
  - TEST_FAQ_DEEP_202606080340_採寸ルール | センチメートル | 肩幅
  - TEST_FAQ_採寸ルール_トップス | センチメートル | 肩幅

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
  - select:select-one `カタログ` required=False disabled=False options=['カタログを選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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

## /admin/products/58e74a25-b86c-5bc3-bc1f-c232b2dbf51f_Product

- finalUrl: `https://www.sqstackstaging.com/admin/products/58e74a25-b86c-5bc3-bc1f-c232b2dbf51f_Product`
- headings: 半袖シャツ / 商品コード / メディア（0件） / バリエーション / 検索エンジンリスティング / ステータス / 商品分類 / タグ
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 追加 / サイズを展開する / カラーを展開する / 選択 / 保存する (disabled)
- fields:
  - input:text `商品名` required=False disabled=False
  - textarea:text `説明文` required=False disabled=False
  - input:file `画像をアップロード` required=False disabled=False
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
  - input:text `ページタイトル` required=False disabled=False
  - textarea:text `メタディスクリプション` required=False disabled=False
  - select:select-one `公開中` required=False disabled=False options=['公開中', '下書き']
  - input:text `商品タイプ` required=False disabled=False
  - input:text `製造元` required=False disabled=False
  - input:text `ブランド` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `サイズを展開する`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `カラーを展開する`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `ブランド`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: すべてのアイテムを選択する | バリエーション | 価格
  - アイテムを選択する | product variant thumbnail S / グレー SKU: 124 | ￥20,000
  - アイテムを選択する | product variant thumbnail M / グレー SKU: 21 | ￥9,980

## /admin/csv_export/csv_export_operation_inventory_logical_quantities

- finalUrl: `https://www.sqstackstaging.com/admin/csv_export/csv_export_operation_inventory_logical_quantities`
- headings: 在庫をCSVでエクスポートする
- buttons: stack-ps-yosuke 陽介 河野 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/inventory_items/9f2fb021-cdce-59dd-8400-66d0bd815d61_InventoryItem

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items/9f2fb021-cdce-59dd-8400-66d0bd815d61_InventoryItem`
- headings: 半袖シャツ / M / グレー / 選択中のロケーション：
- tabs: すべて / 店舗 / 倉庫
- buttons: stack-ps-yosuke 陽介 河野 / その他のアクション / 選択してください / すべて / 店舗 / 倉庫 / 検索と絞り込みの結果 / 販売可能数を編集 / 前へ (disabled) / 次へ (disabled)
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他のアクション
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他のアクション
  - `その他のアクション`: stack-ps-yosuke 陽介 河野 / その他のアクション
- table1: ロケーション | 販売可能 | 引当済み | 取置中 | 破損 | 検品 | 予備 | 手持ち | 積送中 | 入荷予定
  - GU 倉庫 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0
  - GU 銀座店 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0
  - TEST_FAQ_DEEP2_202606080343_ロケーション | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0

## /admin/inventory_movement_orders/fd048e5c-050e-5fe2-afe5-ddad3d09afa9_InventoryMovementOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_movement_orders/fd048e5c-050e-5fe2-afe5-ddad3d09afa9_InventoryMovementOrder`
- headings: #IM-1022 / 外部システムから連携されている移動伝票です / 配送元 / 配送先 / 商品 / 詳細 / 関連
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: 商品 | 数量
  - 486125-09-XL | 1
  - 486125-31-XL | 1
  - 487973-64-36 | 1

## /admin/inventory_adjustment_orders/4dffea8e-dea2-5327-8844-90862115e523_InventoryAdjustmentOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/4dffea8e-dea2-5327-8844-90862115e523_InventoryAdjustmentOrder`
- headings: #IA-1009 / ロケーション / 商品 / 詳細
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | 商品コード | SKU | 増減数
  - エアリズムコットンT PINK / L | 483457 | 483457-10-L | -1

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

## /admin/inventory_allocation_requests/396629c7-27d6-57af-b652-dcc9691eb4f6_InventoryAllocationRequest

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/396629c7-27d6-57af-b652-dcc9691eb4f6_InventoryAllocationRequest`
- headings: 在庫依頼 / 対象商品 / 確保済み在庫 / 依頼先
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 依頼先の操作 (disabled)
- fields:
  - input:checkbox `すべてのアイテムを選択する` required=False disabled=False checked=False
  - input:checkbox `アイテムを選択する` required=False disabled=False checked=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作
- table1: すべてのアイテムを選択する | ロケーション | 確保数 | 移動伝票 | 確保日時
  - アイテムを選択する | ユニクロEC | 1 | 2026年06月21日 12:03
- table2: ロケーション | 販売可能数
  - ユニクロEC | 成功 確保済 | 0

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
  - select:select-one `カタログ` required=False disabled=False options=['選択してください', 'TEST_FAQ_カタログ001', 'TEST_FAQ_DEEP_202606080340_カタログ', 'UNIQLO']
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

## /admin/settings/users/user_358DNqj6iJtcvMhxAwTLlCzyGWU

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_358DNqj6iJtcvMhxAwTLlCzyGWU`
- headings: サポートアカウントStack / 基本情報 / ユーザーテナント / 権限
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=False
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['選択してください', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作

## /admin/settings/users/user_35E68KNK1pCOobD4ZwdoaHsnNo0

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_35E68KNK1pCOobD4ZwdoaHsnNo0`
- headings: 福田涼介 / 基本情報 / ユーザーテナント / 権限
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['選択してください', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作

## /admin/settings/users/user_3CbpZwl1x5ohfuyFmuv1t8VQXyo

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3CbpZwl1x5ohfuyFmuv1t8VQXyo`
- headings: 菅野将貴 / 基本情報 / ユーザーテナント / 権限
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['選択してください', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作

## /admin/settings/users/user_3Dz5ZnyYjoaDwlnz2ffJE7NZTGb

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3Dz5ZnyYjoaDwlnz2ffJE7NZTGb`
- headings: 河野陽介 / 基本情報 / ユーザーテナント / 権限
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=False
  - input:checkbox `テストテナント` required=False disabled=False checked=False
  - select:select-one `権限グループ` required=False disabled=False options=['選択してください', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作

## /admin/settings/users/user_3FOeZAow9g1pTX8HYyjifwXk4re

- finalUrl: `https://www.sqstackstaging.com/admin/settings/users/user_3FOeZAow9g1pTX8HYyjifwXk4re`
- headings: 権限テスト / 基本情報 / ユーザーテナント / 権限
- buttons: stack-ps-yosuke 陽介 河野 / その他の操作 / 保存する
- fields:
  - input:text `姓` required=False disabled=False
  - input:text `名` required=False disabled=False
  - input:email `メールアドレス` required=False disabled=False
  - input:checkbox `ユニクロ` required=False disabled=False checked=True
  - input:checkbox `TEST_FAQ_COVERAGE_20260615_テナント_EDIT` required=False disabled=False checked=True
  - input:checkbox `テストテナント` required=False disabled=False checked=True
  - select:select-one `権限グループ` required=False disabled=False options=['選択してください', '特権管理者', 'TEST_権限検証_20260620']
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / その他の操作
  - `その他の操作`: stack-ps-yosuke 陽介 河野 / その他の操作

## /admin/settings/tenants/cee012a1-a15a-5ec5-871f-5e41a330617f_Tenant

- finalUrl: `https://www.sqstackstaging.com/admin/settings/tenants/cee012a1-a15a-5ec5-871f-5e41a330617f_Tenant`
- headings: テストテナント / 基本情報 / CRM
- buttons: stack-ps-yosuke 陽介 河野 / 基本情報を編集する / テナントIDをコピーする / 保存する (disabled)
- fields:
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

## /admin/settings/translation/translation_rules/19b42234-5a07-55fa-812f-4e483d8f2a99_TranslationRule

- finalUrl: `https://www.sqstackstaging.com/admin/settings/translation/translation_rules/19b42234-5a07-55fa-812f-4e483d8f2a99_TranslationRule`
- headings: Test_中国語 / 各種設定 / 商品 / カスタマイズ項目を追加する / 商品オプション / カスタマイズ項目を追加する / 商品オプション値 / カスタマイズ項目を追加する
- buttons: stack-ps-yosuke 陽介 河野 / 保存する (disabled)
- fields:
  - input:text `名前` required=False disabled=False
  - select:select-one `言語` required=False disabled=True options=['日本語', '英語', '中国語（簡体字）', '中国語（繁体字）', '韓国語', 'スペイン語', 'フランス語', 'ドイツ語', 'ヒンディー語', 'タイ語']
  - input:checkbox `翻訳データを自動で作成する` required=False disabled=False checked=True
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

## /admin/settings/metafield_definitions/organization

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/organization`
- headings: 組織メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/product

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/product`
- headings: 商品メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/product_variant

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/product_variant`
- headings: バリエーションメタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/purchasing_customer

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/purchasing_customer`
- headings: 顧客メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/order`
- headings: 注文メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/draft_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/draft_order`
- headings: 下書き注文メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/company

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/company`
- headings: 会社メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/location

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/location`
- headings: ロケーションメタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/order_price_adjustment_rule

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/order_price_adjustment_rule`
- headings: ディスカウントメタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_movement_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_movement_order`
- headings: 在庫移動伝票メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_adjustment_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_adjustment_order`
- headings: 在庫調整伝票メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_reservation_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_reservation_order`
- headings: 在庫取置伝票メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_purchase_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_purchase_order`
- headings: 発注伝票メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_inbound_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_inbound_order`
- headings: 入荷指示メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_outbound_order

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_outbound_order`
- headings: 出荷指示メタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/inventory_supplier

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_supplier`
- headings: 仕入れ先ベンダーメタフィールドの定義
- buttons: stack-ps-yosuke 陽介 河野
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野

## /admin/settings/metafield_definitions/create/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/create/create`
- headings: undefinedメタフィールドの定義を追加する
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

## /admin/settings/product_measurement_rules/c0b14297-a257-5868-a913-5b05b199f8f6_ProductMeasurementRule

- finalUrl: `https://www.sqstackstaging.com/admin/settings/product_measurement_rules/c0b14297-a257-5868-a913-5b05b199f8f6_ProductMeasurementRule`
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

## /admin/products/58e74a25-b86c-5bc3-bc1f-c232b2dbf51f_Product/variants/create

- finalUrl: `https://www.sqstackstaging.com/admin/products/58e74a25-b86c-5bc3-bc1f-c232b2dbf51f_Product/variants/create`
- headings: バリエーションを追加する / オプション / メディア / 価格設定 / 在庫 / 販売 / 配送 / 関税情報
- buttons: stack-ps-yosuke 陽介 河野 / 画像を選択する / 作成する
- fields:
  - select:select-one `サイズ` required=False disabled=False options=['選択してください', 'S', 'M', 'L']
  - select:select-one `カラー` required=False disabled=False options=['選択してください', 'グレー', 'ブラック', 'ピンク']
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
  - select:select-one `原産国コード` required=False disabled=False options=['選択してください', 'ベルギー', 'バーレーン', 'チリ', 'フランス領ギアナ', 'イスラエル', 'モルディブ', 'ボリビア', 'コロンビア', 'マン島', 'モーリタニア', 'ナミビア', 'オランダ', 'セントビンセント・グレナディーン', 'オランダ領アンティル', 'バミューダ', 'キューバ', 'ニカラグア', 'サンピエール・ミクロン', 'ポルトガル', 'イギリス領インド洋地域', 'モロッコ', 'マルティニーク', 'ソロモン諸島', 'セントヘレナ', 'タンザニア', 'スイス', 'チェコ', 'パラグアイ', 'シンガポール', 'アフガニスタン', 'バングラデシュ', '中央アフリカ共和国', 'ハイチ', 'スロバキア', '南スーダン', 'シリア', 'ブータン', 'トケラウ', 'ベトナム', 'エチオピア', 'アイルランド', 'リトアニア', 'モントセラト', 'ノルウェー', 'セーシェル', 'ケニア', 'タジキスタン', 'バハマ', 'ベリーズ', 'マラウイ', 'ナウル', 'スウェーデン', 'クリスマス島', 'パナマ', 'リビア', 'スリナム', 'トルコ', 'ベネズエラ', 'フランス南方・南極地域', 'チュニジア', 'アンドラ', 'ボスニア・ヘルツェゴビナ', 'ブルキナファソ', 'ウガンダ', 'クウェート', 'ケイマン諸島', 'ウクライナ', 'アルゼンチン', 'セントクリストファー・ネイビス', '西サハラ', '日本', 'エスワティニ', 'トンガ', 'イギリス', 'ウズベキスタン', 'デンマーク', 'エクアドル', 'ハンガリー', 'イラク', 'マルタ', 'スーダン', 'サモア', 'コソボ', 'オランダ領カリブ', 'ココス諸島', 'ハード島とマクドナルド諸島', 'タイ', 'ブルンジ', 'ソマリア', 'タークス・カイコス諸島', 'トリニダード・トバゴ', 'サン・バルテルミー', 'コスタリカ', 'ノーフォーク島', 'クロアチア', '韓国', 'アンギラ', '中国', 'キプロス', 'ドイツ', 'インドネシア', 'インド', 'カザフスタン', 'モナコ', 'コンゴ共和国', 'コートジボワール', 'レバノン', 'マカオ', 'パプアニューギニア', 'トルクメニスタン', '台湾', 'マヨット', 'ヨルダン', 'シエラレオネ', '南アフリカ', 'その他の地域', 'ブルネイ', 'ピトケアン諸島', 'フランス領ポリネシア', 'ルーマニア', '合衆国領有小離島', 'アメリカ合衆国', 'ミャンマー', 'メキシコ', 'スペイン', 'フランス', 'リヒテンシュタイン', 'モザンビーク', 'サンマリノ', 'イタリア', 'チャド', 'ブラジル', 'クック諸島', 'カーボベルデ', 'カンボジア', 'ニューカレドニア', 'トリスタン・ダ・クーニャ', 'ザンビア', 'アルバ', 'オーストリア', 'オーランド諸島', 'ボツワナ', 'エストニア', 'フェロー諸島', 'サウジアラビア', 'バルバドス', 'ガボン', 'ガーンジー', 'ホンジュラス', 'ニウエ', 'バヌアツ', 'ガンビア', 'ガイアナ', 'ラトビア', 'モルドバ', 'パレスチナ', 'ベラルーシ', 'ガーナ', 'アイスランド', 'ポーランド', 'ジンバブエ', 'ジョージア', 'オマーン', 'スロベニア', 'セネガル', 'エリトリア', 'ナイジェリア', 'カタール', 'ロシア', 'ウォリス・フツナ', 'キルギス', 'ニュージーランド', 'サントメ・プリンシペ', 'ジャージー', 'フィリピン', 'スヴァールバル諸島およびヤンマイエン島', 'トーゴ', 'アンゴラ', 'ベナン', '赤道ギニア', 'ルワンダ', 'カナダ', 'ジブチ', 'パキスタン', 'ウルグアイ', 'エルサルバドル', 'フォークランド諸島', 'グアドループ', '北朝鮮', 'ブルガリア', 'フィンランド', 'スリランカ', '北マケドニア', 'ギニア', 'マダガスカル', 'シント・マールテン', 'カメルーン', 'アルジェリア', 'レユニオン', 'ラオス', 'イエメン', 'ドミニカ共和国', 'ギニアビサウ', 'コモロ', 'リベリア', 'ギリシャ', 'イラン', 'モンゴル', 'アンティグア・バーブーダ', 'ドミニカ国', 'サウスジョージア・サウスサンドウィッチ諸島', 'レソト', 'モーリシャス', 'ペルー', 'イギリス領ヴァージン諸島', 'アセンション島', 'ジブラルタル', 'キリバス', 'ルクセンブルク', 'アゼルバイジャン', '香港', 'サン・マルタン', 'アルバニア', '東ティモール', 'ブーベ島', 'グレナダ', 'グアテマラ', 'バチカン市国', 'コンゴ民主共和国', 'キュラソー', 'フィジー', 'ジャマイカ', 'ツバル', 'アラブ首長国連邦', 'オーストラリア', 'エジプト', 'グリーンランド', 'モンテネグロ', 'マリ', 'セルビア', 'セントルシア', 'マレーシア', 'ニジェール', 'ネパール', 'アルメニア']
  - input:text `統計品目 (HS) コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / variant thumbnail S / グレー / variant thumbnail M / グレー
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / variant thumbnail S / グレー / variant thumbnail M / グレー

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

## /admin/inventory_items/9f2fb021-cdce-59dd-8400-66d0bd815d61_InventoryItem/history

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_items/9f2fb021-cdce-59dd-8400-66d0bd815d61_InventoryItem/history`
- headings: 半袖シャツ
- buttons: stack-ps-yosuke 陽介 河野 / 選択
- fields:
  - input:text `ロケーション` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `ロケーション`: stack-ps-yosuke 陽介 河野

## /admin/products/2c32fb97-1f83-5cae-b20c-3d83046800d0_Product/variants/92cfda5b-cf04-55f2-a4a1-719e562cbc0a_ProductVariant

- finalUrl: `https://www.sqstackstaging.com/admin/products/2c32fb97-1f83-5cae-b20c-3d83046800d0_Product/variants/92cfda5b-cf04-55f2-a4a1-719e562cbc0a_ProductVariant`
- headings: BLACK / XL / オプション / メディア / 価格 / 在庫 / 原価 / 販売 / 配送
- buttons: stack-ps-yosuke 陽介 河野 / 画像を選択する / 原価を登録する / 更新する
- fields:
  - select:select-one `カラー` required=False disabled=False options=['選択してください', 'BEIGE', 'GRAY', 'NAVY', 'BLACK']
  - select:select-one `サイズ` required=False disabled=False options=['選択してください', 'XS', 'S', 'M', 'L', 'XL']
  - input:checkbox `` required=False disabled=False checked=False
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
  - select:select-one `原産国コード` required=False disabled=False options=['選択してください', 'ブーベ島', 'フィジー', 'フェロー諸島', 'パラグアイ', 'ザンビア', 'アルバニア', 'グアドループ', 'モナコ', 'ニカラグア', 'ソマリア', 'サントメ・プリンシペ', 'モルドバ', 'タンザニア', '中央アフリカ共和国', 'コスタリカ', 'グレナダ', 'ハード島とマクドナルド諸島', 'クロアチア', 'シリア', 'グリーンランド', 'ホンジュラス', '合衆国領有小離島', 'エクアドル', 'ジブラルタル', 'ハンガリー', 'アラブ首長国連邦', 'ミャンマー', 'オランダ', 'ニュージーランド', 'トンガ', 'マリ', 'ベナン', 'カーボベルデ', 'ギリシャ', 'ルクセンブルク', 'スウェーデン', 'セントヘレナ', 'グアテマラ', 'ヨルダン', 'マカオ', 'モザンビーク', 'フィリピン', 'タイ', 'バルバドス', 'エストニア', 'ノルウェー', 'ピトケアン諸島', 'ロシア', 'ベラルーシ', 'コロンビア', 'カザフスタン', 'サウジアラビア', 'バミューダ', 'イギリス', 'ギニアビサウ', 'ペルー', 'ポーランド', 'ウォリス・フツナ', 'その他の地域', 'アンゴラ', 'ブラジル', 'ネパール', 'チャド', 'ベルギー', 'ボツワナ', 'コンゴ共和国', 'ニジェール', 'サンピエール・ミクロン', 'エルサルバドル', 'ツバル', 'アンティグア・バーブーダ', 'ジョージア', '南アフリカ', '北マケドニア', 'モーリタニア', 'トケラウ', 'ボスニア・ヘルツェゴビナ', 'ジャマイカ', 'レバノン', 'フランス南方・南極地域', 'コートジボワール', 'クック諸島', 'ドイツ', 'カンボジア', 'モーリシャス', 'セネガル', '南スーダン', 'ウズベキスタン', 'オーランド諸島', 'ブルンジ', 'ガボン', 'イラク', 'セントルシア', 'スーダン', 'チュニジア', 'イギリス領ヴァージン諸島', 'アンドラ', '香港', 'マン島', 'キリバス', 'ニウエ', 'ルーマニア', 'スロバキア', 'チェコ', 'セントクリストファー・ネイビス', 'ウガンダ', 'エスワティニ', 'アンギラ', 'パレスチナ', 'ポルトガル', 'ウルグアイ', 'キューバ', 'サモア', 'イラン', 'リトアニア', 'ケニア', 'アフガニスタン', 'オランダ領カリブ', 'アイルランド', 'コモロ', 'ナミビア', 'ソロモン諸島', 'タジキスタン', 'ボリビア', 'フィンランド', 'ハイチ', 'モロッコ', 'ナイジェリア', 'セーシェル', 'トーゴ', 'ナウル', 'ウクライナ', 'バヌアツ', 'ココス諸島', 'ガーンジー', 'キルギス', 'スリランカ', 'レユニオン', 'スリナム', 'アルゼンチン', 'クリスマス島', 'キプロス', 'パナマ', 'バーレーン', 'チリ', '日本', 'ケイマン諸島', 'ラオス', 'デンマーク', 'イギリス領インド洋地域', 'イタリア', 'パプアニューギニア', 'セントビンセント・グレナディーン', 'ブルキナファソ', 'フランス領ギアナ', '中国', 'アルジェリア', 'カタール', 'オランダ領アンティル', 'バハマ', 'シンガポール', 'ベネズエラ', 'サウスジョージア・サウスサンドウィッチ諸島', 'ジャージー', '台湾', 'モンテネグロ', 'マルタ', 'オマーン', 'ドミニカ国', 'リビア', '北朝鮮', 'モントセラト', 'ブルガリア', 'ブルネイ', 'ブータン', 'ベリーズ', 'ギニア', 'イスラエル', 'コンゴ民主共和国', 'ガーナ', 'アイスランド', 'ノーフォーク島', 'オーストリア', 'アゼルバイジャン', '韓国', 'ラトビア', 'サンマリノ', 'ベトナム', 'フォークランド諸島', 'リベリア', 'ニューカレドニア', 'シエラレオネ', 'アメリカ合衆国', 'バングラデシュ', 'カナダ', 'カメルーン', 'キュラソー', 'タークス・カイコス諸島', '東ティモール', 'コソボ', 'アルバ', 'ガンビア', 'インドネシア', 'クウェート', 'エチオピア', 'リヒテンシュタイン', 'サン・バルテルミー', 'インド', 'マレーシア', 'セルビア', 'シント・マールテン', 'トリニダード・トバゴ', 'エジプト', '西サハラ', 'フランス', 'モンゴル', 'モルディブ', 'パキスタン', 'スヴァールバル諸島およびヤンマイエン島', 'アルメニア', 'スイス', '赤道ギニア', 'マダガスカル', 'ドミニカ共和国', 'マラウイ', 'イエメン', 'アセンション島', 'マルティニーク', 'メキシコ', 'ジンバブエ', 'ジブチ', 'オーストラリア', 'レソト', 'ルワンダ', 'スロベニア', 'エリトリア', 'トルクメニスタン', 'トルコ', 'バチカン市国', 'マヨット', 'スペイン', 'サン・マルタン', 'トリスタン・ダ・クーニャ', 'ガイアナ', 'フランス領ポリネシア']
  - input:text `統計品目 (HS) コード` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野 / BEIGE / XS / BEIGE / S / BEIGE / M / BEIGE / L / BEIGE / XL / GRAY / XS / GRAY / S / GRAY / M / GRAY / L / GRAY / XL / NAVY / XS / NAVY / S / NAVY / M / NAVY / L / NAVY / XL / BLACK / XS / BLACK / S
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野 / BEIGE / XS / BEIGE / S / BEIGE / M / BEIGE / L / BEIGE / XL / GRAY / XS / GRAY / S / GRAY / M / GRAY / L / GRAY / XL / NAVY / XS / NAVY / S / NAVY / M / NAVY / L / NAVY / XL / BLACK / XS / BLACK / S

## /admin/inventory_outbound_orders/de6aa7c3-d276-5c7d-bed5-29e9af103bec_InventoryOutboundOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_outbound_orders/de6aa7c3-d276-5c7d-bed5-29e9af103bec_InventoryOutboundOrder`
- headings: #IO-1022 / 出荷明細 / 出荷履歴 / 詳細 / 出荷先ロケーション
- buttons: stack-ps-yosuke 陽介 河野 / 出荷実績を登録する (disabled) / 出荷実績の明細を展開する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - input:text `配送方法` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 出荷予定 | 出荷済み
  - オーバーサイズスウェットシャツ BLACK / XL | 486125-09-XL | 1 | 1
  - オーバーサイズスウェットシャツ BEIGE / XL | 486125-31-XL | 1 | 1
  - バギーカーブジーンズ BLUE / 36 | 487973-64-36 | 1 | 1

## /admin/inventory_inbound_orders/fb950bd4-5de7-52f3-b282-21191ea08996_InventoryInboundOrder

- finalUrl: `https://www.sqstackstaging.com/admin/inventory_inbound_orders/fb950bd4-5de7-52f3-b282-21191ea08996_InventoryInboundOrder`
- headings: #II-1022 / 入荷明細 / 入荷履歴 / 詳細
- buttons: stack-ps-yosuke 陽介 河野 / 入荷実績の明細を展開する
- fields:
  - input:text `ロケーション` required=False disabled=False
  - input:text `種別` required=False disabled=False
- opened choices:
  - `button`: stack-ps-yosuke 陽介 河野
  - `stack-ps-yosuke 陽介 河野`: stack-ps-yosuke 陽介 河野
  - `入荷実績の明細を展開する`: stack-ps-yosuke 陽介 河野
- table1: 商品 | SKU | 入荷予定 | 入荷済み
  - オーバーサイズスウェットシャツ BLACK / XL | 486125-09-XL | 1 | 1
  - オーバーサイズスウェットシャツ BEIGE / XL | 486125-31-XL | 1 | 1
  - バギーカーブジーンズ BLUE / 36 | 487973-64-36 | 1 | 1

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

## /admin/settings/metafield_definitions/product/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/product/create`
- headings: 商品メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/product_variant/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/product_variant/create`
- headings: バリエーションメタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/purchasing_customer/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/purchasing_customer/create`
- headings: 顧客メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/order/create`
- headings: 注文メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/draft_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/draft_order/create`
- headings: 下書き注文メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/company/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/company/create`
- headings: 会社メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/location/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/location/create`
- headings: ロケーションメタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/order_price_adjustment_rule/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/order_price_adjustment_rule/create`
- headings: ディスカウントメタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_movement_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_movement_order/create`
- headings: 在庫移動伝票メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_adjustment_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_adjustment_order/create`
- headings: 在庫調整伝票メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_reservation_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_reservation_order/create`
- headings: 在庫取置伝票メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_purchase_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_purchase_order/create`
- headings: 発注伝票メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_inbound_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_inbound_order/create`
- headings: 入荷指示メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_outbound_order/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_outbound_order/create`
- headings: 出荷指示メタフィールドの定義を追加する
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

## /admin/settings/metafield_definitions/inventory_supplier/create

- finalUrl: `https://www.sqstackstaging.com/admin/settings/metafield_definitions/inventory_supplier/create`
- headings: 仕入れ先ベンダーメタフィールドの定義を追加する
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
