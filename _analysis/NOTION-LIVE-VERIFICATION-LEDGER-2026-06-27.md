# Notion 実機重点検証台帳 2026-06-27

## 目的

`04-notion` 全24分類について、本文の断定表現をSQ staging実機で再確認し、実機で確認できないものは「未確認」「連携待ち」「開発元確認」に落とす。

今回のきっかけは、`01-SQ全体・共通導線` のロケーション説明に「倉庫はリテールポータル対象に出ない」と読める誤表現が残っていたこと。以後はNotion本文を優先監査対象にする。

## 検証ルール

- 実機確認は `https://www.sqstackstaging.com/admin` を正とする。
- 画面に表示された事実だけを「確定」とする。
- 外部接続・実注文・実顧客・別権限ログインが必要なものは、無理に確定せず `連携待ち` または `要確認` にする。
- ユーザー追加/削除、秘密値表示、本番操作は行わない。
- テストデータを作る場合は `TEST_NOTION_20260627_...` の接頭辞を使う。
- スナップショットは `_analysis/live-notion-verification-2026-06-27/` に保存する。
- ステータス遷移がある機能は、フォーム項目だけでは確定扱いにしない。操作前後で以下を確認する。
  - 詳細画面のステータス表示・実行可能ボタンの変化
  - 一覧のタブ/フィルタ/件数/行の移動先
  - 関連する伝票・指示・履歴・在庫区分の増減
  - エラー時のバリデーション文言と、途中状態から戻れるか
- ステータスを動かす検証は、既存業務データではなく `TEST_NOTION_20260627_...` などの検証データまたは明らかな既存TESTデータで行い、作成・実行・キャンセル・クローズ・アーカイブまで証跡を残す。

## 初回棚卸し

| No | Notion分類 | `/admin` URL数 | 強い断定表現 | 未確認/連携待ち表現 | 優先度 | 初回ステータス |
|:--|:--|--:|--:|--:|:--|:--|
| 01 | SQ全体・共通導線 | 24 | 25 | 8 | 高 | 2026-06-27再確認済み。ロケーション種別/リテールポータル/店舗受取の説明を実機根拠で修正済み。標準24分類の範囲表も現行番号へ修正 |
| 02 | アカウント・権限 | 5 | 59 | 13 | 高 | 管理メンバー一覧/追加/詳細、権限グループ作成/削除、管理ユーザーCSV、誤URL404を2026-06-27再確認。実ユーザー追加・除外・別権限ログイン効果は未実行 |
| 03 | 組織・通知 | 7 | 46 | 15 | 中 | 設定トップ/テナント一覧・作成フォーム・詳細、通知用メールアドレスの空保存/追加/選択/削除を2026-06-27再確認。通知の実送信とユーザーテナントの権限効果は未確認 |
| 04 | 基本マスタ | 10 | 68 | 15 | 高 | 2026-06-27再確認済み。ロケーション作成、アーカイブ/解除/再アーカイブ、一覧列・候補モーダル変化、ロケーショングループ/取引先/ブランド/決済方法/販売員のフォームとエラーを確認済み |
| 05 | 商品・SKU | 7 | 59 | 11 | 高 | 商品一覧/作成/バリエーション作成/非公開作成/アーカイブ解除/再アーカイブ/削除を2026-06-27再確認。ステータス移動と削除後URLエラーまで確認済み。外部チャネル同期は連携待ち |
| 06 | カタログ | 13 | 56 | 14 | 高 | カタログ作成フォームと各連携フォームのカタログ指定を実機確認済み。同期実動作は連携待ち |
| 07 | 店舗受取商品 | 3 | 20 | 19 | 高 | 商品側一覧/追加ダイアログ/直接作成URL404、店舗側ロケーションルールを実機確認済み |
| 08 | カスタムデータ | 5 | 22 | 13 | 中 | 2026-06-27再確認済み。メタフィールド定義作成、3文字namespace/key保存、商品詳細値保存、使用箇所0→1、削除後の一覧/商品詳細表示消滅を確認。外部連携反映は連携待ち |
| 09 | 翻訳 | 4 | 18 | 11 | 中 | 2026-06-27再確認済み。翻訳トップ、商品翻訳対象一覧/詳細、ルール作成/更新/削除、言語変更不可を確認。実翻訳生成/チャネル反映は未確認 |
| 10 | 採寸 | 4 | 21 | 3 | 中 | 2026-06-27再確認済み。採寸作成、5項目上限、詳細readonly、一覧表示、商品紐付けUIなし、削除/編集UIなしを確認。`TEST_MEASURE_20260627_0439` はUI削除不可のため残存 |
| 11 | 価格・販売制御 | 18 | 77 | 19 | 高 | 販売価格ルール作成/通常価格登録・削除/販売上限空保存を実機確認済み。チャネル適用は連携待ち |
| 12 | 在庫状態・在庫数 | 6 | 40 | 14 | 高 | ロケーション説明、調整伝票/取置伝票後の在庫数変化を修正済み |
| 13 | 在庫伝票 | 10 | 49 | 11 | 高 | ロケーション説明、分類番号参照、調整理由4択、調整/取置伝票ステータス遷移を修正済み |
| 14 | 入出荷・在庫依頼 | 5 | 49 | 16 | 高 | 在庫依頼→移動→出荷→入荷を `#IM-1025/#IO-1025/#II-1025` で実機確認済み。完了後の再実行不可も再確認済み |
| 15 | 発注・仕入 | 8 | 41 | 27 | 高 | 発注伝票の下書き→発注済み→入荷指示作成→入荷完了→在庫反映、別伝票のキャンセル、完了後キャンセル不可を `#IP-1007/#IP-1008/#II-1026` で実機確認済み。取引先削除/PDF/メール/権限差分は未確認 |
| 16 | 注文・返品 | 7 | 36 | 56 | 高 | 注文/下書き/返品の一覧・絞り込み・直URLエラーを2026-06-27再確認。実注文のステータス遷移・在庫/顧客/ポイント/売上反映は連携待ち |
| 17 | 顧客・会社 | 10 | 57 | 23 | 高 | 顧客/会社一覧、会社作成現行フォーム、会社ロケーション、担当者ダイアログ、B2B TODOを2026-06-27再確認。会社作成はロケーション同時登録ではなく会社本体のみ |
| 18 | CRM | 24 | 99 | 34 | 高 | ディスカウント/注文ポイント/ポイント子メニュー/会員ランクの主要導線を2026-06-27再確認。実注文適用・保存後倍率反映は連携/データ待ち |
| 19 | 店舗業務・リテールポータル | 5 | 35 | 23 | 高 | リテールポータル作成フォーム/ロケーション選択を実機確認済み。接続後挙動は未確認 |
| 20 | 標準販売チャネル連携 | 11 | 70 | 35 | 高 | カタログ/在庫同期関連のフォーム項目を実機確認済み。接続後挙動は未確認 |
| 21 | 物流・返品・外部アプリ連携 | 11 | 68 | 39 | 高 | 出荷管理/Yamato B2/DHL/返品一覧/ロジザード/Recustomerを2026-06-27再確認。CSV実取込・エクスポートON実行・外部接続後挙動は連携待ち |
| 22 | CSV・PDF・データ移行 | 33 | 58 | 7 | 高 | CSVインポート/エクスポート/PDF/Yamato B2の主要導線を2026-06-27再確認。原価の所属グループとインポート完了後disabled状態を修正済み |
| 23 | API・Webhook・開発者連携 | 4 | 19 | 29 | 中 | 2026-06-27再確認済み。アプリ一覧/作成/詳細、空保存エラー、Webhookダイアログ、リクエストログTODOを確認。秘密値は証跡内でマスク済み。発行/作成後の削除・失効導線未確認のため、Storefrontトークン発行とWebhook実作成は未実行 |
| 24 | 会計・売上実績・分析 | 8 | 17 | 26 | 中 | 2026-06-27再確認済み。売上実績一覧空状態、CSVエクスポート注文軸/明細軸の履歴列・成功完了・ダウンロードリンク、作成フォーム空保存エラー、手動作成URL404、分析3画面TODOを確認。注文からの売上生成は連携待ち |

## 2026-06-27 実機確認ログ

### L-001 管理画面ログイン状態

- URL: `https://www.sqstackstaging.com/admin`
- 結果: ログイン済み管理画面を表示できた。
- スナップショット: `_analysis/live-notion-verification-2026-06-27/admin-home-snapshot.md`

### L-002 ロケーション説明の修正

- 対象: `01-SQ全体・共通導線`, `04-基本マスタ`, `12-在庫状態・在庫数`, `13-在庫伝票`, `14-入出荷・在庫依頼`, `19-店舗業務・リテールポータル`, `22-CSV・PDF・データ移行`
- 問題: 「倉庫はリテールポータル対象に出ない」と読める説明が残っていた。
- 正しい整理:
  - 場所種別は `倉庫` / `店舗` の2種のみ。
  - リテールポータル連携では `店舗ロケーション` は店舗種別、`在庫ロケーション` は倉庫種別。
  - 店舗受取のロケーション選択肢は店舗種別。
- 対応: 上記7ファイルを修正済み。`13-在庫伝票` に残っていた旧分類番号参照（`13.入出荷・在庫依頼`）も `14.入出荷・在庫依頼` に修正。

### L-003 ロケーション作成フォーム

