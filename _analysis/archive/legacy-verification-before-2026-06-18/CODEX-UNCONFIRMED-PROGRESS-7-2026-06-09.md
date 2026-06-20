# 未確認項目 追加進捗レビュー 7（Codex / Playwright）

作成日: 2026-06-09

方針: 元のFAQ/分析ファイルは変更せず、残っていた「実注文・下書き注文・返品・顧客・売上実績」の現在状態を実画面で再確認した。保存・作成系の確定操作は行っていない。

## 今回の追加証跡

- `faq/_analysis/deep-screen-verification-20260609/order_customer_accounting_current_probe.mjs`
- `faq/_analysis/deep-screen-verification-20260609/order-customer-accounting-current-records.json`
- `faq/_analysis/deep-screen-verification-20260609/order-customer-accounting-current-screenshots/`
- `faq/_analysis/deep-screen-verification-20260609/order_customer_accounting_action_probe.mjs`
- `faq/_analysis/deep-screen-verification-20260609/order-customer-accounting-action-records.json`
- `faq/_analysis/deep-screen-verification-20260609/order-customer-accounting-action-screenshots/`

## 確認できたこと

| 確認項目 | 実画面結果 | FAQでの扱い |
|---|---|---|
| 注文一覧 | `/admin/orders` は `注文管理` と表示。現在は `アイテムが見つかりませんでした`。 | 注文一覧画面の存在は確認済み。注文詳細・注文起点フローは未確認。 |
| 注文作成URL | `/admin/orders/create` は `予期せぬエラーが発生しました`。 | 管理画面から注文を直接作成できるとは書かない。 |
| 下書き注文一覧 | `/admin/draft_orders` は `下書き` と表示。現在は `注文が見つかりませんでした`。 | 下書き一覧の存在は確認済み。 |
| 下書き注文作成 | 一覧に `注文を作成する` は表示されるが、Polaris上は disabled class。クリック試行は遷移せず、`/admin/draft_orders/create` 直打ちは `予期せぬエラー`。 | 下書き注文作成フローは未確認。 |
| 返品一覧 | `/admin/order_returns` は `返品` と表示。現在は `アイテムが見つかりませんでした`。 | 返品一覧の存在は確認済み。 |
| 返品作成URL | `/admin/order_returns/create` は `このページは存在しないようです`。 | 返品起票は注文詳細など別導線の可能性がある。現環境では未確認。 |
| 顧客一覧 | `/admin/purchasing_customers` は `顧客管理` と表示。現在は `アイテムが見つかりませんでした`。 | 顧客一覧画面の存在は確認済み。 |
| 顧客作成URL | `/admin/purchasing_customers/create` は `予期せぬエラー`。 | 顧客を管理画面から直接作成できるとは書かない。 |
| 顧客インポート | 一覧に `インポート` ボタンは表示。クリック後も画面遷移・モーダル表示は確認できなかった。 | 顧客データの生成/取込フローは別途CSVインポートやチャネル連携の検証が必要。 |
| 売上実績一覧 | `/admin/sale_change_line_items` は `売上実績` と表示。現在は `アイテムが見つかりませんでした`。 | 売上実績画面の存在は確認済み。 |
| 売上実績作成 | 一覧に `売上実績を作成する` は表示されるが、Polaris上は disabled class。クリック試行は遷移せず、`/create` 直打ちは404。 | 売上実績を手動作成できるとは書かない。注文/チャネル起点の自動生成は未確認。 |

## FAQ本文への判断

`faq/SQ-FAQ.html` では、次の境界を守るのが安全。

- 書ける: 注文管理、下書き、返品、顧客管理、売上実績の画面入口はある。
- 書ける: 現在のstagingでは注文・顧客・返品・売上実績の実データがない。
- 書かない: 注文詳細の項目、返品起票手順、返金反映、売上実績の自動生成条件。
- 書かない: 顧客が販売チャネル経由で必ず自動生成される、という断定。

推奨表現:

> 注文・顧客・売上実績は、それぞれ管理画面上の一覧ページがあります。ただし今回の検証環境では実注文/顧客/売上データが存在せず、注文詳細、返品起票、売上実績の自動生成条件までは確認できていません。

## 今回も残す未確認

| 項目 | 理由 |
|---|---|
| 注文詳細画面 | 注文一覧が空で、詳細リンクが存在しない。 |
| 下書き注文作成 | 作成ボタンはdisabled状態で、直打ちcreateもエラー。 |
| 返品起票・返金反映 | 返品一覧は空、create直打ちは404。実注文データが必要。 |
| 顧客詳細・チャネル経由自動生成 | 顧客一覧が空、create直打ちはエラー。Shopify/スマレジ等の接続注文が必要。 |
| 売上実績の自動生成条件 | 売上実績一覧が空、手動作成導線も無効/404。実注文またはチャネル連携データが必要。 |
