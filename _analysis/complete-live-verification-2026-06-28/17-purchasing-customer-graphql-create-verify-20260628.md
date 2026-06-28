# 購入顧客を内部GraphQLで作成して一覧・詳細を確認 2026-06-28

- 作成方法: 管理画面セッションの内部GraphQL `purchasingCustomerCreate`
- 顧客ID: `83e62e4e-2e9c-57bd-bee1-db9b794d8e88_PurchasingCustomer`
- メール: `sq-faq-customer-20260628094055@example.invalid`
- タグ: `FAQ_E2E_20260628`
- 一覧にメール表示: `False`
- 検索パネル表示: `False`
- メール検索結果に表示: `None`
- フィルタメニュー表示: `None`
- 詳細URL: `/admin/purchasing_customers/83e62e4e-2e9c-57bd-bee1-db9b794d8e88_PurchasingCustomer`
- 詳細にメール表示: `True`
- 詳細にポイント/注文/ランク系表示: `point=True`, `order=True`, `rank=True`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/17-purchasing-customer-graphql-create-verify-20260628.json`

## 備考

- 管理画面UIには購入顧客の新規作成ボタンはありません。今回の作成は内部GraphQLでの検証用シードです。
- `purchasingCustomerCreate` の削除mutationは今回の読み取り専用スキーマ確認では見つかっていません。検証顧客はタグとメールで識別します。
