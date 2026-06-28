# 16 注文・返品 空状態再確認 2026-06-28

- 実行日時: 2026-06-27T22:37:44.221079+00:00
- JSON: `_analysis/complete-live-verification-2026-06-28/16-orders-returns-empty-state-recheck-20260628.json`
- エラー数: `0`

## 結果

- 注文一覧は空状態: `True`
- 注文一覧の検索/絞り込みUIあり: `False`
- `/admin/orders/create` は予期せぬエラー画面: `True`
- 下書き一覧は空状態: `True`
- 下書き `注文を作成する` クリック後URL: `{'beforeUrl': 'https://www.sqstackstaging.com/admin/draft_orders', 'clicked': False, 'afterUrl': 'https://www.sqstackstaging.com/admin/draft_orders', 'error': 'TimeoutError(\'Locator.click: Timeout 5000ms exceeded.\\nCall log:\\n  - waiting for get_by_text("注文を作成する", exact=True).first\\n    - locator resolved to <span class="Polaris-Text--root Polaris-Text--bodySm Polaris-Text--medium">注文を作成する</span>\\n  - attempting click action\\n    2 × waiting for element to be visible, enabled and stable\\n      - element is visible, enabled and stable\\n      - scrolling into view if needed\\n      - done scrolling\\n      - <div class="Polaris-Box Polaris-Box--printHidden">…</div> intercepts pointer events\\n    - retrying click action\\n    - waiting 20ms\\n    2 × waiting for element to be visible, enabled and stable\\n      - element is visible, enabled and stable\\n      - scrolling into view if needed\\n      - done scrolling\\n      - <div class="Polaris-Box Polaris-Box--printHidden">…</div> intercepts pointer events\\n    - retrying click action\\n      - waiting 100ms\\n    9 × waiting for element to be visible, enabled and stable\\n      - element is visible, enabled and stable\\n      - scrolling into view if needed\\n      - done scrolling\\n      - <div class="Polaris-Box Polaris-Box--printHidden">…</div> intercepts pointer events\\n    - retrying click action\\n      - waiting 500ms\\n    - waiting for element to be visible, enabled and stable\\n    - element is visible, enabled and stable\\n    - scrolling into view if needed\\n    - done scrolling\\n\')'}`
- `/admin/draft_orders/create` は予期せぬエラー画面: `True`
- 返品一覧は空状態: `True`
- 返品一覧の検索/絞り込み/キャンセル/交換出荷UIあり: `False`
- `/admin/order_returns/create` は存在しない画面: `True`

## 判断

- 現行の注文/下書き/返品一覧は、空状態と直URLエラーまで確認済み。
- 注文データあり状態の列・検索/絞り込み・ステータス遷移・返品処理は、注文/返品データ投入または外部チャネル接続が必要。