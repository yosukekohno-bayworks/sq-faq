# OmnibusCore 通知メール重複保存 実機確認 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration/notification_emails`
- 検証メール: `sq-faq-omni-dupe-20260628072128@example.com`

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 初期一覧は空 | `True` |
| 1回目追加後に対象メールが一覧表示 | `True` |
| 2回目追加後の対象メール行数 | `1` |
| 2回目追加後に重複不可ヒント/表示あり | `True` |
| GraphQLエラー | `['エラーが発生しました。しばらくしてから再度お試しください']` |
| 削除後に対象メールが残っていない | `True` |

## 判断

- 通知メールは一覧が空の状態から追加でき、追加後に名前/メールアドレスが一覧へ表示された。
- 同じメールアドレスを2回目に追加しようとすると、一覧に2行目は増えず、ダイアログ内に重複不可の文言が表示された。今回の確認範囲ではGraphQL errorsは返っていないため、サーバー側エラー文言としては扱わない。
- 検証用通知メールは確認後に削除済み。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-omnibus-notification-email-duplicate-20260628.json`
