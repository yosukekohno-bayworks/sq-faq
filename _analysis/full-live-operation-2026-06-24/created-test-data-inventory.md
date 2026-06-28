# 検証で作成/残存した主なテストデータ 2026-06-24

実機検証のため、ユーザー追加/削除以外のテストデータを作成している。削除導線が見つからない/未確認のものは残存している可能性がある。

| area | data |
|:--|:--|
| e2e | `product_code=TEST_FAQ_20260624_GU_092214, sku_code=TEST_FAQ_20260624_GU_092214_NAVY_M, variant_url=https://www.sqstackstaging.com/admin/products/67a7cbec-a3f8-5f8e-995b-1f3fbfa02db1_Product/variants/1fcf313c-c8e2-5eec-83f8-f2e445a9abe6_ProductVariant` |
| e2e | `作成データ: TEST_FAQ_20260624_取引先_092214, TEST_FAQ_20260624_ブランド_092214, TEST_FAQ_20260624_決済_092214, TEST_FAQ_20260624_GU店舗_OFF_092214, TEST_FAQ_20260624_GU倉庫_ON_092214, TEST_FAQ_20260624_カタログ_092214, TEST_FAQ_20260624_GU_092214` |
| report | `TEST_FAQ_20260624_TRANSLATION_CRUD_093701` |
| report | `TEST_FAQ_20260624_MEASURE_CRUD_093821` |
| report | `#IA-1012` |
| report | `#IM-1024` |
| report | `#IO-1024` |
| report | `#II-1024` |
| 販売価格 | `https://www.sqstackstaging.com/admin/product_price_rules/17b071f4-a6ef-5e31-a8bc-5c77099b24ef_ProductPriceRule` |
| 予約販売 | `https://www.sqstackstaging.com/admin/inventory_back_order_rules/06712f89-dc3f-5c05-8eba-be8025942358_InventoryBackOrderRule` |
| 販売閾値 | `https://www.sqstackstaging.com/admin/inventory_threshold_rules` |
| 誕生日ポイント | `https://www.sqstackstaging.com/admin/point_calculation_birthday_rules/da162c01-a8a2-50bd-979c-1ce4959bc1ae_PointCalculationBirthdayRule` |
| ポイント失効通知 | `https://www.sqstackstaging.com/admin/point_expiration_notification_rule` |
| 会員ランク | `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules` |
| Recustomer | `https://www.sqstackstaging.com/admin/recustomer_integrations` |
## 2026-06-24 追加片付け

| data | status |
|:--|:--|
| `TEST_FAQ_20260624 GU検証Tシャツ 092214` / `TEST_FAQ_20260624_GU_092214` | 削除済み（商品詳細 > その他の操作 > 商品を削除する） |
| `TEST_FAQ_20260624_カタログ_092214` | 削除済み（カタログ詳細 > その他の操作 > カタログを削除する） |

## 2026-06-24 追加片付け・再検証（継続実行）

| data | status |
|:--|:--|
| `TEST_FAQ_20260624_ブランド_092214` | 削除済み（ブランド一覧で対象行選択 > 削除する > 確認） |
| `TEST_FAQ_20260624_決済_092214` | 削除済み（決済方法一覧で対象行選択 > 削除する > 確認） |
| `TEST_FAQ_20260624_TRANSLATION_CRUD_093701` | 削除済み（翻訳ルール一覧で対象行選択 > 削除する > 確認）。一覧のアプリエラーは再現せず |
| `TEST_FAQ_20260624_取引先_092214` | 削除済み（取引先一覧で対象行選択 > アーカイブする > 確認ダイアログ「取引先を削除しますか？」で削除する） |
| `TEST_FAQ_20260624_COMPANY_102911` / `TEST_FAQ_20260624_COMPANY_LOC_102911` | 作成成功。会社詳細・会社一覧の対象行選択後とも削除/アーカイブ導線なしのため残存 |
| `TEST_FAQ_20260624_MEASURE_CRUD_093821` | 一覧/詳細で削除導線未確認のため残存 |
| `TEST_FAQ_20260624_GU倉庫_ON_092214` / `TEST_FAQ_20260624_GU店舗_OFF_092214` | ロケーション一覧に表示あり。対象行のチェックボックスを自動操作で取得できず、削除/アーカイブ未実行 |
| `TEST_FAQ_20260624_Recustomer_100908` | 削除済み。2026-06-24追加再検証で、行選択後の `アクション` → `接続を削除する` → `削除する` により削除確認 |

