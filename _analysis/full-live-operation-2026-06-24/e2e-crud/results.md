# SQ E2E CRUD実機テストログ 2026-06-24

- 実行対象: `https://www.sqstackstaging.com`
- browser-use profile: `bay-works.com`
- テストデータ接頭辞: `TEST_FAQ_20260624`
- 制約: 既存ユーザー/既存ユーザーデータは操作しない。商品を追加する場合はGU製品として作成。

## 結果

### 2026-06-24T09:22:17+09:00 OK OPEN /admin
- URL: `https://www.sqstackstaging.com/admin`
- 見出し: stack-ps-yosuke / 商品管理 / 在庫管理 / 注文管理 / 顧客管理 / CSVでデータをインポートする
- 通知: stack-ps-yosuke。このページの準備が整いました / 商品管理 商品の追加・編集、付加情報の管理、カタログの作成ができます。 在庫管理 在庫の移動、仕入れ、在庫の状況を確認することができます。 注文管理 販売チャネルで作成された注文の管理、注文の追跡、顧客への通知ができます。 顧客管理 顧客情報の管理、顧客の注文履歴、顧客の分析ができます。 CSVでデータをインポートする CSVファイルを使ってデータの書き込み・編集ができます。 CSVでデータをエクスポートする 指定のデータをCSV形式でエクスポートできます PDFでデータをエクスポートする 指定のデータをPDF形式でエクスポートできます
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 stack-ps-yosuke。このページの準備が整いました stack-ps-yosuke 設定 商品管理 商品の追加・編集、付加情報の管理、カタログの作成ができます。 在庫管理 在庫の移動、仕入れ、在庫の状況を確認することができます。 

### 2026-06-24T09:22:20+09:00 OK OPEN /admin/settings/suppliers/create
- URL: `https://www.sqstackstaging.com/admin/settings/suppliers/create`
- 見出し: 取引先を作成
- 通知: 取引先を作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 取引先を作成。このページの準備が整いました 取引先を作成 取引先名 取引先コード 保存する

### 2026-06-24T09:22:22+09:00 OK 取引先CRUD: 入力
- URL: `https://www.sqstackstaging.com/admin/settings/suppliers/create`
- 詳細: {"fills": [{"ok": true, "label": "取引先名", "value": "TEST_FAQ_20260624_取引先_092214"}, {"ok": true, "label": "取引先コード", "value": "TEST_FAQ_20260624_SUP_092214"}], "selects": [], "checks": []}
- 見出し: 保存されていない取引先 / 取引先を作成
- 通知: 取引先を作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない取引先 取り消す 保存する 取引先を作成。このページの準備が整いました 取引先を作成 取引先名 取引先コード 保存する

### 2026-06-24T09:22:24+09:00 OK 取引先CRUD: 保存
- URL: `https://www.sqstackstaging.com/admin/settings/suppliers`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: 取引先
- 通知: 取引先。このページの準備が整いました / 取引先を作成しました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 取引先。このページの準備が整いました 取引先 インポート 取引先を作成 すべて アーカイブ すべてのアイテムを選択する 名前 コード アイテムを選択する TEST_FAQ_20260624_取引先_092214 TEST_FAQ_20260

### 2026-06-24T09:22:28+09:00 OK OPEN /admin/settings/brands/create
- URL: `https://www.sqstackstaging.com/admin/settings/brands/create`
- 見出し: ブランド
- 通知: ブランド。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ブランド。このページの準備が整いました ブランド 名前 外部ID コード 保存する

### 2026-06-24T09:22:29+09:00 OK ブランドCRUD: 入力
- URL: `https://www.sqstackstaging.com/admin/settings/brands/create`
- 詳細: {"fills": [{"ok": true, "label": "名前", "value": "TEST_FAQ_20260624_ブランド_092214"}, {"ok": true, "label": "外部ID", "value": "TEST_FAQ_20260624_BR_EXT_092214"}, {"ok": true, "label": "コード", "value": "TEST_FAQ_20260624_BR_092214"}], "selects": [], "checks": []}
- 見出し: ブランド
- 通知: ブランド。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ブランド。このページの準備が整いました ブランド 名前 外部ID コード 保存する

