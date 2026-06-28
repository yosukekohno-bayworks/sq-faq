# 23 API・Webhook Webhook作成/表示 実機確認 2026-06-28

## 対象

- アプリ: `TEST_FAQ_20260624_APP_113636`
- 画面: `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- 検証用エンドポイント: `https://sq-faq-webhook.invalid/20260627173343`

## 操作

1. アプリ詳細画面で `Webhookを作成する` をクリックした。
2. イベントで `注文の作成` を選択した。
3. エンドポイントに検証用 `.invalid` URLを入力した。
4. 保存した。
5. 保存後のアプリ詳細画面と、削除/停止/編集導線の有無を確認した。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| Webhook保存 | 成功 |
| 保存後トースト | `Webhookを追加しました` |
| 保存後の表示 | Webhookセクションに `注文の作成 https://sq-faq-webhook.invalid/20260627173343・JSON` と表示 |
| 作成後URL | アプリ詳細画面のまま |
| 明示的な編集ボタン | 確認できず |
| 明示的な削除/停止ボタン | 確認できず |
| Webhook行のチェックボックス | 確認できず |
| 送信成功/失敗ステータス | 確認できず |
| クリーンアップ | 削除導線がないため未実施。検証Webhookは残存 |

## 判断

- Webhookは管理画面から実作成でき、作成後はイベント名・エンドポイント・形式 `JSON` がアプリ詳細のWebhookセクションに表示される。
- 作成直後の画面上では、Webhook単位の編集/削除/停止操作や送信成功/失敗ステータスは確認できなかった。
- 検証用エンドポイントは `.invalid` ドメインのため、実在する外部受信先には送らない前提の安全な宛先として扱う。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/23-webhook-create-cleanup-20260628.json`
- 実行スクリプト: `_analysis/complete-live-verification-2026-06-28/webhook_create_cleanup_20260628.py`