- URL: `https://www.sqstackstaging.com/admin/settings/locations/create`
- 結果: ロケーション作成フォームに `名前*`, `コード*`, `場所種別*`, `店舗受け取りを有効にする`, `在庫依頼を受け付ける`, `ポイント利用種別*` が表示されることを確認。
- 場所種別: 既存検証ログで `倉庫` / `店舗` の2択を確認済み。今回のフォーム再確認でも `場所種別*` は独立項目として表示。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/location-create-snapshot-deep.md`
  - `_analysis/live-notion-verification-2026-06-27/location-create-place-type-open.md`

### L-004 リテールポータル連携作成フォーム

- URL: `https://www.sqstackstaging.com/admin/retail_portal_integrations/create`
- 結果: 作成フォームに `店舗ロケーション*`, `在庫ロケーション*`, `テナント*`, `カタログ*`, `販売閾値ルール`, 5つのチェックボックス、`保存する` が表示されることを確認。
- 店舗ロケーション選択: ダイアログタイトルは `ロケーションを選択する`。列は `名前` / `場所コード`。候補には `ユニクロ - 銀座店 R0001`, `GU 銀座店` など店舗系ロケーションが表示。
- 在庫ロケーション選択: 同じダイアログで、候補には `ユニクロ物流倉庫 W0001`, `GU 倉庫` など倉庫系ロケーションが表示。
- 結論: 「倉庫はリテールポータルに出ない」は誤り。倉庫種別は `在庫ロケーション` としてリテールポータル連携に出る。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/retail-portal-create-snapshot.md`
  - `_analysis/live-notion-verification-2026-06-27/retail-portal-store-location-dialog-deep.md`
  - `_analysis/live-notion-verification-2026-06-27/retail-portal-inventory-location-dialog-deep.md`

### L-005 店舗受取ロケーションルール

- URL: `https://www.sqstackstaging.com/admin/local_pickup_retail_location_rules/create`
- 結果: 作成フォームは `ロケーション*` と `保存する` の構成。
- ロケーション選択: 候補には `ユニクロ - 銀座店 R0001`, `GU 銀座店` など店舗系ロケーションが表示。
- 検索確認: 倉庫コード `W0001` を検索すると0件、店舗コード `R0001` を検索すると `ユニクロ - 銀座店 R0001` が1件表示。
- 結論: 店舗受取のロケーション選択肢は店舗種別側に絞られている。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-rule-create-snapshot.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-rule-location-dialog-deep.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-rule-location-dialog-search-W0001.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-rule-location-dialog-search-R0001.md`

### L-006 店舗受取商品（商品側）

- URL: `https://www.sqstackstaging.com/admin/local_pickup_product_variants`
- 結果: h1 `店舗受取`、副題 `店舗受取可能バリエーション一覧`、ボタン `バリエーションを追加する`、列 `バリエーション` / `商品コード` / `SKU`、既存SKU一覧を確認。
- 追加導線: `バリエーションを追加する` から `バリエーションを選択する` ダイアログが開く。ダイアログには `SKUコードで検索する`, `絞り込みを追加`, SKU候補一覧, `キャンセル`, `選択する` が表示。
- 選択挙動: 未選択時の `選択する` はdisabled。SKUを2件チェックした状態でボタンが有効化され、DOM上も複数行が同時にcheckedになることを確認。
- 追加保存: `TEST_E2E_20260622_GU_1905_NAVY_M` を検索して選択し、`選択する` を押すとダイアログが閉じ、一覧20→21件、対象SKUが一覧先頭に即時表示。
- 重複追加: 追加済みの同じSKUは追加ダイアログの検索候補に残るが、再度選択して `選択する` を押しても一覧は21件のまま、対象SKUの出現は1回のみ。
- 削除/解除: 追加済みSKUの行チェック後に一覧右上 `削除する` が表示。確認ダイアログ `商品バリエーションを削除しますか？`、本文 `選択している1件のバリエーションを削除します。この処理は巻き戻すことができません`、ボタン `キャンセル` / `削除する`。削除後は一覧21→20件、対象SKUは消え、選択状態は0件。
- 削除後候補: 削除後に同じSKUを追加ダイアログで検索すると再び候補に表示。
- 直接URL: `/admin/local_pickup_product_variants/create` は404で `このページは存在しないようです` を表示。追加は一覧画面上のダイアログ経由。
- 未確認: 外部チャネル側の店舗受取表示、店舗側ロケーションルールとの接続後の最終業務効果、カタログ指定との優先関係。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-product-variants-list-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-product-variants-add-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-product-variants-add-dialog-two-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-product-variants-create-direct.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-before-add.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-row-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-add-dialog-search-test-sku.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-after-add-test-sku.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-after-duplicate-attempt.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-test-sku-selected-for-delete.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-delete-confirm-test-sku.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-list-after-delete-test-sku.md`
  - `_analysis/live-notion-verification-2026-06-27/local-pickup-07-add-dialog-after-delete-search-test-sku.md`

### L-007 カタログと外部連携フォーム

- カタログ作成 URL: `https://www.sqstackstaging.com/admin/catalogs/create`
- 結果: 作成フォームは `タイトル*` と `保存する` のみ。カタログ単体に出品範囲・同期範囲・店舗受取可否・在庫出力条件を設定する項目は確認できない。
- Shopify URL: `https://www.sqstackstaging.com/admin/shopify_integrations/create`
  - `カタログ*` 必須、`ロケーショングループ*` 必須、`注文による在庫変動を起こさない` などを確認。
- OmnibusCore URL: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/create`
  - `商品同期設定 > カタログ` と `在庫設定 > ロケーショングループ / 在庫予約ルール / 販売上限ルール` を確認。
- スマレジ URL: `https://www.sqstackstaging.com/admin/smaregi_integrations/create`
  - `商品連携設定 > カタログ` と `在庫設定 > 在庫同期の方向` を確認。方向の選択肢は `スマレジからSQへ在庫を同期する`, `SQからスマレジへ在庫を同期する`, `在庫を同期しない`。
- リテールポータル: L-004で `カタログ*` 必須を確認済み。
- 結論: 「外部システムへ在庫数を出すとき、どの商品を対象にするかの一覧としてカタログを使う」は、CSV在庫エクスポートではなく、外部連携フォーム側のカタログ指定として扱うのが実機上妥当。ただし、カタログ内の商品だけが実際に同期されるか、同期頻度、失敗時挙動は接続後の確認待ち。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/catalog-create-snapshot-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/shopify-create-catalog-snapshot.md`
  - `_analysis/live-notion-verification-2026-06-27/omnibus-create-catalog-snapshot-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/smaregi-create-catalog-inventory-snapshot.md`

### L-008 調整伝票のステータス遷移と在庫反映

- 対象: `13-在庫伝票`, `12-在庫状態・在庫数`, 現行FAQ/サポート表
- URL: `/admin/inventory_adjustment_orders/create`
- TESTデータ:
  - 調整伝票: `#IA-1013`
  - ロケーション: `TEST_E2E_20260622_GU倉庫_ON_1905`
  - SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
  - 増減数: `+2`
- 作成フォーム/詳細の理由選択肢: `廃棄`, `紛失`, `在庫差異`, `その他`。旧記述の `見本`, `棚卸差異` は現行実機に表示されない。
- 理由未選択: `選択してください` のまま保存・実行できた。必須とは断定しない。
- 実行前詳細:
  - ステータス: `注意 未完了` / `未実施`
  - 操作: `キャンセル`, `実行`
- 実行確認ダイアログ:
  - タイトル: `在庫調整を実行する`
  - 文言: 明細の差分値が在庫数に反映され、この処理は巻き戻せない
  - 操作: `キャンセル`, `実行する`
- 実行後詳細:
  - ステータス: `完了` / `実施済み`
  - 操作: `キャンセル`のみ表示。`実行`ボタンは消える
  - 明細: 読み取り表示で対象SKUに `+2`
  - 詳細欄: 作成者/作成日に加え、実行者/実行日が表示される
- 在庫一覧変化:
  - 対象ロケーション/SKUの実行前: 販売可能7 / 引当済み0 / 取置中0 / 手持ち7
  - 実行後: 販売可能9 / 引当済み0 / 取置中0 / 手持ち9
- 一覧タブ:
  - `/admin/inventory_adjustment_orders` のタブは `すべて`, `未実施`, `実施済み`, `キャンセル`
  - `#IA-1013` は一覧行で `完了 実施済み`、実施日あり
  - `未実施` / `実施済み` タブの選択状態とURL（`?tab=1`, `?tab=2`）は変わるが、今回のスナップショットではタブ選択だけで行が除外される挙動は確認できなかった。タブ名だけで「移動して消える」とは断定しない。
- 対応:
  - `04-notion/12-在庫状態・在庫数.md`
  - `04-notion/13-在庫伝票.md`
  - 現行FAQ/サポート表の調整理由表記
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-create-initial.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-create-filled-plus2.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-detail-before-execute.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-exec-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-detail-after-execute.md`
  - `_analysis/live-notion-verification-2026-06-27/status-inventory-before-adjustment-target-location.md`
  - `_analysis/live-notion-verification-2026-06-27/status-inventory-after-adjustment-target-location-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-list-after-execute.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-list-executed-tab.md`
  - `_analysis/live-notion-verification-2026-06-27/status-adjustment-list-unexecuted-tab-after-execute.md`

### L-009 取置伝票のステータス遷移と在庫反映

- 対象: `13-在庫伝票`, `12-在庫状態・在庫数`, `01-by-feature/取置伝票`, `02-by-task/取置伝票を作成する`, `_support/statuses`
- URL: `/admin/inventory_reservation_orders/create`
- TESTデータ:
  - 取置伝票: `#IR-1009`
  - ロケーション: `TEST_E2E_20260622_GU倉庫_ON_1905`
  - SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
  - 数量: `1`
- 作成フォーム:
  - `ロケーション`, `メモ`, `商品`, `保存する`
  - 商品参照ダイアログでSKUを選び、数量を1に設定して保存
- 保存後:
  - 保存後の遷移先は詳細ではなく取置伝票一覧
  - 一覧最新行: `#IR-1009`, ロケーション `TEST_E2E_20260622_GU倉庫_ON_1905`, ステータス `情報 未完了 / 未処理`, 作成日 `2026年06月27日 00:45`
  - 対象SKU在庫: 販売可能9→8 / 引当済み0 / 取置中0→1 / 手持ち9のまま
- 詳細（未処理）:
  - 上部には独立ステータス表示が見えず、操作は `処理済みとしてマークする`
  - 詳細商品表には複数明細が表示された。後続確認では複数SKU明細は仕様として再現済みで、詳細の商品明細テーブルは伝票固有表示として扱わない
  - 2026-06-28後続確認: 複数SKU明細は作成フォームで設定できる仕様として再現済み。ただし詳細の商品明細テーブルは複数伝票で同じ34行が表示されたため、伝票固有明細として扱わない
- 処理済み確認ダイアログ:
  - タイトル: `処理済みとしてマークする`
  - 文言: `取置伝票を処理済みにすることで、取置中の在庫が解放されます。`
  - 操作: `キャンセル`, `実行する`
- 処理後:
  - 詳細上部: `完了 / 処理済み`
  - `処理済みとしてマークする` ボタンは消える
  - 一覧行: `完了 / 処理済み`
  - 対象SKU在庫: 販売可能8→9 / 引当済み0 / 取置中1→0 / 手持ち9のまま
- 対応:
  - `04-notion/12-在庫状態・在庫数.md`
  - `04-notion/13-在庫伝票.md`
  - `01-by-feature/取置伝票.md`
  - `02-by-task/取置伝票を作成する.md`
  - `_support/statuses.md`
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-create-initial.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-create-location-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-product-dialog-search-target.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-create-product-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-create-filled-qty1.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-list-after-save.md`
  - `_analysis/live-notion-verification-2026-06-27/status-inventory-after-reservation-save-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-detail-before-process.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-process-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-detail-after-process.md`
  - `_analysis/live-notion-verification-2026-06-27/status-inventory-after-reservation-process-loaded.md`
  - `_analysis/live-notion-verification-2026-06-27/status-reservation-list-after-process.md`

### L-010 在庫依頼から移動・出荷・入荷までのステータス遷移と在庫反映

- 対象: `14-入出荷・在庫依頼`, `12-在庫状態・在庫数`, `13-在庫伝票`, `01-by-feature/在庫依頼`, `01-by-feature/移動伝票`, `02-by-task/取り寄せ販売の処理手順`
- URL: `/admin/inventory_allocation_requests/create`
- TESTデータ:
  - 在庫依頼: `46fd468a-2570-5dc2-9f0d-a96471824d1e_InventoryAllocationRequest`
  - 移動伝票: `#IM-1025`
  - 出荷指示: `#IO-1025`
  - 入荷指示: `#II-1025`
  - SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
  - 移動元: `TEST_E2E_20260622_GU倉庫_ON_1905`
  - 移動先: `TEST_E2E_20260622_GU店舗_OFF_1905`
  - 数量: `1`
- 在庫依頼作成直後:
  - 詳細上部: `情報 / 確認待ち`
  - 操作: `その他の操作`, `在庫を引当てる`
  - 確保済み数量: `0 / 1 点`
  - 残り確保数: `1 点`
  - チャネル: `web-admin`
  - 在庫変化なし。移動元は販売可能9 / 引当済み0 / 取置中0 / 手持ち9、移動先は販売可能1 / 引当済み0 / 取置中0 / 手持ち1。
- 引当後:
  - 詳細上部: `成功 / 確保済み`
  - 確保済み数量: `1 / 1 点`
  - 残り確保数: `0 点`
  - `在庫を引当てる` ボタンは消える
  - 確保済み一覧 `/admin/inventory_allocation_request_confirmations` に対象行が表示される
  - 在庫変化なし。移動元9/0/0/9、移動先1/0/0/1のまま。
- 移動伝票作成:
  - 確保済み一覧には既存の別行も残っていたため、`ロケーション: TEST_E2E_20260622_GU倉庫_ON_1905` で絞り込んで対象1行だけにしてから実行。
  - `移動伝票を作成する` ダイアログは `移動元` の選択が必要。未選択では `実行する` がdisabled。
  - 実行後トースト: `移動伝票を一括作成しました`
  - 確保済み一覧の対象行は消える
  - 在庫依頼詳細の確保済み在庫行に `#IM-1025` リンクが追加される
  - `#IM-1025` 詳細上部: `情報 未完了 / 出荷待ち`
  - `#IM-1025` には `外部システムから連携されている移動伝票です` の警告が表示され、関連として `#IO-1025` / `#II-1025` が生成される
  - 在庫変化: 移動元は販売可能9→8、取置中0→1、手持ち9のまま。移動先一覧には `情報 入荷予定` バッジが表示され、主要4列は販売可能1 / 引当済み0 / 取置中0 / 手持ち1のまま。