### 2026-06-24T09:22:31+09:00 OK ブランドCRUD: 保存
- URL: `https://www.sqstackstaging.com/admin/settings/brands`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: ブランド
- 通知: ブランド。このページの準備が整いました / ブランドを追加しました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | コード | 外部ID | 更新日時
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ブランド。このページの準備が整いました ブランド 追加する すべてのアイテムを選択する 名前 コード 外部ID 更新日時 アイテムを選択する UNIQLO UNIQLO 2026年06月21日 アイテムを選択する GU GU 2026年06

### 2026-06-24T09:22:32+09:00 INFO ブランドCRUD: 削除ボタン確認
- URL: `https://www.sqstackstaging.com/admin/settings/brands`
- 詳細: 削除ボタンなし/無効のため削除未実行
- 見出し: ブランド
- 通知: ブランド。このページの準備が整いました / ブランドを追加しました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | コード | 外部ID | 更新日時
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ブランド。このページの準備が整いました ブランド 追加する すべてのアイテムを選択する 名前 コード 外部ID 更新日時 アイテムを選択する UNIQLO UNIQLO 2026年06月21日 アイテムを選択する GU GU 2026年06

### 2026-06-24T09:22:36+09:00 OK OPEN /admin/settings/payment_methods/create
- URL: `https://www.sqstackstaging.com/admin/settings/payment_methods/create`
- 見出し: 決済方法を作成する / 詳細
- 通知: 決済方法を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 決済方法を作成する。このページの準備が整いました 決済方法を作成する 詳細 名前 コード ゲートウェイ 支払い待ちでも注文を出荷する 代引き 保存する

### 2026-06-24T09:22:37+09:00 OK 決済方法CRUD: 入力
- URL: `https://www.sqstackstaging.com/admin/settings/payment_methods/create`
- 詳細: {"fills": [{"ok": true, "label": "名前", "value": "TEST_FAQ_20260624_決済_092214"}, {"ok": true, "label": "コード", "value": "TEST_FAQ_20260624_PAY_092214"}, {"ok": true, "label": "ゲートウェイ", "value": "manual_test"}], "selects": [], "checks": [{"ok": true, "label": "支払い待ちでも注文を出荷する", "checked": false}, {"ok": true, "label": "代引き", "checked": false}]}
- 見出し: 保存されていない決済方法 / 決済方法を作成する / 詳細
- 通知: 決済方法を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない決済方法 取り消す 保存する 決済方法を作成する。このページの準備が整いました 決済方法を作成する 詳細 名前 コード ゲートウェイ 支払い待ちでも注文を出荷する 代引き 保存する

### 2026-06-24T09:22:39+09:00 OK 決済方法CRUD: 保存
- URL: `https://www.sqstackstaging.com/admin/settings/payment_methods`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: 決済方法
- 通知: 決済方法。このページの準備が整いました / 決済方法を作成しました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | コード | ゲートウェイ
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 決済方法。このページの準備が整いました 決済方法 決済方法を作成 すべて すべてのアイテムを選択する 名前 コード ゲートウェイ アイテムを選択する TEST_FAQ_決済 test_faq_payment test_gateway アイテ

### 2026-06-24T09:22:43+09:00 OK OPEN /admin/settings/locations/create
- URL: `https://www.sqstackstaging.com/admin/settings/locations/create`
- 見出し: ロケーションを作成 / 基本情報 / 所在地・連絡先 / 販売設定
- 通知: ロケーションを作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ロケーションを作成。このページの準備が整いました ロケーションを作成 基本情報 名前 このロケーションに短い名前を付けて、簡単に識別できるようにします。注文や商品などのエリアでこの名前が表示されます。 表示名 コード 場所種別 選択してくだ

