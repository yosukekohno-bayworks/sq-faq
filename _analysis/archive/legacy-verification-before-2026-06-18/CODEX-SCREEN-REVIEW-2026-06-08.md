# SQ FAQ 実画面レビュー（2026-06-08）

> 方針: 元のFAQ/分析ファイルは変更しない。齟齬・漏れ・嘘の可能性は本レビューに集約する。
> 対象: SQ staging 管理画面、公開ヘルプ、ローカルFAQ/分析資料。

## 実画面確認の前提

- 確認日時: 2026-06-08 JST
- 確認環境: `https://www.sqstackstaging.com/admin`
- ログイン状態: `stack-ps-yosuke` / `陽介 河野`
- 証跡:
  - `faq/_analysis/screen-audit/20260608-104211/00-admin-entry.png`
  - `faq/_analysis/screen-audit/20260608-104315-readonly-flow/`
  - `faq/_analysis/screen-audit/20260608-104443-inventory/`
  - `faq/_analysis/screen-audit/20260608-104921-adjust-available/`
  - `faq/_analysis/screen-audit/20260608-105503-allocation-flow-correct-headless/`
  - `faq/_analysis/screen-audit/20260608-105700-movement-exec/`
  - `faq/_analysis/screen-audit/20260608-105809-ship-receive/`
  - `faq/_analysis/screen-audit/20260608-105952-inbound-complete/`
  - `faq/_analysis/screen-audit/20260608-110238-close-bad-request-3/`
  - `faq/_analysis/screen-audit/20260608-110613-purchase-order-create-attempt/`
  - `faq/_analysis/screen-audit/20260608-110657-purchase-order-list-after/`

## 現時点の画面一致確認

### 管理画面ホーム

- 左ナビに以下が表示されることを実画面で確認:
  - ホーム、商品管理、在庫管理、注文管理、顧客管理、発注管理、販売設定、会計、分析
  - オペレーション: 入荷管理、出荷管理、在庫依頼
  - CRM: ディスカウント、ポイント、会員ランク
  - 販売チャネル: Shopify、OmnibusCore、スマレジ、リテールポータル、卸売
  - 設定

### 取り寄せ販売FAQの画面名・ボタン名

`faq/02-by-task/取り寄せ販売の処理手順.md` の主要画面とボタン名は、読み取り範囲では現行画面と一致。

| 確認対象 | 実画面で確認した表示 |
|:--|:--|
| 在庫依頼一覧 | `在庫依頼を作成する`、タブ `確認待ち` / `確保済み` / `終了` |
| 在庫依頼作成 | `商品バリエーション`、`希望数`、`移動先ロケーション`、`リクエスト先ロケーション`、`保存する` |
| 確保済み一覧 | `移動伝票を作成する`、タブ `すべて` |
| 出荷管理 | `インポート`、`条件指定でエクスポート`、タブ `保留中` / `出荷待ち` / `依頼済み` / `作業中` / `欠品・要対応` / `出荷完了` |
| 入荷管理 | タブ `入荷待ち` / `入荷依頼済み` / `入荷作業中` / `要対応` / `入荷完了` / `キャンセル` |

## 取り寄せ販売フローの実操作結果

### 使用したテストデータ

- SKU: `486125-31-L`
- 商品: オーバーサイズスウェットシャツ / BEIGE / L
- 数量: 2
- 移動元: 物流倉庫
- 移動先: ユニクロ - 銀座店
- 補足: FAQ本文の既存例は `486125-31-XL` だが、現行画面で物流倉庫の表示SKUが全0だったため、画面上で確認しやすい `486125-31-L` を使って再検証した。

### 通し確認できたこと

| ステップ | 実画面結果 |
|:--|:--|
| 事前在庫調整 | 物流倉庫の `486125-31-L` を販売可能2・手持ち2に更新できた。トースト: `販売可能数を更新しました` |
| 在庫依頼作成 | `確認待ち` で作成。トースト: `在庫依頼を作成しました` |
| 在庫引当 | `確認待ち` から `確保済み` に変化。確保済み数量 `2 / 2`。トースト: `在庫を引当てました` |
| 確保済み一覧 | `商品 / SKU / 確保数 / 移動元 / 移動先 / 確保日時` が表示。`移動元=物流倉庫`、`移動先=ユニクロ - 銀座店` |
| 移動伝票作成 | トースト: `移動伝票を一括作成しました`。`#IM-1001` が生成 |
| 出荷指示生成 | 出荷管理に `#IO-1001` が生成。出荷待ち1件 |
| 入荷指示生成 | 入荷管理に `#II-1001` が生成。入荷待ち1件 |
| 出荷実績登録 | `#IO-1001` が `出荷完了` に変化。トースト: `出荷を完了しました` |
| 入荷実績登録 | `#II-1001` が `入荷完了` に変化。トースト: `入荷を完了しました` |
| 移動伝票完了 | `#IM-1001` が `完了 / 入荷完了` に変化 |
| 最終在庫 | `486125-31-L`: ユニクロ - 銀座店が販売可能2・手持ち2、物流倉庫が0 |