- 出荷実績登録:
  - `#IO-1025` 実行前: `情報 未完了 / 出荷待ち`、引当ステータス `情報 未完了 / 引当待ち`、出荷予定1 / 出荷済み0
  - ダイアログ項目: `配送キャリア`, `追跡コード`, `キャンセル`, `登録する`
  - 空欄のまま登録できた
  - 登録後: `成功 完了 / 出荷完了`、出荷予定1 / 出荷済み1、`出荷実績を登録する` ボタンはdisabled
  - 引当ステータスは登録後も `情報 未完了 / 引当待ち` のまま
  - 出荷完了タブ `?tab=complete` に `#IO-1025` が表示される
  - 在庫変化: 移動元は販売可能8 / 引当済み0 / 取置中1→0 / 手持ち9→8。移動先一覧は `情報 積送中` バッジになり、主要4列は1/0/0/1のまま。
- 入荷完了:
  - `#II-1025` 実行前: `入荷待ち`、入荷予定1 / 入荷済み0
  - `入荷指示を一括受領で完了する` は `/complete` へのリンク
  - 確認画面文言: `未受領分をすべて受け取って入荷実績を完了します。この処理は巻き戻すことができません。`
  - 完了後: `#II-1025` は `成功 完了 / 入荷完了`、入荷予定1 / 入荷済み1
  - 入荷完了タブ `?tab=5` に `#II-1025` が表示される
  - 親 `#IM-1025` も `成功 完了 / 入荷完了` になる
  - 在庫変化: 移動先は販売可能1→2、手持ち1→2、引当済み0・取置中0のまま。移動元は販売可能8 / 引当済み0 / 取置中0 / 手持ち8のまま。
- 追加観測:
  - 移動先一覧で `情報 積送中` 表示中の対象行をクリックすると、`/admin/inventory_items/137c461d-..._InventoryItem?location_id=4f100847-..._Location` が `アイテムが見つかりませんでした` になった。積送中の9区分詳細は今回の画面からは直接確認できていないため、一覧バッジと出荷/入荷指示を根拠に扱う。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-create-filled-qty1.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-after-save-attempt.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-detail-after-allocate.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-confirmation-filtered-before-movement.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-movement-dialog-ready.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-detail-after-movement-create.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-movement-detail-after-create.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-outbound-detail-before-shipment.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-outbound-shipment-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-outbound-detail-after-shipment.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inbound-detail-before-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inbound-complete-confirm.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inbound-detail-after-complete.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-movement-detail-after-complete.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-source-before.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-dest-before.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-source-after-allocate.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-dest-after-allocate.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-source-after-movement-create.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-dest-after-movement-create.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-source-after-shipment.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-dest-after-shipment.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-source-final.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inventory-dest-final.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-outbound-complete-tab.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-flow-inbound-complete-tab.md`

### L-011 発注・仕入の発注済み後入荷指示作成、入荷完了、キャンセル

- 対象: `15-発注・仕入`, `01-by-feature/発注管理`, `_support/statuses`, `_support/symptoms`
- URL:
  - `/admin/inventory_purchase_orders`
  - `/admin/inventory_purchase_orders/create`
  - `/admin/inventory_purchase_orders/<id>/create_inventory_inbound_order`
  - `/admin/inventory_inbound_orders`
  - `/admin/inventory_items/137c461d-51a3-545e-8c58-2402bae9fef7_InventoryItem`
- TESTデータ:
  - 発注伝票: `#IP-1007`, `#IP-1008`
  - 発注起点入荷指示: `#II-1026`
  - 取引先: `TEST_E2E_20260622_取引先_1905`
  - テナント: `ユニクロ`
  - SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
  - 入荷先: `TEST_E2E_20260622_GU倉庫_ON_1905`
  - 数量: `1`
- 空保存バリデーション:
  - 発注伝票作成フォーム: `取引先を選択してください`, `テナントを選択してください`, `商品を1つ以上追加してください`
  - 発注起点入荷指示フォーム: `入荷先のロケーションを選択してください`
- 発注伝票作成:
  - `#IP-1007` / `#IP-1008` は下書き保存できた
  - 下書き詳細: `注意 / 下書き`
  - 商品選択時の初期値: 単価1990、数量0、税率10
  - 単価100・数量1・税率10に変更した場合、作成フォーム入力中の明細金額は `￥100`
- 発注済み:
  - 発注確認ダイアログ文言: `発注後は伝票を編集できません。発注後に入荷指示を作成できます。`
  - 実行後は同じ発注伝票詳細URLに戻る
  - 詳細上部: `情報 / 発注済み`
  - 商品見出し: `発注済み商品`
  - 明細/一覧金額: `￥110`
  - 主要導線: `入荷指示を作成する`
  - 発注実行だけでは入荷管理一覧に新規行は増えず、対象SKUの入荷予定も増えない
- 発注起点の入荷指示作成:
  - `#IP-1007` の `入荷指示を作成する` は `/create_inventory_inbound_order` へ遷移
  - フォームは発注明細のSKU・数量1を引き継ぎ、入荷先ロケーションだけ未選択
  - 入荷先候補には店舗/倉庫が表示され、`TEST_E2E_20260622_GU倉庫_ON_1905` を選択して保存
  - 保存後は発注伝票詳細へ戻る
  - 入荷管理一覧に `#II-1026`, 到着ロケーション `TEST_E2E_20260622_GU倉庫_ON_1905`, 種別 `発注`, 作業ステータス `情報 入荷待ち` が表示
  - 入荷待ちタブの新規件数は0→1
  - 入荷指示詳細では種別欄が `仕入れ` と表示される
  - 対象SKU在庫: 発注前/発注後は販売可能8 / 手持ち8 / 入荷予定0。`#II-1026` 作成後は販売可能8 / 手持ち8 / 入荷予定+1
- 入荷実績登録:
  - `#II-1026` 詳細上部: `情報 / 入荷待ち`
  - 入荷明細: 入荷予定1 / 入荷済み0
  - `入荷実績を登録する` フォームは入荷予定1 / 入荷済み0 / 今回受領0で表示
  - 今回受領1で登録
  - 登録後: `#II-1026` は `成功 完了 / 入荷完了`
  - 入荷待ち新規件数は1→0
  - 入荷完了タブ `?tab=complete` に `#II-1026` が表示
  - 入荷履歴に `2026年06月27日 01:29` が表示
  - 対象SKU在庫: `TEST_E2E_20260622_GU倉庫_ON_1905` が販売可能8→9、手持ち8→9、入荷予定+1→0
  - 発注伝票 `#IP-1007` は入荷完了後も `情報 / 発注済み` のまま。発注伝票詳細に `#II-1026` の関連リンクは表示されない
- キャンセル:
  - 入荷指示未作成の `#IP-1008` では、発注済み詳細の `その他の操作 > キャンセルする` が有効
  - キャンセル確認ダイアログ文言: `発注伝票をキャンセルします。この処理は巻き戻すことができません。`
  - 実行後: `#IP-1008` は `キャンセル済み`、キャンセル者/キャンセル日時が表示
  - `キャンセルする` はdisabledになり、`入荷指示を作成する` もリンクではなく無効表示になる
  - キャンセル後も対象SKU在庫は販売可能9 / 手持ち9 / 入荷予定0のまま
  - 入荷管理一覧に `#IP-1008` 起点の入荷指示は増えない
  - 入荷完了済みの `#IP-1007` では `キャンセルする` がdisabled
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-create-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-create-filled.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-detail-draft.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-order-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-detail-ordered.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-list-after-order.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inventory-after-order-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-create-inbound-form-initial.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-create-inbound-empty-error.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-create-inbound-location-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-list-after-manual-create.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inventory-after-inbound-create-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-detail-before-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-receive-form.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-detail-after-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-complete-tab-after-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inventory-after-receive-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-detail-after-inbound-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-detail-actions-after-inbound-receive.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-cancel-path-detail-draft.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-cancel-path-detail-ordered.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-cancel-path-cancel-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-cancel-path-detail-cancelled.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-list-after-cancel-tests.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inventory-after-cancel-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-inbound-list-after-cancel-path.md`
  - `_analysis/live-notion-verification-2026-06-27/purchase-15-invalid-inventory-suppliers-404-recheck.md`

### L-012 価格・販売制御（販売価格・販売上限）

- 対象: `11-価格・販売制御`, `01-by-feature/販売設定`, `02-by-task/販売価格を設定する`, `02-by-task/販売上限を設定する`, サポート制約/エラー表
- 販売価格 URL: `/admin/product_price_rules`
- TESTデータ:
  - 販売価格ルール: `TEST_NOTION_20260627_PRICE_RULE_0156`
  - SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
  - 通常価格: 税抜1000 / 税込1100
- 販売価格ルール作成フォーム:
  - `ルール名*`, `通貨*`, `保存する`
  - 通貨は `select` で、選択肢は `米ドル`, `ユーロ`, `日本円`, `タイ バーツ`, `シンガポール ドル`
  - 初期値は `JPY` / 日本円
- 作成後の遷移:
  - `保存する` 後、旧記述の詳細トップ/カード画面ではなく、作成したルールの通常価格一覧 `/product_variant_regulars` へ遷移
  - 画面上部に `販売価格ルール`, `通貨: 日本円`, ルール名, `ルールを編集する`
  - 下部は `通常価格` / `セール価格` タブ構成。通常価格タブが選択状態
- 通貨変更不可:
  - `ルールを編集する` モーダルでルール名は編集可能
  - 通貨欄は `JPY` のdisabled入力で、`通貨は編集できません` と表示
- 通常価格登録:
  - 通常価格タブの `登録する` はページ遷移ではなく `通常価格を登録する` モーダルを開く
  - モーダル項目は `商品バリエーション`, `価格`, `価格(税込)`
  - `商品バリエーション` の `選択` から `バリエーションを選択する` ダイアログが開く
  - ダイアログ検索 `TEST_E2E_20260622_GU_1905_NAVY_M` で候補1件に絞り込み
  - 保存後は同じ通常価格一覧に戻り、列 `バリエーション`, `SKU`, `税抜価格`, `税込価格` で `￥1,000`, `￥1,100` が表示
- 通常価格削除:
  - 通常価格一覧のSKU行リンクから詳細 `/product_variant_regulars/{ProductVariant}` へ遷移
  - 詳細には価格/価格(税込)入力、`削除する`, `保存する`
  - 削除確認: `通常価格を削除する`
  - 本文: `この通常価格を削除します。この処理は巻き戻すことができません。`
  - 確定後は通常価格一覧へ戻り、トースト `通常価格を削除しました`
  - 削除直後の一覧には対象SKU行が残ったが、一覧再読み込み後に消えた
- 販売価格ルール本体削除:
  - 販売価格ルール一覧でTEST行のみ選択すると `1を選択済み` と `削除する` が表示
  - 削除確認: `販売価格ルールを削除しますか？`
  - 本文: `選択されている1件の販売価格ルールを削除しますか？ この処理は巻き戻すことができません。`
  - 確定後は一覧からTEST行が消え、トースト `販売価格ルールを削除しました`
- 販売上限:
  - URL: `/admin/inventory_sale_limit_rules/create`
  - フォームは `販売上限ルール名`, `チャネル`, `保存する`
  - DOM入力欄は販売上限ルール名のみ。チャネル選択肢は未接続のため表示なし
  - 空保存で同じURLに留まり、`販売上限ルール名を入力してください` と `チャネルを選択してください` が表示
- 未確認/連携待ち:
  - セール価格の現行モーダル挙動、終了日時空欄の扱い
  - 予約販売/販売閾値の2026-06-27再検証
  - 販売価格/予約販売/販売上限/販売閾値の外部チャネル適用後の実挙動
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-list.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-after-create-regular-list.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-edit-modal.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-register-open.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-sku-dialog-open.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-sku-dialog-search-test-sku.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-filled-before-save.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-after-save-list.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-delete-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-after-delete-immediate.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-regular-price-after-delete-reload.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-list-with-test-rule.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-rule-selected-for-delete.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-rule-delete-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-product-price-rule-after-delete.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-sale-limit-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/price-11-sale-limit-empty-save-errors.md`

