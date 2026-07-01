# 2026-07-01 商品バリエーションCSVエクスポート 実機確認

## 対象

- 画面: `/admin/csv_export/csv_export_operation_product_variants/create`
- 履歴: `/admin/csv_export/csv_export_operation_product_variants`
- 項目: `商品情報を含める`

## 確認結果

`商品情報を含める` をOFF/ONの2通りで実行した。どちらも実行後は履歴一覧へ戻り、完了後に `成功 完了` と `ダウンロード` リンクが表示された。

| 設定 | 作成時刻表示 | 履歴の表示 | CSV行数 | CSVサイズ |
|:--|:--|:--|--:|--:|
| OFF | 2026年07月01日 12:20 | `成功 完了` / `含めない` | 98 | 8,344 bytes |
| ON | 2026年07月01日 12:21 | `成功 完了` / `成功 含める` | 98 | 14,228 bytes |

ON行の `商品情報` 列には、チェック付き状態を表す `成功` テキストと `含める` が同居して表示された。OFF行は `含めない` のみ。

## CSVヘッダー差分

OFF:

```csv
SKU,ProductVariantExternalID,ProductVariantTitle,ProductOption1Name,ProductOption1Value,ProductOption1ValueCode,ProductOption2Name,ProductOption2Value,ProductOption2ValueCode,ProductOption3Name,ProductOption3Value,ProductOption3ValueCode,Price,PriceCurrencyCode,Barcode,JAN,EAN,UPC,SupplierSKU,Weight,WeightUnit,CountryOfOrigin,HarmonizedSystemCode
```

ON:

```csv
ProductCode,ProductExternalID,ProductTitle,ProductStatus,ProductType,ProductVendor,BrandName,BrandCode,SKU,ProductVariantExternalID,ProductVariantTitle,ProductOption1Name,ProductOption1Value,ProductOption1ValueCode,ProductOption2Name,ProductOption2Value,ProductOption2ValueCode,ProductOption3Name,ProductOption3Value,ProductOption3ValueCode,Price,PriceCurrencyCode,Barcode,JAN,EAN,UPC,SupplierSKU,Weight,WeightUnit,CountryOfOrigin,HarmonizedSystemCode
```

## サンプル行の差分

- OFF: `SKU=483457-09-XL`, `ProductVariantTitle=BLACK / XL`, `Price=1500`, `PriceCurrencyCode=JPY`
- ON: 上記に加えて `ProductCode=483457`, `ProductTitle=エアリズムコットンT`, `ProductStatus=ACTIVE`, `ProductVendor=UNIQLO`, `BrandName=UNIQLO`, `BrandCode=UNIQLO`

## ドキュメント反映先

- `04-notion/22-CSV・PDF・データ移行.md`
- `01-by-feature/CSVエクスポート・PDFエクスポート.md`
- `02-by-task/データをCSV・PDFでエクスポートする.md`
- `03-faq/CSVインポート・エクスポートのよくある質問.md`
- `_analysis/NOTION-LIVE-VERIFICATION-LEDGER-2026-06-27.md`
- `_analysis/WBS-JULY-END-SCOPE-REVIEW-2026-06-21.md`
