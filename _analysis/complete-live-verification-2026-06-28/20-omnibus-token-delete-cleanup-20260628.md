# OmnibusCore アクセストークン削除クリーンアップ 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration`
- 方針: トークン値・全文本文・スクリーンショットは保存しない。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 削除前にトークン作成日時が表示 | `True` |
| 削除前にトークン用 `削除` ボタンが表示 | `True` |
| 削除クリック後に確認ダイアログ表示 | `True` |
| リロード後に未設定文言へ戻った | `True` |
| リロード後の期限日数 | `1` |
| 非GET通信 | `[{'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}]` |

## 判断

- `トークンを作成` 後の画面には、マスク済みトークン、作成日時、トークン用の `削除` ボタン、追加の `トークンを作成` ボタンが表示される。
- トークン用の `削除` クリック後、確認ダイアログを経て削除でき、再読み込み後は `アクセストークンが設定されていません` に戻った。
- 前段で空欄検証した `下書き注文の有効期限日数` は、再読み込み後 `1` に戻っている。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-omnibus-token-delete-cleanup-20260628.json`
