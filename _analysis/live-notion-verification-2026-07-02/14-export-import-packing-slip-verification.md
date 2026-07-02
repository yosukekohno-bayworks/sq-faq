# 14 export/import/packing slip verification - 2026-07-02

## Scope

- SQ staging outbound export/import screens.
- Yamato B2 Cloud CSV export and import.
- Packing slip PDF export.
- Gmail download mail check via browser-use profile `bay-works.com`.

## Yamato B2 condition export

- Screen: `/admin/inventory_outbound_orders/export/yamato_b2_cloud`
- Confirmed form output labels:
  - `ヤマトB2クラウド取り込み用CSV`
  - `同梱する納品書PDF`
- Confirmed fields:
  - `開始日時`
  - `終了日時`
  - `配送先 (国)`
  - `決済方法`: `すべての決済` / `代引きのみ` / `代引き以外の決済`
  - `出荷作業ステータス`: `指定しない` / `出荷待ち` / `保留中` / `依頼済み` / `作業中` / `欠品・要対応` / `キャンセル済み` / `出荷完了`
  - `注文タグ（含む）`
  - `注文タグ（除外）`
  - `CSVの出力後に出荷指示のステータスを出荷作業中に変更する`
- New condition export test at around 23:43:
  - Checkbox OFF.
  - Toast: `ヤマトB2クラウドのエクスポートを開始しました`.
  - No new history row or new mail found during this verification window.

## Yamato B2 successful CSV mail/history

- History: `/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds`
- Existing row:
  - Created: `2026年07月02日 23:34`
  - Status: `成功 完了`
  - Download button enabled.
- Mail:
  - From: `noreply@notification.sqstackstaging.com`
  - Subject: `出荷指示 - ヤマトB2クラウドのCSVエクスポートが完了しました | SQ`
  - Time: `2026年7月2日(木) 23:35`
  - Body says the download link expires at `2026/7/3 00:05`.
  - The mail contained one download link for CSV. No packing-slip PDF link was found.
- Downloaded CSV artifact: `yamato-mail-download-2335.csv`
- CSV:
  - Encoding: UTF-8.
  - Rows: 2 (header + 1 data row).
  - Header count: 13.
  - Headers:
    - `送り状種類`
    - `お客様管理番号`
    - `お届け先名`
    - `お届け先電話番号`
    - `お届け先郵便番号`
    - `お届け先住所`
    - `お届け先住所（アパートマンション名）`
    - `出荷予定日`
    - `お届け予定（指定）日`
    - `配達時間帯`
    - `コレクト代金引換額（税込）`
    - `コレクト内消費税額等`
    - `備考欄`
  - Data row used management number `#IO-1047`.

## Outbound list bulk Yamato CSV export

- Screen: `/admin/inventory_outbound_orders`
- Action path: select row -> `アクション` -> `エクスポート` -> `ヤマトB2クラウド（CSV）`
- Tested row: `#IO-1050`.
- Modal:
  - Title: `ヤマトB2クラウドのCSVをエクスポートする`
  - Checkbox: `エクスポートした出荷指示のステータスを作業中に更新する`
- Result:
  - Created history row at `2026年07月02日 23:47`.
  - After reload, row became `重大 失敗`.
  - Download disabled.
  - No completion/failure mail found.
  - Public UI/GraphQL fields did not expose a failure reason.

## Packing slip PDF export

- Screen: `/admin/inventory_outbound_orders`
- Action path: select row -> `アクション` -> `エクスポート` -> `納品書（PDF）`
- Tested row: `#IO-1048`.
- Modal:
  - Title: `納品書をPDFでエクスポートする`
  - Body: `選択されている出荷指示の納品書をPDFでエクスポートします。`
- Result:
  - New tab: `/admin/pdf_export/pdf_export_operation_packing_slips`
  - Created row at `2026年07月02日 23:49`.
  - After reload, row became `重大 失敗`.
  - Download disabled.
  - Existing visible rows were also `重大 失敗`.
  - No PDF/packing-slip completion mail found.
  - Public UI/GraphQL fields did not expose a failure reason.
  - No PDF content could be verified.

## Yamato B2 import

- List: `/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds`
- Confirmed:
  - H1: `ヤマトB2クラウドの出荷実績をCSVでインポートする`
  - Template link exists and opens Google Sheets.
  - `新規インポート` exists.
  - Visible history rows were `未実行`.
- Template:
  - Definition CSV artifact: `yamato-b2-template-definition.csv`
  - Format CSV artifact: `yamato-b2-template-format.csv`
  - Headers:
    - `伝票番号`
    - `お届け先コード`
    - `お届け先名`
    - `荷物状況`
    - `日付`
    - `時刻`
    - `出荷日`
    - `ｻｲｽﾞ品目`
    - `運賃`
    - `お客様管理番号`
  - Required: `伝票番号`, `出荷日`, `お客様管理番号`.
  - Other seven columns are read and ignored by processing, according to the template definition.
- Empty save:
  - Create URL: `/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds/create`
  - Empty save stayed on the same create page.
  - No visible red error message was found.
  - No job was created.
- Invalid management-number CSV test:
  - Artifact: `yamato-b2-import-invalid-management-20260702.csv`
  - `お客様管理番号`: `TEST_NO_SUCH_IO_20260702_2358`
  - Save created detail URL ending `b855e8ae-4e8c-5044-aacc-1490e108ce59_CSVImportOperationFulfillmentByYamatoB2Cloud`.
  - Immediate and after 20 seconds:
    - Message: `CSVのバリデーションを実行しています。バリデーションが完了すると、取り込み処理を実行できるようになります。`
    - `実行する` disabled.
    - `実行ステータス`: `未実行`
    - `検証成功`: `0件の出荷結果`
    - `検証失敗`: `0件の出荷結果`

## DHL import

- List: `/admin/csv_import/csv_import_operation_fulfillment_by_dhls`
- Confirmed:
  - H1: `DHLの出荷実績をCSVでインポートする`
  - `新規インポート` exists.
  - No template link found.
  - List was empty.
- Create URL: `/admin/csv_import/csv_import_operation_fulfillment_by_dhls/create`
- Empty save:
  - Stayed on the same create page.
  - No visible red error message was found.
  - No job was created.
