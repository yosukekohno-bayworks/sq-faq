# 未確認項目 追加進捗レビュー 2（Codex / Playwright）

作成日: 2026-06-08

方針: 元のFAQ/分析ファイルは変更せず、残っていた未確認のうち、画面操作で追加確認できるものだけをPlaywrightで再検証した。

## 今回の追加証跡

- `faq/_analysis/deep-screen-verification-20260608/unconfirmed-remaining-records.json`
- `faq/_analysis/deep-screen-verification-20260608/unconfirmed-remaining-screenshots/`
- `faq/_analysis/deep-screen-verification-20260608/unconfirmed-omnibus-retry-records.json`
- `faq/_analysis/deep-screen-verification-20260608/unconfirmed-omnibus-retry-screenshots/`

変更系の保存・削除・外部接続実行は押していない。フォーム項目、空状態、404、画面エラー、正規リンク到達を確認した。

## 今回進んだ項目

| 項目 | 追加確認結果 | FAQでの扱い |
|---|---|---|
| OmnibusCore実レコード詳細 | 一覧の `TEST_MAKER_001` から正規URL `/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration` に到達。詳細画面が表示される。 | `TEST_MAKER_001` 文字列をURLにした推測URLは誤り。正規URLはUUID付き。 |
| OmnibusCore詳細設定 | 詳細画面で、カタログ、カラー/サイズオプション名、ロケーショングループ、在庫予約ルール、販売上限ルール、下書き注文の有効期限日数、出荷指示ステータス、トークン作成、連携削除、保存ボタンを確認。 | 設定項目は書ける。同期後の注文/在庫反映は未確認のまま。 |
| ロジザード作成画面 | `/admin/logizard_integrations/create` に到達。設定名、グループ番号、接続番号、Partner APIエンドポイント、オーナーID、ユーザーID、パスワード、アプリケーションキー、AuthKey発行スキップ、入荷/出荷/実績エクスポートのファイルID・パターンID、商品バリエーション識別キーを確認。 | 「連携作成フォームがある」「SKU/JAN/EAN/UPCで商品マッピングキーを選ぶ」は書ける。同期挙動は未確認。 |
| PDFエクスポートトップ | `/admin/pdf_export` は `PDFエクスポート` と表示。項目は `納品書`、説明は「指定された出荷指示の納品書をエクスポートします」。 | PDF機能の入口は確認済み。 |
| 納品書PDF一覧 | `/admin/pdf_export/pdf_export_operation_packing_slips` は表示されるが空状態。フォームや新規作成ボタンはない。 | 実PDF出力はまだ書けない。対象出荷指示が必要。 |
| PDF納品書テンプレート | `/admin/settings/pdf_template_package_slip` で `HTMLテンプレート` textarea と `保存する` を確認。 | テンプレート編集画面の存在は書ける。テンプレート保存・PDF反映は未実施。 |
| 下書き注文create直打ち | `/admin/draft_orders/create` は画面エラー。GraphQL応答に `invalid id format(UUID_Suffix): create` が出る。 | 直URLで下書き注文作成画面が開くとは書かない。 |
| 返品create直打ち | `/admin/order_returns/create` は404。 | 返品起票は実注文詳細など正規導線が必要。直URL作成は不可。 |
| 売上実績create直打ち | `/admin/sale_change_line_items/create` は404。 | 売上実績の手動作成導線は確認できない。注文起点/連携起点の生成は未確認。 |
| 権限グループ差分 | `特権管理者` は70権限すべてON。`TEST_FAQ_店舗スタッフ` は4権限のみON。 | 権限グループ設定の差分は書ける。ログイン後UI差分は未確認。 |
| ユーザー作成フォーム | 姓、名、メールアドレス、権限グループのラジオ（特権管理者 / TEST_FAQ_店舗スタッフ）を確認。 | ユーザー作成時に権限グループを選べることは書ける。招待/通知リスクがあるため保存は未実施。 |

## 権限グループの実測差分

`特権管理者`:

- チェックボックス: 70
- ON: 70
- OFF: 0

`TEST_FAQ_店舗スタッフ`:

- チェックボックス: 70
- ON: 4
- OFF: 66
- ONだった権限:
  - 在庫の閲覧権限（inventory:read）
  - 注文の閲覧権限（orders:read）
  - 店舗ポータル連携の閲覧権限（retail_portal_integrations:read）
  - 店舗スタッフの閲覧権限（retail_staff_members:read）

## 今回も残す未確認

| 項目 | 残す理由 |
|---|---|
| OmnibusCore/Shopify/スマレジ/Recustomer/ロジザードの同期挙動 | 接続情報・外部側データ・同期実行条件がない。OmnibusCoreは接続レコード自体はあるが、注文/在庫同期の結果までは追えない。 |
| 納品書PDFの実ファイル | PDF対象になる出荷指示が一覧にない。`/create` や `/new` の推測URLは404。 |
| 注文詳細・返品起票 | 注文/返品一覧が空。返品create直打ちは404。 |
| 会計/売上実績の自動生成 | 売上実績一覧が空、create直打ちは404。注文や連携データが必要。 |
| 権限別ログイン時のUI差分 | `TEST_FAQ_店舗スタッフ` の設定内容は確認できたが、そのユーザーでログインしていない。 |
| 発注伝票保存後の入荷連携 | 既存証跡で、取引先/テナント/SKU/単価/数量まで入力後、作成時に画面エラー。再実行は成功時に実データを増やす可能性があるため今回は避けた。 |
| 出荷と入荷の逆順/完全並行処理 | 既存実操作は出荷後に入荷。逆順や同時進行は未検証。 |

## FAQ本文への反映方針

- 外部連携は「設定フォーム・設定項目は確認済み」と「連携後の自動同期は未確認」を分ける。
- PDFは「PDFエクスポート入口」と「HTMLテンプレート編集」は書けるが、納品書PDFの内容や出力結果は断定しない。
- 権限は「グループごとに権限ON/OFFを設定できる」「ユーザー作成時に権限グループを選ぶ」までは書ける。ボタン非表示・メニュー制限などログイン後挙動は未確認。
- 下書き注文、返品、売上実績の `create` 直URLは存在しない/壊れているため、FAQでは直URL作成を案内しない。
- 発注伝票は、フォーム入力までは確認済みだが、現stagingでは保存エラー。発注後の入荷連携は断定しない。
