# SQ管理画面 サイトマップ（偵察記録）

> 最終確認: 2026-06-05　|　調査者: PM（Playwright偵察）　|　**初期偵察は読み取り中心**
> このファイルは初期偵察のサイトマップ記録です。最新の正本は `CODEX-OPS-PLAYWRIGHT-VERIFICATION-2026-06-18.md`、旧ログとの照合結果は `CODEX-LEGACY-RECONCILIATION-2026-06-18.md`、FAQ制作時の読む順番は `../00-getting-started/SQ学習・FAQ制作整理マップ.md` を優先してください。

<!-- 注: 本ファイルは初期偵察記録。後続の検証では TEST_FAQ 接頭辞のテストデータ作成・伝票登録（在庫依頼/引当/移動伝票/入荷・出荷実績/調整伝票#IA-1000/取引先TEST_FAQ_Supplier・Supplier2/OmnibusCore TEST_MAKER_001/予約販売ルール等）を一部実施した。実顧客データの破壊・削除・外部連携の実接続は行っていない。詳細は各詳細ファイル（11-operations.md・13-channels.md・14-settings.md 等）を参照。 -->

## 接続情報（実機確認済み）
- システムURL: `https://www.sqstackstaging.com/` → 管理画面 `/admin`
- 認証: **Clerk / パスワードレス**（`accounts.sqstackstaging.com`）。メール検証リンク or 6桁コード。パスワードは無い。
- ログインメール: `yosuke.kohno@bay-works.com`
- ログイン後に **組織選択**（現在: `stack-ps-yosuke` / ユーザー: 陽介 河野）
- **現行ヘルプセンター**: `https://docs.sqstack.com/docs/guide/introduction`（公開ドキュメント）
- 製品アップデート: `https://stack-inc.notion.site/...`（Notion）

## サイドナビ構成（初期偵察時: 24項目・5グループ）

### メイン
| ラベル | URL |
|:--|:--|
| ホーム | `/admin` |
| 商品管理 | `/admin/products` |
| 在庫管理 | `/admin/inventory_items` |
| 注文管理 | `/admin/orders` |
| 顧客管理 | `/admin/purchasing_customers` |
| 発注管理 | `/admin/inventory_purchase_orders` |
| 販売設定 | `/admin/product_price_rules` |
| 会計 | `/admin/sale_change_line_items` |
| 分析 | `/admin/analytics` |

### オペレーション（グループ見出し）
| ラベル | URL |
|:--|:--|
| 入荷管理 | `/admin/inventory_inbound_orders` |
| 出荷管理 | `/admin/inventory_outbound_orders` |
| 在庫依頼 | `/admin/inventory_allocation_requests` |

### CRM（グループ見出し）
| ラベル | URL |
|:--|:--|
| ディスカウント | `/admin/order_price_adjustment_rules` |
| ポイント | `/admin/point_calculation_rules` |
| 会員ランク | `/admin/customer_rank_calculation_rules` |

### 販売チャネル（グループ見出し）
| ラベル | URL |
|:--|:--|
| Shopify | `/admin/shopify_integrations` |
| OmnibusCore | `/admin/omnibus_core_integrations` |
| スマレジ | `/admin/smaregi_integrations` |
| リテールポータル | `/admin/retail_portal_integrations` |
| 卸売 | `/admin/b2b` |

### その他
| ラベル | URL |
|:--|:--|
| 設定 | `/admin/settings` |

## ホーム画面のクイックリンク
- 商品管理 / 在庫管理 / 注文管理 / 顧客管理
- CSVインポート `/admin/csv_import` ・ CSVエクスポート `/admin/csv_export` ・ PDFエクスポート `/admin/pdf_export`
- 製品アップデートを見る（Notion） ・ ヘルプセンターを見る（docs.sqstack.com）

## 議事録（2026-05-20）と照合した要点
- SQ = EC運営の基幹システム。商品/在庫/注文/CRM/販売設定/Shopify連携/WMS連携を一体で持つ。
- 最も複雑な運用 = **取り寄せ在庫販売**（在庫依頼→移動伝票→入荷実績→出荷の自動連携）。マイケルコースが6/1全店導入の最複雑ユースケース。
- ヘルプは「機能別」でなく**担当者ロール別（運営者/管理者/店舗スタッフ）**の目的志向構造にする方針。
- 当面の優先度は「**正確性・精度優先**」（平易化は後工程）。

## 追記（2026-06-05）: 実機巡回で判明した補正
初期巡回時に39画面を巡回（詳細は `02-home.md`〜`15-csv-pdf.md`）。サイトマップへの補正:

**新発見サブメニュー（上表に未記載）**
- 商品管理 → カタログ `/admin/catalogs` / 店舗受取 `/admin/local_pickup_product_variants`
- 在庫管理 → 移動伝票 `/admin/inventory_movement_orders` / 調整伝票 `/admin/inventory_adjustment_orders` / 取置伝票 `/admin/inventory_reservation_orders`
- 注文管理 → 下書き `/admin/draft_orders` / 返品 `/admin/order_returns`
- 顧客管理 → 会社 `/admin/companies`
- 販売設定 → 販売価格 / 予約販売 `/admin/inventory_back_order_rules` / 販売上限 `/admin/inventory_sale_limit_rules` / 販売閾値 `/admin/inventory_threshold_rules`
- 在庫依頼 → 確保済み `/admin/inventory_allocation_request_confirmations`

**ラベル不一致（ナビ名 ≠ 画面h1）** — FAQ用語統一の注意点
- 「ポイント」→ 画面は「注文ポイント」 ／ 「会計」→ 画面は「売上実績」

**未実装（画面が "TODO" 表示）**: 分析 `/admin/analytics` ／ 卸売 `/admin/b2b`

**取り寄せ販売フロー（実機確認）**: 在庫依頼（確認待ち）→ 確保済み →「移動伝票を作成する」→ 移動伝票 → 入荷管理 → 出荷管理
- 入荷ステータス6段階: 入荷待ち / 入荷依頼済み / 入荷作業中 / 要対応 / 入荷完了 / キャンセル
- 出荷ステータス6段階: 保留中 / 出荷待ち / 依頼済み / 作業中 / 欠品・要対応 / 出荷完了

**未踏（要再訪）**: 注文詳細・顧客詳細（データ0件で未確認）/ 入荷作成フォーム

<!-- 訂正 2026-06-08: 以下5項目は後続調査で補完・実機確認済みのため未踏リストから削除した。権限グループ＝14-settings.md L144（実証済み 2026-06-06）/ 翻訳＝14-settings.md L301（✓実機確認 2026-06-07）/ 採寸ルール＝14-settings.md L366（✓実機確認 2026-06-07）/ CSVインポート個別フォーム＝15-csv-pdf.md L127〜 / Recustomer連携フォーム＝14-settings.md L398〜・05-orders.md L392。最新の未確認一覧は CONFIRMATION-LIST.md に集約。 -->
<!-- TODO: 「リテールポータル」= 店舗スタッフ向け権限制限ビュー。別ログイン導線があるか要確認 -->
