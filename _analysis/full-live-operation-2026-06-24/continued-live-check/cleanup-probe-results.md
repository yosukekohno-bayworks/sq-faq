# 残テストデータ削除導線プローブ 2026-06-24

| 対象 | URL | 存在 | app_error | 削除導線 | アーカイブ導線 | 備考 |
|:--|:--|:--:|:--:|:--:|:--:|:--|
| `TEST_FAQ_20260624_取引先_092214` | `/admin/settings/suppliers` | True | False | False | True |  |
| `TEST_FAQ_20260624_ブランド_092214` | `/admin/settings/brands` | True | False | True | False |  |
| `TEST_FAQ_20260624_決済_092214` | `/admin/settings/payment_methods` | True | False | True | False |  |
| `TEST_FAQ_20260624_GU倉庫_ON_092214` | `/admin/settings/locations` | True | False | None | None | Locator.check: Timeout 3000ms exceeded.
Call log:
  - waiting for locator("tr").filter(has_text="TEST_FAQ_20260624_GU倉庫_ON_092214").first.locator("input[type=checkbox]").first
 |
| `TEST_FAQ_20260624_GU店舗_OFF_092214` | `/admin/settings/locations` | True | False | None | None | Locator.check: Timeout 3000ms exceeded.
Call log:
  - waiting for locator("tr").filter(has_text="TEST_FAQ_20260624_GU店舗_OFF_092214").first.locator("input[type=checkbox]").first
 |
| `TEST_FAQ_20260624_Recustomer_100908` | `/admin/recustomer_integrations` | True | False | False | False |  |
| `TEST_FAQ_20260624_MEASURE_CRUD_093821` | `/admin/settings/product_measurement_rules` | True | False | None | None | Locator.check: Timeout 3000ms exceeded.
Call log:
  - waiting for locator("tr").filter(has_text="TEST_FAQ_20260624_MEASURE_CRUD_093821").first.locator("input[type=checkbox]").first
 |
| `TEST_FAQ_20260624_TRANSLATION_CRUD_093701` | `/admin/settings/translation/translation_rules` | True | False | True | False |  |