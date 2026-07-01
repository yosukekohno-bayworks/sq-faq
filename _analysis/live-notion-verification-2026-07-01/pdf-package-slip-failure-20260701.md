# 納品書PDFエクスポート追加確認（2026-07-01）

## 確認対象

- 出荷管理一覧の一括操作から作成される納品書PDFジョブ
- GraphQL mutation: `pdfExportOperationPackageSlipExecute`
- 履歴クエリ: `pdfExportOperationPackageSlips`

## 実機結果

1. `#IO-1048`（配送、`inventoryAllocationStatus=WAITING`）で `pdfExportOperationPackageSlipExecute` を実行。
   - ジョブ `72baef05-ee74-59ef-8f23-8990e2de8366_PDFExportOperationPackageSlip` が作成された。
   - 約20秒後、`isFailedExecutionJob=true`、`isCompletedExecutionJob=false`、`filepath=""`、`downloadURL=null` になった。

2. `#IO-1020`（配送、`inventoryAllocationStatus=ALLOCATED`、数量5）で同じmutationを実行。
   - ジョブ `4bad4180-a3b9-5602-87ba-34166e057a3c_PDFExportOperationPackageSlip` が作成された。
   - 約20秒後、`isFailedExecutionJob=true`、`isCompletedExecutionJob=false`、`filepath=""`、`downloadURL=null` になった。

3. 既存の `#IO-1046`（配送、`WAITING`）と `#IO-1047`（店頭販売による商品の受け渡し、`WAITING`）のPDFジョブも同じく失敗状態。

## 補足

- `PDFExportOperationPackageSlip` 型には公開フィールドとして `filepath`、`downloadURL`、`isRunningExecutionJob`、`isFailedExecutionJob`、`isCompletedExecutionJob`、`inventoryOutboundOrders` などはあるが、失敗理由メッセージのフィールドは確認できない。
- 納品書テンプレート `pdfTemplatePackageSlipGet` は取得でき、HTMLテンプレートは存在する（長さ5933文字）。
- 今回の範囲では、出荷指示が `ALLOCATED` でもPDF生成は成功しなかったため、「引当待ちだから失敗」とは断定できない。

## 証跡

- `_analysis/live-notion-verification-2026-07-01/pdf-package-slip-jobs-20260701-2304.json`
