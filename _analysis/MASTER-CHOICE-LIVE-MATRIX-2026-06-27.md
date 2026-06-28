# 設定マスタ候補表示 実機確認マトリクス（2026-06-27）

## 結論

「設定でマスタが未登録だと各業務画面の選択肢が空になる」と一律には言えません。実機では、候補が出ない原因は次の4種類に分かれます。

| 原因 | 実機で確認した例 |
|:--|:--|
| マスタ/データが0件 | ディスカウントの顧客追加ダイアログは顧客0件で空表示、`選択する` disabled |
| 検索条件・種別フィルタ不一致 | 店舗受取/リテールポータルのロケーション選択で、店舗欄に倉庫コード、倉庫欄に店舗コードを入れると0件 |
| 連携・チャネル未接続 | 販売上限ルール作成のチャネル候補が空で、保存時に `チャネルを選択してください` |
| 参照UIが存在しない/標準UIでは紐づけ不可 | 採寸ルールは商品紐づけUIなし。通知用メール、APIアプリ、決済方法は管理画面単体で候補先を再現できない |

既存のテナント・ブランド・取引先などを全削除して「組織全体を0件化」する検証は実施していません。既存検証環境を壊すためです。代わりに、既存候補の有無、検索不一致、種別不一致、連携未接続、作成/削除済みテストデータの反映を組み合わせて確認しています。

## マトリクス