### 結論

- `faq/02-by-task/取り寄せ販売の処理手順.md` の中核フローは、現行画面でも概ね正しい。
- ただし、下記の文言は読み手の誤操作を避けるためレビュー上の修正提案を出す。

## 齟齬・修正提案

### SR-01: 「出荷と入荷は並行処理可能」は断定が強い

- 対象: `faq/02-by-task/取り寄せ販売の処理手順.md`
- 現記述: `ステップ4（出荷）とステップ5（入荷）は並行して処理できます（順序は問いません）。`
- レビュー結果: 今回はFAQの通常順序どおり、出荷実績登録後に入荷実績登録した。この順序では通る。入荷を先に実行できるかは未検証。
- 修正提案: FAQ本文では「通常は実運用の流れに沿って出荷後に入荷を登録してください。順序制約は要確認」と弱める。

### SR-02: 事前在庫の前提が不足している

- 対象: 取り寄せ販売の通し再現
- 実画面: 検証開始時点の `在庫管理 : 物流倉庫` 一覧では、表示範囲の販売不可/確定済み/販売可能/手持ちはすべて0だった。
- 影響: 移動元に販売可能在庫がないと、在庫引当の前提が崩れる。今回は事前に `販売可能在庫数を編集する` ダイアログでテスト在庫を作ってから通した。
- 修正提案: FAQに「事前に移動元ロケーションに販売可能在庫があること」を明記すると、実運用者に親切。

### SR-03: `リクエスト先ロケーション` は任意表示だが、この手順では実質必須

- 対象: `ステップ1: 在庫依頼を作成する`
- 実画面: `移動先ロケーション` は必須表示、`リクエスト先ロケーション` は必須表示ではない。
- 実操作結果: `リクエスト先ロケーション` を入れ損ねても在庫依頼自体は保存できた。ただし詳細では `依頼先 ロケーションはありません` となり、引当ダイアログでロケーション未選択エラーが出る。
- 修正提案: FAQでは「画面上は任意表示でも、取り寄せ販売手順ではリクエスト先ロケーションを必ず指定する」と明記する。

### SR-04: 入荷一覧は「行全体」ではなく管理番号リンクを押すのが確実

- 対象: `ステップ5: 入荷実績を登録する`
- 現記述: `入荷指示の行をクリックして詳細画面を開く`
- 実画面: 入荷一覧の `#II-1001` は `<a href="/admin/inventory_inbound_orders/...">` の管理番号リンク。行クリックでは詳細に遷移しないケースがあった。
- 修正提案: `入荷指示の管理番号（例: #II-1001）をクリックして詳細画面を開く` にする。

### SR-05: 発注伝票経由の入荷連携は現行画面でも未実証

- 対象: `faq/_analysis/07-purchase-orders.md`、`faq/_analysis/11-operations.md`、発注伝票経由の入荷説明。
- 実操作: `TEST_FAQ_Supplier2` / `ユニクロ` / `486125-31-L` / 数量1 / 金額 `￥3,600` で `作成する` を押下。
- 結果: 作成フォームに残り、画面に `エラーが発生しました。しばらくしてから再度お試しください` と表示。コンソールは `CombinedGraphQLErrors`。
- 発注管理一覧: 保存後確認でも `アイテムが見つかりませんでした`。発注伝票は作成されていない。
- 修正提案: FAQでは「発注伝票から入荷指示が自動生成される」と断定しない。現時点では「設計上想定されるが、現行stagingでは発注伝票保存エラーにより未確認」とする。

### SR-06: 公開ヘルプの正規URLとページ構成は現行状態で再確認が必要

- 対象: `faq/_analysis/01-helpcenter-coverage-gap.md`、`faq/_analysis/02-helpcenter-pages.md`、`faq/_analysis/SUMMARY.md` の公開ヘルプ評価。
- 実確認（2026-06-08 JST 再確認）:
  - `https://docs.sqstack.com/docs/guide/introduction` は 200。
  - `https://docs.sqstack.com/guide/introduction` は 404。
  - `https://docs.sqstack.com/docs/guide/shopify-integration` は 200。
  - `https://docs.sqstack.com/guide/shopify-integration` は 404。
  - `https://docs.sqstack.com/docs/guide/retail-portal-integration` は 200。
  - `https://docs.sqstack.com/guide/retail-portal-integration` は 404。
  - `https://docs.sqstack.com/docs/llms.txt` は 200。
  - `https://docs.sqstack.com/llms.txt` は 404。
  - `https://docs.sqstack.com/docs/llms-full.txt` は 200。
  - `https://docs.sqstack.com/llms-full.txt` は 404。