### L-013 14.入出荷・在庫依頼 完了後導線の再確認

- 対象: `14-入出荷・在庫依頼`, `01-by-feature/移動伝票`, `01-by-feature/出荷管理`, `01-by-feature/入荷管理`, `_support/statuses.md`, `_support/constraints.md`
- 再確認対象:
  - 親移動伝票: `#IM-1025`
  - 出荷指示: `#IO-1025`
  - 入荷指示: `#II-1025`
- 親移動伝票 `#IM-1025`:
  - URL: `/admin/inventory_movement_orders/d7573bf2-aba0-574f-ac27-774061ea17d9_InventoryMovementOrder`
  - 現行表示: `成功 完了 / 入荷完了`
  - `外部システムから連携されている移動伝票です` の警告を表示
  - 関連リンクとして `#IO-1025` / `#II-1025` を表示
  - `その他の操作` メニュー内に `キャンセル` は残るが disabled
- 出荷指示 `#IO-1025`:
  - 出荷完了タブ `?tab=complete` に表示
  - 詳細は `成功 完了 / 出荷完了` と `情報 未完了 / 引当待ち`
  - 出荷予定1 / 出荷済み1
  - `出荷実績を登録する` は表示されるが `aria-disabled=true` と disabled クラスで再実行不可
  - 作成元リンクは `#IM-1025`
- 入荷指示 `#II-1025`:
  - 入荷完了タブ `?tab=5` に表示
  - 詳細は `成功 完了 / 入荷完了`
  - 入荷予定1 / 入荷済み1
  - `入荷指示を一括受領で完了する` と `入荷実績を登録する` は `href` なしの disabled リンクで再実行不可
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/allocation-14-current-movement-1025-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-14-current-outbound-complete-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-14-current-outbound-1025-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-14-current-inbound-complete-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/allocation-14-current-inbound-1025-detail-link-click-recheck.md`

### L-014 22.CSV・PDF・データ移行 主要導線の再確認

- 対象: `22-CSV・PDF・データ移行`, `01-by-feature/CSVインポート`, `01-by-feature/CSVエクスポート・PDFエクスポート`, CSV/PDF関連FAQ/作業別/サポート表
- CSVインポートトップ `/admin/csv_import`:
  - 9グループ・22カテゴリを再確認。
  - 現行UIでは `原価` は「価格」ではなく「商品」グループに表示。
  - `商品` グループは `商品 / 商品画像 / 商品バリエーション / 商品バリエーション画像 / カタログ / 原価`。
  - `価格` グループは `販売価格 (通常) / 販売価格 (セール)`。
- CSVインポート作成フォーム:
  - `原価` はファイルのみ。空保存で `ファイルを選択してください`。
  - `販売可能在庫` は `絶対値で反映する` / `差分値で反映する` とファイルアップロード。
  - `販売価格 (通常)` は `販売価格ルール` とファイルアップロード。
  - `キャンペーン対象商品` は `ポイントキャンペーン` の検索型選択とファイルアップロード。
- ポイント一括加算/減算:
  - 一括加算フォームは `テナント` と `顧客IDの種別` を表示。空保存で `テナントを選択してください` と `顧客IDの種別を選択してください`。
  - 一括減算フォームは `テナント` とファイルのみ。空保存で `テナントを選択してください`、テナント選択後の保存で `ファイルを選択してください`。
- CSVインポート履歴:
  - 販売可能在庫インポート一覧に既存履歴があり、行は `成功 完了`。
  - 実行済み詳細では `検証ステータス: 成功 完了`, `実行ステータス: 成功 完了`, `検証成功: 1個の商品`, `検証失敗: 0個の商品`。
  - 完了後も `実行する` ボタンは残るがdisabledで再実行不可。
  - `0個の商品` の検証失敗リンクでも見出し `検証失敗` の画面へ遷移。
- CSVエクスポートトップ `/admin/csv_export`:
  - 5グループ・9カテゴリを再確認。
  - トップには `エクスポート` ボタンはなく、カテゴリ行リンクで遷移。
- CSVエクスポート作成/履歴:
  - 在庫CSVエクスポート作成フォームは `ロケーション` 指定のみ。`カタログ` 指定なし。
  - ロケーション選択ダイアログは `すべて / 店舗 / 倉庫` タブ。
  - 売上実績（注文軸）一覧には `成功 完了` と `ダウンロード` リンクが表示。
- PDF/Yamato B2:
  - PDFエクスポートトップは `PDFエクスポート`、出荷>納品書行を表示。
  - `/admin/pdf_export/pdf_export_operation_packing_slips/create` は `このページは存在しないようです`。
  - ヤマトB2条件指定エクスポートは `/admin/inventory_outbound_orders/export/yamato_b2_cloud`。
  - 出力物として `ヤマトB2クラウド取り込み用CSV` と `同梱する納品書PDF` を表示。
  - `CSVの出力後に出荷指示のステータスを出荷作業中に変更する` はデフォルトOFF。
- スナップショット/構造ログ:
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-top-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-top-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-unit-costs-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-unit-costs-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-inventory-available-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-regular-price-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-plus-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-plus-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-minus-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-minus-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-minus-tenant-selected-file-error-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-inventory-available-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-inventory-available-detail-complete-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-inventory-available-detail-complete-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-inventory-available-validation-failure-empty-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-campaign-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-import-point-campaign-create-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-top-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-top-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-inventory-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-inventory-location-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-sale-changes-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-export-sale-changes-list-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-pdf-export-top-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-pdf-export-top-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/csv22-pdf-export-create-404-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-yamato-b2-export-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/csv22-yamato-b2-export-form-structure-recheck.json`

### L-015 18.CRM 主要導線の再確認

- 対象: `18-CRM`, `01-by-feature/ディスカウント`, `01-by-feature/ポイント`, `01-by-feature/会員ランク`, CRM関連作業別、サポート表
- ディスカウント `/admin/order_price_adjustment_rules`:
  - 一覧タブは `すべて / 有効 / スケジュール済み / 期限切れ`。列はタイトル、クーポンコード、ステータス、有効期間、対象顧客、対象店舗、利用回数、テナント。
  - 作成フォームの空保存で `タイトルを入力してください`, `クーポンコードを入力してください`, `テナントを選択してください`, `割引率を入力してください`, 開始/終了日時の未入力エラーを確認。
  - 必須項目を埋めた新規保存試行では一覧に新規TEST行が出ず、作成成功遷移は未確認。
  - 既存詳細は `成功` と `有効` バッジ、`基本情報 / 利用履歴 / 顧客管理 / 店舗管理 / 商品管理` タブを表示。
  - 顧客管理は `追加する` でメニューが開く。`顧客を選択して追加` は有効、`顧客セグメントを選択して追加` はdisabled。顧客0件でも `顧客を選択する` ダイアログは開くが `選択する` はdisabled。
  - 店舗管理は `ロケーションを追加する` / `ロケーショングループを追加する`。ロケーション追加フォームの適用種別は `値引き` が選択可能、`金種` はdisabled。
  - 商品管理は `バリエーションを選択する` ダイアログが開き、SKUコード検索と商品バリエーション行を表示。
- 注文ポイント `/admin/point_calculation_rules`:
  - 一覧h1は `注文ポイント`。2026-06-27再確認ではタブ表示なし。列は `ルール / 利用テナント数`。
  - 作成フォームは `基本設定`, `付与対象`, `ポイントのライフサイクル`, `会員ランク算出ルール`, `ポイントキャンペーン優先ルール` の構成。
  - 現行ラベルは `付与までの日数（オンライン）`, `付与までの日数（店舗）`, `利用可能になってから有効な日数`。旧ラベル `オンライン注文のポイント有効までの日数` 等は現行UIでは使わない。
  - 既存 `TEST_FAQ_注文ポイント付与ルール` 詳細は表示可能。2026-06-19のクライアントエラーは再現せず。
  - 会員ランク倍率のURLは `/rank_multipliers`。`追加する` で `会員ランク倍率を追加する` ダイアログが開き、`会員ランク*`, `倍率*` を表示。
  - 商品倍率のURLは `/point_multiplier_products`。`追加する` で `商品倍率を追加する` ダイアログが開き、`商品`, `倍率*` を表示。推測URL `/product_multipliers` は404。
  - 倍率行の保存、保存後の一覧移動、実注文への計算反映は未確認。
- ポイントキャンペーン:
  - 一覧列は `タイトル / 種別 / 注文ポイント付与ルール / 開始日時 / 終了日時 / 作成日時`。
  - 作成フォームは種別選択前は基本情報中心。種別 `なし` 選択後に付与方法、ポイント入力、対象注文ポイント付与ルール、適用条件が表示される。
  - 種別 `なし` の空保存でタイトル、開始日時、終了日時、ポイント、対象注文ポイント付与ルールの未入力エラーを確認。
  - 種別 `会員ランク` の既存詳細から `会員ランクを追加する` を押すと `/customer_ranks/create` に遷移し、`会員ランク算出ルール*`, `会員ランク*`, `ポイント倍率*` を表示。
- 誕生日/利用外商品/失効通知:
  - 誕生日ポイント作成フォームは `タイトル`, `表示タイトル`, `ポイント`, `有効期間`。
  - 利用外商品は `商品を選択する*` から商品選択ダイアログを開く。列は `商品 / 商品コード` で、SKU/バリエーション単位ではない。
  - 失効通知作成フォームは `タイトル`, `通知予定日`。
- 会員ランク:
  - 一覧タブは `すべて` のみ。
  - 作成フォームの期間は `1年間`, `直近365日`, `無期限`。開始月デフォルトは `1月`。
  - `直近365日` を選ぶと `開始月`, `会員ランクを月初に算出する`, `会員ランクを次の算出期間に持ち越す` が非表示。
  - 既存詳細のBronzeは `0円の獲得で達成` と表示。Bronze編集では購入金額入力と削除ボタンがdisabled。
  - `除外商品を管理する` は `/exclude_products` へ遷移し、一覧列は `商品 / 商品コード`。
- ステータス/移動確認:
  - ディスカウント既存詳細のステータス表示は確認したが、今回の新規作成保存が成立しなかったため `有効` / `スケジュール済み` / `期限切れ` の一覧タブ移動は未確認。
  - 注文ポイント倍率・ポイントキャンペーン条件・会員ランク反映は、実注文/実顧客または保存後データが必要なため、ステータス移動と実計算は未確認。
- 主なスナップショット:
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-detail-basic-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-customers-select-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-locations-add-location-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-discount-product-add-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-rule-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-rule-detail-basic-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-rule-rank-multiplier-add-click-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-rule-product-multiplier-add-click-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-campaign-create-type-none-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-point-campaign-rank-add-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-customer-rank-create-period-365-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/crm18-customer-rank-bronze-edit-recheck.md`

### L-016 21.物流・返品・外部アプリ連携の再確認

- 対象: `21-物流・返品・外部アプリ連携`, `01-by-feature/出荷管理`, `02-by-task/ヤマトB2クラウドで出荷業務を行う`, サポート表
- 出荷管理 `/admin/inventory_outbound_orders`:
  - タブは `すべて / 保留中 / 出荷待ち / 依頼済み / 作業中 / 欠品・要対応 / 出荷完了`。
  - ステータス別URLは `on_hold / waiting / requested / in_progress / rejected / complete`。`出荷完了` は `?tab=complete`。
  - 2026-06-27再確認では、キャンセル済み行 `#IO-1015`, `#IO-1014`, `#IO-1007` は「すべて」タブに `キャンセル済み` として表示され、ステータス別タブには表示されなかった。
