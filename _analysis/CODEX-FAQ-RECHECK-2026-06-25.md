# Codex FAQ再確認メモ 2026-06-25

## 対象

- `faq/00-getting-started/`: 8件
- `faq/01-by-feature/`: 25件
- `faq/02-by-task/`: 31件
- `faq/03-faq/`: 6件
- `faq/04-notion/`: 26件
- 生成物: `SQ-FAQ.html` / `SQ完全ガイド.html` / `SQ-サポートデスク.html` / `SQ-データ相関図.html` / `04-notion.zip`

## 確認結果

- Markdown本文: 96件を確認。
- `SQ-FAQ.html`: 00-03配下の70記事がタイトルベースで全件収録済み。
- Markdownリンク: リンク切れ0件。
- 画像リンク: リンク切れ0件。
- ローカルHTMLリンク: リンク切れ0件。
- 未整理TODOコメント: 0件。
- 仮リンク/次エリア名/古い翻訳・採寸統合参照: 0件。
- Recustomerの古い「削除導線なし」誤記: 0件。
- 相関図からデータ事典①②へのリンクキー: `SQ-FAQ.html` 側の `data-key` と一致。

## 修正

- `04-notion.zip` を再作成した。
- 修正理由: 旧zipは26件のMarkdownを含んでいたが、zip内エントリ名が文字化けしていた。
- 修正後: zip内の26件が `faq/04-notion/*.md` とファイル名・本文とも一致。日本語ファイル名はUTF-8フラグ付き。

## 再生成確認

以下を再実行し、既存HTMLとの差分なしを確認した。

```sh
python3 build_help.py
python3 build_guide.py
python3 build_support.py
python3 build_graph.py
```

出力:

- `SQ-FAQ.html`: 70記事
- `SQ完全ガイド.html`: 18セクション
- `SQ-サポートデスク.html`: 251行
- `SQ-データ相関図.html`: 53ノード / 99エッジ

## 残る前提

外部サービスの実接続、実注文・実顧客・実売上データ、メール/PDF実出力、巻き戻し不可操作、ユーザー追加/削除は、最新の完了監査と同じく対象外または例外管理のまま。