- `docs/llms-full.txt` から確認できた `Source:` は12件:
  - `app-integrations`
  - `customers`
  - `data-management`
  - `discounts`
  - `introduction`
  - `inventory`
  - `orders`
  - `point`
  - `products`
  - `rank`
  - `retail-portal-integration`
  - `shopify-integration`
- ただしトップページから内部リンクをたどると、`/docs/guide/...` 配下で46 URLが200。例: `products/create-product`、`products/create-catalog`、`point/handle-returns-and-cancellations`、`import-export`。
- 修正提案: FAQ監査では正規URLを `/docs/guide/...` に統一する。ページ数・薄さ評価は `llms-full.txt` のトップ12件だけで判断せず、子ページ46件を含めて確認日時付きで再集計する。

## 未確認

- 入荷実績を出荷実績より先に登録できるか。
- 在庫4区分/7区分の全ロジック。今回の最終状態では `物流倉庫: 0`、`ユニクロ - 銀座店: 販売可能2・手持ち2` まで確認したが、途中の各区分増減式は未検証。
- 発注伝票経由の入荷連携。現行画面でも発注伝票保存エラーのため未実証。

## 後片付け

- 途中で誤作成した未完了の在庫依頼（`2026年06月08日 10:51` 作成、リクエスト先未指定）は、画面上の `在庫依頼をクローズする` → `実行する` で終了済み。
- 最終的に未完了の在庫依頼バッジは消えた。

## 全ファイル確認の追加結果

### 棚卸し

- 対象フォルダ総数: 2,551ファイル。
- 拡張子別:
  - `yml`: 1,294
  - `log`: 649
  - `png`: 475
  - `txt`: 60
  - `md`: 37
  - `json`: 27
  - `py`: 2
  - `html`: 2
  - `docx`: 1
  - その他: `.DS_Store` 2、`bin` 2
- 文書/コード系（`md/txt/json/py/html/docx`）は全件を棚卸しし、キーワード・差分・重要セクションで照合した。
- スクショ475枚はコンタクトシート12枚に集約して目視確認した。
  - `faq/_analysis/screen-audit/contact-sheets-20260608/`

### 議事録docxの要点

- FAQは「わかりやすさ」より「正確性・精度」を優先する方針。
- 機能別ではなく、利用者/役割/目的別にFAQを構成する方針。
- 重要テーマは Shopify データ、予約販売/バックオーダー、WMS、リテールポータル。
- 取り寄せ販売は最重要・最複雑な業務として扱う必要がある。

### 文書内の未確認マーカー

`TODO / 要確認 / 未確認 / 未実証 / 推測 / 仮説 / 要検証 / 不明` のヒット数が多いファイル:

| 件数 | ファイル |
|:--|:--|
| 259 | `faq/_analysis/SQ-調査報告.html` |
| 40 | `faq/_analysis/14-settings.md` |
| 40 | `faq/_analysis/03-products.md` |
| 39 | `faq/_analysis/11-operations.md` |
| 36 | `faq/_analysis/08-sales-settings.md` |
| 32 | `faq/_analysis/CODEX-REVIEW-2.md` |
| 31 | `faq/_analysis/CODEX-VERIFICATION.md` |
| 31 | `faq/_analysis/12-crm.md` |
| 25 | `faq/_analysis/04-inventory.md` |
| 23 | `faq/_analysis/SUMMARY.md` |

結論: 既存分析は実機確認を多く含むが、未確認・推測・古いスナップショットもまだ多い。FAQ本文へ転記する前に、確定/未確認のラベルを必ず見る必要がある。

## Playwright/スクショ証跡の集計

### 証跡量

- `.playwright-mcp`: `page-*.yml` 1,294件、`console-*.log` 649件。
- 今回追加した実画面監査証跡: `faq/_analysis/screen-audit/` 配下に `png` 79件、`json` 26件、`txt` 59件。
- 既存/今回分を含むスクショ全体: `png` 475件。

### consoleログの分類