- ヤマトB2クラウド出荷実績インポート:
  - `/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds` は h1 `ヤマトB2クラウドの出荷実績をCSVでインポートする`。
  - 一覧に `テンプレート` と `新規インポート` が表示。空一覧は `アイテムが見つかりませんでした`。
  - `/create` は `CSVファイル` アップロードと `保存する`。空保存で `ファイルを選択してください`。
- DHL出荷実績インポート:
  - `/admin/csv_import/csv_import_operation_fulfillment_by_dhls` は h1 `DHLの出荷実績をCSVでインポートする`。
  - 一覧に `新規インポート` が表示。2026-06-27再確認では `テンプレート` リンクは表示なし。
  - `/create` は `CSVファイル` アップロードと `保存する`。空保存で `ファイルを選択してください`。
- ヤマトB2クラウド条件指定エクスポート:
  - `/admin/inventory_outbound_orders/export/yamato_b2_cloud` は h1 `条件指定でヤマトB2クラウドのCSVをエクスポートする`。
  - 出力物として `ヤマトB2クラウド取り込み用CSV` と `同梱する納品書PDF` を表示。
  - 項目は `開始日時`, `終了日時`, `配送先 (国)`, `決済方法`, `出荷作業ステータス`, `注文タグ（含む）`, `注文タグ（除外）`, `CSVの出力後に出荷指示のステータスを出荷作業中に変更する`。
  - 出荷作業ステータス選択肢は `指定しない / 出荷待ち / 保留中 / 依頼済み / 作業中 / 欠品・要対応 / キャンセル済み / 出荷完了`。
  - ステータス変更チェックはデフォルトOFF。2026-06-27再確認ではON実行はせず、実際の一覧移動は未確認。
- 返品:
  - `/admin/order_returns` は h1 `返品` の一覧画面として存在。空一覧と検索絞り込みを表示。
  - `/admin/order_returns/create` は `このページは存在しないようです`。
- ロジザード:
  - `/admin/logizard_integrations` は h1 `ロジザード連携`、一覧0件、`追加する`。
  - `/admin/logizard_integrations/create` は `設定名`, 接続情報, 認証情報, 入荷設定, 出荷設定, 出荷箱明細実績エクスポート設定, 商品マッピング設定を表示。
  - `商品バリエーションを特定するキー` は `SKUコード / JANコード / EANコード / UPCコード`、デフォルトはSKUコード。
  - 空保存で設定名、3桁のグループ番号/接続番号、認証情報、入荷/出荷/出荷箱明細のファイルID・パターンIDの未入力エラーを表示。
- Recustomer:
  - `/admin/recustomer_integrations` は h1 `Recustomer`、一覧0件、`アカウントを接続`。
  - `/admin/recustomer_integrations/create` は `ストアID*`, `シークレット*`, `保存する`。
  - 空保存で `ストアIDを入力してください`, `シークレットを入力してください`。
- ステータス・影響確認:
  - 今回はCSV実取込、エクスポート実行、外部接続作成は行っていないため、出荷指示の実ステータス移動・メールリンク・外部同期・返品反映は未確認。
  - ステータスを動かす検証を行う場合は、実行前後で対象行がどのタブへ移動するか、詳細ステータス、実行可能ボタン、関連履歴、在庫区分の変化を確認する。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/ext21-outbound-list-loaded-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-outbound-tabs-current-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-yamato-import-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-yamato-import-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-yamato-import-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-dhl-import-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-dhl-import-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-dhl-import-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-yamato-export-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-order-returns-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-order-returns-create-404-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-logizard-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-logizard-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-logizard-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-recustomer-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-recustomer-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/ext21-recustomer-empty-save-recheck.md`

### L-017 ロケーション種別と用途の再確認

- 対象: `04-基本マスタ`, `01-SQ全体・共通導線`, `19-店舗業務・リテールポータル`, `01-by-feature/設定`
- `/admin/settings/locations/create`:
  - h1 は `ロケーションを作成`。
  - `場所種別` は `倉庫 / 店舗` の2種。
  - フォームには `店舗受け取りを有効にする`, `在庫依頼を受け付ける`, `ポイント利用種別` が表示。
- `/admin/retail_portal_integrations/create`:
  - `店舗ロケーション` と `在庫ロケーション` の2つのロケーション選択を表示。
  - `店舗ロケーション` ダイアログは店舗種別のみ。例: `ユニクロ - 銀座店 / R0001`, `TEST_E2E_20260622_GU店舗_OFF_1905`。
  - `在庫ロケーション` ダイアログは倉庫種別のみ。例: `ユニクロ物流倉庫 / W0001`, `TEST_E2E_20260622_GU倉庫_ON_1905`。
- `/admin/local_pickup_retail_location_rules/create`:
  - h1 は `店舗受取を作成する`。
  - `ロケーション` ダイアログは店舗種別のみ。倉庫例 `W0001` や `TEST_E2E_20260622_WH_1905` は表示されなかった。
- 判断:
  - ロケーション種別2択と、リテールポータル/店舗受取での種別別候補表示は確定扱い。
  - `店舗受け取りを有効にする` のON/OFFが候補表示やストアフロントでの受取可否にどう影響するかは接続環境で未確認。
  - 手動の在庫依頼・移動伝票では倉庫/店舗の両方が移動元・移動先に関与するため、`倉庫=出荷元だけ`, `店舗=受け口だけ` のような全機能共通の断定はしない。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/location-role-dialog-recheck.md`

### L-018 16.注文・返品 / 17.顧客・会社の再確認

- 対象: `16-注文・返品`, `17-顧客・会社`, `01-by-feature/注文管理`, `01-by-feature/顧客管理`, `01-by-feature/会社`, `02-by-task/会社（法人顧客）を登録する`
- 注文管理 `/admin/orders`:
  - h1 `注文管理`、タブ `すべて`、空状態 `アイテムが見つかりませんでした` / `絞り込みや検索ワードを変更してみてください`。
  - `検索と絞り込みの結果` 展開後に `注文番号で検索する`, `キャンセル`, `名前を付けて保存`, `絞り込みを追加`。
  - 絞り込みは `テナント`, `タグ付けされている`, `タグ付けされていません`, `チャネル`。
  - `/admin/orders/create` は `予期せぬエラーが発生しました`。
- 下書き `/admin/draft_orders`:
  - h1 `下書き`、タブ `すべて`、空状態 `注文が見つかりませんでした`。
  - `注文を作成する` は表示されるが `href` なし。
  - 展開後は `注文番号で検索する`, `キャンセル` のみで、`絞り込みを追加` と `名前を付けて保存` はなし。
  - `/admin/draft_orders/create` は `予期せぬエラーが発生しました`。
- 返品 `/admin/order_returns`:
  - h1 `返品`、タブなし、空状態 `アイテムが見つかりませんでした`。
  - 絞り込みは `キャンセル`, `交換出荷`。注文番号検索はなし。
  - `/admin/order_returns/create` は `このページは存在しないようです`。
- 顧客管理 `/admin/purchasing_customers`:
  - h1 `顧客管理`、タブ `すべて`、空状態 `アイテムが見つかりませんでした`。
  - `インポート` メニューは `ポイント一括付与` のみ。
  - 絞り込みは `テナント`, `メタフィールド`, `会員証バーコード`。
  - `/admin/purchasing_customers/create` は `予期せぬエラーが発生しました`。
- 会社 `/admin/companies`:
  - h1 `会社`、タブ `すべて`、列 `会社 / ロケーション / 総注文数 / 販売合計 / 作成日`。
  - `インポート` はクリックしても反応なし。
  - `/admin/companies/create` の現行フォームは `会社名`, `会社ID`, `コード` のみ。ロケーション/住所/担当者は表示されない。
  - 空保存で `会社名を入力してください`, `会社コードを入力してください`。
  - 既存会社詳細から `直近の注文`, `ロケーション`, `担当者`, 右サイドバーの会社ID/メモを確認。
- 会社ロケーション:
  - `/admin/companies/{id}/locations/create` は `ロケーション名`, `ロケーションID`, `コード`, 配送先住所, 請求先住所。
  - 空保存でロケーション名、国、姓/名、郵便番号、都道府県、市区町村、住所の未入力エラーを確認。
  - ロケーション詳細では `このロケーションからはまだ注文がありません`、ロケーションID/コード/配送先住所/請求先住所/メモを表示。
- 担当者:
  - 会社詳細の `担当者を追加` で `担当者を作成する` モーダルが開く。
  - 項目は `姓`, `名`, `メールアドレス`, `電話番号`。
  - 空保存で `姓を入力してください`, `名を入力してください`, `メールアドレスを入力してください`。
  - `/admin/companies/{id}/contacts/create` 直URLは `予期せぬエラーが発生しました`。
- 卸売 `/admin/b2b`: h1 `卸売`、本文 `TODO`。
- ステータス・移動確認:
  - 注文/返品/顧客はデータ0件のため、詳細ステータス変更、一覧上の移動先、在庫/顧客/ポイント/売上への反映は未確認。
  - 会社/会社ロケーション/担当者はステータス別タブがなく、今回の確認はフォーム構成・空保存・詳細表示まで。注文履歴/売上表示は注文データ0件のため未確認。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/orders16-customers17-recheck.md`

### L-019 02.アカウント・権限の再確認

- 対象: `02-アカウント・権限`, `01-by-feature/設定`, `02-by-task/管理メンバーを追加する`, `02-by-task/権限グループを作成する`, `03-faq/設定と権限のよくある質問`, サポート表
- 管理メンバー一覧 `/admin/settings/users`:
  - h1 `管理メンバー`。
  - 右上ボタンは `権限グループ一覧`, `インポート`, `追加する`。
  - `権限グループ一覧` は `/admin/settings/permission_groups`、`インポート` は `/admin/csv_import/csv_import_operation_users`、`追加する` は `/admin/settings/users/create` へ遷移。
  - キーワード検索欄は `キーワードで検索する`。`絞り込みを追加` の条件は `メールアドレス` のみ。
  - 一覧列は `名前`, `メールアドレス`, `権限グループ`。
- ユーザー追加 `/admin/settings/users/create`:
  - h1 `ユーザーを追加する`。
  - 項目は `姓*`, `名*`, `メールアドレス*`, `権限グループ`。
  - 権限グループは作成済みグループのラジオボタン単一選択。2026-06-27時点の選択肢は `特権管理者`, `TEST_権限検証_20260620`。
  - 空保存で `姓を入力してください`, `名を入力してください`, `メールアドレスを入力してください`。権限グループ未選択だけの保存可否は未確認。
  - 実ユーザー作成保存は行っていない。
- 既存メンバー詳細 `/admin/settings/users/{id}`:
  - `基本情報`, `ユーザーテナント`, `権限` の3セクションと、それぞれの `保存する` を確認。
  - `ユーザーテナント` はチェックボックス一覧。
  - `権限` は `権限グループ` コンボボックス。`適用されている権限一覧: 76件` アコーディオンで全76件を表示。
  - 詳細下部に `ユーザーを組織から除外` セクションと `組織から除外する` ボタンを確認。2026-06-27時点では `その他の操作` メニュー内ではない。
  - 実ユーザー除外は影響が大きいため実行せず、確認ダイアログ・除外後のログイン/再追加可否は未確認。
- 権限グループ一覧 `/admin/settings/permission_groups`:
  - h1 `権限グループ`。
  - 列は `名前`, `権限数`。`作成する` から `/admin/settings/permission_groups/create` へ遷移。
  - 既存行は `特権管理者` が権限数76、`TEST_権限検証_20260620` が権限数1。
  - 2026-06-27再確認では、`特権管理者` と管理メンバーに割り当て済みのカスタムグループはチェックボックスdisabled。
- 権限グループ作成 `/admin/settings/permission_groups/create`:
  - h1 `権限グループを作成する`。
  - 項目は `グループ名*` と76権限チェックボックス。
  - 空保存で `権限グループ名を入力してください`, `権限を選択してください`。
  - `TEST_NOTION_20260627_PERMISSION_0326` を `お知らせの閲覧権限（announcements:read）` の1権限で作成し、作成後に権限グループ詳細へ遷移することを確認。
  - 一覧へ戻ると `TEST_NOTION_20260627_PERMISSION_0326` が権限数1で表示。
- 権限グループ削除の状態変化:
  - 未割当の一時作成グループ `TEST_NOTION_20260627_PERMISSION_0326` を選択すると、一覧上部に `1を選択済み` と `権限グループを削除` が表示。
  - 削除ダイアログはタイトル `権限グループを削除しますか？`、本文 `選択された1件の権限グループを削除します。この処理は巻き戻すことができません。`。
  - `削除する` 実行後、対象行は一覧から消え、トースト `権限グループを削除しました` が表示。
- 管理ユーザーCSV:
  - `/admin/csv_import/csv_import_operation_users` は h1 `管理ユーザーをCSVでインポートする`。
  - 一覧には `テンプレート`, `新規インポート`、空状態 `アイテムが見つかりませんでした`。
  - `/create` は `CSVファイル` アップロードのみ。空保存で `ファイルを選択してください`。
- 誤URL:
  - `/admin/settings/staffs`, `/admin/settings/members`, `/admin/settings/organization_users` は `このページは存在しないようです`。
  - 管理メンバーの正しいURLは `/admin/settings/users`。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/account02-users-list-main-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-filter-menu-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-create-form-deep-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-create-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-detail-loaded-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-detail-permissions-expanded-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-groups-list-deep-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-created-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-groups-list-after-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-selected-for-delete-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-delete-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-permission-group-after-delete-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-import-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-import-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-user-import-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-invalid-staffs-404-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-invalid-members-404-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-invalid-current-404-recheck.md`