### 2026-06-24T09:22:44+09:00 OK ロケーションCRUD 店舗_OFF: 入力
- URL: `https://www.sqstackstaging.com/admin/settings/locations/create`
- 詳細: {"fills": [{"ok": true, "label": "名前", "value": "TEST_FAQ_20260624_GU店舗_OFF_092214"}, {"ok": true, "label": "表示名", "value": "TEST_FAQ_20260624_GU店舗_OFF_092214"}, {"ok": true, "label": "コード", "value": "TEST_FAQ_20260624_STORE_092214"}], "selects": [{"ok": true, "label": "場所種別", "text": "店舗", "value": "RETAIL"}, {"ok": true, "label": "ポイント利用種別", "text": "値引き", "value": "DISCOUNT"}], "checks": [{"ok": true, "label": "店舗受け取りを有効にする", "checked": true}, {"ok": true, "label": "在庫依頼を受け付ける", "checked": false}]}
- 見出し: 保存されていないロケーション / ロケーションを作成 / 基本情報 / 所在地・連絡先 / 販売設定
- 通知: ロケーションを作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていないロケーション 取り消す 保存する ロケーションを作成。このページの準備が整いました ロケーションを作成 基本情報 名前 このロケーションに短い名前を付けて、簡単に識別できるようにします。注文や商品などのエリアでこの名前が表示

### 2026-06-24T09:22:46+09:00 OK ロケーションCRUD 店舗_OFF: 保存
- URL: `https://www.sqstackstaging.com/admin/settings/locations/295e5a69-c97b-53df-b947-1dc9f559d00d_Location`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: ロケーション / 基本情報 / 所在地 / 連絡先 / 所属ロケーショングループ / ロケーションをアーカイブ
- 通知: ロケーション。このページの準備が整いました / 0/5000 / ロケーションを作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ロケーション。このページの準備が整いました ロケーション TEST_FAQ_20260624_GU店舗_OFF_092214 基本情報 ロケーションID 295e5a69-c97b-53df-b947-1dc9f559d00d_Locati

### 2026-06-24T09:22:49+09:00 OK OPEN /admin/settings/locations/create
- URL: `https://www.sqstackstaging.com/admin/settings/locations/create`
- 見出し: ロケーションを作成 / 基本情報 / 所在地・連絡先 / 販売設定
- 通知: ロケーションを作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ロケーションを作成。このページの準備が整いました ロケーションを作成 基本情報 名前 このロケーションに短い名前を付けて、簡単に識別できるようにします。注文や商品などのエリアでこの名前が表示されます。 表示名 コード 場所種別 選択してくだ

### 2026-06-24T09:22:50+09:00 OK ロケーションCRUD 倉庫_ON: 入力
- URL: `https://www.sqstackstaging.com/admin/settings/locations/create`
- 詳細: {"fills": [{"ok": true, "label": "名前", "value": "TEST_FAQ_20260624_GU倉庫_ON_092214"}, {"ok": true, "label": "表示名", "value": "TEST_FAQ_20260624_GU倉庫_ON_092214"}, {"ok": true, "label": "コード", "value": "TEST_FAQ_20260624_WH_092214"}], "selects": [{"ok": true, "label": "場所種別", "text": "倉庫", "value": "WAREHOUSE"}, {"ok": true, "label": "ポイント利用種別", "text": "値引き", "value": "DISCOUNT"}], "checks": [{"ok": true, "label": "店舗受け取りを有効にする", "checked": false}, {"ok": true, "label": "在庫依頼を受け付ける", "checked": true}]}
- 見出し: 保存されていないロケーション / ロケーションを作成 / 基本情報 / 所在地・連絡先 / 販売設定
- 通知: ロケーションを作成。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていないロケーション 取り消す 保存する ロケーションを作成。このページの準備が整いました ロケーションを作成 基本情報 名前 このロケーションに短い名前を付けて、簡単に識別できるようにします。注文や商品などのエリアでこの名前が表示

