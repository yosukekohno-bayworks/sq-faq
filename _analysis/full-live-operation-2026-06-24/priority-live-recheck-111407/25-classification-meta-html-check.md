# 25分類メタ/HTML反映チェック（2026-06-24 追加）

| file | status | verified | admin URLs | SQ-FAQ | Guide | Support | Graph |
|:--|:--|:--|--:|:--:|:--:|:--:|:--:|
| `01-SQ全体・共通導線.md` | 完成寄り | 2026-06-20 | 23 | — | — | — | — |
| `02-アカウント・権限.md` | 完成寄り | 2026-06-20 | 4 | — | — | ✅ | — |
| `03-組織・通知.md` | 完成寄り | 2026-06-20 | 7 | — | — | — | — |
| `04-基本マスタ.md` | 完成寄り | 2026-06-24 | 7 | — | — | — | — |
| `05-商品・SKU.md` | 完成寄り | 2026-06-22 | 7 | ✅ | ✅ | — | — |
| `06-カタログ.md` | 完成寄り | 2026-06-24 | 9 | ✅ | ✅ | ✅ | ✅ |
| `07-店舗受取商品.md` | 完成寄り | 2026-06-21 | 2 | — | — | — | — |
| `08-カスタムデータ.md` | 完成寄り | 2026-06-20 | 5 | ✅ | ✅ | ✅ | — |
| `09-翻訳.md` | 完成寄り | 2026-06-24 | 3 | ✅ | ✅ | ✅ | ✅ |
| `09b-採寸.md` | 完成寄り | 2026-06-24 | 4 | ✅ | ✅ | ✅ | — |
| `10-価格・販売制御.md` | 完成寄り 要確認 | 2026-06-21 | 18 | — | — | — | — |
| `11-在庫状態・在庫数.md` | 完成寄り | 2026-06-22 | 6 | — | — | — | — |
| `12-在庫伝票.md` | 完成寄り | 2026-06-24 | 8 | — | — | — | — |
| `13-入出荷・在庫依頼.md` | 一部確認 | 2026-06-22 | 5 | — | — | — | — |
| `14-発注・仕入.md` | 一部確認 | 2026-06-24 | 7 | — | — | — | — |
| `15-注文・返品.md` | 一部確認 連携待ち | 2026-06-20 | 7 | ✅ | ✅ | — | — |
| `16-顧客・会社.md` | 一部確認 連携待ち | 2026-06-24 | 10 | ✅ | ✅ | — | — |
| `17-CRM.md` | 完成寄り 一部確認 | 2026-06-20 | 18 | ✅ | ✅ | — | — |
| `18-店舗業務・リテールポータル.md` | 一部確認 | 2026-06-20 | 4 | — | — | — | — |
| `19-標準販売チャネル連携.md` | 連携待ち | 2026-06-20 | 11 | — | — | ✅ | — |
| `20-物流・返品・外部アプリ連携.md` | 連携待ち | 2026-06-20 | 11 | — | — | ✅ | — |
| `21-CSV・PDF・データ移行.md` | 完成寄り 一部確認 | 2026-06-21 | 23 | — | — | — | — |
| `22-API・Webhook・開発者連携.md` | 完成寄り | 2026-06-20 | 4 | — | — | — | — |
| `23-会計・売上実績・分析.md` | 一部確認 TODO表示 | 2026-06-20 | 8 | — | — | — | — |
| `24-未実装・将来機能.md` | TODO表示 | 2026-06-20 | 6 | — | — | — | — |
| `25-顧客別個別仕様・運用差分.md` | 資料由来 | 2026-06-20 | 8 | — | — | — | — |

## JSON