### L-020 03.組織・通知の再確認

- 対象: `03-組織・通知`, `01-by-feature/設定`, `02-by-task/初期設定の手順`, `02-by-task/その他のマスタを登録する`, サポート表
- 設定トップ `/admin/settings`:
  - 設定トップと組織IDセクションの存在を再確認。
- テナント `/admin/settings/tenants`:
  - 一覧は h1 `テナント`、導線 `テナントを作成`、列 `名前`。
  - 2026-06-27時点の行は `TEST_FAQ_20260624_TENANT_170037`, `テストテナント`, `TEST_FAQ_COVERAGE_20260615_テナント_EDIT`, `ユニクロ`。
  - 一覧に行選択チェックボックスや削除アクションは確認できない。
- テナント作成 `/admin/settings/tenants/create`:
  - フォームは `テナント名` のみ。プレースホルダーは `ブランド`。
  - 空欄では `保存する` が `aria-disabled=true` で通常クリックできない。テナント名入力後は `aria-disabled=false` になり、クリアすると再び無効化される。
  - 通常操作では空保存バリデーション文言は表示されない。
  - データ作成は行っていない。
- テナント詳細:
  - 既存テストテナント `TEST_FAQ_20260624_TENANT_170037` で確認。
  - セクションは `基本情報` と `CRM`。
  - 基本情報は `テナントID`, `テナント名`, `注文IDプレフィックス`。
  - CRMは `ポイントルール`, `ランクルール`, `誕生日ポイント付与ルール`, `失効予定通知ルール` の選択欄。
  - 詳細画面にも削除ボタンは確認できない。
- 通知用メールアドレス `/admin/settings/organization_notification_emails`:
  - 一覧は h1 `通知用メールアドレス`、導線 `メールアドレスを追加`、列 `名前` / `メールアドレス`。
  - 作成フォームは `名前`, `メールアドレス`。メールアドレス欄は `type=email`、プレースホルダー `you@company.com`。
  - 空保存で `名前を入力してください`, `メールアドレスを入力してください` を確認。
  - `TEST_NOTION_20260627_NOTIFICATION_0339` / `test-notion-20260627-notification-0339@example.com` を作成。保存後は一覧へ戻り、対象行が追加され、トースト `通知用メールアドレスを追加しました` が表示。
  - 対象行を選択すると `1を選択済み` と `削除する` が表示。
  - 削除ダイアログはタイトル `通知用メールアドレスを削除しますか？`、本文 `選択された1件の通知用メールアドレスを削除します。この処理は巻き戻すことができません。`。
  - 削除確定後は対象行が一覧から消え、トースト `通知用メールアドレスを削除しました` が表示。今回の一覧はテスト行追加で2件、削除後に既存1件へ戻った。
- 未確認:
  - 通知用メールアドレスにどの業務イベントで実メールが送られるか。
  - 管理メンバー詳細の `ユーザーテナント` が別権限ユーザーの一覧/詳細/操作権限をどう制限するか。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/org03-settings-top-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenants-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenants-list-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenant-create-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenant-create-empty-result.json`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenant-create-button-enable-result.json`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenant-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-tenant-detail-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-emails-list-before-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-create-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-empty-result.json`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-filled-before-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-emails-list-after-create-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-selected-for-delete-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-delete-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-after-delete-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/org03-notification-email-after-delete-result.json`

### L-021 05.商品・SKUの再確認

- 対象: `05-商品・SKU`, `01-by-feature/商品管理`, `02-by-task/商品を作成する`, `02-by-task/商品を編集する`, `02-by-task/商品をアーカイブ・削除する`, `03-faq/商品と商品登録のよくある質問`, サポート表
- 商品一覧 `/admin/products`:
  - h1 `商品管理`、導線 `インポート` / `商品を作成する`、タブ `すべて / 公開中 / 下書き / アーカイブ済み` を確認。
  - 列は `商品`, `ステータス`, `商品コード`, `在庫`, `カタログ`, `商品タイプ`, `製造元`。
  - `在庫` 列は在庫数量ではなく `0個のバリエーション`, `1個のバリエーション`, `20個のバリエーション` などのバリエーション数。
  - インポートメニューは `商品`, `商品画像`, `商品バリエーション`, `商品メタフィールド`, `商品バリエーションメタフィールド`。
- 商品作成 `/admin/products/create`:
  - 商品コードのヘルプは `半角英数字（A〜Z、a〜z、0〜9）、ハイフン（-）、アンダースコア（_）のみご入力ください。`。
  - 空保存で `商品コードを入力してください`, `商品名を入力してください`, `オプション名が空のフィールドがあります`, `選択してください`。
  - 全角/スペースを含む商品コードでは `利用できない文字が含まれています`。
- 非公開作成:
  - `TEST_NOTION_20260627_PRODUCT_0447` / `TEST_NOTION_20260627 商品 0447` を `非公開` で作成。
  - 保存後は詳細 `/admin/products/fd8966cc-6151-54c1-a169-5021a96c5676_Product` に遷移し、トースト `商品を作成しました`。
  - 詳細のステータスは `アーカイブ済み`。右側ステータス欄に `管理画面では、商品リスト以外は非表示です。`。
  - 商品作成直後はSKUは自動作成されず、詳細は `バリエーションがありません`、一覧は `0個のバリエーション`。
  - 一覧検索では `すべて` と `アーカイブ済み` タブに出て、`下書き` タブには出ない。
- アーカイブ解除:
  - アーカイブ済み詳細の `その他の操作` には `商品のアーカイブを解除する` と `商品を削除する`。
  - 解除ダイアログは `商品のアーカイブを解除しますか？`、本文 `この商品のアーカイブを解除すると、ステータスが下書きに変更され再び作業できるようになります。`。
  - 解除後は詳細ステータスが `下書き` になり、非表示説明文は消える。
  - 一覧では `下書き` タブに表示され、`アーカイブ済み` タブから消える。
- バリエーション/SKU作成:
  - 商品詳細の `バリエーションを追加する` から `/variants/create` へ遷移。
  - 作成フォームは商品オプション値 `M` をセレクトで選び、`上代*`, `SKU (最小管理単位)*`, `メーカーSKU`, `在庫を追跡する`, `在庫切れの場合でも販売を続ける`, `配送を必須にする` などを表示。`在庫を追跡する` と `在庫切れの場合でも販売を続ける` は初期OFF、`配送を必須にする` は初期ON。
  - `TEST_NOTION_20260627_SKU_0447` を作成すると `/admin/products/{id}/variants/dc1266c3-2301-543f-a91e-0af566bc2cd2_ProductVariant` へ遷移。
  - バリエーション詳細には `在庫管理` リンク、`原価` セクション、`原価を登録する`, `UPC`, `更新する` が表示。
  - 商品詳細に戻るとSKU行が表示され、商品一覧の在庫列は `1個のバリエーション` に変化。
- 再アーカイブ:
  - 下書き詳細の `その他の操作` には `商品をアーカイブする` と `商品を削除する`。
  - アーカイブダイアログは `商品をアーカイブしますか?`、本文 `この商品をアーカイブすると、販売チャネルと管理画面上で非表示になります。商品リストにあるステータス絞り込み機能を使用して商品を探します。`。
  - 実行後は詳細ステータスが `アーカイブ済み` に戻り、非表示説明文が再表示。
  - 一覧では `下書き` タブから消え、`アーカイブ済み` タブに `1個のバリエーション` のまま表示。
- 削除:
  - 削除ダイアログは `商品を削除しますか？`、本文 `この商品を削除しますか？` / `この処理は巻き戻すことができません。`、ボタン `キャンセル` / `削除する`。
  - 削除後は `/admin/products` へ戻る。商品コード/SKU検索では対象行なし。
  - 削除済み商品URLは `該当するProductが見つかりませんでした。`、削除済みバリエーションURLは `該当するProductVariantが見つかりませんでした。`。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/product05-products-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-products-list-structure-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/product05-products-import-menu-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-create-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-create-empty-save-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-create-empty-result.json`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-create-invalid-code-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-created-archived-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-created-visible-in-archived-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-unarchive-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-unarchive-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-unarchive-visible-in-draft-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-unarchive-absent-from-archived-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-variant-create-form-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-variant-created-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-detail-after-variant-created-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-list-after-variant-created-draft-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-archive-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-archive-detail-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-archive-absent-from-draft-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-archive-visible-in-archived-tab-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-delete-dialog-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-after-delete-list-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-product-deleted-detail-error-recheck.md`
  - `_analysis/live-notion-verification-2026-06-27/product05-variant-deleted-detail-error-recheck.md`

### L-022 04.基本マスタの再確認

- 対象: `04-基本マスタ`, `01-by-feature/設定`, `02-by-task/初期設定の手順`, `02-by-task/その他のマスタを登録する`, `01-by-feature/発注管理`, `15-発注・仕入`, サポート表
- ロケーション作成:
  - `/admin/settings/locations/create` は `名前*`, `表示名`, `コード*`, `場所種別*`, `ロケーションの住所を登録する`, `マップ`, `電話番号`, `メールアドレス`, `店舗受け取りを有効にする`, `在庫依頼を受け付ける`, `ポイント利用種別*`。
  - 空保存では `ロケーション名を入力してください`, `コードを入力してください`。場所種別は `倉庫`、ポイント利用種別は `値引き` が初期選択。
  - `TEST_NOTION_20260627_店舗_041001` / `TEST_NOTION_STORE_041001` を店舗種別、店舗受取ON、在庫依頼ONで作成。
- ロケーションのアーカイブ遷移:
  - 作成直後の詳細は公開設定 `公開`、`アーカイブする` ボタンあり。
  - 店舗受取ルール `/admin/local_pickup_retail_location_rules/create` のロケーション選択候補に作成直後の店舗ロケーションが表示。
  - `アーカイブする` クリックで確認ダイアログ `ロケーションをアーカイブしますか？`。本文は `ロケーションはいつでもアーカイブを解除することができます。アーカイブされたロケーションは管理画面やストアフロントからも非表示となります。`。
  - アーカイブ確定後、詳細上部に `このロケーションはアーカイブされています。` と説明文が表示され、ボタンは `アーカイブを解除する` に変化。公開設定は `非公開` でdisabled。
  - 一覧 `/admin/settings/locations` では `すべて` タブの同じ行に残り、公開列 `情報 非公開`、アーカイブ列 `アーカイブ済み`。
  - アーカイブ後も店舗受取ルールのロケーション選択候補に `TEST_NOTION_20260627_店舗_041001` が表示され、選択後フォーム値として入った（保存は未実行）。
  - `アーカイブを解除する` 後は警告表示が消え、ボタンは `アーカイブする` に戻る。一覧のアーカイブ列は空に戻るが、公開設定/公開列は `非公開` のまま。
  - 検証用ロケーションは最終的に再アーカイブ済み。