### 2026-06-24T09:22:53+09:00 OK ロケーションCRUD 倉庫_ON: 保存
- URL: `https://www.sqstackstaging.com/admin/settings/locations/b111b7e0-f00b-5823-a41f-2d345f56badc_Location`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: ロケーション / 基本情報 / 所在地 / 連絡先 / 所属ロケーショングループ / ロケーションをアーカイブ
- 通知: ロケーション。このページの準備が整いました / 0/5000 / ロケーションを作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 ロケーション。このページの準備が整いました ロケーション TEST_FAQ_20260624_GU倉庫_ON_092214 基本情報 ロケーションID b111b7e0-f00b-5823-a41f-2d345f56badc_Locatio

### 2026-06-24T09:22:56+09:00 OK OPEN /admin/catalogs/create
- URL: `https://www.sqstackstaging.com/admin/catalogs/create`
- 見出し: カタログを作成する
- 通知: カタログを作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 カタログを作成する。このページの準備が整いました カタログを作成する タイトル 保存する

### 2026-06-24T09:22:57+09:00 OK カタログCRUD: 入力
- URL: `https://www.sqstackstaging.com/admin/catalogs/create`
- 詳細: {"fills": [{"ok": true, "label": "タイトル", "value": "TEST_FAQ_20260624_カタログ_092214"}], "selects": [], "checks": []}
- 見出し: カタログを作成する
- 通知: カタログを作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 カタログを作成する。このページの準備が整いました カタログを作成する タイトル 保存する

### 2026-06-24T09:22:59+09:00 OK カタログCRUD: 保存
- URL: `https://www.sqstackstaging.com/admin/catalogs/9f57cf1f-6ac0-5dce-ae32-6976aefb3f5c_Catalog`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: TEST_FAQ_20260624_カタログ_092214
- 通知: TEST_FAQ_20260624_カタログ_092214。このページの準備が整いました / 商品を作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 TEST_FAQ_20260624_カタログ_092214。このページの準備が整いました TEST_FAQ_20260624_カタログ_092214 自動追加ルール SKU一覧 その他の操作 商品を追加する 商品コードで

### 2026-06-24T09:23:03+09:00 OK OPEN /admin/products/create
- URL: `https://www.sqstackstaging.com/admin/products/create`
- 見出し: 商品を作成する / メディア / バリエーション / 検索エンジンリスティング / ステータス / 商品分類
- 通知: 商品を作成する。このページの準備が整いました / 0/5000 / 0/5000
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 商品を作成する。このページの準備が整いました 商品を作成する 商品コード 半角英数字（A〜Z、a〜z、0〜9）、ハイフン（-）、アンダースコア（_）のみご入力ください。 商品名 説明文 0/5000 メディア 画像をアッ

### 2026-06-24T09:23:04+09:00 WARN 商品: GU製品入力
- URL: `https://www.sqstackstaging.com/admin/products/create`
- 詳細: {"fills": [{"ok": true, "label": "商品コード", "value": "TEST_FAQ_20260624_GU_092214"}, {"ok": true, "label": "商品名", "value": "TEST_FAQ_20260624 GU検証Tシャツ 092214"}, {"ok": true, "label": "説明文", "value": "E2E検証用のGU製品。既存ユーザーには紐づけない。"}, {"ok": true, "label": "オプション名", "value": "カラー"}, {"ok": true, "label": "オプション値", "value": "NAVY / M"}, {"ok": true, "label": "コード", "value": "NAVY_M"}, {"ok": true, "label": "ページタイトル", "value": "TEST_FAQ_20260624 GU検証Tシャツ 092214"}, {"ok": true, "label": "メタディスクリプション", "value": "E2E検証用"}, {"ok": true, "label": "商品タイプ", "value": "Tシャツ"}, {"ok": true, "label": "製造元", "value": "GU"}], "selects": [{"ok": true, "label": "種別", "text": "カラー", "value": "COLOR"}, {"ok": false, "reason": "select not found", "labels": "下書き"}]}
- 見出し: 保存されていない変更があります / 商品を作成する / メディア / バリエーション / 検索エンジンリスティング / ステータス
- 通知: 商品を作成する。このページの準備が整いました / 26/5000 / 6/5000
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 商品を作成する。このページの準備が整いました 商品を作成する 商品コード 半角英数字（A〜Z、a〜z、0〜9）、ハイフン（-）、アンダースコア（_）のみご入力ください

