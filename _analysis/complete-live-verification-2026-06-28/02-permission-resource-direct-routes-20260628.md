# 02 権限リソース: 未導線リソースの直接URL確認

日時: 2026-06-28

## 確認結果

| 内部キー | 確認URL | 結果 |
|:--|:--|:--|
| `announcements` | `/admin/announcements` | 画面あり。h1相当は `お知らせ`、主ボタンは `お知らせを配信`、空状態は `お知らせはありません` |
| `mile_items` | `/admin/mile_items` | `このページは存在しないようです` |
| `next_engine_integrations` | `/admin/next_engine_integrations` | `このページは存在しないようです` |

## 反映判断

- `announcements` は左メニュー/設定画面には表示されないが、直URLの管理画面は存在する。
- `mile_items` と `next_engine_integrations` は、権限リソースとしては存在するが現行管理画面の直接URLは存在しない。
