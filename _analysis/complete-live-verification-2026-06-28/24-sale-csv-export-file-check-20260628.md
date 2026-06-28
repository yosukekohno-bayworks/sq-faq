# 売上実績CSV 実ファイル確認 2026-06-28

- JSON証跡: `_analysis/complete-live-verification-2026-06-28/24-sale-csv-export-file-check-20260628.json`

| 種別 | 実行送信 | ダウンロード | 文字コード | 行数 | FAQ注文 | 対象SKU | ヘッダー |
|:--|:--|:--|:--|--:|:--|:--|:--|
| 売上実績（注文軸） | `True` | `True` | `utf-8-sig` | 6 | `True` | `False` | `ID / イベント / 作成元 / 作成元オブジェクトID / 店舗コード / 処理日時 / 税込フラグ / 通貨コード / 売上 / 税額 / 小計 / 小計に対する税額 / 送料 / 送料に対する税額 / 注文に対する割引額 / 注文明細に対する割引額 / 送料に対する割引額 / 利用ポイント` |
| 売上実績（明細軸） | `True` | `True` | `utf-8-sig` | 6 | `False` | `True` | `SaleChangeID / SaleChangeLineItemID / 処理日時 / SKU / 数量 / 通貨コード / 売上 / 税額 / 割引合計 / ポイント配賦額 / 注文割引配賦額` |

## 詳細

### 売上実績（注文軸）
- tenantSelected: `True` via `select[0]`
- datesFilled: `True` / `[{'label': '開始日時', 'method': 'label', 'value': '2026-06-28T00:00'}, {'label': '終了日時', 'method': 'label', 'value': '2026-06-29T00:00'}]`
- savedAs: `/Users/kounoyousuke/App Building/SQ/faq/_analysis/complete-live-verification-2026-06-28/24-sale-csv-sale_changes-20260628140738.csv`
- firstDataRows: `[['13860272-daf4-546a-b0fd-3a7144bd1b88_SaleChange', 'ORDER_REFUND', 'FAQ_INTERNAL_GRAPHQL', '71bb5d90-ed76-57d0-83bf-bf1bdee7d684_OrderRefund', '', '2026-06-28T01:19:58Z', 'true', 'JPY', '-1990', '0', '-1990', '0', '0', '0', '0', '0', '0', '0'], ['2a85c6ad-d747-5133-8dd7-547d1d27f3ef_SaleChange', 'ORDER', 'FAQ_REMAINING_AUTHONLY', '68dee76e-36de-5a27-a182-5505ed6dd576_Order', '', '2026-06-28T05:03:10Z', 'true', 'JPY', '1990', '0', '1990', '0', '0', '0', '0', '0', '0', '0'], ['c73b427b-7486-579d-910c-184c68873f44_SaleChange', 'ORDER', 'FAQ_REMAINING_UNPAID-NOFULFILL', 'c5d520b4-39f1-518e-ad2f-e2b655a0684f_Order', '', '2026-06-28T05:01:27Z', 'true', 'JPY', '1990', '0', '1990', '0', '0', '0', '0', '0', '0', '0'], ['e14ef9dc-4d72-5810-9e99-a36a48ee7476_SaleChange', 'ORDER', 'FAQ_REMAINING_EXCHANGE', '2d53b63c-df1e-58c4-89b8-338b2537276a_Order', '', '2026-06-28T05:01:33Z', 'true', 'JPY', '1990', '0', '1990', '0', '0', '0', '0', '0', '0', '0'], ['e5f76363-3cb3-5387-8b47-41d14d2b9307_SaleChange', 'ORDER', 'FAQ_INTERNAL_GRAPHQL', '4c7e4e96-6d5b-5c73-bf86-9693cf7c4734_Order', '', '2026-06-28T01:11:34Z', 'true', 'JPY', '1990', '0', '1990', '0', '0', '0', '0', '0', '0', '0']]`

### 売上実績（明細軸）
- tenantSelected: `True` via `select[0]`
- datesFilled: `True` / `[{'label': '開始日時', 'method': 'label', 'value': '2026-06-28T00:00'}, {'label': '終了日時', 'method': 'label', 'value': '2026-06-29T00:00'}]`
- savedAs: `/Users/kounoyousuke/App Building/SQ/faq/_analysis/complete-live-verification-2026-06-28/24-sale-csv-sale_change_line_items-20260628140738.csv`
- firstDataRows: `[['13860272-daf4-546a-b0fd-3a7144bd1b88_SaleChange', '91dda7c6-ff4c-50fc-a447-dabf47ec4695_SaleChangeLineItem', '2026-06-28T01:19:58Z', 'TEST_E2E_20260622_GU_1905_NAVY_M', '-1', 'JPY', '-1990', '0', '0', '0', '0'], ['e5f76363-3cb3-5387-8b47-41d14d2b9307_SaleChange', 'a41a9700-01f6-5449-b9a9-129e509977a6_SaleChangeLineItem', '2026-06-28T01:11:34Z', 'TEST_E2E_20260622_GU_1905_NAVY_M', '1', 'JPY', '1990', '0', '0', '0', '0'], ['c73b427b-7486-579d-910c-184c68873f44_SaleChange', 'ab96b53d-a012-568f-95d5-3a6282aaa54d_SaleChangeLineItem', '2026-06-28T05:01:27Z', 'TEST_E2E_20260622_GU_1905_NAVY_M', '1', 'JPY', '1990', '0', '0', '0', '0'], ['2a85c6ad-d747-5133-8dd7-547d1d27f3ef_SaleChange', 'c5dda51c-e02d-5872-badb-7738500ba32d_SaleChangeLineItem', '2026-06-28T05:03:10Z', 'TEST_E2E_20260622_GU_1905_NAVY_M', '1', 'JPY', '1990', '0', '0', '0', '0'], ['e14ef9dc-4d72-5810-9e99-a36a48ee7476_SaleChange', 'd0875ec7-5fe7-5497-aedf-5c6436777420_SaleChangeLineItem', '2026-06-28T05:01:33Z', 'TEST_E2E_20260622_GU_1905_NAVY_M', '1', 'JPY', '1990', '0', '0', '0', '0']]`

## 判断

- 注文軸/明細軸のCSVダウンロードリンクから実ファイルを保存し、ヘッダーとデータ行を確認する。
- `containsFaqOrder` / `containsTargetSku` がtrueなら、2026-06-28の検証注文・対象SKUを含む実データ出力として扱える。
