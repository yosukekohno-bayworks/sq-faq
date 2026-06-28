# 三者不一致: 実機NG URL × FAQ/25分類参照 2026-06-24

実機で `存在しない/アプリエラー/TODO` だったURLのうち、FAQまたは25分類が本文で参照しているもの。

これは「FAQ/HTML・25分類・実機」の確定的な不一致候補（記述が実機と食い違う）。

| 実機状態 | URL | 参照しているFAQ/分類ファイル |
|:--|:--|:--|
| todo | `/admin/analytics` | 04-notion/01-SQ全体・共通導線.md, 04-notion/23-会計・売上実績・分析.md, 04-notion/24-未実装・将来機能.md, _support/screens.md |
| todo | `/admin/analytics/reports` | 04-notion/23-会計・売上実績・分析.md, 04-notion/24-未実装・将来機能.md, _support/constraints.md, _support/screens.md |
| todo | `/admin/analytics/revenue` | 04-notion/23-会計・売上実績・分析.md, 04-notion/24-未実装・将来機能.md, _support/constraints.md, _support/screens.md |
| todo | `/admin/b2b` | 00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md, 01-by-feature/会社.md, 04-notion/01-SQ全体・共通導線.md, 04-notion/16-顧客・会社.md, 04-notion/24-未実装・将来機能.md, _support/constraints.md, _support/screens.md |
| app_error | `/admin/draft_orders/create` | 00-getting-started/SQ完全ガイド.md, 00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md, 01-by-feature/注文管理.md, 03-faq/注文と出荷のよくある質問.md, 04-notion/15-注文・返品.md, _support/constraints.md, _support/errors.md, _support/symptoms.md |
| not_found | `/admin/order_returns/create` | 01-by-feature/注文管理.md, 04-notion/15-注文・返品.md, 04-notion/20-物流・返品・外部アプリ連携.md, _support/errors.md |
| not_found | `/admin/pdf_export/pdf_export_operation_packing_slips/create` | 00-getting-started/SQ完全ガイド.md, 00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md, 01-by-feature/CSVエクスポート・PDFエクスポート.md, 02-by-task/データをCSV・PDFでエクスポートする.md, 04-notion/20-物流・返品・外部アプリ連携.md, 04-notion/21-CSV・PDF・データ移行.md |
| app_error | `/admin/purchasing_customers/create` | 00-getting-started/SQ実測学習ガイド.md, 00-getting-started/データ事典②-商品・在庫・運用のデータとステータス.md, 01-by-feature/ディスカウント.md, 01-by-feature/顧客管理.md, 04-notion/16-顧客・会社.md, _support/errors.md, _support/screens.md |
| not_found | `/admin/sale_change_line_items/create` | 00-getting-started/SQ完全ガイド.md, 01-by-feature/会計（売上実績）.md, 04-notion/23-会計・売上実績・分析.md, _support/constraints.md |
| not_found | `/admin/settings/metafield_definitions/create` | 04-notion/08-カスタムデータ.md |

合計: 10 件
