# 画面・URL索引

| ナビ表記 | 画面見出し(h1) | URL | ひとこと説明 | 機能ガイド |
|:--|:--|:--|:--|:--|
| ホーム | （組織名、例: stack-ps-yosuke） | /admin | ダッシュボード。クイックリンクと製品アップデートへのリンクを表示 | - |
| 商品管理 | 商品管理 | /admin/products | 商品の一覧・作成・編集・アーカイブ | 商品管理.md |
| 商品管理 > カタログ | カタログ | /admin/catalogs | 商品をグループ化するカタログの管理 | カタログ.md |
| 商品管理 > 店舗受取 | 店舗受取 | /admin/local_pickup_product_variants | 店舗受取を有効にするバリエーションの管理 | - |
| 在庫管理 | 在庫管理 : | /admin/inventory_items | SKU×ロケーション単位の在庫数確認・編集 | 在庫管理.md |
| 在庫管理 > 移動伝票 | 移動伝票 | /admin/inventory_movement_orders | ロケーション間の在庫移動伝票を管理 | 移動伝票.md |
| 在庫管理 > 調整伝票 | 調整伝票 | /admin/inventory_adjustment_orders | 棚卸し・廃棄などの在庫数手動調整を記録 | 調整伝票.md |
| 在庫管理 > 取置伝票 | 取置伝票 | /admin/inventory_reservation_orders | 特定用途への在庫確保を管理 | 取置伝票.md |
| 注文管理 | 注文管理 | /admin/orders | 販売チャネルから流入した注文の一覧・追跡 | 注文管理.md |
| 注文管理 > 下書き | 下書き | /admin/draft_orders | 管理画面から手動起票する注文の管理 | 注文管理.md |
| 注文管理 > 返品 | 返品 | /admin/order_returns | 返品処理の一覧確認と絞り込み | 注文管理.md |
| 顧客管理 | 顧客管理 | /admin/purchasing_customers | チャネル経由で流入した顧客の一覧・絞り込み | 顧客管理.md |
| 顧客管理（直接作成URL） | 予期せぬエラーが発生しました | /admin/purchasing_customers/create | 通常導線のない顧客作成URL。直接アクセスしても作成フォームは開かない | 顧客管理.md |
| 顧客管理 > 会社 | 会社 | /admin/companies | B2B法人顧客（会社）の管理 | 会社.md |
| 発注管理 | 発注管理 | /admin/inventory_purchase_orders | 取引先への発注伝票の作成・管理 | 発注管理.md |
| 販売設定 | 販売価格ルール | /admin/product_price_rules | 販売価格ルールの一覧（サブメニューのトップ） | 販売設定.md |
| 販売設定 > 販売価格 | 販売価格ルール (セール価格) / 販売価格ルール | /admin/product_price_rules | 商品価格（通常・セール）の管理 | 販売設定.md |
| 販売設定 > 予約販売 | 予約販売ルール | /admin/inventory_back_order_rules | 在庫0でも販売継続するバックオーダーのルール管理 | 販売設定.md |
| 販売設定 > 販売上限 | 販売上限ルール | /admin/inventory_sale_limit_rules | 販売数量の上限を定めるルール管理 | 販売設定.md |
| 販売設定 > 販売閾値 | 販売閾値ルール | /admin/inventory_threshold_rules | 在庫が閾値以下のときの挙動を制御するルール管理 | 販売設定.md |
| 会計 | 売上実績 | /admin/sale_change_line_items | 売上実績の一覧確認・CSVエクスポート | 会計（売上実績）.md |
| 分析 | 分析 | /admin/analytics | 分析トップ（未実装・TODO表示） | - |
| 分析 > 収益 | 売上 | /admin/analytics/revenue | 収益レポート（未実装・TODO表示）。ナビ名「収益」と画面h1「売上」は不一致 | - |
| 分析 > レポート | レポート | /admin/analytics/reports | レポート（未実装・TODO表示） | - |
| 入荷管理 | 入荷管理 | /admin/inventory_inbound_orders | 入荷指示の一覧・入荷実績登録 | 入荷管理.md |
| 出荷管理 | 出荷管理 | /admin/inventory_outbound_orders | 出荷指示の一覧・出荷実績登録・ヤマトB2クラウドCSV連携 | 出荷管理.md |
| 在庫依頼 | 在庫依頼 | /admin/inventory_allocation_requests | 取り寄せ販売の起点。在庫確保依頼の作成・管理 | 在庫依頼.md |
| 在庫依頼 > 確保済み | 確保済み | /admin/inventory_allocation_request_confirmations | 引当完了済み在庫の確認と移動伝票一括作成 | 在庫依頼.md |
| ディスカウント | ディスカウント | /admin/order_price_adjustment_rules | クーポンコード付き注文割引ルールの作成・管理 | ディスカウント.md |
| ディスカウント > 顧客管理 | 顧客管理 | /admin/order_price_adjustment_rules/{id}/customers | 対象顧客をメール検索で追加するタブ。顧客0件の環境では追加不可 | ディスカウント.md |
| ディスカウント > 店舗管理 | 店舗管理 | /admin/order_price_adjustment_rules/{id}/locations | 対象ロケーション/ロケーショングループを管理するタブ。ロケーションは追加・適用種別変更・削除可 | ディスカウント.md |
| ポイント | 注文ポイント | /admin/point_calculation_rules | 注文ポイント付与ルールの作成・管理。ナビ名「ポイント」と画面h1「注文ポイント」は不一致 | ポイント.md |
| ポイント > 注文ポイント > 会員ランク倍率 | 会員ランク倍率 | /admin/point_calculation_rules/{id}/point_multiplier_customer_ranks | タブと「追加する」ボタンは確認済み。2026-06-19時点では追加フォーム表示までは確認できていない | ポイント.md |
| ポイント > 注文ポイント > 商品倍率 | 商品倍率 | /admin/point_calculation_rules/{id}/point_multiplier_products | タブと「追加する」ボタンは確認済み。2026-06-19時点では追加フォーム表示までは確認できていない | ポイント.md |
| ポイント > キャンペーン | ポイントキャンペーン | /admin/point_campaign_order_rules | ポイント増倍・追加付与キャンペーンの管理 | ポイント.md |
| ポイント > キャンペーン > 会員ランク設定 | 会員ランクのキャンペーン設定 | /admin/point_campaign_order_rules/{id}/customer_ranks | 会員ランク種別キャンペーンのランク別倍率を追加・削除する | ポイント.md |
| ポイント > キャンペーン > 購入金額設定 | 購入金額のキャンペーン設定 | /admin/point_campaign_order_rules/{id}/purchase_prices | 購入金額種別キャンペーンの金額条件と倍率を追加・削除する | ポイント.md |
| ポイント > キャンペーン > 商品設定 | 商品のキャンペーン設定 | /admin/point_campaign_order_rules/{id}/product_variants | 商品種別キャンペーンの対象SKUと倍率を追加・削除する | ポイント.md |
| ポイント > 誕生日 | 誕生日ポイント付与ルール | /admin/point_calculation_birthday_rules | 誕生日ボーナスポイントのルール管理 | ポイント.md |
| ポイント > 誕生日 > 会員ランク別設定 | 会員ランク | /admin/point_calculation_birthday_rules/{id}/customer_ranks | 誕生日ポイントを会員ランク別に上書き設定する | ポイント.md |
| ポイント > 利用外商品 | 利用外商品 | /admin/point_application_excluded_products | ポイント利用対象外商品の登録 | ポイント.md |
| ポイント > 失効通知 | 失効通知 | /admin/point_expiration_notification_rule | ポイント失効前の通知ルール設定 | ポイント.md |
| 会員ランク | 会員ランク | /admin/customer_rank_calculation_rules | 会員ランク算出ルールの作成・管理 | 会員ランク.md |
| Shopify | Shopify連携 | /admin/shopify_integrations | ShopifyストアとSQの連携設定 | Shopify連携.md |
| OmnibusCore | OmnibusCore連携 | /admin/omnibus_core_integrations | OmnibusCore（オムニチャネルEC）との連携設定 | OmnibusCore連携.md |
| スマレジ | スマレジ連携 | /admin/smaregi_integrations | スマレジPOSとの連携設定。ナビ名「スマレジ」と画面h1「スマレジ連携」は不一致 | スマレジ連携.md |
| リテールポータル | リテールポータル連携 | /admin/retail_portal_integrations | 店舗スタッフ向けリテールポータルとの連携設定 | リテールポータル連携.md |
| 卸売 | 卸売 | /admin/b2b | 卸売（B2B）機能（未実装・TODO表示） | - |
| 設定 | 設定 | /admin/settings | 設定トップ。組織IDの確認とサブページ一覧 | 設定.md |
| 設定 > 管理メンバー | 管理メンバー | /admin/settings/users | 管理画面にアクセスできるメンバーの追加・管理 | 設定.md |
| 設定 > 管理メンバー（権限グループ） | 権限グループ一覧 | /admin/settings/permission_groups | 権限グループの作成・管理（管理メンバー画面内ボタンから遷移） | 設定.md |
| 設定 > テナント | テナント | /admin/settings/tenants | 事業部（テナント）マスタの管理 | 設定.md |
| 設定 > ロケーション | ロケーション | /admin/settings/locations | 在庫拠点（店舗・倉庫）マスタの管理 | 設定.md |
| 設定 > ロケーショングループ | ロケーショングループ | /admin/settings/location_groups | ロケーションをグループ化する設定 | 設定.md |
| 設定 > ブランド | ブランド | /admin/settings/brands | 商品に紐づけるブランドマスタの管理 | 設定.md |
| 設定 > 取引先 | 取引先 | /admin/settings/suppliers | 仕入先（発注の相手）マスタの管理 | 設定.md |
| 設定 > 決済方法 | 決済方法 | /admin/settings/payment_methods | 顧客が使用する決済方法マスタの管理 | 設定.md |
| 設定 > 販売員 | 販売員 | /admin/settings/retail_staff_members | 販売員マスタの管理 | 設定.md |
| 設定 > 納品書 | 納品書 | /admin/settings/pdf_template_package_slip | 納品書PDFテンプレートの管理 | 設定.md |
| 設定 > 通知用メールアドレス | 通知用メールアドレス | /admin/settings/organization_notification_emails | お知らせ・アラートメールの受信アドレス管理 | 設定.md |
| 設定 > アプリ | アプリ | /admin/settings/apps | Admin APIアクセス用アプリ（APIキー）の管理 | 設定.md |
| 設定 > ロジザード | ロジザード連携 | /admin/logizard_integrations | ロジザードZERO（WMS）との連携設定 | 設定.md |
| 設定 > Recustomer | Recustomer連携 | /admin/recustomer_integrations | 返品・交換プラットフォームRecustomerとの連携設定 | 設定.md |
| 設定 > 翻訳 | 翻訳 | /admin/settings/translation | 多言語翻訳ルールの管理（10言語対応） | 設定.md |
| 設定 > メタフィールド定義 | メタフィールド定義 | /admin/settings/metafield_definitions | 各オブジェクトへのカスタムフィールド追加定義 | 設定.md |
| 設定 > 採寸ルール | 採寸ルール | /admin/settings/product_measurement_rules | 衣料品の採寸項目・単位の定義 | 設定.md |
| ツール > CSVインポート | CSVインポート | /admin/csv_import | 22カテゴリ対応の一括データインポート | CSVインポート.md |
| ツール > CSVエクスポート | CSVエクスポート | /admin/csv_export | 在庫・売上実績・ポイント変動履歴などのCSV出力 | CSVエクスポート・PDFエクスポート.md |
| ツール > PDFエクスポート | PDFエクスポート | /admin/pdf_export | 納品書PDFのエクスポートカテゴリ確認。2026-06-19時点では任意新規生成ボタンは表示されず、直接作成URLも404相当 | CSVエクスポート・PDFエクスポート.md |