## 2026-06-24 追加片付け・整合修正（継続2）

| data | status |
|:--|:--|
| `TEST_FAQ_20260624_GU倉庫_ON_092214` | アーカイブ済み（ロケーション詳細 > アーカイブする > 確認）。通知 `ロケーションをアーカイブしました`、詳細に `アーカイブを解除する` 表示 |
| `TEST_FAQ_20260624_GU店舗_OFF_092214` | アーカイブ済み（同上） |
| `TEST_FAQ_20260624_MEASURE_CRUD_093821` | 残存。採寸ルール詳細/一覧とも削除・編集導線なしを再確認 |
| `TEST_FAQ_20260624_Recustomer_100908` | 削除済み。削除後、一覧は `アイテムが見つかりませんでした` 表示 |
| `#IA-1012` | 残存。詳細は `該当するProductVariantが見つかりませんでした` 表示。参照先テストSKU削除による表示エラーとして記録 |

## 2026-06-24 追加整合（継続5）

| data | status |
|:--|:--|
| `#IA-1012` | 詳細表示エラー `該当するProductVariantが見つかりませんでした` をFAQ/25分類/サポート台帳へ反映済み。参照先テストSKU削除後の履歴表示エラーとして扱う |

## 2026-06-24 追加実機検証（継続7）

| data | status |
|:--|:--|
| `#IP-1005` | 新規発注伝票。下書き作成→発注済み→キャンセル済みまで実行済み。対象SKU `486125-31-XL`、単価100円・数量1・税率10%、金額 `￥110`。入荷管理一覧は発注後0秒/5秒/15秒で0件のまま。 |

## 2026-06-24 追加実機検証（継続8）

| data | status |
|:--|:--|
| `#IP-1006` | 新規発注伝票。下書き作成→発注済み→GraphQLで対象SKU `486125-31-XL` の全18ロケーション `incoming` 合計0確認→キャンセル済みまで実行済み。金額 `￥110`。 |


## 2026-06-24 追加再検証（低カバレッジ分類）

| データ | 状態 | 備考 |
|:--|:--|:--|
| `TEST_FAQ_20260624_PERMISSION_112959` | 削除済み | 権限未選択では `権限を選択してください`。`users:read` を1件選択して作成後、一覧の `権限グループを削除` で削除確認 |
| `TEST_FAQ_20260624_NOTIFY_113425` / `test+faq-113425@example.com` | 削除済み | 通知用メールアドレス。作成時に誤入力で名前が連結表示になったが、対象メールアドレス行を選択し `削除する` で削除確認 |
| `TEST_FAQ_20260624_APP_113636` | 残存 | APIアプリ。作成後、詳細画面・一覧カードとも削除導線未確認。アクセストークン/シークレットはログへ出力せず、状態ファイルはマスク済み |

## 2026-06-24 追加再検証（テナント・メタフィールド）

| データ | 状態 | 備考 |
|:--|:--|:--|
| `TEST_FAQ_20260624_TENANT_170037` | 残存 | テナント作成成功。詳細・一覧とも削除導線なし |
| `TEST_FAQ_20260624_META_170126` | 作成未完了 | `/admin/settings/metafield_definitions/create` は存在しないページ。正しい導線は一覧の `定義を追加する`。作成フォームで必須バリデーション `タイプを選択してください` を確認。タイプ選択UIの自動操作が不安定だったため作成は未完了 |

## 2026-06-24 追加再検証（ロケーショングループ）

| データ | 状態 | 備考 |
|:--|:--|:--|
| `TEST_FAQ_20260624_LG_171810` | 残存 | ロケーショングループ作成成功。作成フォームは名前+ロケーション選択が必要で、未選択時 `ロケーションを選択してください`。作成後の「このグループに新しいロケーションを自動的に含める」はdisabled。詳細・一覧とも削除導線未確認 |
