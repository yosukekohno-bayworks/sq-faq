# Recustomer / OmnibusCore フォーム再確認 2026-06-28

## Recustomer

- 一覧URL: `/admin/recustomer_integrations`
- 見出し: `Recustomer`
- 一覧アクション: `アカウントを接続`
- 一覧状態: `アイテムが見つかりませんでした`
- 作成URL: `/admin/recustomer_integrations/create`
- 作成見出し: `アカウントを接続する`
- 作成フォーム項目: `ストアID` / `シークレット`

結論: 管理画面UIで確認できるのはRecustomerアカウント接続フォームまで。返品・交換フローやSQ側の反映先は接続環境での検証が必要。

## OmnibusCore

- 一覧URL: `/admin/omnibus_core_integrations`
- 見出し: `OmnibusCore`
- 一覧列: `メーカーコード` / `テナント` / `カタログ` / `ロケーショングループ` / `連携日時`
- 作成URL: `/admin/omnibus_core_integrations/create`
- 作成見出し: `OmnibusCore連携を作成する`
- 作成フォームのセクション: `商品同期設定` / `在庫設定` / `注文設定`
- 主な項目: `テナント` / `メーカーコード` / `カタログ` / `カラーオプション名` / `サイズオプション名` / `ロケーショングループ` / `在庫予約ルール` / `販売上限ルール` / `下書き注文の有効期限日数`

結論: OmnibusCoreは実機フォーム上で商品同期設定・在庫設定・注文設定を確認できる。接続後の同期挙動や下書き注文期限切れ時の処理は未確認。
