# 会社担当者 追加後行表示・削除 実機確認 2026-06-28

- 対象会社: `/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company`
- 検証用メール: `sq-faq-company-contact-20260627205837@example.com`

## 結果

| 項目 | 結果 |
|:--|:--|
| rowExistedBeforeDelete | `True` |
| rowHadDetailLink | `False` |
| selectShowsDelete | `True` |
| deleteDialogTitle | `True` |
| deleteRemovedRowAfterReload | `True` |

## 判断

- 会社担当者は会社詳細のダイアログから作成でき、保存後は担当者テーブルに名前/メールアドレスで表示される。
- 行自体には詳細リンクがなく、担当者詳細画面へ遷移する導線は確認できない。
- 行選択後に `担当者を削除` が表示され、確認ダイアログから削除できる。検証用担当者は削除済み。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/17-company-contact-add-delete-20260628.json`
