# HTML再生成差分チェック 2026-06-24

一時コピー `/tmp/sq_faq_build_check_20260624` 上で `build_*.py` を実行し、現行HTMLとの差分を確認した。本体HTMLは上書きしていない。

| ファイル | 一致 | 現行bytes | 再生成bytes | 備考 |
|:--|:--:|--:|--:|:--|
| `SQ-FAQ.html` | ⚠️ | 1198698 | 1893976 | 差分あり |
| `SQ完全ガイド.html` | ✅ | 246274 | 246274 | 完全一致 |
| `SQ-サポートデスク.html` | ✅ | 176891 | 176891 | 完全一致 |
| `SQ-データ相関図.html` | ✅ | 25861 | 25861 | 完全一致 |

## buildログ

```
OK: /private/tmp/sq_faq_build_check_20260624/SQ-FAQ.html articles=70 bytes=1893976
OK: /private/tmp/sq_faq_build_check_20260624/SQ完全ガイド.html sections=18 bytes=246274
OK: /private/tmp/sq_faq_build_check_20260624/SQ-サポートデスク.html rows=236 bytes=176891
OK: /private/tmp/sq_faq_build_check_20260624/SQ-データ相関図.html nodes=53 edges=99 bytes=25861
```
