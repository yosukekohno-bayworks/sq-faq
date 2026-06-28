# 組織ID・テナントID UI確認 2026-06-28

## 方針

- IDの実値は記録せず、形式と表示/編集可否/コピー導線だけを確認。
- クリップボード確認では元の内容を出力せず、確認後に復元を試行。

## 結果

| 項目 | 結果 |
|:--|:--|
| 設定トップに組織ID表示 | `True` |
| 組織IDの形式 | `['a8225dc5..._Organization']` |
| 組織IDコピー導線 | `{'buttonFound': True, 'clipboardReadable': True, 'clipboardMatchesOrgId': True, 'maskedClipboard': 'a8225dc5..._Organization', 'maskedOsClipboard': 'a8225dc5..._Organization'}` |
| テナント一覧を開ける | `True` |
| テナント詳細にテナントID表示 | `True` |
| テナントIDの形式 | `['f6262fd1..._Tenant']` |
| テナント詳細の主要ラベル | `['テナント名', '注文IDプレフィックス', 'ポイントルール', 'ランクルール', '誕生日ポイント付与ルール', '失効予定通知ルール']` |
| テナントID入力欄の編集不可性 | `テナントID用の編集input/selectは検出されず、表示テキストとして確認` |
| テナントIDコピー導線 | `{'buttonFound': False, 'clipboardReadable': True, 'clipboardMatchesTenantId': False, 'maskedClipboard': '', 'maskedOsClipboard': ''}` |

## 判断

- 設定トップでは `組織ID` が `{uuid}_Organization` 形式で表示され、コピー導線も確認できる。
- テナント詳細では `テナントID` が `{uuid}_Tenant` 形式で表示される。
- テナント詳細で編集対象として確認できるのは `テナント名` と `注文IDプレフィックス` で、テナントIDは編集欄として扱われていない。
- 組織ID/テナントIDをAPIや外部連携でどう渡すかは、この画面だけでは確定できない。管理画面UIで確定できるのは表示・コピー・システム生成IDであることまで。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/03-org-tenant-id-ui-20260628.json`
