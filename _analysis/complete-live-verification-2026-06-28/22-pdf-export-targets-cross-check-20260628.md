# PDFエクスポート対象伝票 横断確認

- 実行日時: 2026-06-27T22:37:44.109662+00:00
- 方法: 各伝票一覧の先頭リンクを開き、詳細画面のPDF/印刷/納品書/ダウンロード系UIを確認。PDFエクスポート直URLも確認。

## 結果

- 移動伝票: `/admin/inventory_movement_orders/d595f669-f394-57e4-887d-fcb49e9bf934_InventoryMovementOrder` h1=['#IM-1029'] keyword controls=0
- 調整伝票: `/admin/inventory_adjustment_orders/656af2b4-e907-52d7-a665-6a7dcef5b31a_InventoryAdjustmentOrder` h1=['#IA-1013'] keyword controls=0
- 取置伝票: `/admin/inventory_reservation_orders/7ade0706-6d15-5c55-a0be-b60386308eb4_InventoryReservationOrder` h1=['#IR-1011'] keyword controls=0
- 出荷指示: `/admin/inventory_outbound_orders/380d6c15-ba98-5391-8397-f8c7ec577c45_InventoryOutboundOrder` h1=['#IO-1029'] keyword controls=0
- 入荷指示: `/admin/inventory_inbound_orders/2ebff63c-e59a-5ee1-ae52-8652e9f721fa_InventoryInboundOrder` h1=['#II-1031'] keyword controls=0
- 発注伝票: `/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder` h1=['#IP-1013'] keyword controls=0

## PDFエクスポート画面

- PDFエクスポート: `/admin/pdf_export` h1=['PDFエクスポート'] keyword controls=1
  - snippet: `理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 PDFエクスポート。このページの準備が整いました PDFエクスポート 出荷 納品書 指定された出荷指示の納品書をエクスポートできます。`
- PDF納品書カテゴリ: `/admin/pdf_export/pdf_export_operation_packing_slips` h1=['納品書をPDFでエクスポートする'] keyword controls=1
  - snippet: `理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 納品書をPDFでエクスポートする。このページの準備が整いました 納品書をPDFでエクスポートする アイテムが見つかりませんでした 絞り込みや検索ワードを変更してみてください`
- PDF納品書作成直URL: `/admin/pdf_export/pdf_export_operation_packing_slips/create` h1=['このページは存在しないようです'] keyword controls=0
- 納品書テンプレート: `/admin/settings/pdf_template_package_slip` h1=['PDF納品書テンプレート'] keyword controls=0
  - snippet: `理 販売設定 会計 分析 オペレーション 入荷管理 出荷管理 在庫依頼 未完了の在庫依頼 3件 3 CRM ディスカウント ポイント 会員ランク 販売チャネル Shopify OmnibusCore スマレジ リテールポータル 卸売 設定 PDF納品書テンプレート。このページの準備が整いました PDF納品書テンプレート HTMLテンプレート 保存する`

## 判断

- 確認した伝票詳細では、PDF/印刷/納品書を生成する明示ボタンは確認できなかった。
- PDFエクスポートはトップに `納品書` カテゴリがあり、カテゴリページ `/admin/pdf_export/pdf_export_operation_packing_slips` も表示されるが空状態で、新規作成/任意生成ボタンは確認できない。`/create` は存在しない画面。
- 現時点で画面上確認できるPDF生成の入口は、ヤマトB2クラウド条件指定エクスポートフォームの出力物 `同梱する納品書PDF` 表示に限って案内する。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/22-pdf-export-targets-cross-check-20260628.json`
