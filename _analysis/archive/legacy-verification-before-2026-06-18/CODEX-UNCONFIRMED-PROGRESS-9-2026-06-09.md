# 未確認項目 追加進捗レビュー 9（Codex / Playwright）

作成日: 2026-06-09

方針: 元のFAQ/分析ファイルは変更せず、残っていた「在庫4区分の表示値/計算式」「在庫詳細・調整/移動/取置伝票の現在状態」を実画面で再確認した。保存、在庫調整の実行、取置作成、移動伝票作成は行っていない。

## 今回の追加証跡

- `faq/_analysis/deep-screen-verification-20260609/inventory_quantities_current_probe.mjs`
- `faq/_analysis/deep-screen-verification-20260609/inventory-quantities-current-records.json`
- `faq/_analysis/deep-screen-verification-20260609/inventory-quantities-current-screenshots/`
- `faq/_analysis/deep-screen-verification-20260609/inventory_quantities_exact_probe.mjs`
- `faq/_analysis/deep-screen-verification-20260609/inventory-quantities-exact-records.json`
- `faq/_analysis/deep-screen-verification-20260609/inventory-quantities-exact-screenshots/`

## 確認できたこと

| 確認項目 | 実画面/GraphQL結果 | FAQでの扱い |
|---|---|---|
| 在庫一覧の4列 | `/admin/inventory_items` は `販売不可 / 確定済み / 販売可能 / 手持ち` を表示。 | 4区分の列名は確認済み。 |
| 対象SKUの一覧値 | `486125-31-L` は物流倉庫ロケーションで `販売不可0 / 確定済み0 / 販売可能-2 / 手持ち-2` と表示。GraphQLでは `available=-2 / reserved=0 / committed=0 / onHand=-2`。 | 現在値としては書けるが、正常期待値としては使わない。過去の逆順検証で在庫前提が崩れている可能性がある。 |
| 対象SKUの詳細値 | `486125-31-L` 詳細では、`ユニクロ - 銀座店: available=4 / committed=0 / reserved=0 / damaged=0 / qualityControl=0 / safetyStock=0 / onHand=4`、`物流倉庫: available=-2 / committed=0 / reserved=0 / damaged=0 / qualityControl=0 / safetyStock=0 / onHand=-2`。 | 詳細画面の7区分表示は確認済み。 |
| 詳細画面の列 | `販売可能 / 確定済み / 確保済み / 破損 / 検品 / 予備 / 手持ち`。 | 一覧4区分より詳細画面の方が細かい。 |
| 計算式 | 今回の対象SKUでは `committed/reserved/damaged/qualityControl/safetyStock` が全て0のため、`available = onHand` になっている。 | 非0ケースがないため、完全な計算式はまだ断定不可。 |
| 販売可能数編集 | 在庫詳細の編集操作で `販売可能在庫数を編集する` ダイアログが開き、`理由`、`数量`、`保存する` を確認。 | ショートカット調整UIの存在は確認済み。保存後に調整伝票が生成されるかは未確認。 |
| 在庫履歴 | 開いた在庫詳細の履歴画面では `在庫の変更履歴はありません` を確認。 | 履歴画面の存在と空状態は確認済み。履歴データあり時の列は未確認。 |
| 調整伝票一覧 | `#IA-1001` は `注意 未完了 / 未実施`、`#IA-1000` は `完了 / 実施済み`。 | 調整伝票の一覧列とステータス例は確認済み。 |
| 調整伝票作成 | 理由選択肢は `廃棄 / 見本 / 紛失 / 棚卸差異 / その他`。 | 理由選択肢は確認済み。 |
| 移動伝票一覧 | `#IM-1000`、`#IM-1001`、`#IM-1002` は全て `成功 完了 / 入荷完了`。タブ/フィルタとして `出荷作業 / 一部受領済み / 受領済み` を確認。 | 完了済み移動伝票の一覧状態は確認済み。中間状態の実フローは既存の逆順検証証跡を参照。 |
| 取置伝票一覧 | `/admin/inventory_reservation_orders` は空。`未処理 / 処理済み` のタブを確認。 | 取置伝票の入口と空状態は確認済み。実作成・処理済み遷移は未確認。 |
| 取置伝票作成 | `/create` は `取置伝票を作成する`、`ロケーション`、`保存する` を確認。 | 作成フォームの存在は確認済み。保存は未実施。 |

## FAQ本文への判断

`faq/SQ-FAQ.html` の在庫4区分については、現在の「要確認」注記を残すのが安全。

今回、画面/API上は次の対応が見えた。

- 一覧: `販売不可 / 確定済み / 販売可能 / 手持ち`
- API: `reserved / committed / available / onHand`
- 詳細: `販売可能 / 確定済み / 確保済み / 破損 / 検品 / 予備 / 手持ち`
- 詳細API: `available / committed / reserved / damaged / qualityControl / safetyStock / onHand`

ただし、今回の実データでは `committed/reserved/damaged/qualityControl/safetyStock` がすべて0だったため、`販売可能 = 手持ち - 確定済み - 販売不可` のような完全式はまだ実証できていない。

推奨表現:

> 在庫一覧では「販売不可・確定済み・販売可能・手持ち」の4区分が表示されます。詳細画面では、さらに「確保済み・破損・検品・予備」などの内訳も表示されます。ただし、注文確定・取置・販売不可在庫が発生した場合の正確な増減式は、今回の検証データでは未確認です。

## 今回も残す未確認

| 項目 | 理由 |
|---|---|
| 在庫4区分の完全な計算式 | 非0の `committed/reserved/damaged/qualityControl/safetyStock` ケースがない。 |
| 注文確定時の `確定済み` 増減 | 注文データが0件。 |
| 取置伝票作成後の `確保済み` 増減 | 取置伝票保存は未実施。 |
| 破損/検品/予備への振替導線 | UI上の専用導線は確認できていない。 |
| 販売可能数編集保存後の内部処理 | 保存操作を行っていないため、調整伝票生成有無は未確認。 |