- ロケーショングループ:
  - 一覧は `すべて` タブのみ。列は `グループ名`, `デフォルト`, `ロケーション`。
  - `/admin/settings/location_groups/create` は `名前*` と `ロケーション` 選択欄。`このグループに新しいロケーションを自動的に含める` は作成フォームに表示されない。
  - 空保存では `グループ名を入力してください`, `ロケーションを選択してください`。
  - 作成フォームのロケーション選択モーダルは `すべて / 店舗 / 倉庫` タブ付きで、アーカイブ済みロケーションも候補に表示。
  - 既存詳細では `このグループに新しいロケーションを自動的に含める` チェックボックスはdisabled。
  - `グループに含まれるロケーション` 画面には `ロケーションを追加` があり、デフォルトロケーション行のチェックボックスはdisabled。
- ブランド:
  - `/admin/settings/brands/create` は `名前*`, `外部ID`, `コード*`。
  - 空保存では `ブランド名を入力してください`, `コードを入力してください`。
  - 一覧はタブではなくチェックボックス付き表。行選択で `1を選択済み` と `削除する` が表示。
- 取引先:
  - `/admin/settings/suppliers/create` は `取引先名*`, `取引先コード*`。取引先コードは必須。
  - 空保存では `取引先名を入力してください`, `取引先コードを入力してください`。
  - 一覧 `/admin/settings/suppliers` は `インポート`, `取引先を作成`, タブ `すべて / アーカイブ`。`インポート` クリック後もURL/本文/ダイアログに変化なし。
- 決済方法:
  - `/admin/settings/payment_methods/create` は `名前*`, `コード*`, `ゲートウェイ*`, `支払い待ちでも注文を出荷する`, `代引き`。
  - 空保存では `決済方法の名前を入力してください`, `この決済方法のコードを入力してください`, `ゲートウェイを入力してください`。
- 販売員:
  - `/admin/settings/retail_staff_members/create` は `姓*`, `名*`, `コード*`, `ロケーション`。
  - 空保存では `名前を入力してください`, `苗字を入力してください`, `コードを入力してください`, `ロケーションを選択してください`。ロケーションは作成時必須。
  - ロケーション選択モーダルは `すべて / 店舗 / 倉庫` タブ付き。アーカイブ済みロケーションも候補に表示。
  - 1件選択すると `1を選択済み` になり、選択済み行以外のcheckboxはdisabled。作成フォームでは単一選択。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-create-empty-save-text.txt`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-detail-created.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-local-pickup-location-modal-before-archive.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-detail-archived-confirmed.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-locations-list-after-archive.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-local-pickup-location-modal-after-archive.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-local-pickup-rule-form-archived-location-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-detail-after-unarchive.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-locations-list-after-unarchive.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-detail-final-rearchived.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-group-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-group-create-empty-save.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-group-location-modal.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-group-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-location-group-locations-edit.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-brand-create-empty-save.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-brands-list-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-supplier-create-empty-save.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-suppliers-import-click-result.json`
  - `_analysis/live-notion-verification-2026-06-27/basic04-payment-method-create-empty-save.md`
  - `_analysis/live-notion-verification-2026-06-27/basic04-retail-staff-location-modal-selected.md`

### L-023 08.カスタムデータ / 09.翻訳 / 10.採寸の再確認

- 対象: `04-notion/08-カスタムデータ.md`, `04-notion/09-翻訳.md`, `04-notion/10-採寸.md`, `01-by-feature/設定.md`, `02-by-task/カスタムデータを設定する.md`, `00-getting-started/SQ完全ガイド.md`, `データ事典①`, サポート表, WBS
- メタフィールド定義:
  - `/admin/settings/metafield_definitions` の対象オブジェクトは16種。実機表示は `仕入れ先ベンダー`。
  - 商品定義作成フォームは `名前*`, `説明`, `ネームスペース*`, `キー*`, `メタフィールドのタイプ*`。空保存エラーは `定義名を入力してください`, `ネームスペースを入力してください`, `キーを入力してください`, `タイプを選択してください`。
  - `abc.def`（3文字同士）で商品メタフィールド定義 `TEST_META_SHORT_20260627` を保存できたため、過去の「4文字以上必須」断定は撤回。現行UIで確認できた制約は最大50文字。
  - 作成後は商品定義一覧へ戻り、行は `TEST_META_SHORT_20260627 abc.def 単一行のテキスト 編集可 0個の商品`。商品詳細には `メタフィールド` セクションが出現し、値は `未設定`。
  - 商品詳細の鉛筆ボタンから値 `TEST_VALUE_20260627` を保存すると、商品詳細表示が値に変わり、定義一覧の使用箇所が `0個の商品` から `1個の商品` へ変化。
  - 定義行を選択して削除すると、確認ダイアログ `メタフィールドの定義を削除しますか？` が表示される。削除後は定義一覧から消え、商品詳細のメタフィールドセクションも表示されなくなった。
- 翻訳:
  - `/admin/settings/translation` は翻訳ルール未選択時に商品リソースを開けない。既存ルール選択後、商品リンクが `/admin/settings/translation/{ruleId}/products` へ遷移可能になる。
  - 商品翻訳一覧は `商品を翻訳する` 画面で商品列のみ。商品詳細へ入ると `商品`, `オプション 1`, `オプション 2` の原文/英語欄が表示されるが、直接編集/保存ボタンは確認できない。
  - 翻訳ルール作成フォームは `名前*`, `言語*`, `翻訳データを自動で作成する`。空保存エラーは `名前を入力してください`, `言語を選択してください`。作成フォーム上では自動生成チェックをONにしてもプロンプト欄は出ない。
  - 保存後の詳細では言語はdisabled。`商品`, `商品オプション`, `商品オプション値`, `メタフィールド` ごとに親プロンプト/カスタムプロンプト欄が表示され、カスタムプロンプト保存で `翻訳ルールを更新しました`。
  - 作成した `TEST_TRANSLATION_20260627_0438` は一覧で行選択後に `削除する`、確認ダイアログ `翻訳ルールを削除しますか？`、削除後は行消滅とトースト `翻訳を削除しました` を確認。
- 採寸:
  - `/admin/settings/product_measurement_rules/create` は `ルール名*`, `採寸単位`, `採寸項目1`, `採寸項目を追加`。採寸単位は `なし` / `センチメートル`。
  - 空保存では `ルール名を入力してください`。採寸項目は最大5件で、5件追加後に `採寸項目を追加` ボタンが消える。
  - `TEST_MEASURE_20260627_0439` を `センチメートル`、5項目で保存。詳細へ遷移し、作成トースト `採寸ルールを作成しました`。
  - 詳細画面の入力欄はreadOnlyで、編集/保存/削除ボタンは確認できない。一覧では採寸項目が `肩幅 / 身幅 / 着丈 / 袖丈 / 裾幅` と `/` 区切りで表示される。
  - 商品詳細には採寸ルール紐付けUIを確認できない。UI削除経路がないため、検証用採寸ルール `TEST_MEASURE_20260627_0439` は残存。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/area08-metafield-product-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/area08-metafield-product-short-created.md`
  - `_analysis/live-notion-verification-2026-06-27/area08-product-detail-metafield-after-value-save.md`
  - `_analysis/live-notion-verification-2026-06-27/area08-metafield-product-list-after-value.md`
  - `_analysis/live-notion-verification-2026-06-27/area08-metafield-delete-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/area08-product-detail-after-definition-delete.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-top-rule-selected.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-products-list.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-product-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-rule-detail-after-create.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-rule-delete-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/area09-translation-rules-list-after-delete.md`
  - `_analysis/live-notion-verification-2026-06-27/area10-measurement-create-five-items.md`
  - `_analysis/live-notion-verification-2026-06-27/area10-measurement-detail-after-create.md`
  - `_analysis/live-notion-verification-2026-06-27/area10-measurement-list-after-create.md`
  - `_analysis/live-notion-verification-2026-06-27/area10-product-detail-check-measurement-attachment.md`

### L-024 24.会計・売上実績・分析の再確認

- 対象: `04-notion/24-会計・売上実績・分析.md`, `01-by-feature/会計（売上実績）.md`, `02-by-task/売上実績をCSVエクスポートする.md`, `01-by-feature/CSVエクスポート・PDFエクスポート.md`, `00-getting-started/SQ完全ガイド.md`, `データ事典②`, サポート表
- 売上実績一覧:
  - `/admin/sale_change_line_items` は h1 `売上実績`。
  - 2026-06-27時点の一覧は空状態で、`アイテムが見つかりませんでした` / `絞り込みや検索ワードを変更してみてください` を表示。
  - `エクスポート` ボタンは有効。`売上実績を作成する` はリンクではなく、手動作成操作はできない。
  - 直接 `/admin/sale_change_line_items/create` にアクセスすると `このページは存在しないようです`。
- エクスポートメニュー:
  - 売上実績一覧の `エクスポート` から `注文軸` と `明細軸` が表示される。
  - `注文軸` は `/admin/csv_export/csv_export_operation_sale_changes`、`明細軸` は `/admin/csv_export/csv_export_operation_sale_change_line_items`。
- CSVエクスポート履歴:
  - 注文軸・明細軸とも h1 は `売上実績（注文軸）をCSVでエクスポートする` / `売上実績（明細軸）をCSVでエクスポートする`。
  - 履歴一覧の列は `作成日`, `テナント`, `対象期間`, `ステータス`, `ダウンロード`。
  - 既存履歴で `ユニクロ`、ステータス `成功` / `完了`、`ダウンロード` リンクを確認。
  - 証跡ファイルでは署名付きダウンロードURLを `<SIGNED_DOWNLOAD_URL_REDACTED>` に伏せ字化済み。
- CSVエクスポート作成フォーム:
  - 注文軸・明細軸とも項目は `テナント*`, `開始日時*`, `終了日時*`。
  - テナント選択肢は `ユニクロ`, `TEST_FAQ_COVERAGE_20260615_テナント_EDIT`, `テストテナント`, `TEST_FAQ_20260624_TENANT_170037`。
  - 空保存エラーは `テナントを選択してください`, `開始日時を入力してください`, `終了日時を入力してください`。
  - 新規エクスポート実行は今回は行っていない。既存履歴で成功完了状態とダウンロードリンク表示を確認。
- 分析:
  - `/admin/analytics` は h1 `分析`、本文 `TODO`。
  - `/admin/analytics/revenue` は h1 `売上`、本文 `TODO`。ナビ名は `収益` なので表記不一致。
  - `/admin/analytics/reports` は h1 `レポート`、本文 `TODO`。
- 残件:
  - 注文データから売上実績が自動生成されるか、売上データありの売上実績一覧列、注文データありで `売上実績を作成する` が有効化されるかは、注文/チャネル接続データ待ち。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-line-items-list.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-line-items-export-menu.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-order-list.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-order-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-order-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-line-list.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-line-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-export-line-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-sale-change-create-404.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-analytics-top-todo.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-analytics-revenue-todo.md`
  - `_analysis/live-notion-verification-2026-06-27/area24-analytics-reports-todo.md`

### L-025 23.API・Webhook・開発者連携の再確認

- 対象: `04-notion/23-API・Webhook・開発者連携.md`, `01-by-feature/設定.md`, `00-getting-started/SQ完全ガイド.md`, サポート表
- アプリ一覧:
  - `/admin/settings/apps` は h1 `アプリ`。
  - `アプリを作成` から `/admin/settings/apps/create` へ遷移。
  - 一覧はカード表示で、既存テストアプリ `TEST_FAQ_20260624_APP_113636` などを確認。
  - 一覧カード上にアクセストークン/シークレット値や削除ボタンは表示されない。
