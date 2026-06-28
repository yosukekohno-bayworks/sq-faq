# FAQ/HTML・25分類・実機 三者整合性監査レポート 2026-06-24

## ステータス

本レポートは一次監査です。静的棚卸しと、実操作E2Eの一部を完了しました。25分類すべての深掘り実操作は継続対象です。

## 実操作E2E結果

- ログ: `_analysis/full-live-operation-2026-06-24/e2e-crud/results.md`
- イベント数: 84
- ステータス: {'OK': 70, 'INFO': 2, 'WARN': 10, 'FAIL': 2}

### 実操作で確認できたこと

- `商品: 保存`: OK
- `商品: GUバリエーション作成`: OK
- `在庫追跡: OFFにして更新`: OK
- `在庫追跡OFF: 在庫依頼フォームにSKUが入る`: OK
- `在庫追跡: ONへ復旧`: OK
- `在庫依頼: 保存`: OK

### 実操作で問題/要再確認になったこと

- WARN `商品: GU製品入力`: {"fills": [{"ok": true, "label": "商品コード", "value": "TEST_FAQ_20260624_GU_092214"}, {"ok": true, "label": "商品名", "value": "TEST_FAQ_20260624 GU検証Tシャツ 092214"}, {"ok": true, "label": "説明文", "value": "E2E検証用のGU製品。既存ユーザーには紐づ
- WARN `調整伝票: ロケーション選択: モーダル検索入力`: {"ok": false, "reason": "search field not found"}
- WARN `調整伝票: 商品行選択`: {"ok": false, "reason": "row not found containing text", "text": "TEST_FAQ_20260624_GU_092214_NAVY_M", "firstRows": []}
- FAIL `調整伝票: 保存後URL確認`: url_changed_from_create=False
- WARN `調整伝票: 実行ボタン確認/押下`: {"ok": false, "reason": "click target not found", "texts": ["実行する", "実施する"]}
- WARN `調整伝票: 実行確認`: {"ok": false, "reason": "click target not found", "texts": ["実行する", "実施する", "更新する"]}
- WARN `在庫依頼: 移動先: モーダル検索入力`: {"ok": false, "reason": "search field not found"}
- WARN `在庫依頼: 依頼先: モーダル検索入力`: {"ok": false, "reason": "search field not found"}
- WARN `移動伝票: 配送元: モーダル検索入力`: {"ok": false, "reason": "search field not found"}
- WARN `移動伝票: 配送先: モーダル検索入力`: {"ok": false, "reason": "search field not found"}
- WARN `移動伝票: 商品行選択`: {"ok": false, "reason": "row not found containing text", "text": "TEST_FAQ_20260624_GU_092214_NAVY_M", "firstRows": []}
- FAIL `移動伝票: 保存後URL確認`: url_changed_from_create=False

## HTML成果物の棚卸し

| ファイル | サイズ | title | link数 |
|:--|--:|:--|--:|
| `SQ-FAQ.html` | 1198698 | SQ FAQ（多軸ビュー） | 851 |
| `SQ-サポートデスク.html` | 176891 | SQ サポートデスク（逆引き） | 196 |
| `SQ-データ相関図.html` | 25861 | SQ データ相関図 | 2 |
| `SQ完全ガイド.html` | 246274 | SQ完全ガイド — ゼロから理解する指南書 | 21 |

### `SQ-FAQ.html` のソース収録確認

`00-getting-started` / `01-by-feature` / `02-by-task` / `03-faq` の主要md名は `SQ-FAQ.html` 内でヒットしました。

## 04-notion 内リンク整合性

- リンク切れ/仮リンク疑い: 16件

- `04-notion/02-アカウント・権限.md` → `03-設定・マスタ.md`
- `04-notion/03-組織・通知.md` → `04-次エリア.md`
- `04-notion/04-基本マスタ.md` → `05-商品管理.md`
- `04-notion/07-店舗受取商品.md` → `./08-次エリア名.md`
- `04-notion/08-カスタムデータ.md` → `./09-次エリア名.md`
- `04-notion/09-翻訳・採寸.md` → `10-商品とバリエーション.md`
- `04-notion/10-価格・販売制御.md` → `11-発注・仕入.md`
- `04-notion/11-在庫状態・在庫数.md` → `12-移動伝票・出荷・入荷.md`
- `04-notion/12-在庫伝票.md` → `13-出荷管理・入荷管理.md`
- `04-notion/15-注文・返品.md` → `16-次エリア名.md`
- `04-notion/16-顧客・会社.md` → `./17-次エリア名.md`
- `04-notion/17-CRM.md` → `18-注文・カート.md`
- `04-notion/19-標準販売チャネル連携.md` → `20-次エリア名.md`
- `04-notion/20-物流・返品・外部アプリ連携.md` → `21-次エリア名.md`
- `04-notion/21-CSV・PDF・データ移行.md` → `22-外部連携.md`
- `04-notion/23-会計・売上実績・分析.md` → `24-次エリア名.md`

## 現時点の重要な不一致/注意

1. `04-notion` 内に既存の仮リンク/リンク切れが残っているため、分類番号の中間挿入はリスクが高い。
2. 実操作E2Eでは基本マスタ・商品・SKU・カタログ・在庫追跡・在庫依頼までは作成/保存確認が進んだ。
3. 調整伝票/移動伝票は商品選択モーダルの操作が自動化で失敗し、保存後URL確認も失敗。手動再検証が必要。
4. HTML成果物は現在のMarkdownから再生成済みか未確定。次にビルド差分確認が必要。

## 次にやること

1. HTMLを一時出力先で再生成し、現行HTMLとの差分を確認する。
2. 25分類ごとに実操作チェックを分割して進める。
3. 自動化が失敗した伝票系はbrowser-useの手動操作で再確認する。
4. 三者不一致を修正候補として分類する（即修正/要Stack確認/実機未確認）。

## 追加実機操作: 翻訳・採寸 2026-06-24 09:37-09:38

### 翻訳ルール

- 作成URL: `/admin/settings/translation/translation_rules/create`
- テスト名: `TEST_FAQ_20260624_TRANSLATION_CRUD_093701`
- 実操作:
  - 名前を入力
  - 言語で `英語` を選択
  - `保存する` を押下
- 結果:
  - 詳細URLへ遷移: `/admin/settings/translation/translation_rules/b98afc2f-97b7-5964-aeaf-a330c9f38a27_TranslationRule`
  - 通知: `翻訳ルールを作成しました`
  - 詳細画面に以下4セクションを確認
    - `商品`
    - `商品オプション`
    - `商品オプション値`
    - `メタフィールド`
  - 各セクションに `親プロンプト` / `カスタムプロンプト` / `カスタマイズ項目を追加する` を確認
  - 詳細画面のボタンは `保存する` のみ。削除ボタンは確認できず
- 注意:
  - 作成後に `/admin/settings/translation/translation_rules` を開くと `Application error: a client-side exception has occurred` が発生
  - `/admin/settings/translation` トップは正常表示に復旧
  - 作成したテスト翻訳ルールは、実機UI上で削除導線未確認のため残存

### 採寸ルール

- 作成URL: `/admin/settings/product_measurement_rules/create`
- テスト名: `TEST_FAQ_20260624_MEASURE_CRUD_093821`
- 実操作:
  - `ルール名` を入力
  - `採寸単位` で `センチメートル` を選択
  - `採寸項目1` に `肩幅` を入力
  - `保存する` を押下
- 結果:
  - 詳細URLへ遷移: `/admin/settings/product_measurement_rules/c3cce272-31c9-50c6-9af2-95e7be3ec25a_ProductMeasurementRule`
  - 通知: `採寸ルールを作成しました`
  - 一覧 `/admin/settings/product_measurement_rules` にテストルールが表示
  - 一覧列: `ルール名` / `単位` / `採寸項目`
  - 表示値: `TEST_FAQ_20260624_MEASURE_CRUD_093821` / `センチメートル` / `肩幅`
  - 詳細画面・一覧画面とも削除ボタンは確認できず
- 注意:
  - 作成したテスト採寸ルールは、実機UI上で削除導線未確認のため残存

### 分類判断への影響

- 翻訳と採寸は同じ `設定 > カスタムデータ` グループ配下だが、実操作上は別URL・別データ・別画面。
- 翻訳はプロンプト/翻訳対象データ種別の管理、採寸は採寸テンプレート管理で、確認観点が明確に異なる。
- `09-翻訳・採寸` は分割した方が、実機仕様とFAQ検索性に合う。

## 追加実機操作: 調整伝票・移動伝票・出荷/入荷 2026-06-24 09:46-09:52

### 調整伝票

- 作成URL: `/admin/inventory_adjustment_orders/create`
- 使用SKU: `TEST_FAQ_20260624_GU_092214_NAVY_M`
- 使用ロケーション: `TEST_FAQ_20260624_GU倉庫_ON_092214`
- 実操作:
  - ロケーション選択モーダルでテスト倉庫を選択
  - 理由 `その他` を選択
  - 商品参照モーダルで対象SKUを選択
  - 増減数 `2` を入力
  - 保存
  - 詳細画面で `実行` を押下
  - 確認ダイアログ `在庫調整を実行する` で `実行する` を押下
- 結果:
  - 調整伝票 `#IA-1012` 作成
  - 実行後ステータス: `完了` / `実施済み`
  - 通知: `在庫調整を実行しました`
- 注意:
  - 実行後の詳細表示上、明細の `増減数` が `0` 表示になっている。保存時は `2` を入力しているため、表示/反映の追加確認が必要。

### 移動伝票

- 作成URL: `/admin/inventory_movement_orders/create`
- 使用SKU: `TEST_FAQ_20260624_GU_092214_NAVY_M`
- 配送元: `TEST_FAQ_20260624_GU倉庫_ON_092214`
- 配送先: `TEST_FAQ_20260624_GU店舗_OFF_092214`
- 実操作:
  - 配送元を選択
  - 配送先を選択
  - 商品参照モーダルで対象SKUを選択
  - 数量 `1` を入力
  - 上部 `保存` を押下
- 結果:
  - 移動伝票 `#IM-1024` 作成
  - 関連出荷指示 `#IO-1024` 自動生成
  - 関連入荷指示 `#II-1024` 自動生成

### 出荷指示

- 対象: `#IO-1024`
- 実操作:
  - `出荷実績を登録する` を押下
  - 配送キャリア/追跡コードは空欄のまま `登録する` を押下
- 結果:
  - ステータス: `成功 完了` / `出荷完了`
  - 出荷予定 `1`、出荷済み `1`
  - 通知: `出荷を完了しました`
- 注意:
  - 引当ステータスは出荷完了後も `引当待ち` 表示のまま。既存実機ログの知見と一致。

### 入荷指示

- 対象: `#II-1024`
- 実操作:
  - `入荷指示を一括受領で完了する` を開く
  - 確認画面で `完了する` を押下
- 結果:
  - ステータス: `成功 完了` / `入荷完了`
  - 入荷予定 `1`、入荷済み `1`
  - 通知: `入荷指示を一括受領で完了しました`

### 親移動伝票の再確認

- 対象: `#IM-1024`
- 出荷完了・入荷完了後の表示:
  - `成功 完了`
  - `入荷完了`
  - 関連: `#IO-1024` / `#II-1024`

### FAQ/25分類への影響

- `12-在庫伝票.md` / `13-入出荷・在庫依頼.md` に記載すべき実機事実:
  - 移動伝票保存で出荷指示・入荷指示が自動生成される。
  - 出荷実績登録は配送キャリア/追跡コード空欄でも完了できる。
  - 入荷指示は `入荷指示を一括受領で完了する` で全量受領できる。
  - 出荷完了後も出荷指示の引当ステータスが `引当待ち` 表示のまま残る場合がある。
- `12-在庫伝票.md` については、調整伝票実行後の明細増減数表示が `0` になる点を追加確認対象にする。


## 追加: 全ページスキャン 2026-06-24

- 出力: `_analysis/full-live-operation-2026-06-24/full-page-scan/scan-results.json` / `scan-results.md`
- 集計: `_analysis/full-live-operation-2026-06-24/full-page-scan/summary-20260624.md`
- 注意: `scan-results.md` のヘッダ日付は元スクリプト由来で2026-06-21表記だが、今回の出力先で2026-06-24に再実行したもの。

| status | count |
|:--|--:|
| ok | 205 |
| not_found | 18 |
| todo | 5 |
| app_error | 2 |

主な要注意ページは `summary-20260624.md` を参照。


## 追加: 空保存バリデーション 2026-06-24

- 出力: `_analysis/full-live-operation-2026-06-24/empty-save-validation/results.md`
- 対象: 49作成フォーム（ユーザー作成/APIアプリ作成は除外）

| status | count |
|:--|--:|
| validation_shown | 41 |
| clicked_no_obvious_validation | 3 |
| not_found | 3 |
| app_error | 2 |

### 要注意

- `/admin/draft_orders/create`: app_error — コンテンツにスキップ  stack-ps-yosuke  陽介 河野  ホーム 商品管理 在庫管理 注文管理 下書き 返品 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ
- `/admin/purchasing_customers/create`: app_error — コンテンツにスキップ  stack-ps-yosuke  陽介 河野  ホーム 商品管理 在庫管理 注文管理 顧客管理 会社 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify Omnibu
- `/admin/point_calculation_rules/create`: clicked_no_obvious_validation — コンテンツにスキップ  stack-ps-yosuke  陽介 河野  ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント キャンペーン 誕生日 利用外商品 失効通知 会員ランク 販売
- `/admin/b2b/create`: not_found — このページは存在しないようです ホームに戻る
- `/admin/settings/tenants/create`: clicked_no_obvious_validation — コンテンツにスキップ  stack-ps-yosuke  陽介 河野  ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCo
- `/admin/settings/metafield_definitions/create`: not_found — このページは存在しないようです ホームに戻る
- `/admin/csv_export/csv_export_operation_product_variants/create`: clicked_no_obvious_validation — コンテンツにスキップ  stack-ps-yosuke  陽介 河野  ホーム 商品管理 在庫管理 注文管理 顧客管理 発注管理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCo
- `/admin/pdf_export/pdf_export_operation_packing_slips/create`: not_found — このページは存在しないようです ホームに戻る

## 追加: 顧客・会社 作成フォーム検証 2026-06-24

### 会社作成フォーム

- URL: `/admin/companies/create`
- 確認項目:
  - `会社名`
  - `会社ID`
  - `担当者`
  - `ロケーション名`
  - `ロケーションID`
  - `コード`
  - 配送先住所一式
  - 請求先住所 `配送先住所と同じ`
- 実操作:
  - テスト会社名・会社ID・ロケーション・住所を入力
  - 国/地域 `日本`、都道府県 `東京都` を選択
  - `保存する` を押下
- 結果:
  - 画面は `/admin/companies/create` のまま。
  - `会社を作成しました` 通知は確認できず。
  - 国/地域/都道府県セレクトの値表示は確認できたが、保存成功まで未達。
- 扱い:
  - 会社作成は実機フォーム構造確認済み、保存成功は追加検証対象。


## 追加: 販売設定・CRM・外部連携 作成操作確認 2026-06-24

- 出力: `_analysis/full-live-operation-2026-06-24/sales-crm-crud/results.md`
- テスト入力は `TEST_FAQ_20260624_*` 接頭辞を使用。
- ユーザー追加/削除は実施していない。

# 販売設定・CRM・外部連携 作成操作確認 2026-06-24

| status | count |
|:--|--:|
| saved_or_detail | 7 |
| validation_or_error | 7 |
| unknown_after_save | 2 |


詳細は上記出力ファイルを参照。

## 追加: 三者突合の確定結果と修正 2026-06-24（Agent 3 / 要件再導出）

### 三者突合表

実機で `not_found / app_error / todo` だったURLを、FAQ/25分類の本文参照と機械突合した。

- 出力: `_analysis/full-live-operation-2026-06-24/tri-consistency-live-ng-vs-docs.md`
- 突合ヒット: 10件（プレースホルダURLは除外）

各ヒットについて、FAQ/分類側が「実機の状態を正しく記述しているか」を本文確認した結果:

| 実機状態 | URL | 文書側の扱い | 判定 |
|:--|:--|:--|:--|
| app_error | `/admin/draft_orders/create` | `予期せぬエラー`と既知記述 | 一致(OK) |
| not_found | `/admin/order_returns/create` | 404と既知記述 | 一致(OK) |
| not_found | `/admin/pdf_export/pdf_export_operation_packing_slips/create` | 存在しないと既知記述 | 一致(OK) |
| app_error | `/admin/purchasing_customers/create` | 予期せぬエラーと既知記述 | 一致(OK) |
| not_found | `/admin/sale_change_line_items/create` | 存在しないと既知記述 | 一致(OK) |
| todo | `/admin/analytics` `/admin/analytics/revenue` `/admin/analytics/reports` | TODO/未実装と既知記述 | 一致(OK) |
| todo | `/admin/b2b` | 未実装/将来機能と既知記述 | 一致(OK) |
| not_found | `/admin/settings/metafield_definitions/create` | **作成フォーム=確定**と誤記 | **不一致(要修正)** |

### 確定不一致の是正: メタフィールド定義の作成URL

- 実機(2026-06-24)再確認:
  - `/admin/settings/metafield_definitions` は一覧。対象オブジェクト(組織/ロケーション/会社/仕入れ先ベンダー/商品/バリエーション/顧客/注文/下書き注文/ディスカウント/在庫移動伝票/在庫調整伝票/在庫取置伝票/発注伝票/入荷指示/出荷指示)を選び「定義を追加する」。
  - 実際の作成URLは対象別: `/admin/settings/metafield_definitions/organization/create`（見出し「組織メタフィールドの定義を追加する」）。
  - `/admin/settings/metafield_definitions/create`（オブジェクト指定なし）は「このページは存在しないようです」。
- 是正: `04-notion/08-カスタムデータ.md` の作成URL・手順・確認状態(4箇所)を、対象オブジェクト別URLに修正済み。
- 横断確認: 誤URL `metafield_definitions/create` は `08-カスタムデータ.md` のみに存在。他(`01-by-feature/設定.md`, `_support/screens.md`)は一覧URLで実在のため修正不要。

### テストデータ後片付け（削除導線の実機確認も兼ねる）

- 商品: 詳細「その他の操作」に `商品をアーカイブする` / `商品を削除する` を確認。`TEST_FAQ_20260624 GU検証Tシャツ 092214` を削除完了。
- カタログ: 詳細「その他の操作 > カタログを削除する」で `TEST_FAQ_20260624_カタログ_092214` を削除完了。
- 残存(削除導線が詳細/一覧に無い、または未片付け): 翻訳ルール・採寸ルール・販売価格/予約販売/販売閾値/誕生日ポイント/会員ランク等のテストルール、取引先/ブランド/決済方法/ロケーション、伝票(`#IA-1012`/`#IM-1024`/`#IO-1024`/`#II-1024`)。これらは `created-test-data-inventory.md` を参照。

### 残課題（goal未完。次に必要な作業）

1. 残テストデータの削除可否を機能ごとに実機確認し、削除できるものは片付ける。
2. `SQ-FAQ.html` を現行 `build_help.py` 出力で再生成するか方針決定（現行は旧「多軸ビュー」、再生成は「ヘルプセンター」で別物）。
3. CSV/PDFの実出力（メール/ダウンロード）挙動の実機確認。
4. `04-notion` リンク切れ16件の実修正（`notion-broken-link-fix-candidates.md` の候補を適用）。

## 追加修正: 04-notion内リンク切れ16件の解消 2026-06-24

`notion-broken-link-fix-candidates.md` の候補に基づき、`04-notion` 内の存在しないMarkdownリンク16件を修正した。

修正後の検証:

```text
BROKEN_04_NOTION_MD_LINKS 0
```

主な修正例:

- `03-設定・マスタ.md` → `03-組織・通知.md`
- `05-商品管理.md` → `05-商品・SKU.md`
- `10-商品とバリエーション.md` → `10-価格・販売制御.md`
- `18-注文・カート.md` → `18-店舗業務・リテールポータル.md`
- `22-外部連携.md` → `22-API・Webhook・開発者連携.md`

これにより、25分類内の「次のエリア」系リンクは実ファイルに解決する状態になった。

## 追加: CSV/PDF実出力導線の実機操作 2026-06-24

### 商品バリエーションCSVエクスポート

- URL: `/admin/csv_export/csv_export_operation_product_variants/create`
- 実操作:
  - フォームを開く
  - `エクスポートを開始する` を押下
- 結果:
  - 一覧 `/admin/csv_export/csv_export_operation_product_variants` へ遷移
  - 通知: `エクスポートを開始しました`
  - 一覧に `2026年06月24日 10:19` / `実行中` / `商品情報 含めない` / `ダウンロード` が一時表示
- 注意:
  - 約10秒後の再読込では一覧が空表示になった。完了後の保持/表示条件/ダウンロード可否は追加確認対象。

### ヤマトB2クラウドCSV + 納品書PDF同梱

- URL: `/admin/inventory_outbound_orders/export/yamato_b2_cloud`
- 実操作:
  - `CSVの出力後に出荷指示のステータスを出荷作業中に変更する` はOFFのまま
  - 初回は `開始日時を入力してください` バリデーション確認
  - `開始日時=2026-01-01T00:00` を入力して `実行する` を押下
- 結果:
  - 出荷管理一覧へ遷移
  - 通知: `ヤマトB2クラウドのエクスポートを開始しました`
  - フォーム上の出力物表示は `ヤマトB2クラウド取り込み用CSV` と `同梱する納品書PDF`
- FAQ/分類への影響:
  - `PDFエクスポート` 単体の `/admin/pdf_export/pdf_export_operation_packing_slips/create` は存在しない一方、ヤマトB2条件指定エクスポートでは納品書PDFが同梱出力物として扱われる、という既存記述は実機と一致。

## 追加修正: 04-notion次エリア表示ラベルの整合 2026-06-24

リンク先だけでなく、本文に残っていた `次エリア名` 表示ラベルも実ファイル名に合わせて修正した。

修正後の検証:

```text
remaining 次エリア label refs: 0
BROKEN_04_NOTION_MD_LINKS 0
```

修正例:

- `[20-次エリア名.md]` → `[20. 物流・返品・外部アプリ連携]`
- `[16. 次エリア名]` → `[16. 顧客・会社]`
- `[08-次エリア名.md]` → `[08. カスタムデータ]`
- `[09-次エリア名.md]` → `[09. 翻訳・採寸]`
- `[17-次エリア名.md]` → `[17. CRM]`

## 追加修正: HTML成果物再生成 2026-06-24

`SQ-FAQ.html` が現行 `build_help.py` の出力と不一致だったため、HTML成果物を現行ソースから再生成した。

実行:

```text
python3 build_help.py
python3 build_guide.py
python3 build_support.py
python3 build_graph.py
```

結果:

| HTML | title | bytes |
|:--|:--|--:|
| `SQ-FAQ.html` | `SQ ヘルプセンター` | 1,893,976 |
| `SQ完全ガイド.html` | `SQ完全ガイド — ゼロから理解する指南書` | 246,274 |
| `SQ-サポートデスク.html` | `SQ サポートデスク（逆引き）` | 176,891 |
| `SQ-データ相関図.html` | `SQ データ相関図` | 25,861 |

これにより、`SQ-FAQ.html` は旧 `SQ FAQ（多軸ビュー）` ではなく、現行 `build_help.py` の `SQ ヘルプセンター` 出力に更新された。

## 継続実行: 2026-06-24 10:23-10:35

### 実機で追加確認したこと

- browser-useで起動済みのChrome（CDP `56189`）へ接続し、SQ stagingを実機操作した。
- 商品バリエーションCSVエクスポート一覧（`/admin/csv_export/csv_export_operation_product_variants`）を再確認し、前回一時的に消えたジョブが `成功 / 完了 / ダウンロード` として表示されることを確認した。
- 会社作成（`/admin/companies/create`）を再検証し、担当者を選択せずに会社＋会社ロケーションのみで保存成功した。
  - 作成会社: `TEST_FAQ_20260624_COMPANY_102911`
  - 作成後URL: `/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company`
  - GraphQL `companyCreate` 成功レスポンスを確認。
  - 郵便番号は `100-0001` のようなハイフン付き形式が必要。ハイフンなし/項目ずれでは `postalCodeは郵便番号の形式で入力してください` が返る。
- 会社詳細・会社一覧の対象行選択後とも、削除/アーカイブ導線は確認できなかった。

### 残テストデータ片付け

UI上で対象行を完全一致選択し、以下を削除した。

| データ | 結果 |
|:--|:--|
| `TEST_FAQ_20260624_ブランド_092214` | 削除済み |
| `TEST_FAQ_20260624_決済_092214` | 削除済み |
| `TEST_FAQ_20260624_TRANSLATION_CRUD_093701` | 削除済み。翻訳ルール一覧のアプリエラーは再現せず |
| `TEST_FAQ_20260624_取引先_092214` | 削除済み（一覧の `アーカイブする` 押下後、確認ダイアログは「取引先を削除しますか？」で表示） |

残存/未片付け:

| データ | 理由 |
|:--|:--|
| `TEST_FAQ_20260624_COMPANY_102911` / `TEST_FAQ_20260624_COMPANY_LOC_102911` | 作成成功したが、会社詳細/一覧で削除・アーカイブ導線なし |
| `TEST_FAQ_20260624_MEASURE_CRUD_093821` | 採寸ルール一覧/詳細で削除導線未確認 |
| `TEST_FAQ_20260624_GU倉庫_ON_092214` / `TEST_FAQ_20260624_GU店舗_OFF_092214` | 一覧に表示あり。対象行チェックボックスを自動操作で取得できず、削除/アーカイブ未実行 |
| `TEST_FAQ_20260624_Recustomer_100908` | 削除済み。行選択後の `アクション` → `接続を削除する` → 確認ダイアログ `削除する` で削除できることを実機確認 |
| `#IA-1012` / `#IM-1024` / `#IO-1024` / `#II-1024` | 伝票実行済みデータ。削除導線未確認。履歴として残存 |

詳細ログ:

- `_analysis/full-live-operation-2026-06-24/continued-live-check/summary.md`
- `_analysis/full-live-operation-2026-06-24/continued-live-check/company-crud-finish4.json`
- `_analysis/full-live-operation-2026-06-24/continued-live-check/cleanup-execute-results.md`
- `_analysis/full-live-operation-2026-06-24/continued-live-check/cleanup-probe-results.md`

### 分類修正

#### カタログ・出品範囲

実機上、`/admin/catalogs/create` で設定できるのはタイトルのみで、カタログ単体に出品範囲/同期範囲の設定項目はない。出品範囲は各チャネル連携側のフォームでカタログを選ぶことで決まる。

対応:

- `04-notion/06-カタログ・出品範囲.md` を `04-notion/06-カタログ.md` に変更。
- 06はカタログ=商品グルーピングに純化。
- `04-notion/19-標準販売チャネル連携.md` に「出品範囲・同期範囲の考え方」を追加。
- 既存リンクを新ファイル名へ更新。

#### 翻訳・採寸

翻訳と採寸は、実機上で別URL・別データ・別CRUDだった。

- 翻訳: `/admin/settings/translation`
- 採寸: `/admin/settings/product_measurement_rules`

対応:

- `04-notion/09-翻訳・採寸.md` を `04-notion/09-翻訳.md` に変更。
- `04-notion/09b-採寸.md` を追加。
- 25分類全体の番号は崩さず、採寸は枝番 `09b` として扱う。

### 再生成・静的検証

実行:

```bash
cd faq
python3 build_help.py
python3 build_guide.py
python3 build_support.py
python3 build_graph.py
```

結果:

| ファイル | title |
|:--|:--|
| `SQ-FAQ.html` | `SQ ヘルプセンター` |
| `SQ完全ガイド.html` | `SQ完全ガイド — ゼロから理解する指南書` |
| `SQ-サポートデスク.html` | `SQ サポートデスク（逆引き）` |
| `SQ-データ相関図.html` | `SQ データ相関図` |

追加検証:

- `BROKEN_04_NOTION_MD_LINKS 0`
- `04-notion.zip` を再作成。Markdown 26件（25分類 + `09b` 枝番）。
- 現行成果物内に旧frontmatter title `06. カタログ・出品範囲` / `09. 翻訳・採寸` は残存なし。

### 現時点の判断

- カタログ/出品範囲は分類を増やさず、06と19に責務分離するのが実機仕様に合う。
- 翻訳/採寸は分けるのが妥当。採寸を `09b` とすることで、既存25分類を大きく崩さずNotion投入時の検索性も上がる。
- 会社作成は保存成功まで確認できたため、16. 顧客・会社のFAQ側にも「郵便番号形式」「担当者なしで作成可能」「削除導線未確認」を反映候補にする。

## 継続実行2: 2026-06-24（独立再検証・HTML側ソース整合）

### 三者整合の構造を再確認（重要）

HTMLビルド（`build_help.py` / `build_guide.py` / `build_support.py` / `build_graph.py`）は **`04-notion/`（25分類）を入力にしていない**。HTML成果物のソースは次のとおり。

- `build_help.py`: `00-getting-started` / `01-by-feature` / `02-by-task` / `03-faq`
- `build_guide.py`: `00-getting-started/SQ完全ガイド.md`
- `build_support.py`: `_support/` + 上記4ディレクトリ
- `build_graph.py`: `00-getting-started` のデータ事典

したがって「三者整合」とは、**同一の実機事実を (A) HTML側ソース と (B) 25分類(04-notion) の双方に反映できているか**を意味する。前回の継続実行は (B) のみ修正していたため、(A) 側に未反映の実機事実が残っていた。

### HTML側ソースへ反映した実機事実

- `faq/01-by-feature/会社.md`
  - 郵便番号バリデーション文言に「`100-0001` のようなハイフン付き7桁。不正形式では `postalCodeは郵便番号の形式で入力してください`」を追記。
  - 「担当者を選択せず会社＋会社ロケーションのみで作成成功（GraphQL `companyCreate` 成功）、削除/アーカイブ導線なし」を追記。
- `faq/02-by-task/会社（法人顧客）を登録する.md`
  - 郵便番号バリデーション文言に同上のハイフン付き形式を追記。
- HTML再生成済み。`SQ-FAQ.html` に「ハイフン付き7桁」「担当者を選択せず」反映を確認。

### 実機で新たに確定した事実

- **ロケーションは削除ではなくアーカイブ**: ロケーション詳細画面に `アーカイブする` ボタンがあり、`TEST_FAQ_20260624_GU倉庫_ON_092214` / `TEST_FAQ_20260624_GU店舗_OFF_092214` をアーカイブ完了（通知「ロケーションをアーカイブしました」）。`アーカイブを解除する` で復帰可能。アーカイブ済み行はデフォルト一覧にも「アーカイブ済み」ラベル付きで残る。
- **採寸ルールは削除導線が存在しない（確定）**: 詳細画面（`/admin/settings/product_measurement_rules/{id}`）にはボタンが一切無く（保存・編集・削除いずれも無し）、一覧側にも行チェックボックスが無い。`TEST_FAQ_20260624_MEASURE_CRUD_093821` は削除不可で残存。
- **Recustomer接続テストデータは削除可能（追加再検証で訂正）**: 一覧の行チェックボックスを選択すると上部に `アクション` が表示され、`接続を削除する` → 確認ダイアログ `削除する` で削除できる。`TEST_FAQ_20260624_Recustomer_100908` はこの手順で削除済み。
- **調整伝票 `#IA-1012` の「増減数0」問題の真因**: 詳細画面は「予期せぬエラーが発生しました／該当するProductVariantが見つかりませんでした」を表示。これは伝票自体のデータ破損ではなく、**伝票が参照していたテスト商品/SKUが既に削除されたため、詳細画面でバリエーションを解決できずエラーになっている**もの。詳細に `再実行` ボタンあり。前回観測の「増減数=2が0に見えた」は、この参照先SKU欠落に起因する表示異常と判断。

### 残存テストデータ（最終）

| データ | 片付け | 理由 |
|:--|:--|:--|
| `TEST_FAQ_20260624_GU倉庫_ON_092214` | アーカイブ済み | ロケーションは削除不可・アーカイブのみ |
| `TEST_FAQ_20260624_GU店舗_OFF_092214` | アーカイブ済み | 同上 |
| `TEST_FAQ_20260624_MEASURE_CRUD_093821` | 残存 | 採寸ルールは削除導線なし（確定） |
| `TEST_FAQ_20260624_Recustomer_100908` | 削除済み | 行選択後の `アクション` → `接続を削除する` で削除可能 |
| `TEST_FAQ_20260624_COMPANY_102911` / `_LOC_102911` | 残存 | 会社は削除/アーカイブ導線なし |
| `#IA-1012` / `#IM-1024` / `#IO-1024` / `#II-1024` | 残存 | 伝票は削除導線なし（履歴として残る）。`#IA-1012` は参照SKU欠落でエラー表示 |

ログ:
- `_analysis/full-live-operation-2026-06-24/continued-live-check/location-archive-results.json`

## 継続実行3: 2026-06-24（ロケーション/採寸のHTML・25分類追加整合）

### 追加修正

前回までの実機確認結果を再点検したところ、25分類側には反映済みでも、HTML側ソースへ未反映の実機事実が残っていたため追加修正した。

#### ロケーション（設定 > ロケーション）

実機で `TEST_FAQ_20260624_GU倉庫_ON_092214` / `TEST_FAQ_20260624_GU店舗_OFF_092214` を詳細画面からアーカイブ実行。

確認できた事実:

- 詳細画面に `アーカイブする` ボタンあり
- 実行後通知: `ロケーションをアーカイブしました`
- 詳細画面表示: `このロケーションはアーカイブされています。アーカイブされたロケーションは管理画面やストアフロントからも非表示となります。`
- `アーカイブを解除する` で復帰可能
- 削除ボタンは確認できず、削除ではなくアーカイブで片付ける

反映先:

- `faq/01-by-feature/設定.md`
- `faq/02-by-task/初期設定の手順.md`
- `faq/04-notion/04-基本マスタ.md`
- `faq/00-getting-started/データ事典①-設定で作るデータ.md`
- `faq/_support/constraints.md`
- `faq/_support/statuses.md`

#### 採寸ルール

実機で採寸ルール詳細/一覧を再確認し、削除/編集導線なしを確定扱いに統一。

反映先:

- `faq/04-notion/09b-採寸.md`
- `faq/01-by-feature/設定.md`
- `faq/02-by-task/カスタムデータを設定する.md`
- `faq/00-getting-started/データ事典①-設定で作るデータ.md`
- `faq/00-getting-started/SQ完全ガイド.md`
- `faq/_support/constraints.md`

### 再生成・検証

実行:

```bash
cd faq
python3 build_help.py
python3 build_guide.py
python3 build_support.py
python3 build_graph.py
```

検証結果:

- `BROKEN_04_NOTION_MD_LINKS 0`
- `04-notion.zip` 再作成済み（Markdown 26件、`09b-採寸.md` 含む）
- `SQ-FAQ.html` にロケーションアーカイブ文言（`このロケーションはアーカイブされています`）反映
- `SQ-FAQ.html` に採寸ルール削除/編集導線なし反映
- `SQ完全ガイド.html` に採寸ルール削除/編集導線なし反映
- `SQ-サポートデスク.html` にロケーションアーカイブ制約・採寸ルール削除/編集導線なし制約反映

## 継続実行4: 2026-06-24（批判的レビュー・独立再検証）

前段の修正を鵜呑みにせず、現在の成果物・実機を独立に検証した。

### 独立検証で確認できたこと（合格）

- `BROKEN_04_NOTION_MD_LINKS 0`、旧分類名（`06-カタログ・出品範囲` / `09-翻訳・採寸`）残存なし。
- 実機でnot_found/app_errorになる主要URLは、FAQ/HTML/25分類が正しく「404/エラー」と記載済みであることをクロスチェックで確認。
  - `/admin/order_returns/create`、`/admin/sale_change_line_items/create`、`/admin/settings/metafield_definitions/create`、`/admin/pdf_export/pdf_export_operation_packing_slips/create`、`/admin/draft_orders/create`、`/admin/purchasing_customers/create` はいずれも複数ドキュメントで正しく明文化済み。
  - FAQが「存在する」と過剰主張しているURLは検出されなかった。
- ロケーションのアーカイブ、採寸の削除導線なし、郵便番号ハイフン形式、会社の担当者なし作成は、最終HTML成果物（SQ-FAQ/ガイド/サポート）に反映済みであることを再レンダリング後に実証。

### 独立検証で見つけた未整合（今回修正）

1. `09b-採寸.md` の本文に「削除ボタンは確認できませんでした」という未確認的トーンが残っていた → 「削除/編集ボタンは存在しません（導線なし確定）」に統一。確認状態テーブルの「✅ 確定（導線なし）」と表現を一致させた。
2. **Recustomer接続済みデータの削除導線**は追加再検証で訂正。登録行を選択すると上部に `アクション` が出て、`接続を削除する` → 確認ダイアログ `削除する` で削除できる。古い「削除導線なし」の記述は以下へ反映し直した:
   - `faq/04-notion/20-物流・返品・外部アプリ連携.md`
   - `faq/02-by-task/ロジザード・Recustomerを接続する.md`
   - `faq/_support/constraints.md`

### 全ページスキャン問題23件の判定

- `not_found` のCSV/PDF系の多くは、スキャンが機械生成した推測URL（実機メニューに存在しないカテゴリ）であり、FAQが言及しないのは正当（過剰主張なし）。
- `/admin/b2b/create` は refs 0 だが、卸売(b2b)自体がTODOと既述のため、派生の作成URL not_found は仕様通りで追加対応不要。
- `todo`（analytics/revenue/reports/b2b/apps admin_api）は24.未実装・将来機能および各FAQで既述。
- 結論: 23件はすべて「既知・記載済み」または「正当なnot_found」で、三者間の新たな矛盾は検出されなかった。

### 再生成・最終検証

- HTML4種を再生成、`04-notion.zip` 再作成（Markdown26件、09b含む）。
- `BROKEN_04_NOTION_MD_LINKS 0`。
- 新規Recustomer記述が `SQ-FAQ.html` / `SQ-サポートデスク.html` に反映済みを確認。
- 4HTMLのtitle健全性を再確認。

## 継続実行5: 2026-06-24（調整伝票の参照先SKU削除エラーを反映）

### 背景

前回までの実機確認で、調整伝票 `#IA-1012` の詳細画面が以下を表示することを確認していた。

- `予期せぬエラーが発生しました`
- `該当するProductVariantが見つかりませんでした。`

これは、調整伝票が参照していたテスト商品/SKUを後から削除したため、伝票履歴が参照先ProductVariantを解決できなくなった表示エラーと判断した。伝票自体の破損ではなく、参照先削除後の履歴表示エラーとして扱う。

### 反映先

HTML側ソース:

- `faq/01-by-feature/調整伝票.md`
- `faq/02-by-task/在庫を調整する.md`

25分類:

- `faq/04-notion/12-在庫伝票.md`

サポート台帳:

- `faq/_support/symptoms.md`
- `faq/_support/constraints.md`

### 追記した案内方針

- 調整伝票詳細で `該当するProductVariantが見つかりませんでした` と表示される場合、その伝票が参照していたSKUが後から削除されている可能性がある。
- 実行済み伝票自体は編集・削除できない。
- 在庫補正が必要な場合は、新しい調整伝票で逆向きに補正する。

### 再生成・検証

- HTML4種を再生成。
- `04-notion.zip` 再作成。
- `BROKEN_04_NOTION_MD_LINKS 0`。
- `SQ-FAQ.html` に `該当するProductVariantが見つかりませんでした` が反映済み。
- `SQ-サポートデスク.html` に対応症状・制約が反映済み。
- `04-notion/12-在庫伝票.md` に同実機事実が反映済み。

## 継続実行6: 2026-06-24（メタデータ整合・独立再検証）

前段の修正を独立に再検証し、本文に2026-06-24の実機追記があるのに frontmatter の `last_verified` が古いままになっていたファイルを是正した。

### 検証で確認できたこと

- 調整伝票の参照先SKU削除エラー（`該当するProductVariantが見つかりませんでした`）は、対象7ファイル（FAQ本文3＋サポート2＋HTML2系統）に実在することを実ファイルで確認。
- `BROKEN_04_NOTION_MD_LINKS 0`。
- 今回までの実機事実8項目（ProductVariantエラー / ロケーションアーカイブ / 採寸削除導線なし / Recustomer削除導線あり（不可逆削除） / 郵便番号ハイフン形式 / 会社担当者なし作成 ほか）が、SQ-FAQ.html・SQ完全ガイド.html・SQ-サポートデスク.html に揃って反映済みであることを再レンダリング後に実証。

### メタデータ是正（last_verified を 2026-06-24 に更新）

本文へ2026-06-24の実機事実を追記済みなのに更新漏れだったファイル:

- `faq/04-notion/04-基本マスタ.md`
- `faq/04-notion/12-在庫伝票.md`
- `faq/01-by-feature/調整伝票.md`
- `faq/01-by-feature/設定.md`
- `faq/02-by-task/在庫を調整する.md`
- `faq/01-by-feature/会社.md`
- `faq/02-by-task/初期設定の手順.md`
- `faq/02-by-task/カスタムデータを設定する.md`
- `faq/02-by-task/ロジザード・Recustomerを接続する.md`

### 25分類の棚卸し現況（wbs_status）

| 状態 | エリア |
|:--|:--|
| 完成寄り | 01,02,03,04,05,06,07,08,09,09b,11,12,22 |
| 完成寄り＋要確認/一部確認 | 10,17,21 |
| 一部確認 | 13,14,18 |
| 一部確認＋連携待ち | 15,16 |
| 連携待ち | 19,20 |
| TODO表示 | 23,24 |
| 資料由来 | 25 |

「連携待ち」「TODO表示」は、外部接続前提・未実装が理由であり、staging単体では検証不能。これらは三者整合上「実機未確認」と明示済みで、現時点の到達可能範囲としては整合済み。

### 再生成・検証

- HTML4種を再生成、`04-notion.zip` 再作成（Markdown26件、09b含む）。
- `BROKEN_04_NOTION_MD_LINKS 0`、4HTMLのtitle健全。

## 継続実行7: 2026-06-24（発注・仕入 #IP-1005 追加実機検証）

### 実機操作

新規に発注伝票 `#IP-1005` を作成し、下書き → 発注済み → キャンセル済みまで実操作した。

- URL: `/admin/inventory_purchase_orders/4595e603-f142-5345-9047-1ef968b0d047_InventoryPurchaseOrder`
- 取引先: `TEST_FAQ_Supplier`
- テナント: `ユニクロ`
- 対象SKU: `486125-31-XL`
- 明細: 単価100円 / 数量1 / 税率10%
- 下書き作成後: `#IP-1005`、ステータス `注意 / 下書き`
- 発注確認ダイアログ文言: `発注を行うと入荷指示が作成されます。発注後は伝票の編集ができません。`
- 発注後: ステータス `情報 / 発注済み`、通知 `発注伝票を発注しました`
- キャンセル確認ダイアログ文言: `発注伝票をキャンセルします。この処理は巻き戻すことができません。`
- キャンセル後: ステータス `キャンセル済み`、通知 `発注伝票をキャンセルしました`

### 追加で確定したこと

- 発注後0秒/5秒/15秒のいずれも、入荷管理一覧は0件のまま。
- `#IP-1005` 起点の入荷指示は入荷管理一覧に表示されなかった。
- 対象SKU `486125-31-XL` の在庫詳細は今回の在庫一覧フィルタでは特定できず、`#IP-1005` に関するSKU入荷予定列は直接未確認。したがって、`#IP-1005` については「入荷管理一覧に反映なし」までを実証範囲とする。
- 明細金額は単価100円・数量1・税率10%で `￥110` と表示された。少なくともこの条件では、発注伝票の明細金額は税率込みで計算される。

### 反映先

- `faq/01-by-feature/発注管理.md`
- `faq/04-notion/14-発注・仕入.md`
- `faq/00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md`
- `faq/00-getting-started/SQ完全ガイド.md`
- `faq/_support/constraints.md`
- `faq/_support/statuses.md`
- `faq/_support/symptoms.md`

### 修正した注意点

一時的に `#IP-1005` でもSKU入荷予定増加なしと読める表現が混入したが、これは過剰断定だったため修正した。現在は次のように切り分けている。

- `#IP-1000`〜`#IP-1004`: 入荷管理一覧への表示なし、SKU入荷予定増加なし。
- `#IP-1005`: 入荷管理一覧への表示なし（発注後0秒/5秒/15秒）。対象SKU詳細は今回未特定。

### 再生成・検証

- HTML4種再生成。
- `04-notion.zip` 再作成。
- `BROKEN_04_NOTION_MD_LINKS 0`。
- `SQ-FAQ.html` / `SQ完全ガイド.html` / `SQ-サポートデスク.html` に `#IP-1005` 反映済み。
- `SQ-FAQ.html` に `単価100円・数量1・税率10%` / `￥110` 反映済み。

## 継続実行8: 2026-06-24（発注・仕入 #IP-1006 精密検証）

### 背景

`#IP-1005` では、発注後0秒/5秒/15秒の入荷管理一覧が0件であることは確認できたが、対象SKU `486125-31-XL` の在庫詳細（入荷予定列）をUIで特定できず、入荷予定については直接証拠が弱かった。

### 追加実機操作

再度、新規発注伝票 `#IP-1006` を作成し、下書き → 発注済み → キャンセル済みまで操作した。

- URL: `/admin/inventory_purchase_orders/9b79a9be-c75e-5bcd-8830-1500f12f1d1e_InventoryPurchaseOrder`
- 対象SKU: `486125-31-XL`
- 明細: 単価100円 / 数量1 / 税率10% / 金額 `￥110`
- 発注後、キャンセル前に認証済みブラウザ上のGraphQLで `InventoryItemsPage` を使い、全18ロケーションの対象SKU在庫を取得。
- 結果: 対象SKU `486125-31-XL` の全18ロケーション `incoming` 合計は `0`。
- 発注後・キャンセル前の入荷管理一覧も0件で、`#IP-1006` / 対象SKUは表示されなかった。
- 後片付けとして `#IP-1006` はキャンセル済みにした。

ログ:

- `_analysis/full-live-operation-2026-06-24/purchase-recheck/issue-graphql-precise-log.json`

### 結論の精密化

現在の正しい切り分け:

- `#IP-1000`〜`#IP-1004`: 入荷管理一覧への表示なし、SKU入荷予定増加なし。
- `#IP-1005`: 入荷管理一覧への表示なし（発注後0秒/5秒/15秒）。対象SKU詳細は当時未特定。
- `#IP-1006`: 入荷管理一覧への表示なし。対象SKU `486125-31-XL` の全18ロケーション `incoming` 合計0を発注後・キャンセル前に確認。

これにより、発注ダイアログの「入荷指示が作成されます」という文言に対して、少なくとも現在のstaging環境では発注ステータスが入荷管理・入荷予定へ直接反映されないことを、より強い証拠で確認した。

### 反映先

- `faq/01-by-feature/発注管理.md`
- `faq/04-notion/14-発注・仕入.md`
- `faq/00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md`
- `faq/00-getting-started/SQ完全ガイド.md`
- `faq/_support/constraints.md`
- `faq/_support/statuses.md`
- `faq/_support/symptoms.md`

### 再生成・検証

- HTML4種再生成。
- `04-notion.zip` 再作成。
- `BROKEN_04_NOTION_MD_LINKS 0`。
- `SQ-FAQ.html` / `SQ完全ガイド.html` / `SQ-サポートデスク.html` に `#IP-1006` 反映済み。
- `SQ-FAQ.html` に `全18ロケーション` / `incoming` / `単価100円・数量1・税率10%` / `￥110` 反映済み。


## 追加再検証: 高優先エリア 13/18/19/20/21（2026-06-24 11:14-）

### 未解決grep: 税抜き金額

`税抜き金額` / `税込み計算ではありません` / `単価 × 数量 を表示` / `一次記録間で差異` を `00-getting-started` / `01-by-feature` / `02-by-task` / `04-notion` / `_support` で再検索しました。ヒットは会員ランクの「税抜き価格でランクを算出する」文脈のみで、発注伝票の古い税抜き断定は残っていません。

### 実機再確認ログ

- 出力先: `_analysis/full-live-operation-2026-06-24/priority-live-recheck-111407/`
- `13. 入出荷・在庫依頼`: 在庫依頼/確保済み/出荷管理/入荷管理を再表示。出荷管理ではタブ（保留中・出荷待ち・依頼済み・作業中・欠品・要対応・出荷完了）と、`インポート`（ヤマトB2クラウド（出荷実績）/ DHL（出荷実績））、`条件指定でエクスポート`（ヤマトB2クラウドのみ）を確認。
- `18. 店舗業務・リテールポータル`: `/admin/retail_portal_integrations/create` と `/admin/local_pickup_retail_location_rules/create` を再表示。店舗ロケーション・在庫ロケーション・テナント・カタログ・販売閾値ルール・許可チェックボックス、店舗受取のロケーション選択を確認。
- `19. 標準販売チャネル連携`: Shopify / OmnibusCore / スマレジの作成フォームを再表示。カタログ/ロケーショングループがチャネル側フォームで扱われることを再確認。
- `20. 物流・返品・外部アプリ連携`: ロジザード作成フォームを再表示し、`Partner APIエンドポイントを使用する` と `AuthKeyの発行をスキップする` を追加確認。Recustomerは行選択後に `アクション` → `接続を削除する` が表示され、確認ダイアログ `削除する` で `TEST_FAQ_20260624_Recustomer_100908` を削除できることを確認。
- `21. CSV/PDF・データ移行`: CSVインポート/CSVエクスポート/PDFエクスポートを再表示。ヤマトB2インポート作成フォームは `CSVファイル` のアップロードと `保存する`、在庫CSVエクスポートは `ロケーション` 選択と `エクスポートを開始する`、PDF納品書 `/create` は引き続き `このページは存在しないようです` を確認。

### 追加修正

- `02-by-task/ロジザード・Recustomerを接続する.md`
- `04-notion/20-物流・返品・外部アプリ連携.md`
- `_support/constraints.md`
- `_analysis/full-live-operation-2026-06-24/created-test-data-inventory.md`



## 追加再検証: 低カバレッジ分類 02/03/22/23/24（2026-06-24）

- 出力先: `faq/_analysis/full-live-operation-2026-06-24/low-coverage-live-recheck-112815/`
- 02. アカウント・権限: 権限グループ作成フォームで全権限OFFのまま保存し、`権限を選択してください` を確認。`users:read` を1件選択して `TEST_FAQ_20260624_PERMISSION_112959` を作成し、一覧の `権限グループを削除` → 確認ダイアログ `削除する` で削除済み。ユーザー追加/削除は未実行。
- 03. 組織・通知: 通知用メールアドレス作成フォームで空/誤入力バリデーションを確認後、`test+faq-113425@example.com` を作成。対象行を選択し `削除する` → 確認ダイアログ `削除する` で削除済み。テナント削除は未確認のまま。
- 22. API・Webhook・開発者連携: `TEST_FAQ_20260624_APP_113636` を作成し、Admin APIのアクセストークン/シークレット、Playground、リクエストログ、Storefront API、Webhook導線を確認。トークン/シークレット値は出力せず状態ログはマスク済み。Webhook未入力保存で `イベントを選択してください` / `エンドポイントを入力してください` を確認。アプリ削除導線は詳細・一覧とも未確認のため、テストアプリは残存。
- 23. 会計・売上実績・分析: 売上実績一覧の `エクスポート` メニューで `注文軸` / `明細軸` を確認。各CSVエクスポート作成画面で `テナント` / `開始日時` / `終了日時` / `エクスポートを開始する` を確認。`/admin/sale_change_line_items/create` は存在しないページのまま。
- 24. 未実装・将来機能: `/admin/analytics` / `/admin/analytics/revenue` / `/admin/analytics/reports` / `/admin/b2b` を再表示し、TODO表示を確認。

### 今回の反映

- `04-notion/02-アカウント・権限.md` / `02-by-task/権限グループを作成する.md`: 権限未選択保存不可を追記。
- `04-notion/03-組織・通知.md` / `02-by-task/その他のマスタを登録する.md`: 通知用メールアドレス削除手順を追記。
- `04-notion/22-API・Webhook・開発者連携.md` / `_support/constraints.md`: APIアプリ削除導線未確認、Webhook未入力バリデーション、秘密値非出力を追記。


## スコープ更新: 連携系は実接続検証対象外（2026-06-24）

ユーザー方針により、Shopify / OmnibusCore / スマレジ / リテールポータル / ロジザードZERO / Recustomer など、外部接続が必要な同期・実データ反映は検証対象外とする。以後の完了判定では、連携系については以下のみを確認対象にする。

- 管理画面のページ存在・見出し
- 未接続状態の表示
- 作成フォームの項目・必須/任意・バリデーション
- FAQ上で「実接続後の同期挙動は対象外/未検証」と明記されていること

この方針により、`連携待ち` は未完了タスクではなく、実接続環境がないための対象外領域として扱う。

## 追加再検証: 非連携領域 10/11/15/17/21/23/24（2026-06-24）

- 出力先: `_analysis/full-live-operation-2026-06-24/non-integration-recheck-142927/`
- 10. 価格・販売制御: 販売価格/予約販売/販売上限/販売閾値の一覧・作成フォームを再表示。販売上限はチャネル選択が必要だが、実接続は対象外。
- 11. 在庫状態・在庫数: 在庫一覧を再表示。追加のCRUDは今回なし。
- 15. 注文・返品: 注文一覧は0件、`/admin/orders/create` と `/admin/draft_orders/create` は `予期せぬエラーが発生しました`、`/admin/order_returns/create` は `このページは存在しないようです` を再確認。
- 17. CRM: ディスカウント/注文ポイント/会員ランクの一覧・作成フォームを再表示。実注文への反映は連携/注文データ前提のため対象外。
- 21. CSV/PDF: CSVインポート/CSVエクスポート/PDFエクスポートのトップを再表示。
- 23/24. 会計・分析・未実装: 売上実績一覧・分析/収益/レポート/卸売TODO表示を再確認。


## 追加再検証: テナント削除導線・メタフィールド定義導線（2026-06-24）

- 出力先: `_analysis/full-live-operation-2026-06-24/targeted-live-recheck-170024/`
- テナント: `TEST_FAQ_20260624_TENANT_170037` を作成。詳細画面には `テナントIDをコピーする` と `保存する` のみ、一覧にも行選択/削除アクションなし。管理画面UIからの削除導線は確認できず、テストテナントは残存。
- メタフィールド定義: `/admin/settings/metafield_definitions/create` は存在しないページ。正しい導線は `/admin/settings/metafield_definitions` の `定義を追加する`。作成フォームで `名前` / `説明` / `ネームスペース` / `キー` / `メタフィールドのタイプ` を確認し、タイプ未選択時の `タイプを選択してください` を確認。タイプ選択UIの自動操作が不安定だったため、定義作成・編集・削除までは未完了。


## 追加再検証: ロケーショングループ自動追加設定（2026-06-24）

- 出力先: `_analysis/full-live-operation-2026-06-24/targeted-live-recheck-171756/`
- `TEST_FAQ_20260624_LG_171810` を作成。作成フォームには `名前` と `ロケーション` 選択があり、ロケーション未選択では `ロケーションを選択してください` が表示され保存不可。
- 作成後詳細画面で `このグループに新しいロケーションを自動的に含める` チェックボックスは `disabled=true`。作成後変更不可としてFAQ/25分類へ反映。
- 詳細・一覧とも削除導線は確認できず、テストロケーショングループは残存。


## 完了監査サマリー（最新反映）

最新の完了監査を `_analysis/full-live-operation-2026-06-24/completion-audit-223327/completion-audit.md` に出力しました。連携実接続はユーザー方針により対象外です。残件は次の扱いで管理します。

| 区分 | 件数 | 扱い |
|:--|--:|:--|
| 連携実接続対象外 | 316 | 対象外 |
| ユーザー追加/削除・別権限ユーザーが必要 | 17 | 対象外（ユーザー操作禁止） |
| 注文/売上/顧客など実データ依存 | 50 | 標準stagingでは検証不可 |
| 未実装/TODO表示/存在しない画面として確認済み | 37 | 仕様として未実装/存在なしを記録済み |
| 巻き戻し不可・外部ファイル/メール出力系 | 23 | 破壊的/外部出力のため例外管理 |
| 開発元確認が必要 | 31 | Stack社確認事項 |
| 非連携・追加確認候補 | 240 | 継続確認候補 |
| 低優先ドキュメントバックログ | 8 | 低優先 |



## 追加再検証: 店舗受取商品 最新UI（2026-06-25）

- 出力先: `_analysis/full-live-operation-2026-06-24/store-pickup-recheck-084249/`（実ファイルの実際の保存先は `2026-06-24` 配下）
- `/admin/local_pickup_product_variants`: h1「店舗受取」、空状態「アイテムが見つかりませんでした」。商品側の `バリエーションを追加する` ボタンは表示されず。
- `/admin/local_pickup_product_variants/create`: `このページは存在しないようです`。
- `/admin/local_pickup_retail_location_rules`: 店舗側の「店舗受取」設定は存在し、`追加する` は表示される。
- 07.店舗受取商品は、過去スクショの追加ダイアログよりも2026-06-25最新UIを優先するよう修正。
