# OmnibusCore トークン作成・期限日数バリデーション確認 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration`
- 方針: アクセストークン値・全文本文・スクリーンショットは保存しない。通信ログもメソッド/パス/ステータスのみ保存する。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 下書き注文の有効期限日数の元値 | `1` |
| 期限日数を空欄にすると保存ボタンが有効 | `True` |
| 空保存後に期限日数エラー表示 | `True` |
| 復旧後リロード値 | `1` |
| トークン作成前の未設定文言 | `True` |
| トークン作成ボタン押下後の未設定文言 | `False` |
| トークン作成ボタン押下後のボタン表示 | `True` |
| トークン作成で発生した非GET通信 | `[{'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}, {'method': 'POST', 'path': '/api/graphql', 'status': 200}]` |
| トークンらしき長い文字列が画面本文に存在 | `False` |

## 判断

- `下書き注文の有効期限日数` を空欄にすると `保存する` は有効になり、保存後に期限日数のバリデーションが表示された。確認後、元値に復旧して再読み込みで復旧値を確認した。
- `トークンを作成` は確認ダイアログなしで非GET通信を発行した。押下後は未設定文言が消え、マスク済みトークン・作成日時・トークン用 `削除` ボタンが表示された。`トークンを作成` ボタン自体は作成後も表示された。
- トークン値は証跡に保存していない。画面本文にトークンらしき長い文字列が存在する可能性はフラグだけ記録した。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-omnibus-token-expiry-validation-20260628.json`