- アプリ作成フォーム:
  - `/admin/settings/apps/create` は h1 `新しいアプリ`。
  - 項目は `アプリ名*`（プレースホルダー `モバイルアプリ`）と `権限`。
  - 権限は38リソース×閲覧/編集の76チェックボックス。
  - 空保存エラーは `アプリ名を入力してください` と `権限が選択されていません`。補足文は `アプリが持つ権限は、必ず1つ以上選択されている必要があります。`
  - アプリ削除/失効導線が未確認のため、新規アプリ作成は今回は実行していない。
- アプリ詳細:
  - 既存テストアプリ詳細 `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App` を確認。
  - `Admin API` に `アクセストークン` / `シークレット`、`Playgroundを開く`、`リクエストログを見る` が表示。
  - 証跡ではアクセストークン/シークレットを `<SECRET_REDACTED>` に伏せ字化済み。
  - `Playgroundを開く` のリンク先は `https://sq.stackservice.com/api/admin/v1/playground`。秘密値露出を避けるため実行画面は開かず。
  - `Storefront API` に `トークンを発行する`、`Webhook` に `Webhookを作成する` が表示。
  - 詳細画面にも一覧カードにも、アプリ削除・トークン失効・アクセストークン/シークレット再発行の導線は確認できない。
- Webhook:
  - `Webhookを作成する` でダイアログ `Webhookを追加する` が開く。
  - 入力項目は `イベント*` と `エンドポイント*`。
  - イベント選択肢は `注文の作成`, `注文の更新`, `在庫の更新` の3種。
  - 空保存すると同じダイアログ内に `イベントを選択してください` / `エンドポイントを入力してください` が表示され、ページ遷移せずWebhookも作成されない。
  - Webhook実作成後の一覧表示・編集/削除/停止導線・送信成功/失敗ステータスは未確認。削除/停止導線と送信影響が未確認のため、実作成は行っていない。
- リクエストログ:
  - `リクエストログを見る` は `/admin/settings/apps/{id}/admin_api` へ遷移。
  - 画面タイトルは `リクエストログ`、補足は `Admin API - TEST_FAQ_20260624_APP_113636`。
  - 本文は `TODO`。ログ行・ステータス・保持期間・詳細項目は確認できない。
- 残件:
  - API直接実行、GraphQLスキーマ、認証ヘッダ形式、Webhook署名方式、Storefront APIの範囲は開発元確認/実行環境待ち。
  - Storefrontトークン発行後の再表示・削除・失効、Webhook作成後の管理導線は未確認。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/area23-apps-list.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-app-create-form.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-app-create-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-app-detail.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-webhook-create-dialog.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-webhook-create-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/area23-request-logs.md`

### L-026 01.SQ全体・共通導線 / 04.基本マスタの最終整理

- 対象: `04-notion/01-SQ全体・共通導線.md`, `04-notion/04-基本マスタ.md`
- 既存実機ログ L-002/L-003/L-004/L-005/L-017/L-022 を再確認し、01/04の「再確認中」ステータスを外した。
- ロケーション説明:
  - 場所種別は `倉庫` / `店舗` の2種のみ。
  - リテールポータル連携では `店舗ロケーション` が店舗種別、`在庫ロケーション` が倉庫種別。
  - 店舗受取ルールのロケーション選択肢は店舗種別。
  - 手動の在庫依頼・移動伝票では倉庫/店舗の両方が関与するため、「倉庫=出荷元だけ」「店舗=受け口だけ」のような全機能共通の断定はしない。
- アーカイブ後の状態変化:
  - ロケーションは詳細の `アーカイブする` でアーカイブ可能。削除ボタンは確認できない。
  - アーカイブ後は詳細に警告が出て、ボタンは `アーカイブを解除する` に変化。
  - 一覧の `すべて` タブに残り、公開列は `非公開`、アーカイブ列は `アーカイブ済み`。
  - 解除後はアーカイブ列が空に戻るが、公開設定は `非公開` のまま。
  - 検証用ロケーションは最終的に再アーカイブ済み。
- 追加修正:
  - `01-SQ全体・共通導線` の「SQが管理するデータの全体像」に旧分類範囲（例: 商品05〜10、在庫11〜14等）が残っていたため、現行24分類に合わせて `05〜11`, `12〜15`, `16〜17`, `18`, `19〜21`, `22〜24` へ修正。

### L-027 設定マスタ未登録時の候補表示に関する追加実験

- きっかけ: `01-SQ全体・共通導線` の「ここでマスタが未登録だと、各業務画面の選択肢が空になります」という断定が、全マスタ/全画面で実験済みか確認。
- 結論:
  - 候補が空になる実例は実機で確認できた。
  - ただし、全マスタ/全画面を0件状態にして一律検証したわけではないため、「各業務画面の選択肢が空になります」とは断定しない。
  - 表現は「多くの業務フォームは設定マスタを参照し、未登録・0件・種別不一致・連携未接続の場合は候補が出ないことがある」に修正。
- 実験1: 店舗受取ルールのロケーション選択
  - URL: `/admin/local_pickup_retail_location_rules/create`
  - ロケーション選択ダイアログは店舗種別ロケーションのみを候補に出す。
  - 倉庫コード `W0001` 検索では `アイテムが見つかりませんでした`。
  - 店舗コード `R0001` 検索では `ユニクロ - 銀座店 / R0001` が1件表示。
  - これは「マスタが未登録」ではなく「種別条件不一致」で候補が空になる例。
- 実験2: 販売上限ルールのチャネル選択
  - URL: `/admin/inventory_sale_limit_rules/create`
  - `チャネル` 見出しは表示されるが、チャネル候補のチェックボックスは表示されない。
  - 空保存で `販売上限ルール名を入力してください` と `チャネルを選択してください`。
  - これはチャネル未接続/候補なしで保存できない例。
- 実験3: ディスカウントの顧客追加
  - URL: `/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule/customers`
  - 顧客管理タブは0件表示。
  - `追加する` → `顧客を選択して追加` で `顧客を選択する` ダイアログは開くが、候補は空で `選択する` はdisabled。
  - これは参照先データ0件で候補が空になる例。
- スナップショット:
  - `_analysis/live-notion-verification-2026-06-27/master-choice-local-pickup-rule-create.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-local-pickup-location-dialog-open.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-local-pickup-location-search-W0001-empty.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-local-pickup-location-search-R0001-one.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-sale-limit-create-channel-empty.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-sale-limit-create-empty-errors.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-discount-customers-tab-empty.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-discount-customers-add-menu.md`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-discount-customers-select-dialog-empty.md`

### L-028 設定マスタ候補表示の全体マトリクス再確認

- きっかけ: L-027の3実験だけでは「設定画面で作る全マスタが、どの業務画面の候補に出るか」の確認として不足していたため、設定マスタ/周辺データを対象に追加で総点検した。
- 追加確認:
  - Shopify/OmnibusCore/スマレジ/リテールポータル作成フォームで、テナント・カタログ・ロケーショングループ・販売価格ルール・予約ルール・販売閾値ルールの候補表示を確認。
  - リテールポータルの店舗ロケーション欄で倉庫コード `W0001` を検索すると0件、在庫ロケーション欄で店舗コード `R0001` を検索すると0件になることを確認。
  - 商品作成のブランド選択ダイアログで既存ブランド候補を確認。
  - 発注伝票作成で取引先・テナント候補を確認。
  - 管理メンバー作成で権限グループ候補を確認。
  - 翻訳トップで翻訳ルール候補を確認。
- 結論:
  - 「設定でマスタが未登録だと各業務画面の選択肢が空になる」と一律には言えない。
  - 候補が出ない原因は、`0件`、`検索条件/種別フィルタ不一致`、`連携・チャネル未接続`、`参照UIなし` に分ける。
  - 既存テナント・ブランド・取引先などの全削除による0件化は、共有検証環境を壊すため実施していない。代わりに、既存候補の有無、検索不一致、種別不一致、チャネル未接続、過去の作成/削除済みテストデータの反映で確認した。
- 反映:
  - `04-notion/01-SQ全体・共通導線.md`
  - `04-notion/02-アカウント・権限.md`
  - `04-notion/19-店舗業務・リテールポータル.md`
  - `04-notion/20-標準販売チャネル連携.md`
  - `00-getting-started/データ事典①-設定で作るデータ.md`
  - `00-getting-started/セットアップガイド.md`
  - `00-getting-started/SQ完全ガイド.md`
  - `03-faq/設定と権限のよくある質問.md`
- 詳細マトリクス:
  - `_analysis/MASTER-CHOICE-LIVE-MATRIX-2026-06-27.md`
- 追加スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/master-choice-shopify-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-omnibus-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-smaregi-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-retail-portal-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-retail-portal-store-search-W0001-empty-data.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-retail-portal-inventory-search-R0001-empty-data.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-product-brand-dialog-data.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-purchase-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-user-create-controls.json`
  - `_analysis/live-notion-verification-2026-06-27/master-choice-translation-rule-menu-data.json`

### L-029 管理メンバー一覧の検索・絞り込み再確認

- きっかけ: `02-アカウント・権限` に「絞り込み条件はメールアドレスのみ」とあるが、実機で名前（`河野`）検索できるという指摘があった。
- 結論:
  - 管理メンバー一覧の **キーワード検索欄**（`キーワードで検索する`）は、姓・名・メールアドレス断片に効く。
  - `河野`、`陽介`、`kohno` はそれぞれ `河野陽介 / yosuke.kohno@bay-works.com` に絞り込まれる。
  - 権限グループ名 `特権管理者` はキーワード検索対象外で0件。
  - **「絞り込みを追加」** の条件は `メールアドレス` のみ。これはキーワード検索とは別の専用フィルタで、`kohno` などの断片では `メールアドレスの形式が正しくありません`、フルメールアドレスでは `?email=...` で1件に絞り込まれる。
- 反映:
  - `04-notion/02-アカウント・権限.md`
  - `02-by-task/管理メンバーを追加する.md`
  - `01-by-feature/設定.md`
- 横断確認:
  - 主要42画面の検索・絞り込みUIをクロールし、`_analysis/live-notion-verification-2026-06-27/search-filter-audit/` に保存。
  - 詳細まとめは `_analysis/SEARCH-FILTER-LIVE-AUDIT-2026-06-27.md`。
- スナップショット/結果:
  - `_analysis/live-notion-verification-2026-06-27/account02-users-keyword-search-name-kono.md`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-keyword-search-name-kono.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-keyword-search-given-yosuke.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-keyword-search-email-kohno.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-keyword-search-permission-admin.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-filter-menu-20260627-recheck.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-email-filter-kohno.json`
  - `_analysis/live-notion-verification-2026-06-27/account02-users-email-filter-exact-email.json`

## 次に確認すること

1. `04-基本マスタ`: 店舗受け取りフラグON/OFFが店舗受取候補・ストアフロント受取可否へ与える影響（接続環境待ち）。
2. `02-アカウント・権限`: 実ユーザー作成保存、組織から除外の確認ダイアログ/除外後ログイン、別権限ユーザーでのメニュー・作成ボタン・権限エラー、ユーザーテナントOFF時の実効果は未実行。
3. ステータス遷移が重要な領域は、作成後のステータス移動・一覧タブ移動・在庫区分変化まで検証する。`13-在庫伝票`, `14-入出荷・在庫依頼`, `15-発注・仕入` は主要フロー確認済み。`16-注文・返品` は注文データ0件のため連携待ち。
4. 以降、URL数と断定表現が多い順に未再確認の設定系分類を確認する。`02 アカウント・権限`、`16 注文・返品`、`17 顧客・会社`、`18 CRM`、`21 物流・返品・外部アプリ連携`、`22 CSV/PDF` は主要導線確認済みだが、実ユーザー/実注文/実顧客/接続後挙動はデータ依存として残す。
