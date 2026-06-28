# スマレジ 解除するボタン安全確認 2026-06-28

- 対象URL: `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration`
- 方針: `解除する` 実ボタンをクリックするが、非GET通信は遮断して連携解除を実行しない。確認ダイアログが出た場合は確定しない。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| クリック前に `解除する` ボタンが表示 | `True` |
| クリック後に確認ダイアログが表示 | `True` |
| ダイアログ | `{'title': ['連携を解除する'], 'buttons': ['閉じる', 'キャンセル', '解除する'], 'textIncludesUnlink': True}` |
| 遮断した非GET通信 | `[]` |
| クリック後URL | `https://www.sqstackstaging.com/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration` |

## 判断

- 見出し `連携を解除` ではなく、実ボタン `解除する` を対象に再確認した。
- 非GET通信を遮断したため、連携解除の確定・データ変化は実行していない。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/20-smaregi-unlink-button-safe-20260628.json`