| 対象データ | 参照先UI | 候補ありの確認 | 候補なし/不一致の確認 | 結論 | 主な証跡 |
|:--|:--|:--|:--|:--|:--|
| テナント | 発注伝票、Shopify、OmnibusCore、スマレジ、リテールポータル、売上実績CSV、ポイントCSV | 発注伝票で5件、Shopify/OmnibusCore/スマレジ/リテールポータルで5件のoptionを確認 | 既存テナント全削除は未実施。native selectのため検索不一致は再現不可 | テナントは多くの必須selectに出る。0件時のUIは未破壊では未確認 | `master-choice-purchase-create-controls.json`, `master-choice-shopify-create-controls.json`, `master-choice-omnibus-create-controls.json`, `master-choice-smaregi-create-controls.json`, `master-choice-retail-portal-create-controls.json` |
| ロケーション | 店舗受取ルール、リテールポータル店舗/在庫ロケーション、在庫/伝票/CSV/販売員/ロケーショングループ | 店舗受取で `R0001`、リテールポータル店舗で店舗群、在庫ロケーションで倉庫群を確認 | 店舗欄で `W0001` 検索0件、在庫欄で `R0001` 検索0件 | ロケーションは用途ごとに種別フィルタあり。未登録以外に、種別不一致でも空になる | `master-choice-local-pickup-location-search-W0001-empty.md`, `master-choice-local-pickup-location-search-R0001-one.md`, `master-choice-retail-portal-store-search-W0001-empty-data.json`, `master-choice-retail-portal-inventory-search-R0001-empty-data.json` |
| ロケーショングループ | Shopify、OmnibusCore | Shopify/OmnibusCoreで `GU グループ`, `ユニクログループ`, `TEST_FAQ_20260624_LG_171810` を確認 | 全件0件化は未実施 | 外部連携の在庫引当元/対象範囲としてselect候補に出る | `master-choice-shopify-create-controls.json`, `master-choice-omnibus-create-controls.json` |
| ブランド | 商品作成・編集のブランド選択ダイアログ、カタログ/販売閾値のブランドコード条件 | 商品作成の `ブランドを選択する` ダイアログで `UNIQLO`, `GU`, TESTブランドを確認 | ダイアログに検索欄なし。全ブランド削除は未実施 | ブランドは商品分類の候補に出る。ただし「空検索」はない | `master-choice-product-brand-dialog-data.json` |
| 取引先 | 発注伝票の取引先select | 発注伝票作成で `TEST_FAQ_Supplier`, `TEST_E2E_20260622_取引先_*` など9件を確認 | 全取引先アーカイブ/削除は未実施 | 発注伝票の必須select候補に出る。アーカイブ後の候補除外は今回未確定に戻す | `master-choice-purchase-create-controls.json`, `basic04-suppliers-list.md` |
| 決済方法 | 注文/出荷の決済条件 | 決済方法作成フォームは確認済み | 実注文データ・決済選択UIが必要。標準stagingで候補先未確認 | 「作成できる」は確定。業務画面の選択肢になるとは断定しない | `basic04-payment-method-create-form.md`, `basic04-payment-method-create-empty-save.md` |
| 販売員 | リテールポータル利用時の販売員識別、販売員作成の初期ロケーション | 販売員作成でロケーション選択UIを確認。既存ロケーション候補あり | ロケーション未選択の空保存で `ロケーションを選択してください` | 販売員自体の選択はリテールポータル接続後の画面依存。管理画面単体では販売員候補先は未確認 | `master-choice-retail-staff-create-controls.json`, `basic04-retail-staff-location-modal.md`, `basic04-retail-staff-create-empty-save.md` |
| 管理メンバー | 管理画面ログイン、権限/テナント割当、リテールポータルユーザー追加候補 | 管理メンバー作成画面で権限グループ候補を確認 | 実ユーザー作成/リテールポータルユーザー追加は未実行 | 管理メンバーの候補化は一部未確認。権限グループ割当UIは確定 | `master-choice-user-create-controls.json`, `account02-user-detail-loaded-recheck.md` |
| 権限グループ | 管理メンバー作成/詳細の権限欄 | ユーザー追加で `特権管理者`, `TEST_権限検証_20260620` のradio候補を確認 | 未割当の一時グループ削除後に一覧から消えることを既存検証で確認 | 候補に出る。作っただけでは効かず、メンバー割当が必要 | `master-choice-user-create-controls.json`, `account02-permission-group-after-delete-recheck.md` |
| 通知用メールアドレス | 通知メール送信先 | 作成/削除フォームは確認済み | 実通知イベントの発生が必要 | 候補選択UIではなく送信先リスト。業務画面の選択肢とは別 | `org03-notification-email-create-form-recheck.md`, `org03-notification-email-after-delete-recheck.md` |
| メタフィールド定義 | 対象オブジェクト詳細の「メタフィールド」セクション、CSV、翻訳対象 | 商品メタフィールド定義作成後、商品詳細にセクション表示・値保存・使用箇所1件を確認 | 定義削除後、商品詳細のメタフィールド表示が消えることを確認 | 典型的な「設定すると業務画面に項目が出る/削除すると消える」データ | `area08-product-detail-metafield-before.md`, `area08-product-detail-metafield-after-value-save.md`, `area08-product-detail-after-definition-delete.md` |
| 翻訳ルール | 翻訳トップのルール選択 | 翻訳トップのメニューに `TEST_FAQ_英語翻訳ルール`, `TEST_FAQ_翻訳ルール_英語`, `Test_中国語` を確認 | ルール全削除は未実施 | 翻訳トップのルール候補に出る。ルール未選択では商品リソースに進めない | `master-choice-translation-rule-menu-data.json`, `area09-translation-top-rule-selected.md` |
| 採寸ルール | 商品への採寸紐づけ | 採寸ルール作成・一覧・詳細readonlyを確認 | 商品詳細で紐づけUIなし、削除/編集UIなし | 管理画面上では「候補として選ぶ」画面を確認できない | `area10-product-detail-check-measurement-attachment.md`, `area10-measurement-detail-after-create.md` |
| アプリ/API | API権限スコープ、Webhook作成 | アプリ作成フォームで76権限スコープ、Webhookダイアログを確認 | 業務画面の候補ではない。API実行は未実施 | 「マスタ選択肢」ではなく外部アクセス設定 | `area23-app-create-form.md`, `area23-webhook-create-dialog.md` |
| カタログ | Shopify/OmnibusCore/スマレジ/リテールポータル連携 | Shopify/リテールポータルは必須、OmnibusCore/スマレジは任意selectとして `TEST_FAQ_カタログ001`, `UNIQLO` を確認 | 全カタログ削除は未実施 | 外部連携で対象商品グループとして指定する。CSV在庫エクスポートとは別 | `master-choice-shopify-create-controls.json`, `master-choice-omnibus-create-controls.json`, `master-choice-smaregi-create-controls.json`, `master-choice-retail-portal-create-controls.json` |
| 販売価格/予約/販売上限/販売閾値ルール | Shopify/OmnibusCore/リテールポータル連携 | Shopifyの販売価格ルール、OmnibusCoreの在庫予約ルール、リテールポータルの販売閾値ルールに候補あり | 販売上限ルールはOmnibusCore側selectがplaceholderのみ。販売上限ルール作成ではチャネル未接続で空保存エラー | ルールにより候補有無が異なる。販売上限はチャネル接続前だと作成/選択が詰まる | `master-choice-shopify-create-controls.json`, `master-choice-omnibus-create-controls.json`, `master-choice-retail-portal-create-controls.json`, `master-choice-sale-limit-create-channel-empty.md` |
| 顧客/顧客セグメント | ディスカウント対象顧客追加 | 顧客0件のため候補なしを確認 | `顧客を選択する` ダイアログ空、`選択する` disabled。顧客セグメント追加はメニュー上disabled | 設定マスタではないが、0件で空になる実例 | `master-choice-discount-customers-select-dialog-empty.md`, `master-choice-discount-customers-add-menu.md` |