### 2026-06-24T09:23:08+09:00 OK 商品: 保存
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: TEST_FAQ_20260624 GU検証Tシャツ 092214 / 商品コード / メディア（0件） / バリエーション / 検索エンジンリスティング / ステータス
- 通知: TEST_FAQ_20260624 GU検証Tシャツ 092214。このページの準備が整いました / 26/5000 / 6/5000 / 商品を作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 TEST_FAQ_20260624 GU検証Tシャツ 092214。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 情報 下書き その他の操作 商品コード TEST_FA

### 2026-06-24T09:23:08+09:00 OK 商品: 作成後のGU製品名確認
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product`
- 詳細: contains `TEST_FAQ_20260624 GU検証Tシャツ 092214` = True
- 見出し: TEST_FAQ_20260624 GU検証Tシャツ 092214 / 商品コード / メディア（0件） / バリエーション / 検索エンジンリスティング / ステータス
- 通知: TEST_FAQ_20260624 GU検証Tシャツ 092214。このページの準備が整いました / 26/5000 / 6/5000 / 商品を作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 TEST_FAQ_20260624 GU検証Tシャツ 092214。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 情報 下書き その他の操作 商品コード TEST_FA

### 2026-06-24T09:23:14+09:00 OK OPEN https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/create
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/create`
- 見出し: バリエーションを追加する / オプション / メディア / 価格設定 / 在庫 / 販売
- 通知: 。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 バリエーションを追加する product variant thumbnail TEST_FAQ_20260624 GU検