```json
[
  {
    "file": "01-SQ全体・共通導線.md",
    "area": "1",
    "title": "01. SQ全体・共通導線",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-20",
    "admin_url_count": 23,
    "sample_urls": [
      "/admin/analytics",
      "/admin/b2b",
      "/admin/customer_rank_calculation_rules",
      "/admin/inventory_allocation_request_confirmations",
      "/admin/inventory_allocation_requests"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "02-アカウント・権限.md",
    "area": "2",
    "title": "02. アカウント・権限",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-20",
    "admin_url_count": 4,
    "sample_urls": [
      "/admin/settings/permission_groups",
      "/admin/settings/permission_groups/create",
      "/admin/settings/users",
      "/admin/settings/users/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "03-組織・通知.md",
    "area": "3",
    "title": "03. 組織・通知",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-20",
    "admin_url_count": 7,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/brands",
      "/admin/settings/organization_notification_emails",
      "/admin/settings/organization_notification_emails/create",
      "/admin/settings/tenants"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "04-基本マスタ.md",
    "area": "4",
    "title": "04. 基本マスタ",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-24",
    "admin_url_count": 7,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/brands",
      "/admin/settings/location_groups",
      "/admin/settings/locations",
      "/admin/settings/payment_methods"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "05-商品・SKU.md",
    "area": "5",
    "title": "05. 商品・SKU",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-22",
    "admin_url_count": 7,
    "sample_urls": [
      "/admin/products",
      "/admin/products/create",
      "/admin/products/{id}",
      "/admin/products/{id}/edit",
      "/admin/products/{id}/variants/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "06-カタログ.md",
    "area": "6",
    "title": "06. カタログ",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-24",
    "admin_url_count": 9,
    "sample_urls": [
      "/admin/catalogs",
      "/admin/catalogs/create",
      "/admin/catalogs/{id}",
      "/admin/catalogs/{id}/automatic_add_rules",
      "/admin/catalogs/{id}/catalog_product_variants"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": true
    }
  },
  {
    "file": "07-店舗受取商品.md",
    "area": "7",
    "title": "07. 店舗受取商品",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-21",
    "admin_url_count": 2,
    "sample_urls": [
      "/admin/local_pickup_product_variants",
      "/admin/local_pickup_retail_location_rules"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "08-カスタムデータ.md",
    "area": "8",
    "title": "08. カスタムデータ",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-20",
    "admin_url_count": 5,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/metafield_definitions",
      "/admin/settings/metafield_definitions/<対象オブジェクト>/create",
      "/admin/settings/metafield_definitions/create",
      "/admin/settings/metafield_definitions/organization/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "09-翻訳.md",
    "area": "9",
    "title": "09. 翻訳",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-24",
    "admin_url_count": 3,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/translation",
      "/admin/settings/translation/translation_rules/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": true
    }
  },
  {
    "file": "09b-採寸.md",
    "area": "9b",
    "title": "09b. 採寸",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-24",
    "admin_url_count": 4,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/product_measurement_rules",
      "/admin/settings/product_measurement_rules/create",
      "/admin/settings/translation"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "10-価格・販売制御.md",
    "area": "10",
    "title": "10. 価格・販売制御",
    "wbs_status": "完成寄り 要確認",
    "last_verified": "2026-06-21",
    "admin_url_count": 18,
    "sample_urls": [
      "/admin/csv_import/csv_import_operation_inventory_back_order_rule_product_variants",
      "/admin/csv_import/csv_import_operation_product_price_rule_sale_prices",
      "/admin/inventory_back_order_rules",
      "/admin/inventory_back_order_rules/[id]",
      "/admin/inventory_back_order_rules/[id]/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "11-在庫状態・在庫数.md",
    "area": "11",
    "title": "11. 在庫状態・在庫数",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-22",
    "admin_url_count": 6,
    "sample_urls": [
      "/admin/csv_export/csv_export_operation_inventory_logical_quantities",
      "/admin/csv_import/csv_import_operation_inventory_logical_available_quantities",
      "/admin/inventory_adjustment_orders",
      "/admin/inventory_items",
      "/admin/inventory_items/[id]"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "12-在庫伝票.md",
    "area": "12",
    "title": "12. 在庫伝票",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-24",
    "admin_url_count": 8,
    "sample_urls": [
      "/admin/inventory_adjustment_orders",
      "/admin/inventory_adjustment_orders/create",
      "/admin/inventory_inbound_orders",
      "/admin/inventory_movement_orders",
      "/admin/inventory_movement_orders/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "13-入出荷・在庫依頼.md",
    "area": "13",
    "title": "13. 入出荷・在庫依頼",
    "wbs_status": "一部確認",
    "last_verified": "2026-06-22",
    "admin_url_count": 5,
    "sample_urls": [
      "/admin/inventory_allocation_request_confirmations",
      "/admin/inventory_allocation_requests",
      "/admin/inventory_allocation_requests/create",
      "/admin/inventory_inbound_orders",
      "/admin/inventory_outbound_orders"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "14-発注・仕入.md",
    "area": "14",
    "title": "14. 発注・仕入",
    "wbs_status": "一部確認",
    "last_verified": "2026-06-24",
    "admin_url_count": 7,
    "sample_urls": [
      "/admin/companies",
      "/admin/inventory_inbound_orders",
      "/admin/inventory_purchase_orders",
      "/admin/inventory_purchase_orders/create",
      "/admin/settings/suppliers"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "15-注文・返品.md",
    "area": "15",
    "title": "15. 注文・返品",
    "wbs_status": "一部確認 連携待ち",
    "last_verified": "2026-06-20",
    "admin_url_count": 7,
    "sample_urls": [
      "/admin/draft_orders",
      "/admin/draft_orders/create",
      "/admin/order_returns",
      "/admin/order_returns/create",
      "/admin/orders"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "16-顧客・会社.md",
    "area": "16",
    "title": "16. 顧客・会社",
    "wbs_status": "一部確認 連携待ち",
    "last_verified": "2026-06-24",
    "admin_url_count": 10,
    "sample_urls": [
      "/admin/b2b",
      "/admin/companies",
      "/admin/companies/create",
      "/admin/companies/{id}",
      "/admin/companies/{id}/locations/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "17-CRM.md",
    "area": "17",
    "title": "17. CRM",
    "wbs_status": "完成寄り 一部確認",
    "last_verified": "2026-06-20",
    "admin_url_count": 18,
    "sample_urls": [
      "/admin/customer_rank_calculation_rules",
      "/admin/customer_rank_calculation_rules/[id]",
      "/admin/customer_rank_calculation_rules/[id]/customer_rank_rules/create",
      "/admin/customer_rank_calculation_rules/[id]/exclude_products",
      "/admin/customer_rank_calculation_rules/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": true,
      "SQ完全ガイド.html": true,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "18-店舗業務・リテールポータル.md",
    "area": "18",
    "title": "18. 店舗業務・リテールポータル",
    "wbs_status": "一部確認",
    "last_verified": "2026-06-20",
    "admin_url_count": 4,
    "sample_urls": [
      "/admin/local_pickup_retail_location_rules",
      "/admin/local_pickup_retail_location_rules/create",
      "/admin/retail_portal_integrations",
      "/admin/retail_portal_integrations/create"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "19-標準販売チャネル連携.md",
    "area": "19",
    "title": "19. 標準販売チャネル連携",
    "wbs_status": "連携待ち",
    "last_verified": "2026-06-20",
    "admin_url_count": 11,
    "sample_urls": [
      "/admin/catalogs",
      "/admin/catalogs/create",
      "/admin/inventory_back_order_rules",
      "/admin/inventory_sale_limit_rules",
      "/admin/omnibus_core_integrations"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "20-物流・返品・外部アプリ連携.md",
    "area": "20",
    "title": "20. 物流・返品・外部アプリ連携",
    "wbs_status": "連携待ち",
    "last_verified": "2026-06-20",
    "admin_url_count": 11,
    "sample_urls": [
      "/admin/inventory_adjustment_orders",
      "/admin/inventory_outbound_orders",
      "/admin/logizard_integrations",
      "/admin/logizard_integrations/create",
      "/admin/order_returns"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": true,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "21-CSV・PDF・データ移行.md",
    "area": "21",
    "title": "CSV/PDF・データ移行",
    "wbs_status": "完成寄り 一部確認",
    "last_verified": "2026-06-21",
    "admin_url_count": 23,
    "sample_urls": [
      "/admin/csv_export",
      "/admin/csv_export/csv_export_operation_inventory_logical_quantities",
      "/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds",
      "/admin/csv_export/csv_export_operation_location_by_location_group",
      "/admin/csv_export/csv_export_operation_order_price_adjustment_usages"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "22-API・Webhook・開発者連携.md",
    "area": "22",
    "title": "22. API/Webhook・開発者連携",
    "wbs_status": "完成寄り",
    "last_verified": "2026-06-20",
    "admin_url_count": 4,
    "sample_urls": [
      "/admin/settings",
      "/admin/settings/apps",
      "/admin/settings/apps/create",
      "/admin/settings/apps/{id}"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "23-会計・売上実績・分析.md",
    "area": "23",
    "title": "会計・売上実績・分析",
    "wbs_status": "一部確認 TODO表示",
    "last_verified": "2026-06-20",
    "admin_url_count": 8,
    "sample_urls": [
      "/admin/analytics",
      "/admin/analytics/reports",
      "/admin/analytics/revenue",
      "/admin/csv_export",
      "/admin/csv_export/csv_export_operation_sale_change_line_items"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "24-未実装・将来機能.md",
    "area": "24",
    "title": "24. 未実装・将来機能",
    "wbs_status": "TODO表示",
    "last_verified": "2026-06-20",
    "admin_url_count": 6,
    "sample_urls": [
      "/admin/analytics",
      "/admin/analytics/reports",
      "/admin/analytics/revenue",
      "/admin/b2b",
      "/admin/purchasing_customers"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  },
  {
    "file": "25-顧客別個別仕様・運用差分.md",
    "area": "25",
    "title": "25. 顧客別個別仕様・運用差分",
    "wbs_status": "資料由来",
    "last_verified": "2026-06-20",
    "admin_url_count": 8,
    "sample_urls": [
      "/admin/inventory_allocation_request_confirmations",
      "/admin/inventory_allocation_requests",
      "/admin/inventory_items",
      "/admin/inventory_movement_orders",
      "/admin/inventory_outbound_orders"
    ],
    "title_in_html": {
      "SQ-FAQ.html": false,
      "SQ完全ガイド.html": false,
      "SQ-サポートデスク.html": false,
      "SQ-データ相関図.html": false
    }
  }
]
```