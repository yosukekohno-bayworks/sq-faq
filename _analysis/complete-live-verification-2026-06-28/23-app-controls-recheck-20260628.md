# 23 API/Webhook アプリ操作導線再確認 2026-06-28

- 対象アプリ: `TEST_FAQ_20260624_APP_113636`
- 対象画面: `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/23-app-controls-recheck-20260628.json`

## 結果

- アプリ詳細で削除/失効/再発行導線なし: `確認`
- アプリ一覧カードで削除/失効/再発行導線なし: `確認`
- Webhook作成後の編集/削除/停止導線なし: `確認`
- リクエストログはTODO表示: `確認`
- Storefrontトークン発行ボタンは表示のみ確認: `確認`

## ステップ

### app-detail

- URL: `https://www.sqstackstaging.com/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- 本文抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 TEST_FAQ_20260624_APP_113636。このページの準備が整いました TEST_FAQ_20260624_APP_113636 ヘルプページ Admin API アクセストークン 2026年06月24日 11:36に作成されました シークレット 2026年06月24日 11:36に作成されました 検証方法 Playgroundのヘッダー設定で、アクセストークンを使用してリクエストを送信できます。 Playgroundを開く リクエストログ このトークンを使用して行われたリクエストのログを閲覧することができます。 リクエストログを見る Storefront API アクセストークンを発行することで、ストアフロントAPIにアクセスできるようになります。 トークンを発行する Webhook イベントに関するJSON通知をURLに送信します 注文の作成 https://sq-faq-webhook.invalid/20260627173343・JSON Webhookを作成する
- 操作要素: `コンテンツにスキップ, /admin, stack-ps-yosuke

陽介 河野, ホーム, 商品管理, 在庫管理, 注文管理, 顧客管理, 発注管理, 販売設定, 会計, 分析, 入荷管理, 出荷管理, 在庫依頼
未完了の在庫依頼 3件
3, ディスカウント, ポイント, 会員ランク, Shopify, OmnibusCore, スマレジ, リテールポータル, 卸売, 設定, /admin/settings/apps, ヘルプページ, Playgroundを開く, リクエストログを見る, トークンを発行する, Webhookを作成する`

### webhook-create-dialog

- URL: `https://www.sqstackstaging.com/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- 本文抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 TEST_FAQ_20260624_APP_113636。このページの準備が整いました TEST_FAQ_20260624_APP_113636 ヘルプページ Admin API アクセストークン 2026年06月24日 11:36に作成されました シークレット 2026年06月24日 11:36に作成されました 検証方法 Playgroundのヘッダー設定で、アクセストークンを使用してリクエストを送信できます。 Playgroundを開く リクエストログ このトークンを使用して行われたリクエストのログを閲覧することができます。 リクエストログを見る Storefront API アクセストークンを発行することで、ストアフロントAPIにアクセスできるようになります。 トークンを発行する Webhook イベントに関するJSON通知をURLに送信します 注文の作成 https://sq-faq-webhook.invalid/20260627173343・JSON Webhookを作成する Webhookを追加する イベント 選択してください 注文の作成 注文の更新 在庫の更新 選択してください エンドポイント キャンセル 保
- 操作要素: `コンテンツにスキップ, /admin, stack-ps-yosuke

陽介 河野, ホーム, 商品管理, 在庫管理, 注文管理, 顧客管理, 発注管理, 販売設定, 会計, 分析, 入荷管理, 出荷管理, 在庫依頼
未完了の在庫依頼 3件
3, ディスカウント, ポイント, 会員ランク, Shopify, OmnibusCore, スマレジ, リテールポータル, 卸売, 設定, /admin/settings/apps, ヘルプページ, Playgroundを開く, リクエストログを見る, トークンを発行する, Webhookを作成する`
- select選択肢: `選択してください, 注文の作成, 注文の更新, 在庫の更新`

### app-list

- URL: `https://www.sqstackstaging.com/admin/settings/apps`
- 本文抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 アプリ。このページの準備が整いました アプリ アプリを作成 TEST_FAQ_20260624_APP_113636 TEST_FAQ_20260624_APP_113636 TEST_FAQ_アプリ TEST_FAQ_アプリ TEST_FAQ_アプリ TEST_FAQ_アプリ
- 操作要素: `コンテンツにスキップ, /admin, stack-ps-yosuke

陽介 河野, ホーム, 商品管理, 在庫管理, 注文管理, 顧客管理, 発注管理, 販売設定, 会計, 分析, 入荷管理, 出荷管理, 在庫依頼
未完了の在庫依頼 3件
3, ディスカウント, ポイント, 会員ランク, Shopify, OmnibusCore, スマレジ, リテールポータル, 卸売, 設定, /admin/settings, アプリを作成, 個の詳細を表示する`

### request-log

- URL: `https://www.sqstackstaging.com/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App/admin_api`
- 本文抜粋: コンテンツにスキップ stack-ps-yosuke 陽介 河野 ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 リクエストログ。このページの準備が整いました リクエストログ Admin API - TEST_FAQ_20260624_APP_113636 TODO
- 操作要素: `コンテンツにスキップ, /admin, stack-ps-yosuke

陽介 河野, ホーム, 商品管理, 在庫管理, 注文管理, 顧客管理, 発注管理, 販売設定, 会計, 分析, 入荷管理, 出荷管理, 在庫依頼
未完了の在庫依頼 3件
3, ディスカウント, ポイント, 会員ランク, Shopify, OmnibusCore, スマレジ, リテールポータル, 卸売, 設定, /admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`