- `_vercel/insights/script.js` の404: 646件。分析タグ由来のノイズとして扱う。
- localhost favicon等の404: 2件。ローカル確認用のノイズ。
- その他の404ルート: 37件。存在しない管理画面URLを探索した証跡として扱い、FAQの正規導線には使わない。
  - 例: `/admin/inventory_suppliers`、`/admin/order_returns/create`、`/admin/customer_ranks`、`/admin/sale_change_line_items/create`、CSV import/exportの一部推測URL。
- `CombinedGraphQLErrors`: 既存ログ17件 + 今回の発注伝票作成検証1件。
- ユーザー向け汎用エラー文言 `エラーが発生しました。しばらくしてから再度お試しください`: 23件。

結論: console上の404の大半はVercel analyticsのノイズ。機能上のリスクとして見るべきは、推測URLの404と発注伝票保存時のGraphQLエラー。

## 追加の齟齬・修正提案

### SR-07: 元Markdownと生成HTMLの状態が一致していない

- 対象:
  - `faq/02-by-task/取り寄せ販売の処理手順.md`
  - `faq/SQ-FAQ.html`
- 元Markdown:
  - frontmatter が `status: 確定`。
  - `ステップ4（出荷）とステップ5（入荷）は並行して処理できます（順序は問いません）。`
- 生成HTML:
  - 見出しバッジは `要確認`。
  - 本文は `順序制約は未検証のため、通常は実運用の流れに沿って出荷後に入荷を登録してください。`
- 影響: FAQの配布物がHTMLなのかMarkdownなのかで、利用者が読む内容が変わる。
- 修正提案: 最終公開前にMarkdownを正として再生成するか、HTML側の修正をMarkdownへ戻す。現時点ではMarkdownの `status: 確定` は強すぎる。

### SR-08: `リクエスト先ロケーション` の旧TODOは今回の実操作で一部解消

- 対象: `faq/_analysis/11-operations.md`
- 既存記述: `在庫依頼の「リクエスト先ロケーション」（任意項目）の意味が不明。在庫の移動元か？`
- 今回の実操作: この取り寄せ販売手順では `リクエスト先ロケーション=引当元/移動元` として動作した。
- ただし: ラベル定義として全業務で常に同じ意味かは未確認。
- 修正提案: FAQでは「この手順では引当元として使う」と書く。全体仕様としての定義は開発元確認扱いにする。

### SR-09: 既存ヘルプ評価は「トップ12件」と「子ページ46件」を分ける必要がある

- `docs/llms-full.txt` はトップ12件のみを `Source:` として返す。
- 画面内リンクのクロールでは `/docs/guide/...` 配下に46 URLがあり、すべて200。
- 例:
  - `products/create-product`
  - `products/create-catalog`
  - `point/handle-returns-and-cancellations`
  - `point/create-point-campaign`
  - `rank/create-customer-rank-calculation-rules`
  - `data-management/create-payment-methods`
  - `shopify-integration/import-data`
  - `import-export`
- 修正提案: 「既存ヘルプは13ページ中12ページが薄い」は古い/粗い。現在は「トップは薄いが、子ページには一部使える仕様がある」に変更する。

### SR-10: `CODEX-REVIEW-3.md` の `/guide/...` 参照は現在の実測と合わない

- 既存レビュー: `/guide/shopify-integration` や `/guide/retail-portal-integration` が閲覧可能だった前提。
- 今回実測: introduction / Shopify / Retail Portal の `/guide/...` はすべて404。
- 修正提案: 正規URLは `/docs/guide/...` に統一し、`/guide/...` の差分評価は現時点では撤回する。

### SR-11: スクショ証跡には正常画面だけでなく404/TODO/バリデーション/空状態が含まれる

- スクショ475枚をコンタクトシート化して確認。
- 画面証跡として有用な一方、以下は「正常フローの根拠」としては使わない:
  - `TODO` 表示画面（分析、卸売など）
  - 404画面
  - バリデーションエラー画面
  - 空状態だけの一覧
  - 発注伝票保存エラー画面
- 修正提案: FAQ根拠画像に使う場合は、正常完了トースト/ステータス変化/対象データが写るものを選ぶ。

### SR-12: 在庫4区分の式は今回の最終在庫だけではまだ確定できない

- 今回確認できた事実:
  - 物流倉庫の `486125-31-L` を販売可能2・手持ち2にした。
  - 社内移動完了後、ユニクロ - 銀座店が販売可能2・手持ち2、物流倉庫が0になった。
- まだ未確認:
  - 確定済み/販売不可/検品/破損/予備/移動中などが絡む計算式。
  - 注文起点で `確定済み` が増減するタイミング。
- 修正提案: FAQでは単純式を確定仕様として載せず、「画面上の各区分の意味」と「実データで要確認」を分ける。
