# 2026-07-01 live verification: area 14/15 PDF, mail, editability

## Scope

- `04-notion/14-入出荷・在庫依頼.md`
- `04-notion/15-発注・仕入.md`
- Focus: PDF/print/mail/export entry points, and operation availability after completion/cancellation/issued status.

## Purchase orders

### `#IP-1014` issued purchase order

- URL: `/admin/inventory_purchase_orders/7b0bb9ff-37f9-5144-99d4-1f3454e69562_InventoryPurchaseOrder`
- Status: `情報 発注済み`
- Visible actions:
  - Primary action: `入荷指示を作成する`
  - `その他の操作`: `キャンセルする`
- Not visible in body, buttons, or loaded detail JS:
  - PDF
  - print
  - mail/email/send
  - edit/save/update/revert-to-draft
- Main inputs on issued detail render read-only or as value display; there is no save/update button.
- `キャンセルする` is enabled while no completed inbound receipt blocks cancellation.

### `#IP-1007` issued purchase order with completed inbound receipt

- URL: `/admin/inventory_purchase_orders/536f9387-9a2b-59da-aab8-131ca9b82a3b_InventoryPurchaseOrder`
- Status: `情報 発注済み`
- Not visible in body, buttons, or loaded detail JS:
  - PDF
  - print
  - mail/email/send
  - edit/save/update/revert-to-draft
- `その他の操作`: `キャンセルする`, but disabled after the related inbound receipt is completed.

Conclusion: The current management UI has no manual purchase order PDF/print entry point and no manual purchase confirmation mail/send entry point. Issued purchase orders are not editable from the current UI. Cancellation remains status-dependent: available before completed receiving, disabled after completed receiving.

## Outbound orders

### List and detail checks

- List URL: `/admin/inventory_outbound_orders`
- Latest inspected detail:
  - `#IO-1047`: `/admin/inventory_outbound_orders/65202d87-7a2a-52dc-a078-b4a504878ef2_InventoryOutboundOrder`
  - Status: `成功 完了 出荷完了`
  - Shipping method: `店頭販売による商品の受け渡し`
- Detail body/buttons/loaded detail JS do not show:
  - PDF
  - print
  - mail/email/send
  - edit/save/update
  - `その他の操作`
- Detail shows `出荷実績を登録する`, but it is disabled on completed outbound orders.
- Important correction: the list-side JS contains `PdfExportOperationPackageSlipExecute`.

### Bulk action PDF flow

Verified from the outbound list:

1. Select one outbound order checkbox.
2. The bulk action bar appears and shows `1を選択済み`.
3. Open `アクション`.
4. Menu section `エクスポート` appears with:
   - `ヤマトB2クラウド（CSV）`
   - `納品書（PDF）`
5. Click `納品書（PDF)`.
6. Confirmation modal appears:
   - Title: `納品書をPDFでエクスポートする`
   - Body: `選択されている出荷指示の納品書をPDFでエクスポートします。`
   - Actions: `キャンセル`, `エクスポート`
7. Click `エクスポート`.
8. New tab opens:
   - `/admin/pdf_export/pdf_export_operation_packing_slips`

### PDF operation results

Attempt 1:

- Source outbound order: `#IO-1047`
- Created at: `2026年07月01日 22:05`
- Initial status: `情報 実行中`
- Final status after reload/wait: `重大 失敗`
- Download button: disabled (`aria-disabled=true`)

Attempt 2:

- Source outbound order: `#IO-1046`
- URL: `/admin/inventory_outbound_orders/e030b4bf-2fc4-5714-b639-e11c6fbce3f7_InventoryOutboundOrder`
- Shipping method: `配送`
- Created at: `2026年07月01日 22:07`
- Final status: `重大 失敗`
- Download button: disabled (`aria-disabled=true`)

Conclusion: Outbound package slip PDF generation does have a live UI path, but it is list bulk action based, not detail based. Both tested completed outbound orders produced failed PDF operations in staging, so file contents/download cannot be confirmed from these two attempts.

## Inbound orders

### List

- URL: `/admin/inventory_inbound_orders`
- The list has no row checkbox/bulk action bar in the inspected state.
- Body/buttons show no PDF, print, mail/email/send, or export entry point.

### Completed detail `#II-1038`

- URL: `/admin/inventory_inbound_orders/4015c9c1-4002-5686-ab1e-2d42182af85b_InventoryInboundOrder`
- Status: `成功 完了 入荷完了`
- No PDF/print/mail/export/other-action entry point.
- `入荷指示を一括受領で完了する` and `入荷実績を登録する` are visible but disabled:
  - `Polaris-Button--disabled`
  - no `href`

### Cancelled detail `#II-1039`

- URL: `/admin/inventory_inbound_orders/f4703cd5-3b10-57da-9012-86727003035c_InventoryInboundOrder`
- Status: `警告 入荷キャンセル`
- No PDF/print/mail/export/other-action entry point.
- `入荷指示を一括受領で完了する` and `入荷実績を登録する` are visible but disabled:
  - `Polaris-Button--disabled`
  - no `href`

### Loaded JS

- Detail chunk `/admin/inventory_inbound_orders/[inventoryInboundOrderID]/page-*.js` has no `PDF`, `印刷`, `メール`, `送信`, or `エクスポート` text.
- List chunk has no PDF/print/mail/send text. It contains export-related implementation text, but no visible Japanese export entry point on the inspected list.

Conclusion: Inbound orders currently have no management UI path for PDF/print/mail/export. Completed/cancelled inbound orders show receipt buttons as disabled links with no `href`.
