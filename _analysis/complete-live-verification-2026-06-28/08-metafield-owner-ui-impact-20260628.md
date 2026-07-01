# メタフィールド定義 16対象 UI反映確認 2026-06-28

- 実行時刻: `2026-06-28T14:02:09.337844+00:00`
- namespace: `faqmf230209`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/08-metafield-owner-ui-impact-20260628.json`

## 結論

- 定義作成の成否、定義一覧での表示、対象画面で入力欄/表示名が出るかを分けて確認した。
- `対象画面に出た` は、定義追加後に代表画面本文へ検証用定義名が新規出現したことを意味する。
- 下書き注文と組織は、現行UIで専用詳細レコードを開けないため、一覧/設定トップでの代表確認に留めた。

## 結果表

| 対象 | ownerType | 定義作成 | 定義一覧 | 代表画面 | 対象画面に出た | メタフィールド文言 | 備考 |
|---|---|---:|---:|---|---:|---:|---|
| 組織 | `ORGANIZATION` | OK | OK | `/admin/settings` | NG | OK | 組織の専用詳細画面は見つからないため、設定トップを代表画面にした。 |
| ロケーション | `LOCATION` | OK | OK | `/admin/settings/locations/1f0fd500-ee41-50b5-afb9-217ab8af9db3_Location` | OK | OK | fallback |
| 会社 | `COMPANY` | OK | OK | `/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company` | OK | OK | fallback |
| 仕入れ先ベンダー | `INVENTORY_SUPPLIER` | NG | NG | `/admin/settings/suppliers/62acd1f7-d25a-5b93-a4e8-fbfcb23b59ff_InventorySupplier` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 商品 | `PRODUCT` | OK | OK | `/admin/products/8cbfb469-83b0-55b4-a2ed-5e77459662db_Product` | OK | OK | discovered from /admin/products |
| バリエーション | `PRODUCT_VARIANT` | OK | OK | `/admin/products/91f45bd1-03b7-5aad-a888-42530a13011d_Product/variants/9d94e684-4882-5ebc-bbbb-513915a8bfc7_ProductVariant` | OK | OK | fallback |
| 顧客 | `PURCHASING_CUSTOMER` | OK | OK | `/admin/purchasing_customers/e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer` | OK | OK | 一覧は空の場合があるため、過去検証で作成済みの検証顧客詳細をfallbackにした。 |
| 注文 | `ORDER` | OK | OK | `/admin/orders/68dee76e-36de-5a27-a182-5505ed6dd576_Order` | OK | OK | discovered from /admin/orders |
| 下書き注文 | `DRAFT_ORDER` | OK | OK | `/admin/draft_orders` | NG | NG | 現行UIでは下書き注文の作成ボタンがdisabled相当で、詳細レコードを開けないため一覧を代表画面にした。 |
| ディスカウント | `ORDER_PRICE_ADJUSTMENT_RULE` | OK | OK | `/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule` | OK | OK | discovered from /admin/order_price_adjustment_rules |
| 在庫移動伝票 | `INVENTORY_MOVEMENT_ORDER` | NG | NG | `/admin/inventory_movement_orders/6dc18986-0648-5a8a-99b0-502555b2306a_InventoryMovementOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 在庫調整伝票 | `INVENTORY_ADJUSTMENT_ORDER` | NG | NG | `/admin/inventory_adjustment_orders/656af2b4-e907-52d7-a665-6a7dcef5b31a_InventoryAdjustmentOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 在庫取置伝票 | `INVENTORY_RESERVATION_ORDER` | NG | NG | `/admin/inventory_reservation_orders/aff62cd3-c383-5d3a-8d30-9236264da806_InventoryReservationOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 発注伝票 | `INVENTORY_PURCHASE_ORDER` | NG | NG | `/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 入荷指示 | `INVENTORY_INBOUND_ORDER` | NG | NG | `/admin/inventory_inbound_orders/30f80d42-c86d-5faf-a0b3-5b6a0bddc9b3_InventoryInboundOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |
| 出荷指示 | `INVENTORY_OUTBOUND_ORDER` | NG | NG | `/admin/inventory_outbound_orders/489665a0-0d2f-57c7-8102-3d1b2c9fdc80_InventoryOutboundOrder` | NG | NG | {"errors":[{"message":"エラーが発生しました。しばらくしてから再度お試しください","path":["metafieldDefinitionCreate"],"locations":[{"line":3,"column |

## 対象画面で出た行

### 組織

- 代表画面: `/admin/settings`
- 定義名: `FAQMF organization 230209`
- 代表画面本文には検証用定義名は出なかった。
- 注記: 組織の専用詳細画面は見つからないため、設定トップを代表画面にした。

### ロケーション

- 代表画面: `/admin/settings/locations/1f0fd500-ee41-50b5-afb9-217ab8af9db3_Location`
- 定義名: `FAQMF location 230209`
- b8af9db3_Location 外部ID 未設定 名前 表示名 コード 場所種別 選択してください 倉庫 店舗 店舗 このロケーションを閉鎖する 閉鎖すると、店舗撤退や倉庫移動などで利用しなくなったロケーションとして扱われます。 所在地 未設定 連絡先 マップ 電話番号 メールアドレス 所属ロケーショングループ 0個のグループに属しています アイテムが見つかりませんでした 絞り込みや検索ワードを変更してみてください メタフィールド FAQMF location 230209 未設定 ロケーションをアーカイブ アーカイブする 公開設定 公開設定 公開 非公開 公開 公開にすることでストアフロントからロケーション情報の参照が可能になります。 販売設定 店舗受取を有効にする 在庫依頼を受け付ける ポイント利用種別 選択してください 値引き 金種 値引き 備考欄 備考欄 0/5000 タグ タグは付与されていません 保存する
- fb9-217ab8af9db3_Location 外部ID 未設定 名前 表示名 コード 場所種別 選択してください 倉庫 店舗 店舗 このロケーションを閉鎖する 閉鎖すると、店舗撤退や倉庫移動などで利用しなくなったロケーションとして扱われます。 所在地 未設定 連絡先 マップ 電話番号 メールアドレス 所属ロケーショングループ 0個のグループに属しています アイテムが見つかりませんでした 絞り込みや検索ワードを変更してみてください メタフィールド FAQMF location 230209 未設定 ロケーションをアーカイブ アーカイブする 公開設定 公開設定 公開 非公開 公開 公開にすることでストアフロントからロケーション情報の参照が可能になります。 販売設定 店舗受取を有効にする 在庫依頼を受け付ける ポイント利用種別 選択してください 値引き 金種 値引き 備考欄 備考欄 0/5000 タグ タグは付与されていません 保存する

### 会社

- 代表画面: `/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company`
- 定義名: `FAQMF company 230209`
- 2911。このページの準備が整いました TEST_FAQ_20260624_COMPANY_102911 2026年06月24日から顧客 直近の注文 この会社はまだ注文していません ロケーション ロケーションを追加 ロケーション 売上 注文 TEST_FAQ_20260624_COMPANY_LOC_102911 ¥0 0 担当者 担当者を追加 アイテムが見つかりませんでした 絞り込みや検索ワードを変更してみてください メタフィールド FAQMF company 230209 未設定 TEST_FAQ_20260624_COMPANY_102911 会社ID TEST_FAQ_COMP_102911 メモ この会社にはメモがありません。
- MPANY_102911。このページの準備が整いました TEST_FAQ_20260624_COMPANY_102911 2026年06月24日から顧客 直近の注文 この会社はまだ注文していません ロケーション ロケーションを追加 ロケーション 売上 注文 TEST_FAQ_20260624_COMPANY_LOC_102911 ¥0 0 担当者 担当者を追加 アイテムが見つかりませんでした 絞り込みや検索ワードを変更してみてください メタフィールド FAQMF company 230209 未設定 TEST_FAQ_20260624_COMPANY_102911 会社ID TEST_FAQ_COMP_102911 メモ この会社にはメモがありません。

### 仕入れ先ベンダー

- 代表画面: `/admin/settings/suppliers/62acd1f7-d25a-5b93-a4e8-fbfcb23b59ff_InventorySupplier`
- 定義名: `FAQMF inventory_supplier 230209`
- 代表画面本文には検証用定義名は出なかった。

### 商品

- 代表画面: `/admin/products/8cbfb469-83b0-55b4-a2ed-5e77459662db_Product`
- 定義名: `FAQMF product 230209`
- TION 情報 下書き その他の操作 商品コード TEST_20260622_OPTION 商品名 説明文 20/5000 メディア（0件） 画像をアップロード 追加 バリエーション バリエーションを追加する サイズ 情報 サイズ S M L カラー 情報 カラー Black 素材 情報 その他 綿 ポリエステル バリエーションがありません 検索エンジンリスティング ページタイトル メタディスクリプション 0/5000 メタフィールド FAQMF product 230209 未設定 ステータス 公開中 下書き 下書き 商品分類 商品タイプ 製造元 ブランド 選択 タグ タグは付与されていません 保存する
- 60622_OPTION 情報 下書き その他の操作 商品コード TEST_20260622_OPTION 商品名 説明文 20/5000 メディア（0件） 画像をアップロード 追加 バリエーション バリエーションを追加する サイズ 情報 サイズ S M L カラー 情報 カラー Black 素材 情報 その他 綿 ポリエステル バリエーションがありません 検索エンジンリスティング ページタイトル メタディスクリプション 0/5000 メタフィールド FAQMF product 230209 未設定 ステータス 公開中 下書き 下書き 商品分類 商品タイプ 製造元 ブランド 選択 タグ タグは付与されていません 保存する

### バリエーション

- 代表画面: `/admin/products/91f45bd1-03b7-5aad-a888-42530a13011d_Product/variants/9d94e684-4882-5ebc-bbbb-513915a8bfc7_ProductVariant`
- 定義名: `FAQMF product_variant 230209`
- プト サウスジョージア・サウスサンドウィッチ諸島 ニカラグア シンガポール ブーベ島 イラク ナウル トルコ ウクライナ サモア オーランド諸島 ジャージー マラウイ ニューカレドニア ボスニア・ヘルツェゴビナ フランス領ポリネシア セントヘレナ バチカン市国 ガボン パプアニューギニア レユニオン バヌアツ バングラデシュ 中央アフリカ共和国 ジョージア 選択してください 統計品目 (HS) コード メタフィールド gift 未設定 FAQMF product_variant 230209 未設定 更新する
- サントメ・プリンシペ 台湾 エジプト サウスジョージア・サウスサンドウィッチ諸島 ニカラグア シンガポール ブーベ島 イラク ナウル トルコ ウクライナ サモア オーランド諸島 ジャージー マラウイ ニューカレドニア ボスニア・ヘルツェゴビナ フランス領ポリネシア セントヘレナ バチカン市国 ガボン パプアニューギニア レユニオン バヌアツ バングラデシュ 中央アフリカ共和国 ジョージア 選択してください 統計品目 (HS) コード メタフィールド gift 未設定 FAQMF product_variant 230209 未設定 更新する

### 顧客

- 代表画面: `/admin/purchasing_customers/e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer`
- 定義名: `FAQMF purchasing_customer 230209`
- 0628140117 から作成 ￥1,990 すべての注文を表示する ポイント 保有ポイント 0 ポイント 付与予定 0 ポイント ポイントを加算 ポイントを減算 ポイント履歴はありません すべての履歴を表示 マイル 保有マイル 0 マイル 累計獲得 0 マイル マイルを加算 マイルを減算 マイル履歴はありません すべての履歴を表示 ディスカウント ディスカウントはありません すべてのディスカウントを表示 メタフィールド 性別 未設定 FAQMF purchasing_customer 230209 未設定 会員番号 FAQUNI0628095318 顧客情報 氏名 検証顧客ユニクロ095318FAQ メールアドレス sq-faq-uniqlo-customer-20260628095318@example.invalid 電話番号 0000000000 SMS認証 未完了 未認証 外部ID FAQ_E2E_UNIQLO_CUSTOMER_20260628095318 作成日時 2026年06月28日 09:53 更新日時 2026年06月28日 09:53 購買サマリー 初回購入日 2026年06月28日 10:11 初回購入場所(店舗コード) FAQ_INTERNAL_GRAPHQL 最終購入日 2026年06月28日 14:03 最終購入場所(店舗コード) FAQ_REMAINING_AUTHONL
- -NOFULFILL-20260628140117 から作成 ￥1,990 すべての注文を表示する ポイント 保有ポイント 0 ポイント 付与予定 0 ポイント ポイントを加算 ポイントを減算 ポイント履歴はありません すべての履歴を表示 マイル 保有マイル 0 マイル 累計獲得 0 マイル マイルを加算 マイルを減算 マイル履歴はありません すべての履歴を表示 ディスカウント ディスカウントはありません すべてのディスカウントを表示 メタフィールド 性別 未設定 FAQMF purchasing_customer 230209 未設定 会員番号 FAQUNI0628095318 顧客情報 氏名 検証顧客ユニクロ095318FAQ メールアドレス sq-faq-uniqlo-customer-20260628095318@example.invalid 電話番号 0000000000 SMS認証 未完了 未認証 外部ID FAQ_E2E_UNIQLO_CUSTOMER_20260628095318 作成日時 2026年06月28日 09:53 更新日時 2026年06月28日 09:53 購買サマリー 初回購入日 2026年06月28日 10:11 初回購入場所(店舗コード) FAQ_INTERNAL_GRAPHQL 最終購入日 2026年06月28日 1
- 注記: 一覧は空の場合があるため、過去検証で作成済みの検証顧客詳細をfallbackにした。

### 注文

- 代表画面: `/admin/orders/68dee76e-36de-5a27-a182-5505ed6dd576_Order`
- 定義名: `FAQMF order 230209`
- 990 x 1 ￥1,990 支払い情報 成功 完了 支払い済み 支払い合計 ￥1,990 小計 1個のアイテム ￥1,990 送料 ￥0 税 ￥0 合計 ￥1,990 決済履歴 日付 ゲートウェイ ペイメントID タイプ ステータス 金額 2026年06月28日 14:03 FAQ_GATEWAY [REDACTED_LONG_VALUE] オーソリ 成功 ￥1,990 メタフィールド FAQMF order 230209 未設定 メモ FAQ残件実機検証: AUTHORIZATIONのみ 顧客情報 検証顧客ユニクロ095318FAQ 過去に5個の注文 連絡先情報 sq-faq-uniqlo-customer-20260628095318@example.invalid 配送先住所 配送先住所なし 請求先住所 請求先住所なし ポイント 付与対象に含む 成功 はい ポイント付与 0ポイント 会員ランク 算出対象に含む 成功 はい タグ #ON-7 FAQ_REMAINING_20260628 FAQ_REMAINING_AUTHONLY
- M 単価 ￥1,990 x 1 ￥1,990 支払い情報 成功 完了 支払い済み 支払い合計 ￥1,990 小計 1個のアイテム ￥1,990 送料 ￥0 税 ￥0 合計 ￥1,990 決済履歴 日付 ゲートウェイ ペイメントID タイプ ステータス 金額 2026年06月28日 14:03 FAQ_GATEWAY [REDACTED_LONG_VALUE] オーソリ 成功 ￥1,990 メタフィールド FAQMF order 230209 未設定 メモ FAQ残件実機検証: AUTHORIZATIONのみ 顧客情報 検証顧客ユニクロ095318FAQ 過去に5個の注文 連絡先情報 sq-faq-uniqlo-customer-20260628095318@example.invalid 配送先住所 配送先住所なし 請求先住所 請求先住所なし ポイント 付与対象に含む 成功 はい ポイント付与 0ポイント 会員ランク 算出対象に含む 成功 はい タグ #ON-7 FAQ_REMAINING_20260628 FAQ_REMAINING_AUTHONLY

### 下書き注文

- 代表画面: `/admin/draft_orders`
- 定義名: `FAQMF draft_order 230209`
- 代表画面本文には検証用定義名は出なかった。
- 注記: 現行UIでは下書き注文の作成ボタンがdisabled相当で、詳細レコードを開けないため一覧を代表画面にした。

### ディスカウント

- 代表画面: `/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule`
- 定義名: `FAQMF order_price_adjustment_rule 230209`
- C 説明文 割引設定 割引方法 選択してください 割引率 割引額 割引率 割引率 % 割引が適用可能な最高購入額を設定する 設定した購入額を超える注文には適用不可になります 適用条件 割引要件 最低購入額 円 最低購入数量 対象商品 すべての商品を割引対象に設定する 利用制限 お客様1人につき1回のみの使用とする 有効期間 開始日時 終了日時 Shopify連携 このディスカウントはShopifyに未連携です 連携する メタフィールド FAQMF order_price_adjustment_rule 230209 未設定 ステータス 成功 有効 テナント ユニクロ 対象顧客 0人 対象店舗 0件 利用回数 0回 保存する
- 0345-DISC 説明文 割引設定 割引方法 選択してください 割引率 割引額 割引率 割引率 % 割引が適用可能な最高購入額を設定する 設定した購入額を超える注文には適用不可になります 適用条件 割引要件 最低購入額 円 最低購入数量 対象商品 すべての商品を割引対象に設定する 利用制限 お客様1人につき1回のみの使用とする 有効期間 開始日時 終了日時 Shopify連携 このディスカウントはShopifyに未連携です 連携する メタフィールド FAQMF order_price_adjustment_rule 230209 未設定 ステータス 成功 有効 テナント ユニクロ 対象顧客 0人 対象店舗 0件 利用回数 0回 保存する

### 在庫移動伝票

- 代表画面: `/admin/inventory_movement_orders/6dc18986-0648-5a8a-99b0-502555b2306a_InventoryMovementOrder`
- 定義名: `FAQMF inventory_movement_order 230209`
- 代表画面本文には検証用定義名は出なかった。

### 在庫調整伝票

- 代表画面: `/admin/inventory_adjustment_orders/656af2b4-e907-52d7-a665-6a7dcef5b31a_InventoryAdjustmentOrder`
- 定義名: `FAQMF inventory_adjustment_order 230209`
- 代表画面本文には検証用定義名は出なかった。

### 在庫取置伝票

- 代表画面: `/admin/inventory_reservation_orders/aff62cd3-c383-5d3a-8d30-9236264da806_InventoryReservationOrder`
- 定義名: `FAQMF inventory_reservation_order 230209`
- 代表画面本文には検証用定義名は出なかった。

### 発注伝票

- 代表画面: `/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder`
- 定義名: `FAQMF inventory_purchase_order 230209`
- 代表画面本文には検証用定義名は出なかった。

### 入荷指示

- 代表画面: `/admin/inventory_inbound_orders/30f80d42-c86d-5faf-a0b3-5b6a0bddc9b3_InventoryInboundOrder`
- 定義名: `FAQMF inventory_inbound_order 230209`
- 代表画面本文には検証用定義名は出なかった。

### 出荷指示

- 代表画面: `/admin/inventory_outbound_orders/489665a0-0d2f-57c7-8102-3d1b2c9fdc80_InventoryOutboundOrder`
- 定義名: `FAQMF inventory_outbound_order 230209`
- 代表画面本文には検証用定義名は出なかった。

## 後片付け

- 削除対象定義数: `9`
- 削除mutation HTTP成功: `OK`
- 追加確認: 全16 ownerType を `metafieldDefinitions` で再検索し、`FAQMF` / `faqmf` で始まる検証用定義の残存は `0` 件
