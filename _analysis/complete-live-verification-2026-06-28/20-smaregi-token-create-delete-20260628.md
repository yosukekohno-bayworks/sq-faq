# スマレジ 外部アクセストークン生成・削除確認 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration`
- 方針: トークン値・全文本文・スクリーンショットは保存しない。連携解除は実行しない。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 生成前に未設定文言が表示 | `True` |
| 生成後に作成日時が表示 | `False` |
| 生成後にトークン用 `削除` が表示 | `False` |
| 生成後も `トークンを作成` が表示 | `True` |
| 削除確認ダイアログが表示 | `False` |
| 削除後リロードで未設定へ戻る | `True` |
| 連携解除ボタンは未実行のまま表示 | `True` |
| 非GET通信 | `[{'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}]` |
| GraphQLエラー | `[]` |

## 判断

- `トークンを作成` は確認ダイアログなしで非GET通信を発行したが、今回の接続済みスマレジレコードでは作成日時・削除ボタンは表示されず、再読み込み後も `外部アクセストークンが設定されていません` のままだった。
- 画面上の明示的なエラー表示は確認できなかった。GraphQLエラーが出ている場合は上表に記録する。
- `連携を解除` は確認対象外のため実行していない。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-smaregi-token-create-delete-20260628.json`
