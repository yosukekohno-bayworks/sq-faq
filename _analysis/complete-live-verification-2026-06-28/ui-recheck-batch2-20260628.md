# UI再確認バッチ2 2026-06-28

## 確認した画面

- 商品作成フォーム: `/admin/products/create`
- バリエーション作成フォーム: `/admin/products/5407c6bf-092c-5c2f-96a6-fa37fcff594f_Product/variants/create`
- 翻訳ルール一覧/作成/詳細
- 採寸ルール一覧/作成/詳細、商品詳細
- 販売上限ルール作成フォーム
- ヤマトB2クラウド条件指定エクスポートフォーム
- 会社詳細/担当者追加/担当者詳細: `/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company`

## 主な結果

| 項目 | 実機結果 |
|:--|:--|
| `在庫を追跡する` 初期状態 | `{'found': True, 'label': '在庫を追跡する', 'checked': False, 'disabled': False, 'value': 'on'}` |
| `在庫切れの場合でも販売を続ける` 初期状態 | `{'found': True, 'label': '在庫切れの場合でも販売を続ける', 'checked': False, 'disabled': False, 'value': 'on'}` |
| `配送を必須にする` 初期状態 | `{'found': True, 'label': '配送を必須にする', 'checked': True, 'disabled': False, 'value': 'on'}` |
| 翻訳ルール詳細の手動実行系ボタン | `[]` |
| 採寸ルール詳細の入力readonly | `[{'label': 'ルール名', 'readOnly': True, 'disabled': False}, {'label': '採寸単位', 'readOnly': True, 'disabled': False}, {'label': '採寸項目1', 'readOnly': True, 'disabled': False}, {'label': '採寸項目2', 'readOnly': True, 'disabled': False}, {'label': '採寸項目3', 'readOnly': True, 'disabled': False}, {'label': '採寸項目4', 'readOnly': True, 'disabled': False}, {'label': '採寸項目5', 'readOnly': True, 'disabled': False}]` |
| 商品詳細に採寸/measurement系導線 | `False` |
| 販売上限空保存エラー | `{'name': True, 'channel': True}` |
| ヤマトB2決済方法選択肢 | `{'found': True, 'label': '決済方法', 'value': 'ALL', 'disabled': False, 'options': ['すべての決済', '代引きのみ', '代引き以外の決済']}` |
| ヤマトB2ステータス変更チェック初期状態 | `{'found': True, 'label': 'CSVの出力後に出荷指示のステータスを出荷作業中に変更する', 'checked': False, 'disabled': False, 'value': 'on'}` |
| 会社担当者を追加して詳細を表示 | `False`（保存トーストまで確認。行表示/削除は `17-company-contact-add-delete-20260628.md` で追加確認） |

## 判断

- 商品バリエーション作成フォームの3チェックボックスは、画面上の初期値として確認済み。ただし外部注文・出荷への実効は注文/チャネル連携前提なので未確認。
- 翻訳ルールのトップ/一覧/作成/詳細の確認範囲では、`実行` / `再実行` / `翻訳する` / `生成` ボタンは見当たらない。
- 採寸ルールはテンプレート定義として表示され、詳細入力はreadonly。商品詳細側に採寸紐づけ導線は見当たらない。
- 販売上限は未接続環境ではチャネル候補が表示されず、空保存でルール名とチャネルの両方のエラーが出る。
- ヤマトB2条件指定フォームでは決済方法3択とステータス変更チェックOFFを確認。実ファイル生成・メール通知は実行していない。
- 会社担当者は会社詳細ダイアログから追加できる。直後のこのバッチでは詳細リンク取得前に終わったため、行表示・詳細リンク有無・削除は `17-company-contact-add-delete-20260628.md` で追加確認した。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/ui-recheck-batch2-20260628.json`

## バリエーション作成フォームのラベル

- `カラー`
- `サイズ`
- `上代`
- `SKU (最小管理単位)`
- `メーカーSKU`
- `在庫を追跡する`
- `在庫切れの場合でも販売を続ける`
- `バーコード`
- `JAN`
- `EAN`
- `重量`
- `単位`
- `配送を必須にする`
- `原産国コード`
- `統計品目 (HS) コード`
