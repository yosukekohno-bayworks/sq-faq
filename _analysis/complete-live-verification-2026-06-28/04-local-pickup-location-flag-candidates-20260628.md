# 店舗受取ロケーション候補とON/OFF 実機確認 2026-06-28

## ロケーション詳細

- `FLAGOFF01`: 店舗受取ON=False / 在庫依頼ON=False / typeVisible=True
- `TEST_E2E_20260622_STORE_1740`: 店舗受取ON=True / 在庫依頼ON=False / typeVisible=True

## 店舗受取ルール作成フォームの候補検索

- `FLAGOFF01`: found=True rowCount=1 rows=['アイテムを選択する TEST_FLAGOFF_20260621 FLAGOFF01']
- `TEST_E2E_20260622_STORE_1740`: found=True rowCount=1 rows=['アイテムを選択する TEST_E2E_20260622_GU店舗_OFF_1740 TEST_E2E_20260622_STORE_1740']
- `W0001`: found=False rowCount=0 rows=[]
- `R0001`: found=True rowCount=1 rows=['アイテムを選択する ユニクロ - 銀座店 R0001']

## 結論

- 店舗受取ルール作成フォームのロケーション候補は、場所種別=店舗で絞られる。
- `店舗受取を有効にする` がOFFの店舗ロケーションも候補に表示されるため、管理画面の候補表示はこのチェックでは絞り込まれない。
- このチェックがストアフロント上の受取可否や連携後の挙動にどう効くかは、接続環境での確認事項として残す。
