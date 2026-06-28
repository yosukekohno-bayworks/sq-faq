# 残テストデータ片付け実行 2026-06-24

| 対象 | 操作 | 実行前 | 実行後残存 | 結果 |
|:--|:--|:--:|:--:|:--|
| `TEST_FAQ_20260624_ブランド_092214` | 削除する | True | False | ['ブランドを削除しました'] |
| `TEST_FAQ_20260624_決済_092214` | 削除する | True | False | ['削除する', '決済方法を削除しました', '決済方法を削除しますか？', '選択されている決済方法を削除します。この処理は巻き戻すことができません。', '削除する'] |
| `TEST_FAQ_20260624_TRANSLATION_CRUD_093701` | 削除する | True | False | ['翻訳を削除しました'] |
| `TEST_FAQ_20260624_取引先_092214` | アーカイブする | True | True | Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_role("button", name=re.compile(r"アーカイブする")).last
    - locator resolved to <button type |