### 2026-06-24T09:23:16+09:00 OK 商品: GUバリエーション入力
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/create`
- 詳細: [{"i": 0, "tag": "SELECT", "type": "select-one", "value": "NAVY / M", "text": "NAVY / M"}, {"i": 1, "tag": "INPUT", "type": "number", "value": "1990", "checked": false, "text": ""}, {"i": 2, "tag": "INPUT", "type": "text", "value": "TEST_FAQ_20260624_GU_092214_NAVY_M", "checked": false, "text": ""}, {"i": 3, "tag": "INPUT", "type": "text", "value": "TEST_FAQ_20260624_GU_092214_NAVY_M_MFG", "checked": false, "text": ""}, {"i": 4, "tag": "INPUT", "type": "checkbox", "value": "on", "checked": false, "text": ""}, {"i": 5, "tag": "INPUT", "type": "checkbox", "value": "on", "checked": false, "text": ""}, {"i": 6, "tag": "INPUT", "type": "text", "value": "", "checked": false, "text": ""}, {"i": 7, "tag": "INPUT", "type": "text", "value": "", "checked": false, "text": ""}]
- 見出し: バリエーションを追加する / オプション / メディア / 価格設定 / 在庫 / 販売
- 通知: 。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 バリエーションを追加する product variant thumbnail TEST_FAQ_20260624 GU検

### 2026-06-24T09:23:19+09:00 OK 商品: GUバリエーション作成
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 詳細: {"ok": true, "text": "作成する", "tag": "BUTTON"}
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました / バリエーションを作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:20+09:00 OK 商品: 作成後のSKU確認
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 詳細: contains `TEST_FAQ_20260624_GU_092214_NAVY_M` = True
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました / バリエーションを作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:20+09:00 INFO 商品: テストデータ情報
- 詳細: product_code=TEST_FAQ_20260624_GU_092214, sku_code=TEST_FAQ_20260624_GU_092214_NAVY_M, variant_url=https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant

### 2026-06-24T09:23:23+09:00 OK OPEN https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:26+09:00 OK 在庫追跡: OFFにして更新
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 詳細: {"check": {"ok": true, "label": "在庫を追跡する", "checked": false}, "click": {"ok": true, "text": "更新する", "tag": "BUTTON"}}
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました / バリエーションを更新しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:30+09:00 OK OPEN /admin/inventory_allocation_requests/create
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する

### 2026-06-24T09:23:31+09:00 OK 在庫追跡OFF: バリエーション選択モーダルを開く
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:23:33+09:00 OK 在庫追跡OFF: 在庫依頼候補: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "placeholder": "SKUコードで検索する", "value": "TEST_FAQ_20260624_GU_092214_NAVY_M"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:23:34+09:00 OK 在庫追跡OFF: 在庫依頼候補: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "row": "アイテムを選択する productVariant thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M TEST_FAQ_20260624_GU_092214 TEST_FAQ_20260624_GU_092214_NAVY_M"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:23:36+09:00 OK 在庫追跡OFF: 在庫依頼候補: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:23:36+09:00 OK 在庫追跡OFF: 在庫依頼フォームにSKUが入る
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: contains `TEST_FAQ_20260624_GU_092214_NAVY_M` = True
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:23:39+09:00 OK OPEN https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:42+09:00 OK 在庫追跡: ONへ復旧
- URL: `https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant`
- 詳細: {"check": {"ok": true, "label": "在庫を追跡する", "checked": true}, "click": {"ok": true, "text": "更新する", "tag": "BUTTON"}}
- 見出し: NAVY / M / オプション / メディア / 価格 / 在庫 / 原価
- 通知: 。このページの準備が整いました / バリエーションを更新しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 カタログ 店舗受取 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 。このページの準備が整いました TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M 在庫管理 product variant thumbnail TEST_FAQ_20260624 GU

### 2026-06-24T09:23:46+09:00 OK OPEN /admin/inventory_adjustment_orders/create
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 見出し: 調整伝票を作成する / ロケーション / 理由 / 商品
- 通知: 調整伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 その他 選択してください 商品 参照 保存する

### 2026-06-24T09:23:47+09:00 OK 調整伝票: ロケーション選択を開く
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 調整伝票を作成する / ロケーション / 理由 / 商品 / ロケーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 その他 選択してください 商品 参照 保存する ロケー

### 2026-06-24T09:23:49+09:00 WARN 調整伝票: ロケーション選択: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": false, "reason": "search field not found"}
- 見出し: 調整伝票を作成する / ロケーション / 理由 / 商品 / ロケーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 その他 選択してください 商品 参照 保存する ロケー

### 2026-06-24T09:23:50+09:00 OK 調整伝票: ロケーション選択: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "row": "アイテムを選択する TEST_FAQ_20260624_GU倉庫_ON_092214 TEST_FAQ_20260624_WH_092214"}
- 見出し: 調整伝票を作成する / ロケーション / 理由 / 商品 / ロケーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 その他 選択してください 商品 参照 保存する ロケー

### 2026-06-24T09:23:52+09:00 OK 調整伝票: ロケーション選択: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品
- 通知: 調整伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:23:53+09:00 OK 調整伝票: 理由選択
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "label": "", "text": "その他", "value": "その他"}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品
- 通知: 調整伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:23:55+09:00 OK 調整伝票: 商品検索
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "placeholder": "商品を検索する", "value": ""}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品
- 通知: 調整伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:23:56+09:00 WARN 調整伝票: 商品行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": false, "reason": "row not found containing text", "text": "TEST_FAQ_20260624_GU_092214_NAVY_M", "firstRows": []}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品
- 通知: 調整伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:23:58+09:00 OK 調整伝票: 参照/追加
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "text": "参照", "tag": "BUTTON"}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:23:59+09:00 OK 調整伝票: 数量入力
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"changed": []}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:24:02+09:00 OK 調整伝票: 保存
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:24:03+09:00 FAIL 調整伝票: 保存後URL確認
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: url_changed_from_create=False
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:24:04+09:00 WARN 調整伝票: 実行ボタン確認/押下
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": false, "reason": "click target not found", "texts": ["実行する", "実施する"]}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:24:07+09:00 WARN 調整伝票: 実行確認
- URL: `https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create`
- 詳細: {"ok": false, "reason": "click target not found", "texts": ["実行する", "実施する", "更新する"]}
- 見出し: 保存されていない変更があります / 調整伝票を作成する / ロケーション / 理由 / 商品 / バリエーションを選択する
- 通知: 調整伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更があります 変更を破棄 保存する 調整伝票を作成する。このページの準備が整いました 調整伝票を作成する ロケーション ロケーション 選択 理由 選択してください 廃棄 見本 紛失 棚卸差異 

### 2026-06-24T09:24:10+09:00 OK OPEN /admin/inventory_allocation_requests/create
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する

### 2026-06-24T09:24:12+09:00 OK 在庫依頼: 商品選択モーダルを開く
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:24:14+09:00 OK 在庫依頼: 商品選択: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "placeholder": "SKUコードで検索する", "value": "TEST_FAQ_20260624_GU_092214_NAVY_M"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:24:15+09:00 OK 在庫依頼: 商品選択: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "row": "アイテムを選択する productVariant thumbnail TEST_FAQ_20260624 GU検証Tシャツ 092214 NAVY / M TEST_FAQ_20260624_GU_092214 TEST_FAQ_20260624_GU_092214_NAVY_M"}
- 見出し: 在庫依頼を作成する / 商品 / リクエスト内容 / バリエーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション 選択 リクエスト内容 希望数 移動先ロケーション 選択 リクエスト先ロケーション 選択 保存する バリエーションを選択する SKUコー

### 2026-06-24T09:24:17+09:00 OK 在庫依頼: 商品選択: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:17+09:00 OK 在庫依頼: 希望数
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "label": "希望数", "value": "1"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:19+09:00 OK 在庫依頼: 移動先選択モーダルを開く
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:21+09:00 WARN 在庫依頼: 移動先: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": false, "reason": "search field not found"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:22+09:00 OK 在庫依頼: 移動先: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "row": "アイテムを選択する TEST_FAQ_20260624_GU店舗_OFF_092214 TEST_FAQ_20260624_STORE_092214"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:24+09:00 OK 在庫依頼: 移動先: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:25+09:00 OK 在庫依頼: 依頼先選択モーダルを開く
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:27+09:00 WARN 在庫依頼: 依頼先: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": false, "reason": "search field not found"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:29+09:00 OK 在庫依頼: 依頼先: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "row": "アイテムを選択する TEST_FAQ_20260624_GU倉庫_ON_092214 TEST_FAQ_20260624_WH_092214"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容 / ロケーションを選択する
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:30+09:00 OK 在庫依頼: 依頼先: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 在庫依頼を作成する / 商品 / リクエスト内容
- 通知: 在庫依頼を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存する 在庫依頼を作成する。このページの準備が整いました 在庫依頼を作成する 商品 商品バリエーション product thumbnail TEST_FAQ_20260624 GU検証Tシャツ 0

### 2026-06-24T09:24:33+09:00 OK 在庫依頼: 保存
- URL: `https://www.sqstackstaging.com/admin/inventory_allocation_requests/726d9d8e-929b-533d-a875-a3a474cd18a0_InventoryAllocationRequest`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: 在庫依頼
- 通知: 在庫依頼 / 在庫依頼を作成しました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 2件 2 確保済み CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 在庫依頼 在庫依頼を作成しました

