# API Playground 導線・認証注入確認 2026-06-28

- 対象アプリ: `TEST_FAQ_20260624_APP_113636`
- 対象画面: `/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/23-api-playground-scope-recheck-20260628.json`

## 結果

- Playgroundリンクを検出: `確認`
- Playgroundリンク先: `https://sq.stackservice.com/api/admin/v1/playground`
- Playgroundページを開けた: `確認`
- stagingアプリ詳細から開いてもリンク先は本番ドメイン: `確認`
- URLクエリにトークン/アプリIDらしき値なし: `確認`
- localStorage/sessionStorageはキー名のみ保存、値は保存なし: `確認`

## アプリ詳細の操作要素

- `stack-ps-yosuke 陽介 河野`
- `トークンを発行する`
- `Webhookを作成する`

## Playgroundページ

- URL: `https://sq.stackservice.com/api/admin/v1/playground`
- title: `GraphQL Playground`
- 本文抜粋: <untitled> GraphiQL 1 # Welcome to GraphiQL 2 # 3 # GraphiQL is an in-browser tool for writing, validating, and 4 # testing GraphQL queries. 5 # 6 # Type queries into this side of the screen, and you will see intelligent 7 # typeaheads aware of the current GraphQL type schema and live syntax and 8 # validation errors highlighted within the text. 9 # 10 # GraphQL queries typically start with a "{" character. Lines that start 11 # with a # are ignored. 12 # 13 # An example GraphQL query might look
- localStorage keys: `graphiql:tabState, graphiql:query, graphiql:shouldPersistHeaders`