### 2026-06-24T09:24:37+09:00 OK OPEN /admin/inventory_movement_orders/create
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 見出し: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- 通知: 移動伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する

### 2026-06-24T09:24:39+09:00 OK 移動伝票: 配送元選択を開く
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを選択する すべて 店舗 倉庫 すべての

### 2026-06-24T09:24:41+09:00 WARN 移動伝票: 配送元: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": false, "reason": "search field not found"}
- 見出し: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを選択する すべて 店舗 倉庫 すべての

### 2026-06-24T09:24:42+09:00 OK 移動伝票: 配送元: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "row": "アイテムを選択する TEST_FAQ_20260624_GU倉庫_ON_092214 TEST_FAQ_20260624_WH_092214"}
- 見出し: 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを選択する すべて 店舗 倉庫 すべての

### 2026-06-24T09:24:43+09:00 OK 移動伝票: 配送元: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- 通知: 移動伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する

### 2026-06-24T09:24:45+09:00 OK 移動伝票: 配送先選択を開く
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "選択", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを

### 2026-06-24T09:24:47+09:00 WARN 移動伝票: 配送先: モーダル検索入力
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": false, "reason": "search field not found"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを

### 2026-06-24T09:24:48+09:00 OK 移動伝票: 配送先: 行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "row": "アイテムを選択する TEST_FAQ_20260624_GU店舗_OFF_092214 TEST_FAQ_20260624_STORE_092214"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / ロケーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました
- 先頭テーブル: すべてのアイテムを選択する | 名前 | 場所コード
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する ロケーションを

### 2026-06-24T09:24:50+09:00 OK 移動伝票: 配送先: 選択確定
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "選択する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- 通知: 移動伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する

### 2026-06-24T09:24:52+09:00 OK 移動伝票: 商品検索
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "placeholder": "商品を検索する", "value": ""}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- 通知: 移動伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する

### 2026-06-24T09:24:53+09:00 WARN 移動伝票: 商品行選択
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": false, "reason": "row not found containing text", "text": "TEST_FAQ_20260624_GU_092214_NAVY_M", "firstRows": []}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加
- 通知: 移動伝票を作成する。このページの準備が整いました
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する

### 2026-06-24T09:24:55+09:00 OK 移動伝票: 商品参照
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "参照", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / バリエーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する バリエーション

### 2026-06-24T09:24:56+09:00 OK 移動伝票: 数量入力
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"changed": []}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / バリエーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU | 在庫数
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 保存する バリエーション

### 2026-06-24T09:24:59+09:00 OK 移動伝票: 保存
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: {"ok": true, "text": "保存する", "tag": "BUTTON"}
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / バリエーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU | 在庫数
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 商品を1つ以上追加してく

### 2026-06-24T09:25:00+09:00 FAIL 移動伝票: 保存後URL確認
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: url_changed_from_create=False
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / バリエーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU | 在庫数
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 商品を1つ以上追加してく

### 2026-06-24T09:25:00+09:00 OK E2E実行完了
- URL: `https://www.sqstackstaging.com/admin/inventory_movement_orders/create`
- 詳細: 作成データ: TEST_FAQ_20260624_取引先_092214, TEST_FAQ_20260624_ブランド_092214, TEST_FAQ_20260624_決済_092214, TEST_FAQ_20260624_GU店舗_OFF_092214, TEST_FAQ_20260624_GU倉庫_ON_092214, TEST_FAQ_20260624_カタログ_092214, TEST_FAQ_20260624_GU_092214
- 見出し: 保存されていない変更 / 移動伝票を作成する / 配送元 / 配送先 / 商品を追加 / バリエーションを選択する
- 通知: 移動伝票を作成する。このページの準備が整いました / 絞り込みを追加
- 先頭テーブル: すべてのアイテムを選択する | バリエーション | 商品コード | SKU | 在庫数
- 抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 移動伝票 調整伝票 取置伝票 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 保存されていない変更 取り消す 保存 移動伝票を作成する。このページの準備が整いました 移動伝票を作成する 配送元 配送元 選択 配送先 配送先 選択 商品を追加 商品を追加する 参照 商品を1つ以上追加してく
